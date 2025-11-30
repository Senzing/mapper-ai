#! /usr/bin/env python3
"""Analyze source data files and generate schema documentation.

Supports CSV, JSON, JSONL, Parquet, and XML formats. Generates markdown
reports with field statistics, data types, and sample values.
"""
import argparse
import csv
import glob
import json
import os
import pathlib
import subprocess
import sys
import time
import xml.etree.ElementTree as ET  # Add import for XML parsing

try:
    import numpy as np
except ImportError:
    np = False

try:
    import pandas as pd
except ImportError:
    pd = False

try:
    import prettytable
except ImportError:
    prettytable = False


# ============================================================================
# FILE READER CLASSES
# ============================================================================

class FileReader:
    """Base class for file readers with common interface."""

    def __init__(self, file_path, encoding="utf-8"):
        self.file_path = file_path
        self.encoding = encoding
        self._file_handle = None

    def __iter__(self):
        return self

    def __next__(self):
        """Return next record. Override in subclasses."""
        raise StopIteration

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def open(self):
        """Open the file for reading. Override in subclasses."""

    def close(self):
        """Close the file."""
        if self._file_handle:
            self._file_handle.close()
            self._file_handle = None


class CSVReader(FileReader):
    """Reader for CSV files with automatic dialect detection."""

    def open(self):
        self._file_handle = open(self.file_path, "r", encoding=self.encoding)
        sample = self._file_handle.read(8192)
        self._file_handle.seek(0)
        try:
            csv_dialect = csv.Sniffer().sniff(sample, delimiters=[",", ";", "|", "\t"])
            self._reader = csv.DictReader(self._file_handle, dialect=csv_dialect)
        except csv.Error:
            # Fallback: try tab delimiter
            self._reader = csv.DictReader(self._file_handle, delimiter="\t")

    def __iter__(self):
        return iter(self._reader)


class SocrataJSONReader(FileReader):
    """Reader for Socrata Open Data JSON format (meta + data arrays)."""

    def __init__(self, file_path, encoding="utf-8"):
        super().__init__(file_path, encoding)
        self.is_socrata = True  # Flag to indicate Socrata format
        self.field_metadata = {}  # Store field descriptions and metadata

    def open(self):
        self._file_handle = open(self.file_path, "r", encoding=self.encoding)
        raw_data = json.load(self._file_handle)

        # Extract schema from meta.view.columns
        columns = raw_data['meta']['view']['columns']

        # Build field name mapping (position -> field name)
        # Use fieldName if available, otherwise use name
        self._field_names = []
        for col in columns:
            field_name = col.get('fieldName', col.get('name', f'col_{col["position"]}'))
            self._field_names.append(field_name)

            # Store field metadata (description, cardinality, etc.)
            self.field_metadata[field_name] = {
                'description': col.get('description', ''),
                'dataTypeName': col.get('dataTypeName', ''),
                'name': col.get('name', '')
            }

            # Add cardinality if available from cachedContents
            if 'cachedContents' in col and 'cardinality' in col['cachedContents']:
                try:
                    self.field_metadata[field_name]['cardinality'] = int(col['cachedContents']['cardinality'])
                except (ValueError, TypeError):
                    pass

        # Get the data arrays
        self._data_arrays = raw_data['data']

    def __iter__(self):
        """Convert each data array to a dict using field names from schema."""
        for row_array in self._data_arrays:
            # Map array values to field names
            row_dict = {}
            for i, value in enumerate(row_array):
                if i < len(self._field_names):
                    row_dict[self._field_names[i]] = value
            yield row_dict


class JSONReader(FileReader):
    """Reader for JSON array files or objects with nested data arrays."""

    def __init__(self, file_path, encoding="utf-8"):
        super().__init__(file_path, encoding)
        self.is_socrata = False  # Flag to indicate if Socrata format
        self.field_metadata = {}  # For Socrata field metadata

    def open(self):
        self._file_handle = open(self.file_path, "r", encoding=self.encoding)
        self._data = json.load(self._file_handle)

        # If root is a list, use it directly
        if isinstance(self._data, list):
            pass
        # If root is an object, look for common data array fields
        elif isinstance(self._data, dict):
            # Check for Socrata format (meta.view.columns + data)
            if (isinstance(self._data.get('meta'), dict) and
                isinstance(self._data['meta'].get('view'), dict) and
                'columns' in self._data['meta']['view'] and
                'data' in self._data):
                # This is Socrata format - close current file and use specialized reader
                self._file_handle.close()
                self.is_socrata = True  # Set flag
                reader = SocrataJSONReader(self.file_path, self.encoding)
                reader.open()
                # Copy field metadata from Socrata reader
                self.field_metadata = reader.field_metadata
                # Replace our data with the Socrata reader's iterator
                self._data = list(reader)
                return

            # Try common field names for data arrays
            for field in ['data', 'rows', 'items', 'records', 'results']:
                if field in self._data and isinstance(self._data[field], list):
                    self._data = self._data[field]
                    break
            else:
                raise ValueError(
                    "JSON file must contain an array at root level or have a "
                    "'data', 'rows', 'items', 'records', or 'results' field containing an array"
                )
        else:
            raise ValueError("JSON file must contain an array or object at root level")

    def __iter__(self):
        return iter(self._data)


class ParseError:
    """Sentinel class to indicate a parse error during iteration."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class JSONLReader(FileReader):
    """Reader for JSONL (JSON Lines) files."""

    def open(self):
        self._file_handle = open(self.file_path, "r", encoding=self.encoding)
        self._line_number = 0

    def __iter__(self):
        for line in self._file_handle:
            self._line_number += 1
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as e:
                yield ParseError(f"Invalid JSON on line {self._line_number}: {e}")


class XMLReader(FileReader):
    """Reader for XML files."""

    def __init__(self, file_path, encoding='utf-8'):
        super().__init__(file_path, encoding)
        self.namespaces = {}

    def open(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        # Extract namespaces from root element
        # ElementTree stores namespaces in the tag as {namespace}tagname
        if root.tag.startswith('{'):
            default_ns = root.tag.split('}')[0][1:]  # Extract namespace URI
            self.namespaces['default'] = default_ns

        # Also check for namespace declarations in attributes
        for key, value in root.attrib.items():
            if key == 'xmlns':
                self.namespaces['default'] = value
            elif key.startswith('{http://www.w3.org/2000/xmlns/}') or key.startswith('xmlns:'):
                prefix = key.split('}')[-1] if '}' in key else key.split(':')[-1]
                self.namespaces[prefix] = value

        self._elements = [self._element_to_dict(child) for child in root]

    def __iter__(self):
        return iter(self._elements)

    def _element_to_dict(self, element):
        """Convert XML element to dictionary."""
        result = {}
        if element.attrib:
            result.update({self._strip_namespace(k): v for k, v in element.attrib.items()})
        if element.text and element.text.strip():
            result['text'] = element.text.strip()

        children = {}
        for child in element:
            child_dict = self._element_to_dict(child)
            tag = self._strip_namespace(child.tag)
            if tag in children:
                if not isinstance(children[tag], list):
                    children[tag] = [children[tag]]
                children[tag].append(child_dict)
            else:
                children[tag] = child_dict

        result.update(children)
        return result

    def _strip_namespace(self, tag):
        """Remove XML namespace from tag."""
        if isinstance(tag, str) and tag.startswith('{'):
            return tag.split('}', 1)[1]
        return tag


class ParquetReader(FileReader):
    """Reader for Parquet files."""

    def open(self):
        if not pd:
            raise ImportError("Pandas must be installed to read parquet files")
        self._data = pd.read_parquet(self.file_path, engine="auto")
        self._records = self._data.to_dict(orient="records")

    def __iter__(self):
        return iter(self._records)

    def close(self):
        # Parquet doesn't need explicit close
        pass


def get_reader(file_type, file_path, encoding="utf-8"):
    """Factory function to get appropriate reader for file type.

    Args:
        file_type: Type of file (csv, json, jsonl, xml, parquet)
        file_path: Path to the file
        encoding: File encoding

    Returns:
        FileReader instance
    """
    readers = {
        'csv': CSVReader,
        'json': JSONReader,
        'jsonl': JSONLReader,
        'xml': XMLReader,
        'xmls': XMLReader,
        'parquet': ParquetReader
    }
    reader_class = readers.get(file_type.lower())
    if not reader_class:
        raise ValueError(f"Unsupported file type: {file_type}")
    return reader_class(file_path, encoding)


# ============================================================================
# NODE CLASS
# ============================================================================

class Node:
    """Represents a node in the data schema tree."""

    def __init__(self, node_id):
        self.node_id = node_id
        self.node_desc = node_id
        self.node_type = None
        self.children = []
        self.description = None  # For field descriptions (e.g., from Socrata meta)

    def add_child(self, obj):
        """Add a child node to this node."""
        self.children.append(obj)

    def render_tree(self):
        """Render the tree structure as a string."""
        tree = f"{self.node_desc} ({self.node_type})\n"
        parents = [{"node": self, "display_children": self.children}]
        while parents:
            if len(parents[-1]["display_children"]) == 0:
                parents.pop()
                continue
            next_node = parents[-1]["display_children"][0]
            parents[-1]["display_children"].pop(0)

            prefix = ""
            for i, _ in enumerate(parents):
                last_child = len(parents[i]["display_children"]) == 0
                if i < len(parents) - 1:  # prior level
                    prefix += "    " if last_child else "\u2502   "
                else:
                    prefix += "\u2514\u2500\u2500 " if last_child else "\u251c\u2500\u2500 "

            tree += f"{prefix}{next_node.node_desc} ({next_node.node_type})\n"
            if next_node.children:
                prior_parents = [x["node"].node_id for x in parents]
                display_children = [x for x in next_node.children if x.node_id not in prior_parents]
                parents.append({"node": next_node, "display_children": display_children})

        return tree


# ============================================================================
# FILE ANALYZER CLASS
# ============================================================================

class FileAnalyzer:
    """Analyzes file structure and collects field statistics."""

    def __init__(self, file_name, file_type, group_by_attr=None, enumerate_config=None):
        self.record_count = 0
        self.root_node = Node("root")
        self.root_node.node_desc = file_name
        self.root_node.node_type = file_type
        self.file_name = file_name
        self.file_type = file_type
        self.table_type = None  # Will be set via detect_table_type()
        self.nodes = {"root": self.root_node}
        self.top_value_count = 10
        self.group_by_attr = group_by_attr
        self.group_by_filter = None  # Can be set after initialization
        self.field_metadata = {}  # For storing field descriptions and other metadata
        self.xml_namespaces = {}  # For storing XML namespace information

        # Handle both old and new enumeration formats
        if enumerate_config:
            if isinstance(enumerate_config, dict):
                # New pivot enumeration format
                self.enumerate_config = enumerate_config
                self.enumerate_attrs = []  # Keep for compatibility
                self.is_pivot_enumeration = True
            else:
                # Legacy enumeration format (list of attributes)
                self.enumerate_attrs = enumerate_config
                self.enumerate_config = None
                self.is_pivot_enumeration = False
        else:
            self.enumerate_attrs = []
            self.enumerate_config = None
            self.is_pivot_enumeration = False

        # For grouped analysis: track nodes and record counts per group
        if group_by_attr:
            self.groups = {}  # group_value -> {nodes: {}, record_count: 0}
            self.group_record_counts = {}  # group_value -> count
        else:
            self.groups = None
            self.group_record_counts = None

        # For code enumeration: track code statistics
        if self.enumerate_attrs or self.is_pivot_enumeration:
            if self.is_pivot_enumeration:
                # Pivot enumeration: track combinations of grouping attributes and their value stats
                if group_by_attr:
                    self.pivot_stats = {}  # group_value -> {(attr1_val, attr2_val, ...): {value_attr_val: {count, records}}}
                else:
                    self.pivot_stats = {}  # {(attr1_val, attr2_val, ...): {value_attr_val: {count, records}}}
                self.enumeration_stats = None  # Not used for pivot enumeration
            else:
                # Legacy enumeration
                if group_by_attr:
                    # Group-aware enumeration: group_value -> attr_path -> {code_value -> {count, records}}
                    self.enumeration_stats = {}
                else:
                    # Standard enumeration: attr_path -> {code_value -> {count, records}}
                    self.enumeration_stats = {}
                    for attr in self.enumerate_attrs:
                        self.enumeration_stats[attr] = {}
                self.pivot_stats = None  # Not used for legacy enumeration
        else:
            self.enumeration_stats = None
            self.pivot_stats = None

    def process_record(self, obj):
        """Process a single record, handling grouping and enumeration if enabled"""
        # Apply group_by filtering if specified
        if self.group_by_attr and self.group_by_filter and isinstance(obj, dict):
            group_value = obj.get(self.group_by_attr, "unknown")
            if str(group_value) != str(self.group_by_filter):
                return  # Skip this record

        # Handle enumeration if enabled
        if (self.enumerate_attrs or self.is_pivot_enumeration) and isinstance(obj, dict):
            try:
                if self.is_pivot_enumeration:
                    self.process_pivot_enumeration(obj)
                elif self.enumerate_attrs:
                    if self.group_by_attr:
                        group_value = obj.get(self.group_by_attr, "unknown")
                        self.process_enumeration_for_group(obj, group_value)
                    else:
                        self.process_enumeration(obj)
            except Exception as e:  # pylint: disable=broad-exception-caught
                print(f"Error processing record {obj.get('id', 'unknown')}: {e}")

        if self.group_by_attr and isinstance(obj, dict):
            group_value = obj.get(self.group_by_attr, "unknown")

            # Initialize group if not exists
            if group_value not in self.groups:
                self.groups[group_value] = {
                    "nodes": {"root": Node("root")},
                    "record_count": 0
                }
                # Initialize root node for this group
                root_node = self.groups[group_value]["nodes"]["root"]
                root_node.node_desc = f"root ({group_value})"
                root_node.node_type = self.root_node.node_type

            # Process this record for the group
            self.groups[group_value]["record_count"] += 1
            self.iterate_obj_for_group(group_value, "root", obj)
        else:
            # Non-grouped processing (original behavior)
            self.iterate_obj("root", obj)

    def process_enumeration_for_group(self, obj, group_value):
        """Process enumeration attributes for a single record within a group"""
        # Initialize group enumeration if not exists
        if group_value not in self.enumeration_stats:
            self.enumeration_stats[group_value] = {}
            for attr in self.enumerate_attrs:
                self.enumeration_stats[group_value][attr] = {}

        for attr_path in self.enumerate_attrs:
            values = self.extract_nested_values(obj, attr_path)
            if values:
                for value in values:
                    if value is not None and value != "":  # Skip None and empty string, but keep False
                        value_str = str(value)
                        if value_str not in self.enumeration_stats[group_value][attr_path]:
                            self.enumeration_stats[group_value][attr_path][value_str] = {
                                'count': 0,
                                'records': set()
                            }
                        self.enumeration_stats[group_value][attr_path][value_str]['count'] += 1
                        # Track which records contain this code (using record ID if available)
                        record_id = obj.get('id', f'record_{self.record_count}')
                        self.enumeration_stats[group_value][attr_path][value_str]['records'].add(record_id)

    def process_enumeration(self, obj):
        """Process enumeration attributes for a single record"""
        for attr_path in self.enumerate_attrs:
            values = self.extract_nested_values(obj, attr_path)
            if values:
                for value in values:
                    if value is not None and value != "":  # Skip None and empty string, but keep False
                        value_str = str(value)
                        if value_str not in self.enumeration_stats[attr_path]:
                            self.enumeration_stats[attr_path][value_str] = {
                                'count': 0,
                                'records': set()
                            }
                        self.enumeration_stats[attr_path][value_str]['count'] += 1
                        # Track which records contain this code (using record ID if available)
                        record_id = obj.get('id', f'record_{self.record_count}')
                        self.enumeration_stats[attr_path][value_str]['records'].add(record_id)

    def process_pivot_enumeration(self, obj):
        """Process pivot enumeration for a single record"""
        config = self.enumerate_config
        level = config['level']
        grouping_attrs = config['grouping_attrs']
        value_attr = config['value_attr']

        # Get the base object at the specified level
        if level and level != 'root':
            base_obj = self.get_nested_value(obj, level)
            if not base_obj:
                return
        else:
            base_obj = obj

        # Extract all attribute values (grouping + value)
        all_attrs = grouping_attrs + [value_attr]
        all_values = []
        max_length = 0

        for attr in all_attrs:
            values = self.extract_nested_values(base_obj, attr)
            all_values.append(values)
            if values:
                max_length = max(max_length, len(values))

        # Check that all attributes have consistent list lengths or are non-lists
        if max_length > 0:
            for i, values in enumerate(all_values):
                if values and len(values) != max_length and len(values) != 1:
                    # Allow single values to be repeated across the list
                    if len(values) > 1:
                        # Instead of throwing an error, just skip this record
                        return

        # If no values found for the value attribute, return
        value_values = all_values[-1]  # Last attribute is the value attribute
        if not value_values:
            return

        # Set max_length to the length of the value attribute if no other attributes have values
        if max_length == 0:
            max_length = len(value_values)

        # Handle group-by organization
        if self.group_by_attr:
            group_value = obj.get(self.group_by_attr, "unknown")
            if group_value not in self.pivot_stats:
                self.pivot_stats[group_value] = {}
            group_pivot_stats = self.pivot_stats[group_value]
        else:
            group_pivot_stats = self.pivot_stats

        # Iterate through all combinations
        for i in range(max_length):
            # Extract grouping values for this iteration
            grouping_values = []
            for j, attr in enumerate(grouping_attrs):
                values = all_values[j]
                if values:
                    if len(values) == 1:
                        # Repeat single value across all iterations
                        grouping_values.append(str(values[0]))
                    else:
                        # Use corresponding item from the list
                        grouping_values.append(str(values[i]))
                else:
                    grouping_values.append('unknown')

            # Extract value for this iteration
            value_values = all_values[-1]  # Last attribute is the value attribute
            if value_values:
                if len(value_values) == 1:
                    value = value_values[0]
                else:
                    value = value_values[i]
            else:
                continue

            if value is None or value == "":
                continue

            # Create grouping key
            grouping_key = tuple(grouping_values)

            # Initialize grouping key if not exists
            if grouping_key not in group_pivot_stats:
                group_pivot_stats[grouping_key] = {}

            # Track the value
            value_str = str(value)
            if value_str not in group_pivot_stats[grouping_key]:
                group_pivot_stats[grouping_key][value_str] = {
                    'count': 0,
                    'records': set()
                }
            group_pivot_stats[grouping_key][value_str]['count'] += 1
            record_id = obj.get('id', f'record_{self.record_count}')
            group_pivot_stats[grouping_key][value_str]['records'].add(record_id)

    def extract_nested_values(self, obj, attr_path):
        """Extract values from nested attribute path like 'properties.type.type'"""
        parts = attr_path.split('.')
        current = obj

        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            elif isinstance(current, list) and current:
                # Check if list contains dicts or scalars
                if isinstance(current[0], dict):
                    # Handle list of dicts - look for the part in each dict
                    new_values = []
                    for item in current:
                        if isinstance(item, dict) and part in item:
                            new_values.append(item[part])
                    if new_values:
                        current = new_values
                    else:
                        return []
                else:
                    # List of scalars (strings, numbers, etc.) - can't extract further
                    # If we still have more parts to navigate, return empty
                    return []
            else:
                return []

        # Handle different types of values
        if isinstance(current, list):
            return current
        elif current is not None:
            return [current]
        else:
            return []

    def get_nested_value(self, obj, attr_path):
        """Get a single nested value (not a list) from attribute path"""
        parts = attr_path.split('.')
        current = obj

        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None

        return current

    def iterate_obj_for_group(self, group_value, prior_key, obj):
        """Iterate object for a specific group"""
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key and key != self.group_by_attr:  # Skip the grouping attribute itself
                    self.update_node_for_group(group_value, prior_key, key, value)
                    # Check for nested structures (include numpy arrays if available)
                    check_types = (dict, list, np.ndarray) if np else (dict, list)
                    if isinstance(value, check_types):
                        self.iterate_obj_for_group(group_value, f"{prior_key}.{key}", value)

        elif isinstance(obj, list):
            for item in obj:
                check_types = (dict, list, np.ndarray) if np else (dict, list)
                if isinstance(item, check_types):
                    self.iterate_obj_for_group(group_value, prior_key, item)
                else:
                    # For lists of scalars, don't duplicate the key
                    self.update_node_for_group(group_value, prior_key, "", item)

    def iterate_obj(self, prior_key, obj):
        """Recursively iterate through object structure to build schema."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key:  # bad csvs have blank field names!
                    self.update_node(prior_key, key, value)
                    # Check for nested structures (include numpy arrays if available)
                    check_types = (dict, list, np.ndarray) if np else (dict, list)
                    if isinstance(value, check_types):
                        self.iterate_obj(f"{prior_key}.{key}", value)

        elif isinstance(obj, list):
            for item in obj:
                check_types = (dict, list, np.ndarray) if np else (dict, list)
                if isinstance(item, check_types):
                    self.iterate_obj(prior_key, item)
                else:
                    # For lists of scalars, don't duplicate the key
                    self.update_node(prior_key, "", item)

    def update_node_for_group(self, group_value, prior_key, key, value):
        """Update node for a specific group"""
        attr_key = f"{prior_key}.{key}" if key else prior_key
        group_nodes = self.groups[group_value]["nodes"]

        if attr_key not in group_nodes:
            group_nodes[attr_key] = Node(attr_key)
            group_nodes[attr_key].node_desc = attr_key.replace("root.", "")
            group_nodes[attr_key].node_type = "unk"
            group_nodes[attr_key].record_count = 0
            group_nodes[attr_key].unique_values = {}
            group_nodes[prior_key].add_child(group_nodes[attr_key])

        if value is not None:
            # Handle numpy arrays and other array-like objects
            try:
                if hasattr(value, '__len__') and not isinstance(value, str):
                    # Check if it's empty for arrays/lists
                    is_empty = len(value) == 0
                else:
                    # For scalar values, check truthiness normally
                    is_empty = not bool(value)
            except (ValueError, TypeError):
                # Fallback for values that can't be easily checked
                is_empty = False

            if not is_empty:
                value_type = str(type(value))[8:-2]

                # Set or update node type
                # Allow promoting 'dict' to 'list' if we encounter a list
                if group_nodes[attr_key].node_type == "unk":
                    group_nodes[attr_key].node_type = value_type
                elif group_nodes[attr_key].node_type == "dict" and value_type == "list":
                    group_nodes[attr_key].node_type = "list"

                if isinstance(value, (dict, list)):
                    value = f"{len(value)} items"
                elif np and isinstance(value, np.ndarray):
                    value = f"array({value.shape}) items"

                # Ensure value is always a string for dictionary key
                value = str(value)

                group_nodes[attr_key].record_count += 1
                if value not in group_nodes[attr_key].unique_values:
                    group_nodes[attr_key].unique_values[value] = 1
                else:
                    group_nodes[attr_key].unique_values[value] += 1

    def update_node(self, prior_key, key, value):
        """Update or create a node with value statistics."""
        attr_key = f"{prior_key}.{key}" if key else prior_key
        if attr_key not in self.nodes:
            self.nodes[attr_key] = Node(attr_key)
            self.nodes[attr_key].node_desc = attr_key.replace("root.", "")
            self.nodes[attr_key].node_type = "unk"

            self.nodes[attr_key].record_count = 0
            self.nodes[attr_key].unique_values = {}
            self.nodes[attr_key].table_context = None  # Will be set later
            self.nodes[attr_key].table_record_count = 0  # Will be set later
            self.nodes[prior_key].add_child(self.nodes[attr_key])

        if value is not None:
            # Handle numpy arrays and other array-like objects
            try:
                if hasattr(value, '__len__') and not isinstance(value, str):
                    # Check if it's empty for arrays/lists
                    is_empty = len(value) == 0
                else:
                    # For scalar values, check truthiness normally
                    is_empty = not bool(value)
            except (ValueError, TypeError):
                # Fallback for values that can't be easily checked
                is_empty = False

            if not is_empty:
                value_type = str(type(value))[8:-2]

                # Set or update node type
                # Allow promoting 'dict' to 'list' if we encounter a list
                if self.nodes[attr_key].node_type == "unk":
                    self.nodes[attr_key].node_type = value_type
                elif self.nodes[attr_key].node_type == "dict" and value_type == "list":
                    self.nodes[attr_key].node_type = "list"

                if isinstance(value, (dict, list)):
                    value = f"{len(value)} items"
                elif np and isinstance(value, np.ndarray):
                    value = f"array({value.shape}) items"

                # Ensure value is always a string for dictionary key
                value = str(value)

                self.nodes[attr_key].record_count += 1
                if value not in self.nodes[attr_key].unique_values:
                    self.nodes[attr_key].unique_values[value] = 1
                else:
                    self.nodes[attr_key].unique_values[value] += 1

    def calculate_table_contexts(self):
        """Calculate table contexts for all nodes.

        For XML/nested structures, identify list nodes as "tables" and set each field's
        table context to its nearest ancestor list. This allows correct percentage calculations
        relative to the appropriate record count.
        """
        # First, identify all list nodes (these are "tables")
        list_nodes = {}
        for node_path, node in self.nodes.items():
            if node.node_type == 'list':
                # Store the actual item count from the node
                # The record_count for a list node represents how many times we saw that list
                # But we need the count of items IN the list
                list_nodes[node_path] = node

        # For each node, find its nearest ancestor list
        for node_path, node in self.nodes.items():
            if node_path == "root":
                continue

            # Find the nearest ancestor list by walking up the path
            path_parts = node_path.split('.')
            table_context_path = None
            table_count = self.record_count  # Default to root record count

            # Walk backwards through ancestors
            for i in range(len(path_parts) - 1, 0, -1):
                ancestor_path = '.'.join(path_parts[:i])
                if ancestor_path in list_nodes:
                    table_context_path = ancestor_path
                    # The table count is the record_count of children of this list
                    # Find a child to get the actual item count
                    for child_path, child_node in self.nodes.items():
                        if child_path.startswith(ancestor_path + '.') and '.' not in child_path[len(ancestor_path) + 1:]:
                            # This is a direct child - its record_count is the list item count
                            table_count = child_node.record_count
                            break
                    break

            node.table_context = table_context_path
            node.table_record_count = table_count

    def detect_table_type(self, table_name=None):
        """Detect table type based on heuristics.

        Returns one of: 'entity', 'relationship', 'config', 'feature'
        """
        if not table_name:
            table_name = pathlib.Path(self.file_name).stem

        table_name_lower = table_name.lower()

        # Check for config/meta patterns
        config_keywords = ['meta', 'metadata', 'config', 'settings', 'schema']
        if any(keyword in table_name_lower for keyword in config_keywords):
            return 'config'

        # Analyze fields
        field_count = len(self.nodes) - 1  # Exclude root
        if field_count == 0:
            return 'entity'  # Default

        # Count ID-like fields (end with _id or start with :@ or :)
        id_field_count = 0
        relationship_keywords = ['from', 'to', 'source', 'target', 'parent', 'child']
        has_relationship_keyword = False

        for node_key, node in self.nodes.items():
            if node_key == 'root':
                continue
            field_name = node.node_desc.lower()

            # Check for ID patterns
            if (field_name.endswith('_id') or
                field_name.startswith(':@') or
                field_name.startswith(':id')):
                id_field_count += 1

            # Check for relationship keywords
            if any(keyword in field_name for keyword in relationship_keywords):
                has_relationship_keyword = True

        # If >50% fields are IDs or has relationship keywords, classify as relationship
        if field_count > 0 and (id_field_count / field_count > 0.5 or has_relationship_keyword):
            return 'relationship'

        # Check for feature patterns (computed/derived fields)
        feature_keywords = ['computed', 'calculated', 'derived', 'region', 'score']
        if any(keyword in table_name_lower for keyword in feature_keywords):
            return 'feature'

        # Default to entity
        return 'entity'

    def matches_filter(self, obj, filter_attr, filter_value):
        """Check if object matches the filter criteria"""
        parts = filter_attr.split(".")
        current = obj

        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return False

        return str(current) == filter_value

    def detect_code_lists(self, max_unique_values=100, min_unique_count=2, max_unique_pct=0.10, min_population_pct=0.05):
        """Auto-detect fields that are likely code lists.

        Detection criteria:
        - Field has string type
        - Small number of unique values (< max_unique_values OR < max_unique_pct of records)
        - Appears in at least min_population_pct of records
        - Has at least min_unique_count unique values (to avoid constants)

        Args:
            max_unique_values: Maximum absolute unique value count (default 100)
            min_unique_count: Minimum unique value count to avoid single-value constants (default 2)
            max_unique_pct: Maximum unique % relative to records (default 10%)
            min_population_pct: Minimum population % (default 5%)

        Returns:
            Dictionary of code list candidates with their statistics
        """
        code_lists = {}

        # Traverse all nodes
        for node_path, node in self.nodes.items():
            if node_path == 'root':
                continue

            # Only consider string fields (codes are typically strings)
            if node.node_type != 'str':
                continue

            # Skip if no records
            if not hasattr(node, 'record_count') or node.record_count == 0:
                continue

            # Get unique value count
            unique_count = len(node.unique_values) if hasattr(node, 'unique_values') else 0
            if unique_count == 0:
                continue

            # Calculate population rate relative to parent table
            table_count = node.table_record_count if hasattr(node, 'table_record_count') and node.table_record_count > 0 else node.record_count
            population_rate = node.record_count / table_count if table_count > 0 else 0

            # Calculate unique percentage
            unique_pct = unique_count / node.record_count if node.record_count > 0 else 0

            # Apply detection criteria
            is_low_cardinality = unique_count <= max_unique_values or unique_pct <= max_unique_pct
            is_not_constant = unique_count >= min_unique_count
            is_well_populated = population_rate >= min_population_pct

            if is_low_cardinality and is_not_constant and is_well_populated:
                # This looks like a code list!
                code_lists[node_path] = {
                    'field': node_path,
                    'unique_count': unique_count,
                    'record_count': node.record_count,
                    'table_count': table_count,
                    'population_pct': population_rate * 100,
                    'unique_pct': unique_pct * 100,
                    'values': node.unique_values,
                    'table_context': node.table_context if hasattr(node, 'table_context') else 'unknown'
                }

        return code_lists

    def generate(self, template):
        """Generate report using appropriate reporter.

        Args:
            template: Type of report ('report', 'markdown', 'enumeration')

        Returns:
            Report data (format depends on reporter type)
        """
        if template == "report":
            reporter = get_reporter('csv', self)
        elif template == "markdown":
            reporter = get_reporter('markdown', self)
        elif template == "enumeration":
            reporter = get_reporter('enumeration', self)
        else:
            # Fallback to CSV reporter
            reporter = get_reporter('csv', self)
        return reporter.generate()

    def generate_grouped_report(self):
        """Generate grouped report. [DEPRECATED: Use get_reporter('csv', analyzer)]"""
        reporter = get_reporter('csv', self)
        return reporter.generate()

    def generate_standard_report(self):
        """Generate standard report. [DEPRECATED: Use get_reporter('csv', analyzer)]"""
        reporter = get_reporter('csv', self)
        return reporter.generate()

    def generate_markdown_report(self):
        """Generate markdown format schema report. [DEPRECATED: Use get_reporter('markdown', analyzer)]"""
        reporter = get_reporter('markdown', self)
        return reporter.generate()

    def generate_enumeration_report(self):
        """Generate enumeration report. [DEPRECATED: Use get_reporter('enumeration', analyzer)]"""
        reporter = get_reporter('enumeration', self)
        return reporter.generate()

    def generate_grouped_enumeration_report(self):
        """Generate grouped enumeration report. [DEPRECATED]"""
        return self.generate_enumeration_report()

    def generate_standard_enumeration_report(self):
        """Generate standard enumeration report. [DEPRECATED]"""
        return self.generate_enumeration_report()

    def generate_pivot_enumeration_report(self):
        """Generate pivot enumeration report. [DEPRECATED]"""
        return self.generate_enumeration_report()



# ============================================================================
# REPORT GENERATOR CLASSES
# ============================================================================

class BaseReporter:
    """Base class for report generators with shared utilities."""

    def __init__(self, analyzer):
        self.analyzer = analyzer

    def _traverse_nodes(self, nodes, root_node):
        """Traverse nodes in depth-first order yielding each node."""
        parents = [{"node": root_node, "children": root_node.children.copy()}]
        while parents:
            if len(parents[-1]["children"]) == 0:
                parents.pop()
                continue
            next_node = parents[-1]["children"][0]
            parents[-1]["children"].pop(0)
            yield next_node
            if next_node.children:
                parents.append({"node": next_node, "children": next_node.children.copy()})


class CSVReporter(BaseReporter):
    """Generates CSV format reports for schema statistics."""

    def generate(self):
        """Generate CSV report (list of lists format)."""
        if self.analyzer.group_by_attr:
            return self._generate_grouped()
        else:
            return self._generate_standard()

    def _generate_standard(self):
        """Generate standard (non-grouped) CSV report."""
        header = ["attribute", "type", "record_cnt", "record_pct", "unique_cnt", "unique_pct"]
        header.extend([f"top_value{i+1}" for i in range(self.analyzer.top_value_count)])

        rows = []
        for node in self._traverse_nodes(self.analyzer.nodes, self.analyzer.root_node):
            attr_code = node.node_desc
            attr_type = node.node_type
            record_cnt = node.record_count
            record_pct = round(record_cnt / self.analyzer.record_count * 100, 2) if self.analyzer.record_count else 0
            unique_cnt = len(node.unique_values)
            unique_pct = round(unique_cnt / record_cnt * 100, 2) if record_cnt else 0

            top_values = [""] * self.analyzer.top_value_count
            if self.analyzer.top_value_count:
                i = 0
                for k, v in sorted(node.unique_values.items(), key=lambda v: v[1], reverse=True):
                    top_values[i] = f"{str(k)[0:50]} ({v})"
                    i += 1
                    if i == self.analyzer.top_value_count:
                        break

            rows.append([attr_code, attr_type, record_cnt, record_pct, unique_cnt, unique_pct] + top_values)

        return [header] + rows

    def _generate_grouped(self):
        """Generate grouped CSV report with schema as first column."""
        header = [self.analyzer.group_by_attr, "attribute", "type", "record_cnt", "record_pct", "unique_cnt", "unique_pct"]
        header.extend([f"top_value{i+1}" for i in range(self.analyzer.top_value_count)])

        rows = []
        for group_value in sorted(self.analyzer.groups.keys()):
            group_data = self.analyzer.groups[group_value]
            group_nodes = group_data["nodes"]
            group_record_count = group_data["record_count"]

            for node in self._traverse_nodes(group_nodes, group_nodes["root"]):
                attr_code = node.node_desc
                attr_type = node.node_type
                record_cnt = node.record_count
                record_pct = round(record_cnt / group_record_count * 100, 2) if group_record_count else 0
                unique_cnt = len(node.unique_values)
                unique_pct = round(unique_cnt / record_cnt * 100, 2) if record_cnt else 0

                top_values = [""] * self.analyzer.top_value_count
                if self.analyzer.top_value_count:
                    i = 0
                    for k, v in sorted(node.unique_values.items(), key=lambda v: v[1], reverse=True):
                        top_values[i] = f"{str(k)[0:50]} ({v})"
                        i += 1
                        if i == self.analyzer.top_value_count:
                            break

                rows.append([group_value, attr_code, attr_type, record_cnt, record_pct, unique_cnt, unique_pct] + top_values)

        return [header] + rows


class TreeReporter(BaseReporter):
    """Generates hierarchical tree-style schema reports."""

    def generate(self):
        """Generate tree-style report."""
        lines = []
        schema_name = pathlib.Path(self.analyzer.file_name).stem

        lines.append(f"# XML Document Schema: {schema_name}")
        lines.append("")
        lines.append(f"**File:** {self.analyzer.file_name}")
        lines.append(f"**Records Analyzed:** {self.analyzer.record_count}")
        lines.append(f"**Total Fields:** {len(self.analyzer.nodes) - 1}")
        lines.append("")

        # Build hierarchical structure
        root_children = self._get_children(self.analyzer.root_node)

        # Categorize top-level elements
        reference_elements = []
        entity_elements = []
        other_elements = []

        for child in root_children:
            if child.node_desc.endswith('Values'):
                reference_elements.append(child)
            elif child.node_type == 'list' and child.record_count > 100:
                entity_elements.append(child)
            else:
                other_elements.append(child)

        if reference_elements:
            lines.append(f"## Reference Elements ({len(reference_elements)})")
            lines.append("")
            for elem in sorted(reference_elements, key=lambda x: x.node_desc):
                lines.extend(self._render_node(elem, 0))
            lines.append("")

        if entity_elements:
            lines.append(f"## Entity Elements ({len(entity_elements)})")
            lines.append("")
            for elem in sorted(entity_elements, key=lambda x: -x.record_count):
                lines.extend(self._render_node(elem, 0))
            lines.append("")

        if other_elements:
            lines.append(f"## Other Elements ({len(other_elements)})")
            lines.append("")
            for elem in sorted(other_elements, key=lambda x: x.node_desc):
                lines.extend(self._render_node(elem, 0))
            lines.append("")

        return "\n".join(lines)

    def _get_children(self, node):
        """Get direct children of a node."""
        children = []
        node_path = node.node_desc

        for node_name, child_node in self.analyzer.nodes.items():
            if node_name in (node_path, "root"):
                continue

            # Check if this is a direct child
            if node_path in ("root", self.analyzer.file_name):
                # Top-level children have no dots or just one segment
                if '.' not in child_node.node_desc:
                    children.append(child_node)
            else:
                # Check if child_node is direct child of node_path
                if child_node.node_desc.startswith(node_path + "."):
                    remainder = child_node.node_desc[len(node_path) + 1:]
                    if '.' not in remainder:
                        children.append(child_node)

        return children

    def _render_node(self, node, depth, max_depth=4):
        """Render a node and its children as tree structure."""
        lines = []
        indent = "  " * depth

        # Node header
        name = node.node_desc.split('.')[-1]
        type_info = node.node_type

        # Add cardinality/count info
        if node.node_type == 'list':
            count_info = f"{node.record_count} items"
        elif node.record_count > 0:
            unique_cnt = len(node.unique_values)
            if unique_cnt <= 20:  # Show codes inline if small
                count_info = f"{node.record_count} records, {unique_cnt} unique"
            else:
                count_info = f"{node.record_count} records"
        else:
            count_info = "empty"

        # Build the line
        line_parts = [f"{indent}├─ **{name}**"]

        if type_info:
            line_parts.append(f" `{type_info}`")

        line_parts.append(f" ({count_info})")

        # Add sample values for leaf nodes with small value sets
        if node.node_type in ('str', 'int', 'float'):
            unique_cnt = len(node.unique_values)
            if 0 < unique_cnt <= 10:
                values = sorted(node.unique_values.keys(), key=lambda k: node.unique_values[k], reverse=True)[:5]
                values_str = ", ".join([f"`{v}`" for v in values])
                if unique_cnt > 5:
                    values_str += f" ... ({unique_cnt} total)"
                line_parts.append(f" → {values_str}")

        lines.append("".join(line_parts))

        # Render children if not too deep
        if depth < max_depth:
            children = self._get_children(node)
            if children:
                # Sort children: dicts/lists first, then others
                children.sort(key=lambda x: (x.node_type not in ('dict', 'list'), x.node_desc))
                for child in children[:20]:  # Limit to first 20 children
                    lines.extend(self._render_node(child, depth + 1, max_depth))

                if len(children) > 20:
                    lines.append(f"{indent}  ... ({len(children) - 20} more fields)")

        return lines


class MarkdownReporter(BaseReporter):
    """Generates Markdown format schema reports."""

    def generate(self):
        """Generate markdown report."""
        if self.analyzer.group_by_attr:
            return self._generate_grouped()
        else:
            return self._generate_standard()

    def _generate_standard(self):
        """Generate standard (single-schema) markdown format."""
        lines = []
        field_count = len(self.analyzer.nodes) - 1
        schema_name = pathlib.Path(self.analyzer.file_name).stem

        # For Socrata format, use "data" as the table name
        if self.analyzer.file_type == 'socrata-json':
            schema_name = 'data'

        # Detect table type if not already set
        if not self.analyzer.table_type:
            self.analyzer.table_type = self.analyzer.detect_table_type(schema_name)

        # Count list nodes (table-like structures)
        list_node_count = sum(1 for node in self.analyzer.nodes.values() if node.node_type == 'list')

        lines.append(f"**File Type:** {self.analyzer.file_type}")
        lines.append(f"**Root Records:** {self.analyzer.record_count}")
        lines.append(f"**List Elements (Tables):** {list_node_count}")
        lines.append(f"**Total Fields:** {field_count}")
        lines.append("")

        # Show XML namespace information if available
        if self.analyzer.xml_namespaces:
            lines.append("**XML Namespaces:**")
            for prefix, uri in sorted(self.analyzer.xml_namespaces.items()):
                if prefix == 'default':
                    lines.append(f"- Default: `{uri}`")
                else:
                    lines.append(f"- {prefix}: `{uri}`")
            lines.append("")
            lines.append("*Note: Generated code must handle these namespaces when parsing XML.*")
            lines.append("")

        # Show all list elements (these are the "tables") in hierarchical structure
        # First pass: collect all list nodes and their child counts
        list_nodes = {}  # display_name -> child_count
        for node_path, node in self.analyzer.nodes.items():
            if node.node_type == 'list' and node_path.startswith('root.'):
                # Get child count for this list
                child_count = 0
                for child_path, child_node in self.analyzer.nodes.items():
                    if child_path.startswith(node_path + '.'):
                        # Find direct children to get item count
                        parts_after = child_path[len(node_path) + 1:]
                        if '.' not in parts_after:
                            child_count = child_node.record_count
                            break
                if child_count > 0:
                    display_name = node_path.replace('root.', '')
                    list_nodes[display_name] = child_count

        # Second pass: find parent list for each list by walking up the path
        list_info = {}  # display_name -> (child_count, parent_name)
        for display_name, child_count in list_nodes.items():
            parent_name = None
            if '.' in display_name:
                # Walk up the path to find the nearest ancestor list
                parts = display_name.split('.')
                for i in range(len(parts) - 1, 0, -1):
                    potential_parent = '.'.join(parts[:i])
                    if potential_parent in list_nodes:
                        parent_name = potential_parent
                        break
            list_info[display_name] = (child_count, parent_name)

        if list_info:
            lines.append("**Data Elements (All Lists):**")

            # Recursive function to display list and its children
            def display_list_hierarchy(list_name, indent_level=0):
                if list_name not in list_info:
                    return
                count, _ = list_info[list_name]
                indent = "  " * indent_level
                lines.append(f"{indent}- {list_name}: {count:,} records")

                # Find and display children
                children = []
                for name, (child_count, child_parent) in list_info.items():
                    if child_parent == list_name:
                        children.append((name, child_count))
                # Sort children by count descending
                for child_name, _ in sorted(children, key=lambda x: -x[1]):
                    display_list_hierarchy(child_name, indent_level + 1)

            # Find and display top-level lists (those with no parent)
            top_level = []
            for name, (count, parent) in list_info.items():
                if parent is None:
                    top_level.append((name, count))

            # Sort top-level by count descending
            for list_name, _ in sorted(top_level, key=lambda x: -x[1]):
                display_list_hierarchy(list_name)

            lines.append("")

        lines.append(f"## Document: {schema_name}")
        lines.append("")
        lines.append("### Fields")
        lines.append("")

        # Create header with separate columns for each sample value
        header_parts = ["| # | Field Name | Type | Records | Pop % | Unique % | Table Context |"]
        for i in range(self.analyzer.top_value_count):
            header_parts.append(f" Sample {i+1} |")
        lines.append("".join(header_parts))

        # Create separator line
        separator_parts = ["|---|------------|------|---------|-------|----------|---------------|"]
        for i in range(self.analyzer.top_value_count):
            separator_parts.append("----------|")
        lines.append("".join(separator_parts))

        # Traverse nodes
        row_num = 0
        for node in self._traverse_nodes(self.analyzer.nodes, self.analyzer.root_node):
            row_num += 1
            field_name = node.node_desc
            field_type = node.node_type
            record_cnt = node.record_count

            # Only calculate percentages for actual data fields, not containers
            if field_type in ('dict', 'list'):
                pop_pct = ""
                unique_pct = ""
            else:
                # Use table context for accurate percentages
                table_count = node.table_record_count if hasattr(node, 'table_record_count') and node.table_record_count > 0 else self.analyzer.record_count
                pop_pct = f"{round(record_cnt / table_count * 100, 1)}%" if table_count else "0%"
                unique_cnt = len(node.unique_values)
                unique_pct = f"{round(unique_cnt / record_cnt * 100, 1)}%" if record_cnt else "0%"

            # Get top sample values with counts
            top_values = []
            for k, v in sorted(node.unique_values.items(), key=lambda v: v[1], reverse=True):
                if len(top_values) >= self.analyzer.top_value_count:
                    break
                top_values.append(f"{str(k)[:50]} ({v})")

            # Pad to ensure we have the right number of columns
            while len(top_values) < self.analyzer.top_value_count:
                top_values.append("")

            # Get table context name (short version)
            table_context_name = ""
            if hasattr(node, 'table_context') and node.table_context:
                # Show just the last part of the table context path
                table_context_name = node.table_context.split('.')[-1]
                table_context_name += f" ({node.table_record_count})"
            else:
                table_context_name = f"root ({self.analyzer.record_count})"

            # Build row with separate columns for each sample
            row_parts = [f"| {row_num} | {field_name} | {field_type} | {record_cnt} | {pop_pct} | {unique_pct} | {table_context_name} |"]
            for value in top_values:
                row_parts.append(f" {value} |")
            lines.append("".join(row_parts))

            # Add description if available (for Socrata files)
            if field_name in self.analyzer.field_metadata:
                metadata = self.analyzer.field_metadata[field_name]
                description = metadata.get('description', '')
                if description:
                    lines.append(f"| | *{description}* | | | | | | | |")

        return "\n".join(lines)

    def _generate_grouped(self):
        """Generate multi-table markdown format."""
        lines = []
        total_tables = len(self.analyzer.groups)
        total_fields = sum(len(group_data["nodes"]) - 1 for group_data in self.analyzer.groups.values())

        lines.append(f"**Total Tables:** {total_tables}")
        lines.append(f"**Total Fields:** {total_fields}")
        lines.append("")
        lines.append(f"**File Type:** {self.analyzer.file_type}")
        lines.append("")

        for group_value in sorted(self.analyzer.groups.keys()):
            group_data = self.analyzer.groups[group_value]
            group_nodes = group_data["nodes"]
            group_record_count = group_data["record_count"]
            field_count = len(group_nodes) - 1

            # Detect table type for this group
            # Temporarily swap nodes to analyze this group
            original_nodes = self.analyzer.nodes
            self.analyzer.nodes = group_nodes
            table_type = self.analyzer.detect_table_type(group_value)
            self.analyzer.nodes = original_nodes

            lines.append(f"## Table: {group_value}")
            lines.append(f"**Table Type:** {table_type}")
            lines.append("")
            lines.append(f"**Record Count:** {group_record_count}")
            lines.append(f"**Field Count:** {field_count}")
            lines.append("")
            lines.append("### Fields")
            lines.append("")

            # Create header
            header_parts = ["| # | Field Name | Type | Records | Pop % | Unique % |"]
            for i in range(self.analyzer.top_value_count):
                header_parts.append(f" Sample {i+1} |")
            lines.append("".join(header_parts))

            # Create separator
            separator_parts = ["|---|------------|------|---------|-------|----------|"]
            for i in range(self.analyzer.top_value_count):
                separator_parts.append("----------|")
            lines.append("".join(separator_parts))

            # Traverse nodes for this group
            row_num = 0
            for node in self._traverse_nodes(group_nodes, group_nodes["root"]):
                row_num += 1
                field_name = node.node_desc
                field_type = node.node_type
                record_cnt = node.record_count

                # Only calculate percentages for actual data fields, not containers
                if field_type in ('dict', 'list'):
                    pop_pct = ""
                    unique_pct = ""
                else:
                    pop_pct = f"{round(record_cnt / group_record_count * 100, 1)}%" if group_record_count else "0%"
                    unique_cnt = len(node.unique_values)
                    unique_pct = f"{round(unique_cnt / record_cnt * 100, 1)}%" if record_cnt else "0%"

                # Get top sample values
                top_values = []
                for k, v in sorted(node.unique_values.items(), key=lambda v: v[1], reverse=True):
                    if len(top_values) >= self.analyzer.top_value_count:
                        break
                    top_values.append(f"{str(k)[:50]} ({v})")

                while len(top_values) < self.analyzer.top_value_count:
                    top_values.append("")

                # Build row
                row_parts = [f"| {row_num} | {field_name} | {field_type} | {record_cnt} | {pop_pct} | {unique_pct} |"]
                for value in top_values:
                    row_parts.append(f" {value} |")
                lines.append("".join(row_parts))

                # Add description if available (for Socrata files)
                if field_name in self.analyzer.field_metadata:
                    metadata = self.analyzer.field_metadata[field_name]
                    description = metadata.get('description', '')
                    if description:
                        lines.append(f"| | *{description}* | | | | | | | |")

            lines.append("")

        return "\n".join(lines)


class EnumerationReporter(BaseReporter):
    """Generates enumeration reports for code value analysis."""

    def generate(self):
        """Generate enumeration report based on config type."""
        if self.analyzer.is_pivot_enumeration:
            return self._generate_pivot_enumeration()
        elif not self.analyzer.enumerate_attrs or not self.analyzer.enumeration_stats:
            return [["No enumeration data available"]]
        else:
            if self.analyzer.group_by_attr:
                return self._generate_grouped_enumeration()
            else:
                return self._generate_standard_enumeration()

    def _generate_standard_enumeration(self):
        """Generate standard (non-grouped) enumeration report."""
        header = ["attribute", "code_value", "record_cnt", "record_pct", "unique_records", "unique_pct"]
        header.extend([f"top_record{i+1}" for i in range(min(self.analyzer.top_value_count, 5))])

        rows = []
        for attr_path in sorted(self.analyzer.enumerate_attrs):
            attr_stats = self.analyzer.enumeration_stats[attr_path]

            if not attr_stats:
                continue

            total_occurrences = sum(stats['count'] for stats in attr_stats.values())
            sorted_codes = sorted(attr_stats.items(), key=lambda x: x[1]['count'], reverse=True)

            for code_value, stats in sorted_codes:
                record_cnt = stats['count']
                record_pct = round(record_cnt / total_occurrences * 100, 2) if total_occurrences else 0
                unique_records = len(stats['records'])
                unique_pct = round(unique_records / self.analyzer.record_count * 100, 2) if self.analyzer.record_count else 0

                sample_records = [""] * min(self.analyzer.top_value_count, 5)
                for i, record_id in enumerate(sorted(stats['records'])):
                    if i >= min(self.analyzer.top_value_count, 5):
                        break
                    sample_records[i] = f"{record_id}"

                rows.append([attr_path, code_value, record_cnt, record_pct, unique_records, unique_pct] + sample_records)

        return [header] + rows

    def _generate_grouped_enumeration(self):
        """Generate grouped enumeration report."""
        header = [self.analyzer.group_by_attr, "attribute", "code_value", "record_cnt", "record_pct", "unique_records", "unique_pct"]
        header.extend([f"top_record{i+1}" for i in range(min(self.analyzer.top_value_count, 5))])

        rows = []
        for group_value in sorted(self.analyzer.enumeration_stats.keys()):
            group_enum_stats = self.analyzer.enumeration_stats[group_value]
            group_record_count = self.analyzer.groups[group_value]["record_count"]

            for attr_path in sorted(self.analyzer.enumerate_attrs):
                attr_stats = group_enum_stats.get(attr_path, {})

                if not attr_stats:
                    continue

                total_occurrences = sum(stats['count'] for stats in attr_stats.values())
                sorted_codes = sorted(attr_stats.items(), key=lambda x: x[1]['count'], reverse=True)

                for code_value, stats in sorted_codes:
                    record_cnt = stats['count']
                    record_pct = round(record_cnt / total_occurrences * 100, 2) if total_occurrences else 0
                    unique_records = len(stats['records'])
                    unique_pct = round(unique_records / group_record_count * 100, 2) if group_record_count else 0

                    sample_records = [""] * min(self.analyzer.top_value_count, 5)
                    for i, record_id in enumerate(sorted(stats['records'])):
                        if i >= min(self.analyzer.top_value_count, 5):
                            break
                        sample_records[i] = f"{record_id}"

                    rows.append([group_value, attr_path, code_value, record_cnt, record_pct, unique_records, unique_pct] + sample_records)

        return [header] + rows

    def _generate_pivot_enumeration(self):
        """Generate pivot enumeration report."""
        if not self.analyzer.pivot_stats:
            return [["No pivot enumeration data available"]]

        config = self.analyzer.enumerate_config
        grouping_attrs = config['grouping_attrs']

        # Create header
        header = []
        if self.analyzer.group_by_attr:
            header.append(self.analyzer.group_by_attr)

        for attr in grouping_attrs:
            header.append(f"{config['level']}.{attr}" if config['level'] != 'root' else attr)

        header.extend(["record_cnt", "record_pct", "unique_values", "unique_pct"])
        header.extend([f"top_value{i+1}" for i in range(min(self.analyzer.top_value_count, 5))])

        rows = []

        if self.analyzer.group_by_attr:
            all_rows = []
            for group_value in self.analyzer.pivot_stats.keys():
                group_pivot_stats = self.analyzer.pivot_stats[group_value]
                group_record_count = self.analyzer.groups[group_value]["record_count"] if self.analyzer.groups else self.analyzer.record_count

                for grouping_key, value_stats in group_pivot_stats.items():
                    total_record_cnt = sum(stats['count'] for stats in value_stats.values())
                    all_records = set()
                    value_counts = {}

                    for value, stats in value_stats.items():
                        all_records.update(stats['records'])
                        value_counts[value] = stats['count']

                    record_pct = round(total_record_cnt / group_record_count * 100, 2) if group_record_count else 0
                    unique_values = len(value_stats)
                    unique_pct = round(unique_values / total_record_cnt * 100, 2) if total_record_cnt else 0

                    top_values = [""] * min(self.analyzer.top_value_count, 5)
                    for i, (value, count) in enumerate(sorted(value_counts.items(), key=lambda x: x[1], reverse=True)):
                        if i >= min(self.analyzer.top_value_count, 5):
                            break
                        top_values[i] = f"{value} ({count})"

                    row = [group_value]
                    row.extend(list(grouping_key))
                    row.extend([total_record_cnt, record_pct, unique_values, unique_pct])
                    row.extend(top_values)
                    all_rows.append(row)

            rows = sorted(all_rows, key=lambda x: (x[0],) + tuple(x[1:len(grouping_attrs)+1]))
        else:
            for grouping_key, value_stats in sorted(self.analyzer.pivot_stats.items()):
                total_record_cnt = sum(stats['count'] for stats in value_stats.values())
                all_records = set()
                value_counts = {}

                for value, stats in value_stats.items():
                    all_records.update(stats['records'])
                    value_counts[value] = stats['count']

                record_pct = round(total_record_cnt / self.analyzer.record_count * 100, 2) if self.analyzer.record_count else 0
                unique_values = len(value_stats)
                unique_pct = round(unique_values / total_record_cnt * 100, 2) if total_record_cnt else 0

                top_values = [""] * min(self.analyzer.top_value_count, 5)
                for i, (value, count) in enumerate(sorted(value_counts.items(), key=lambda x: x[1], reverse=True)):
                    if i >= min(self.analyzer.top_value_count, 5):
                        break
                    top_values[i] = f"{value} ({count})"

                row = list(grouping_key)
                row.extend([total_record_cnt, record_pct, unique_values, unique_pct])
                row.extend(top_values)
                rows.append(row)

        return [header] + rows


class CodeListReporter(BaseReporter):
    """Generates code list enumeration reports with auto-detection."""

    def generate(self):
        """Generate code list report showing all detected code fields and their values."""
        # Detect code lists
        code_lists = self.analyzer.detect_code_lists()

        if not code_lists:
            return [['No code lists detected']]

        # Sort by field name
        sorted_code_lists = sorted(code_lists.items(), key=lambda x: x[0])

        # Create header
        header = ['Field', 'Code Value', 'Count', '%', 'Table Context', 'Total Codes']

        rows = []
        for field_path, info in sorted_code_lists:
            # Sort values by count (descending)
            sorted_values = sorted(info['values'].items(), key=lambda x: x[1], reverse=True)

            for i, (code_value, count) in enumerate(sorted_values):
                pct = (count / info['record_count'] * 100) if info['record_count'] > 0 else 0

                row = [
                    field_path if i == 0 else '',  # Only show field name on first row
                    code_value,
                    count,
                    f"{pct:.1f}%",
                    info['table_context'] if i == 0 else '',
                    info['unique_count'] if i == 0 else ''
                ]
                rows.append(row)

            # Add separator row after each field
            if sorted_code_lists[-1][0] != field_path:
                rows.append(['', '', '', '', '', ''])

        return [header] + rows


def get_reporter(report_type, analyzer):
    """Factory function to get appropriate reporter.

    Args:
        report_type: Type of report (csv, markdown, tree, enumeration, codelist)
        analyzer: FileAnalyzer instance

    Returns:
        Reporter instance
    """
    reporters = {
        'csv': CSVReporter,
        'markdown': MarkdownReporter,
        'tree': TreeReporter,
        'enumeration': EnumerationReporter,
        'codelist': CodeListReporter
    }
    reporter_class = reporters.get(report_type.lower())
    if not reporter_class:
        raise ValueError(f"Unsupported report type: {report_type}")
    return reporter_class(analyzer)


def strip_namespace(tag):
    """Return XML tag without namespace info like '{ns}Tag'."""
    if isinstance(tag, str) and tag.startswith('{'):
        return tag.split('}', 1)[1]
    return tag


def element_to_dict(element):
    """Convert an XML element to a dictionary recursively."""
    result = {}
    if element.attrib:
        result.update({strip_namespace(k): v for k, v in element.attrib.items()})
    if element.text and element.text.strip():
        result['text'] = element.text.strip()

    children = {}
    for child in element:
        child_dict = element_to_dict(child)
        tag = strip_namespace(child.tag)
        if tag in children:
            if not isinstance(children[tag], list):
                children[tag] = [children[tag]]
            children[tag].append(child_dict)
        else:
            children[tag] = child_dict

    result.update(children)
    return result


def report_viewer(report):
    """Display report using prettytable with pager."""
    table_object = prettytable.PrettyTable()
    table_object.horizontal_char = "\u2500"
    table_object.vertical_char = "\u2502"
    table_object.junction_char = "\u253c"
    table_object.field_names = report[0]
    table_object.add_rows(report[1:])
    for column in report[0]:
        if any(column.endswith(x) for x in ["cnt", "pct"]):
            table_object.align[column] = "r"
        else:
            table_object.align[column] = "l"
    report_str = table_object.get_string()
    less = subprocess.Popen(["less", "-FMXSR"], stdin=subprocess.PIPE)
    try:
        less.stdin.write(report_str.encode("utf-8"))
        less.stdin.close()
        less.wait()
        print()
    except IOError as ex:
        print(f"\n{ex}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze file structure and generate statistics reports or code enumeration analyses.",
        epilog="""
USAGE EXAMPLES:

Schema Analysis (discover file structure):
  %(prog)s data.jsonl -o schema.csv
  %(prog)s data.jsonl --group_by schema -o schema_by_type.csv

Code Enumeration (analyze specific attribute values):
  %(prog)s data.jsonl --enumerate "properties:type,country:number" -o analysis.csv
  %(prog)s data.jsonl --group_by schema=Identification --enumerate "properties:type:number" -o id_types.csv

Legacy Enumeration (backward compatibility):
  %(prog)s data.jsonl --enumerate "properties.type" -o codes.csv

Filtering:
  %(prog)s data.jsonl --filter "status=active" -o filtered_schema.csv
  %(prog)s data.jsonl --group_by schema=Person --enumerate "properties:name:identifier" -o person_names.csv

ENUMERATION FORMATS:
  Legacy: --enumerate "attr1,attr2"          (lists code values in specified attributes)
  Pivot:  --enumerate "level:dims:value"     (cross-tabulates dimensions against values)

  Example: --enumerate "properties:type,country:number"
    - Level: properties (base object level)
    - Dimensions: type,country (grouping attributes)
    - Value: number (attribute being analyzed)

GROUP_BY FORMATS:
  Basic:     --group_by schema               (group statistics by schema)
  Filtered:  --group_by schema=Person        (group by schema, show only Person records)
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("input_file",
                       help="Input file or directory path (supports CSV, JSON, JSONL, Parquet, XML)")
    parser.add_argument("-t", "--file_type",
                       help='File type: "csv", "jsonl", "json", "parquet", "xml" (auto-detected if not specified)')
    parser.add_argument("-e", "--encoding", default="utf-8",
                       help="File encoding (default: utf-8)")
    parser.add_argument("-o", "--output_file",
                       help="Output CSV file path (required for --enumerate, optional for schema analysis)")
    parser.add_argument("--top_values", type=int, default=5,
                       help="Number of top values to display/analyze (default: 5)")
    parser.add_argument("--filter",
                       help="Filter records: 'attribute=value' (e.g., 'status=active', 'type=Person')")
    parser.add_argument("--group_by",
                       help="Group analysis by attribute. Formats: 'attr' or 'attr=value' (e.g., 'schema' or 'schema=Person')")
    parser.add_argument("--enumerate",
                       help="""Enumerate code values. Formats:
Legacy: 'attr1,attr2' - list codes in attributes
Pivot: 'level:dimensions:value' - cross-tabulate dimensions vs values
Example: 'properties:type,country:number'""")
    parser.add_argument("--detect-codes", action="store_true",
                       help="Auto-detect and enumerate code lists (low-cardinality string fields)")
    args = parser.parse_args()

    # Handle directory input
    if os.path.isdir(args.input_file):
        # Find all data files in directory
        data_extensions = ('.csv', '.json', '.jsonl', '.xml', '.xmls', '.parquet')
        file_list = []
        for ext in data_extensions:
            pattern = os.path.join(args.input_file, f'*{ext}')
            file_list.extend(glob.glob(pattern))

        if not file_list:
            print(f"\nNo data files found in directory: {args.input_file}\n")
            print(f"Supported extensions: {', '.join(data_extensions)}\n")
            sys.exit(1)

        file_list.sort()  # Process in consistent order
        print(f"\nFound {len(file_list)} file(s) in directory {args.input_file}\n")
    else:
        # Handle file pattern input
        file_list = glob.glob(args.input_file)
        if not file_list:
            print("\nPlease supply a valid input file specification on the command line\n")
            sys.exit(1)

    if not args.file_type:
        ext = pathlib.Path(file_list[0]).suffix.lower()
        if ext in (".parquet", ".json", ".jsonl", ".xml", ".xmls"):
            args.file_type = ext[1:] if ext != ".xmls" else "xml"  # Map .xmls to 'xml'
        else:
            args.file_type = "csv"
    else:
        args.file_type = args.file_type.lower()

    if args.file_type.lower() == "parquet" and not pd:
        print("\nPandas must be installed to analyze parquet files, try: pip3 install pandas\n")
        sys.exit(1)
    if args.file_type.lower() in ("xml", "xmls") and not hasattr(ET, 'parse'):  # Update check to include xmls
        print("\nxml.etree.ElementTree is required for XML files.\n")
        sys.exit(1)

    proc_start_time = time.time()
    shut_down = 0

    # Parse group_by parameter - check for filtering syntax
    group_by_attr = None
    group_by_filter = None
    if args.group_by:
        if '=' in args.group_by:
            group_by_attr, group_by_filter = args.group_by.split('=', 1)
        else:
            group_by_attr = args.group_by

    # Parse enumeration parameter - check for new pivot syntax
    enumerate_config = None
    if args.enumerate:
        if ':' in args.enumerate and args.enumerate.count(':') == 2:
            # New pivot syntax: level:grouping_attributes:value_attribute
            level, grouping_attrs, value_attr = args.enumerate.split(':')
            enumerate_config = {
                'level': level.strip(),
                'grouping_attrs': [attr.strip() for attr in grouping_attrs.split(',')],
                'value_attr': value_attr.strip()
            }
        else:
            # Legacy syntax for backward compatibility
            enumerate_config = [attr.strip() for attr in args.enumerate.split(',')]

    # Check for conflicting options
    if enumerate_config and not args.output_file:
        print("\nError: When using --enumerate, you must specify -o/--output_file for the enumeration CSV output.\n")
        sys.exit(1)

    analyzer = FileAnalyzer(args.input_file, args.file_type, group_by_attr, enumerate_config)
    analyzer.top_value_count = args.top_values

    # Set group_by filter if specified
    if group_by_filter:
        analyzer.group_by_filter = group_by_filter

    # Parse filter if provided
    filter_attr = None
    filter_value = None
    if args.filter:
        filter_attr, filter_value = args.filter.split("=")

    # Determine if we should auto-group by file when processing multiple files
    auto_group_by_file = len(file_list) > 1 and not group_by_attr
    if auto_group_by_file:
        # Enable grouping by filename
        analyzer.group_by_attr = "_source_file"
        analyzer.groups = {}
        print(f"Auto-grouping by source file (processing {len(file_list)} files)\n")

    # Error handling constants
    MAX_ERRORS_DISPLAYED = 10
    ERROR_THRESHOLD_PCT = 10
    MIN_RECORDS_FOR_THRESHOLD = 100
    MAX_CONSECUTIVE_ERRORS = 10

    # Error tracking variables
    error_count = 0
    consecutive_errors = 0

    try:
        file_num = 0
        for file_name in file_list:
            file_num += 1
            print(f"reading file {file_num} of {len(file_list)}: {file_name}")

            # Auto-detect file type for each file (useful when processing directories)
            file_type = args.file_type
            if len(file_list) > 1 and not args.file_type:
                ext = pathlib.Path(file_name).suffix.lower()
                if ext in (".parquet", ".json", ".jsonl", ".xml", ".xmls"):
                    file_type = ext[1:] if ext != ".xmls" else "xml"
                else:
                    file_type = "csv"

            # Extract schema name from filename (remove extension)
            schema_name = pathlib.Path(file_name).stem

            # Use the new reader factory
            reader = get_reader(file_type, file_name, args.encoding)

            with reader:
                # Check if Socrata format was detected (after open()) and update file_type
                if hasattr(reader, 'is_socrata') and reader.is_socrata:
                    analyzer.file_type = 'socrata-json'
                    # Transfer field metadata from reader to analyzer
                    if hasattr(reader, 'field_metadata'):
                        analyzer.field_metadata = reader.field_metadata

                # Capture XML namespaces if available
                if hasattr(reader, 'namespaces') and reader.namespaces:
                    analyzer.xml_namespaces = reader.namespaces

                for row in reader:
                    # Check for parse errors (returned as ParseError sentinel)
                    if isinstance(row, ParseError):
                        error_count += 1
                        consecutive_errors += 1
                        if error_count <= MAX_ERRORS_DISPLAYED:
                            print(f"ERROR: {row}", file=sys.stderr)
                        elif error_count == MAX_ERRORS_DISPLAYED + 1:
                            print("(additional errors suppressed)", file=sys.stderr)

                        # Check consecutive errors threshold
                        if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                            print(f"\nABORTED: {MAX_CONSECUTIVE_ERRORS} consecutive parse errors", file=sys.stderr)
                            shut_down = 1
                            break

                        # Check percentage threshold (after minimum records)
                        total_processed = analyzer.record_count + error_count
                        if total_processed >= MIN_RECORDS_FOR_THRESHOLD:
                            error_pct = (error_count / total_processed) * 100
                            if error_pct >= ERROR_THRESHOLD_PCT:
                                print(f"\nABORTED: Error rate {error_pct:.1f}% exceeds {ERROR_THRESHOLD_PCT}% threshold", file=sys.stderr)
                                shut_down = 1
                                break
                        continue

                    consecutive_errors = 0  # Reset on success

                    # Add schema identifier if auto-grouping
                    if auto_group_by_file and isinstance(row, dict):
                        row["_source_file"] = schema_name

                    if args.filter and not analyzer.matches_filter(row, filter_attr, filter_value):
                        continue

                    analyzer.record_count += 1
                    if analyzer.record_count % 10000 == 0:
                        print(f"{analyzer.record_count:,} rows read")

                    # Use the new process_record method that handles grouping
                    analyzer.process_record(row)

                if shut_down:
                    break  # Exit file loop if aborted

    except KeyboardInterrupt:
        shut_down = 9

    status = "complete" if shut_down == 0 else ("aborted" if shut_down == 1 else "interrupted")
    print(f"\n{analyzer.record_count:,} rows read, file {status}")
    if error_count > 0:
        print(f"{error_count:,} records skipped due to parse errors\n")
    else:
        print()

    # Calculate table contexts for proper percentage calculations
    analyzer.calculate_table_contexts()

    # If enumeration is requested, only generate enumeration report
    if enumerate_config:
        has_enumeration_data = (analyzer.enumeration_stats and any(analyzer.enumeration_stats.values())) or \
                              (analyzer.pivot_stats and any(analyzer.pivot_stats.values()))
        if has_enumeration_data:
            enum_report = analyzer.generate_enumeration_report()
            if len(enum_report) > 1:  # Has data beyond header
                if args.output_file:
                    with open(args.output_file, "w") as file:
                        writer = csv.writer(file)
                        writer.writerows(enum_report)
                    print(f"enumeration report saved to {args.output_file}\n")
                else:
                    print("\n" + "="*60)
                    print("CODE ENUMERATION REPORT")
                    print("="*60)

                    if prettytable:
                        report_viewer(enum_report)
                    else:
                        # Simple text output for enumeration
                        header = enum_report[0]
                        print(f"{'Attribute':<30} {'Code Value':<20} {'Count':<8} {'Pct':<8} {'Records':<8} {'Sample Records':<50}")
                        print("-" * 120)
                        for row in enum_report[1:]:
                            if len(row) >= 6:
                                sample_records = " | ".join(str(r) for r in row[6:] if r)
                                print(f"{row[0]:<30} {row[1]:<20} {row[2]:<8} {row[3]:<8} {row[4]:<8} {sample_records:<50}")
                        print()
            else:
                print("No enumeration data found for the specified attributes.\n")
        else:
            print("No enumeration data found for the specified attributes and filters.\n")
            print("This could be because:")
            print("- No records matched the group filter criteria")
            print("- The specified attribute paths don't exist in the data")
            print("- The data structure doesn't match the expected format")
            print("\nTip: Try running without --enumerate first to see the schema structure.\n")
            sys.exit(1)

        # Exit after enumeration - don't generate schema report
        sys.exit(shut_down)
    elif args.detect_codes:
        # Generate code list report
        reporter = get_reporter('codelist', analyzer)
        code_report = reporter.generate()

        if len(code_report) > 1:  # Has data beyond header
            if args.output_file:
                with open(args.output_file, "w") as file:
                    writer = csv.writer(file)
                    writer.writerows(code_report)
                print(f"code list report saved to {args.output_file}\n")
            else:
                print("\n" + "="*80)
                print("AUTO-DETECTED CODE LISTS")
                print("="*80)
                print()

                if prettytable:
                    report_viewer(code_report)
                else:
                    # Simple text output for code lists
                    header = code_report[0]
                    print(f"{'Field':<40} {'Code Value':<20} {'Count':<8} {'%':<8} {'Table':<20} {'Total':<8}")
                    print("-" * 120)
                    for row in code_report[1:]:
                        if len(row) >= 6 and row[0]:  # Skip separator rows
                            print(f"{row[0]:<40} {row[1]:<20} {row[2]:<8} {row[3]:<8} {row[4]:<20} {row[5]:<8}")
                        elif len(row) >= 6:
                            # Continuation row (same field)
                            print(f"{'':40} {row[1]:<20} {row[2]:<8} {row[3]:<8} {'':20} {'':8}")
                    print()
        else:
            print("\nNo code lists detected. Try adjusting detection thresholds.\n")

        # Exit after code list report - don't generate schema report
        sys.exit(shut_down)
    else:
        # Generate main schema report
        if args.output_file:
            # Check if output should be tree, markdown or CSV
            output_file = pathlib.Path(args.output_file)
            output_name = output_file.name.lower()
            output_ext = output_file.suffix.lower()

            if '.tree.md' in output_name or output_name.endswith('_tree.md'):
                # Generate tree format
                reporter = get_reporter('tree', analyzer)
                tree_content = reporter.generate()
                with open(args.output_file, "w") as file:
                    file.write(tree_content)
                print(f"tree schema saved to {args.output_file}\n")
            elif output_ext == '.md':
                # Generate markdown format
                markdown_content = analyzer.generate_markdown_report()
                with open(args.output_file, "w") as file:
                    file.write(markdown_content)
                print(f"markdown schema saved to {args.output_file}\n")
            else:
                # Generate CSV format (default)
                report_rows = analyzer.generate("report")
                with open(args.output_file, "w") as file:
                    writer = csv.writer(file)
                    writer.writerows(report_rows)
                print(f"statistical report saved to {args.output_file}\n")
        elif prettytable:
            # Display to console
            report_rows = analyzer.generate("report")
            report_viewer(report_rows)
        else:
            # Fallback: simple text output when prettytable is not available
            output_lines = []
            output_lines.append("Statistical Analysis Report:")
            output_lines.append("=" * 100)
            header = report_rows[0] if report_rows else []
            if header:
                output_lines.append(f"{'Attribute':<25} {'Type':<15} {'Count':<8} {'Pct':<8} {'Unique':<8} {'Top Value':<30}")
                output_lines.append("-" * 100)
                for row in report_rows[1:]:  # Skip header row
                    if len(row) >= 7:  # Ensure we have enough columns
                        output_lines.append(f"{row[0]:<25} {row[1]:<15} {row[2]:<8} {row[3]:<8} {row[4]:<8} {row[6]:<30}")
            output_lines.append("")
            output_lines.append("Note: Install prettytable for better formatted output: pip install prettytable")
            output_lines.append("Or use -o filename.csv to save report to CSV file")
            output_lines.append("")

            # Use less pager for better viewing experience
            report_str = "\n".join(output_lines)
            try:
                less = subprocess.Popen(["less", "-FMXSR"], stdin=subprocess.PIPE)
                less.stdin.write(report_str.encode("utf-8"))
                less.stdin.close()
                less.wait()
                print()
            except (IOError, FileNotFoundError) as ex:
                # Fallback to print if less is not available
                print(report_str)

    sys.exit(shut_down)
