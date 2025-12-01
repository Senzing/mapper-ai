#!/usr/bin/env python3
"""
ICIJ → Senzing Mapper

Maps all ICIJ Offshore Leaks data to Senzing JSON format:
- Entities (organizations)
- Officers (people and organizations)
- Intermediaries (people and organizations)
- Others (organizations)

Denormalizes registered_address relationships onto all entity types.

Usage:
  python3 icij_mapper.py /path/to/icij/data
  python3 icij_mapper.py /path/to/icij/data --sample 100
  python3 icij_mapper.py /path/to/icij/data -o output.jsonl
  python3 icij_mapper.py /path/to/icij/data --entities-only
  python3 icij_mapper.py . --officers-only
"""

import csv
import json
import re
import sys
from collections import defaultdict


def load_addresses(filename='nodes-addresses.csv'):
    """Load address nodes into memory.

    Returns:
        dict: node_id → address record
    """
    addresses = {}
    print(f"Loading addresses from {filename}...")

    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            addresses[row['node_id']] = row

    print(f"  Loaded {len(addresses):,} address records")
    return addresses


def load_registered_addresses(filename='relationships.csv'):
    """Load registered_address relationships.

    Returns:
        dict: entity_node_id → address_node_id
    """
    entity_to_address = {}
    print(f"Loading registered_address relationships from {filename}...")

    count = 0
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['rel_type'] == 'registered_address':
                entity_to_address[row['node_id_start']] = row['node_id_end']
                count += 1

    print(f"  Loaded {count:,} registered_address relationships")
    return entity_to_address


def detect_record_type(name):
    """Detect if name is a person or organization.

    Args:
        name: Name string

    Returns:
        str: "PERSON" or "ORGANIZATION"
    """
    if not name:
        return "ORGANIZATION"

    # Indicators of person names
    person_indicators = [
        r'\b(MR|MRS|MS|MISS|DR|PROF)\b',  # Titles
        r'\b(JR|SR|II|III|IV)\b',  # Suffixes
        r'^[A-Z][a-z]+\s+[A-Z][a-z]+$',  # FirstName LastName
        r',\s*(MR|MRS|MS|MISS|DR)',  # Comma + title
    ]

    # Indicators of organization names
    org_indicators = [
        r'\b(LTD|LLC|INC|CORP|CORPORATION|COMPANY|CO|SA|NV|BV|AG|GMBH|SL|SRL|SARL|TRUST|FOUNDATION)\b',
        r'\b(LIMITED|INCORPORATED|ASSOCIATES|PARTNERS|GROUP|HOLDINGS)\b',
    ]

    name_upper = name.upper()

    # Check org indicators first (stronger signal)
    for pattern in org_indicators:
        if re.search(pattern, name_upper):
            return "ORGANIZATION"

    # Check person indicators
    for pattern in person_indicators:
        if re.search(pattern, name_upper):
            return "PERSON"

    # Default: if comma-separated likely person, otherwise organization
    if ',' in name:
        return "PERSON"

    return "ORGANIZATION"


def parse_person_name(name):
    """Parse person name into components.

    Args:
        name: Name string

    Returns:
        dict: NAME_FULL, NAME_FIRST, NAME_LAST if parseable
    """
    if not name:
        return {"NAME_FULL": ""}

    # Remove extra whitespace
    name = ' '.join(name.split())

    result = {"NAME_FULL": name}

    # Try "LAST, FIRST" format
    if ',' in name:
        parts = name.split(',', 1)
        if len(parts) == 2:
            last = parts[0].strip()
            first = parts[1].strip()
            # Remove titles
            first = re.sub(r'\b(MR|MRS|MS|MISS|DR|PROF)\.?\s*', '', first, flags=re.IGNORECASE).strip()
            if first and last:
                result["NAME_FIRST"] = first
                result["NAME_LAST"] = last
                return result

    # Try "FIRST LAST" format (2 words only)
    words = name.split()
    if len(words) == 2:
        result["NAME_FIRST"] = words[0]
        result["NAME_LAST"] = words[1]

    return result


def map_entity(entity, address_record=None):
    """Map ICIJ entity (organization) to Senzing JSON format.

    Args:
        entity: Entity record dict
        address_record: Optional address record dict

    Returns:
        dict: Senzing JSON record
    """
    senzing_record = {
        "DATA_SOURCE": "ICIJ_ENTITIES",
        "RECORD_ID": entity['node_id']
    }

    features = []
    features.append({"RECORD_TYPE": "ORGANIZATION"})

    # Names
    if entity.get('name'):
        features.append({"NAME_ORG": entity['name'], "NAME_TYPE": "PRIMARY"})

    if entity.get('original_name') and entity['original_name'] != entity.get('name'):
        features.append({"NAME_ORG": entity['original_name'], "NAME_TYPE": "ORIGINAL"})

    if entity.get('former_name'):
        features.append({"NAME_ORG": entity['former_name'], "NAME_TYPE": "FORMER"})

    # Tax ID
    if entity.get('ibcRUC'):
        features.append({
            "TAX_ID_NUMBER": entity['ibcRUC'],
            "TAX_ID_COUNTRY": entity.get('jurisdiction', '')
        })

    # Registered address (denormalized)
    if address_record:
        addr_full = address_record.get('address', '')
        if addr_full:
            features.append({
                "ADDR_FULL": addr_full,
                "ADDR_TYPE": "REGISTERED",
                "ADDR_COUNTRY": address_record.get('country_codes', '')
            })

    # Entity's own address field
    if entity.get('address'):
        features.append({
            "ADDR_FULL": entity['address'],
            "ADDR_TYPE": "PRIMARY"
        })

    # Incorporation date
    if entity.get('incorporation_date'):
        features.append({"DATE_OF_FORMATION": entity['incorporation_date']})

    senzing_record["FEATURES"] = features

    # Payload attributes
    if entity.get('jurisdiction'):
        senzing_record['jurisdiction'] = entity['jurisdiction']
    if entity.get('jurisdiction_description'):
        senzing_record['jurisdiction_description'] = entity['jurisdiction_description']
    if entity.get('company_type'):
        senzing_record['company_type'] = entity['company_type']
    if entity.get('internal_id'):
        senzing_record['internal_id'] = entity['internal_id']
    if entity.get('inactivation_date'):
        senzing_record['inactivation_date'] = entity['inactivation_date']
    if entity.get('struck_off_date'):
        senzing_record['struck_off_date'] = entity['struck_off_date']
    if entity.get('dorm_date'):
        senzing_record['dorm_date'] = entity['dorm_date']
    if entity.get('status'):
        senzing_record['status'] = entity['status']
    if entity.get('service_provider'):
        senzing_record['service_provider'] = entity['service_provider']
    if entity.get('country_codes'):
        senzing_record['country_codes'] = entity['country_codes']
    if entity.get('countries'):
        senzing_record['countries'] = entity['countries']
    if entity.get('sourceID'):
        senzing_record['sourceID'] = entity['sourceID']
    if entity.get('valid_until'):
        senzing_record['valid_until'] = entity['valid_until']
    if entity.get('note'):
        senzing_record['note'] = entity['note']

    return senzing_record


def map_officer(officer, address_record=None):
    """Map ICIJ officer (person or organization) to Senzing JSON format.

    Args:
        officer: Officer record dict
        address_record: Optional address record dict

    Returns:
        dict: Senzing JSON record
    """
    senzing_record = {
        "DATA_SOURCE": "ICIJ_OFFICERS",
        "RECORD_ID": officer['node_id']
    }

    features = []

    # Detect record type
    record_type = detect_record_type(officer.get('name', ''))
    features.append({"RECORD_TYPE": record_type})

    # Name
    if officer.get('name'):
        if record_type == "PERSON":
            name_parts = parse_person_name(officer['name'])
            features.append(name_parts)
        else:
            features.append({"NAME_ORG": officer['name'], "NAME_TYPE": "PRIMARY"})

    # Country of association
    if officer.get('countries'):
        features.append({"COUNTRY_OF_ASSOCIATION": officer['countries']})

    # Registered address (denormalized)
    if address_record:
        addr_full = address_record.get('address', '')
        if addr_full:
            features.append({
                "ADDR_FULL": addr_full,
                "ADDR_TYPE": "REGISTERED",
                "ADDR_COUNTRY": address_record.get('country_codes', '')
            })

    senzing_record["FEATURES"] = features

    # Payload
    if officer.get('country_codes'):
        senzing_record['country_codes'] = officer['country_codes']
    if officer.get('sourceID'):
        senzing_record['sourceID'] = officer['sourceID']
    if officer.get('valid_until'):
        senzing_record['valid_until'] = officer['valid_until']
    if officer.get('note'):
        senzing_record['note'] = officer['note']

    return senzing_record


def map_intermediary(intermediary, address_record=None):
    """Map ICIJ intermediary (person or organization) to Senzing JSON format.

    Args:
        intermediary: Intermediary record dict
        address_record: Optional address record dict

    Returns:
        dict: Senzing JSON record
    """
    senzing_record = {
        "DATA_SOURCE": "ICIJ_INTERMEDIARIES",
        "RECORD_ID": intermediary['node_id']
    }

    features = []

    # Detect record type
    record_type = detect_record_type(intermediary.get('name', ''))
    features.append({"RECORD_TYPE": record_type})

    # Name
    if intermediary.get('name'):
        if record_type == "PERSON":
            name_parts = parse_person_name(intermediary['name'])
            features.append(name_parts)
        else:
            features.append({"NAME_ORG": intermediary['name'], "NAME_TYPE": "PRIMARY"})

    # Address from intermediary record itself
    if intermediary.get('address'):
        features.append({
            "ADDR_FULL": intermediary['address'],
            "ADDR_TYPE": "PRIMARY"
        })

    # Registered address (denormalized)
    if address_record:
        addr_full = address_record.get('address', '')
        if addr_full:
            features.append({
                "ADDR_FULL": addr_full,
                "ADDR_TYPE": "REGISTERED",
                "ADDR_COUNTRY": address_record.get('country_codes', '')
            })

    # Country of association
    if intermediary.get('countries'):
        features.append({"COUNTRY_OF_ASSOCIATION": intermediary['countries']})

    senzing_record["FEATURES"] = features

    # Payload
    if intermediary.get('status'):
        senzing_record['status'] = intermediary['status']
    if intermediary.get('internal_id'):
        senzing_record['internal_id'] = intermediary['internal_id']
    if intermediary.get('country_codes'):
        senzing_record['country_codes'] = intermediary['country_codes']
    if intermediary.get('sourceID'):
        senzing_record['sourceID'] = intermediary['sourceID']
    if intermediary.get('valid_until'):
        senzing_record['valid_until'] = intermediary['valid_until']
    if intermediary.get('note'):
        senzing_record['note'] = intermediary['note']

    return senzing_record


def map_other(other, address_record=None):
    """Map ICIJ other entity (organization) to Senzing JSON format.

    Args:
        other: Other record dict
        address_record: Optional address record dict

    Returns:
        dict: Senzing JSON record
    """
    senzing_record = {
        "DATA_SOURCE": "ICIJ_OTHERS",
        "RECORD_ID": other['node_id']
    }

    features = []
    features.append({"RECORD_TYPE": "ORGANIZATION"})

    # Name
    if other.get('name'):
        features.append({"NAME_ORG": other['name'], "NAME_TYPE": "PRIMARY"})

    # Registered address (denormalized)
    if address_record:
        addr_full = address_record.get('address', '')
        if addr_full:
            features.append({
                "ADDR_FULL": addr_full,
                "ADDR_TYPE": "REGISTERED",
                "ADDR_COUNTRY": address_record.get('country_codes', '')
            })

    # Incorporation date
    if other.get('incorporation_date'):
        features.append({"DATE_OF_FORMATION": other['incorporation_date']})

    # Country of association
    if other.get('countries'):
        features.append({"COUNTRY_OF_ASSOCIATION": other['countries']})

    senzing_record["FEATURES"] = features

    # Payload
    if other.get('type'):
        senzing_record['entity_type'] = other['type']
    if other.get('struck_off_date'):
        senzing_record['struck_off_date'] = other['struck_off_date']
    if other.get('closed_date'):
        senzing_record['closed_date'] = other['closed_date']
    if other.get('jurisdiction'):
        senzing_record['jurisdiction'] = other['jurisdiction']
    if other.get('jurisdiction_description'):
        senzing_record['jurisdiction_description'] = other['jurisdiction_description']
    if other.get('country_codes'):
        senzing_record['country_codes'] = other['country_codes']
    if other.get('sourceID'):
        senzing_record['sourceID'] = other['sourceID']
    if other.get('valid_until'):
        senzing_record['valid_until'] = other['valid_until']
    if other.get('note'):
        senzing_record['note'] = other['note']

    return senzing_record


def main():
    """Main mapping function."""
    import argparse
    import os

    parser = argparse.ArgumentParser(description='Map ICIJ data to Senzing JSON format')
    parser.add_argument('input_dir', help='Directory containing ICIJ CSV files')
    parser.add_argument('-o', '--output', default='icij_mapped.jsonl', help='Output JSONL file')
    parser.add_argument('--sample', type=int, help='Only process first N records per file (for testing)')
    parser.add_argument('--entities', help='Entities CSV file (default: input_dir/nodes-entities.csv)')
    parser.add_argument('--officers', help='Officers CSV file (default: input_dir/nodes-officers.csv)')
    parser.add_argument('--intermediaries', help='Intermediaries CSV file (default: input_dir/nodes-intermediaries.csv)')
    parser.add_argument('--others', help='Others CSV file (default: input_dir/nodes-others.csv)')
    parser.add_argument('--addresses', help='Addresses CSV file (default: input_dir/nodes-addresses.csv)')
    parser.add_argument('--relationships', help='Relationships CSV file (default: input_dir/relationships.csv)')
    parser.add_argument('--entities-only', action='store_true', help='Only map entities')
    parser.add_argument('--officers-only', action='store_true', help='Only map officers')
    parser.add_argument('--intermediaries-only', action='store_true', help='Only map intermediaries')
    parser.add_argument('--others-only', action='store_true', help='Only map others')
    args = parser.parse_args()

    # Set default file paths based on input directory
    if not args.entities:
        args.entities = os.path.join(args.input_dir, 'nodes-entities.csv')
    if not args.officers:
        args.officers = os.path.join(args.input_dir, 'nodes-officers.csv')
    if not args.intermediaries:
        args.intermediaries = os.path.join(args.input_dir, 'nodes-intermediaries.csv')
    if not args.others:
        args.others = os.path.join(args.input_dir, 'nodes-others.csv')
    if not args.addresses:
        args.addresses = os.path.join(args.input_dir, 'nodes-addresses.csv')
    if not args.relationships:
        args.relationships = os.path.join(args.input_dir, 'relationships.csv')

    print("=" * 70)
    print("ICIJ → SENZING MAPPER")
    print("=" * 70)
    print()

    # Load reference data
    addresses = load_addresses(args.addresses)
    entity_to_address = load_registered_addresses(args.relationships)
    print()

    total_records = 0
    total_with_address = 0

    with open(args.output, 'w', encoding='utf-8') as outfile:

        # Process entities
        if not any([args.officers_only, args.intermediaries_only, args.others_only]):
            print(f"Processing entities from {args.entities}...")
            count = 0
            with_addr = 0

            with open(args.entities, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if args.sample and count >= args.sample:
                        break

                    address_node_id = entity_to_address.get(row['node_id'])
                    address_record = addresses.get(address_node_id) if address_node_id else None
                    if address_record:
                        with_addr += 1

                    senzing_record = map_entity(row, address_record)
                    outfile.write(json.dumps(senzing_record) + '\n')

                    count += 1
                    if count % 100000 == 0:
                        print(f"  {count:,} entities processed...")

            print(f"  ✓ {count:,} entities mapped ({with_addr:,} with registered address)")
            total_records += count
            total_with_address += with_addr
            print()

        # Process officers
        if not any([args.entities_only, args.intermediaries_only, args.others_only]):
            print(f"Processing officers from {args.officers}...")
            count = 0
            with_addr = 0

            with open(args.officers, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if args.sample and count >= args.sample:
                        break

                    address_node_id = entity_to_address.get(row['node_id'])
                    address_record = addresses.get(address_node_id) if address_node_id else None
                    if address_record:
                        with_addr += 1

                    senzing_record = map_officer(row, address_record)
                    outfile.write(json.dumps(senzing_record) + '\n')

                    count += 1
                    if count % 100000 == 0:
                        print(f"  {count:,} officers processed...")

            print(f"  ✓ {count:,} officers mapped ({with_addr:,} with registered address)")
            total_records += count
            total_with_address += with_addr
            print()

        # Process intermediaries
        if not any([args.entities_only, args.officers_only, args.others_only]):
            print(f"Processing intermediaries from {args.intermediaries}...")
            count = 0
            with_addr = 0

            with open(args.intermediaries, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if args.sample and count >= args.sample:
                        break

                    address_node_id = entity_to_address.get(row['node_id'])
                    address_record = addresses.get(address_node_id) if address_node_id else None
                    if address_record:
                        with_addr += 1

                    senzing_record = map_intermediary(row, address_record)
                    outfile.write(json.dumps(senzing_record) + '\n')

                    count += 1
                    if count % 10000 == 0:
                        print(f"  {count:,} intermediaries processed...")

            print(f"  ✓ {count:,} intermediaries mapped ({with_addr:,} with registered address)")
            total_records += count
            total_with_address += with_addr
            print()

        # Process others
        if not any([args.entities_only, args.officers_only, args.intermediaries_only]):
            print(f"Processing others from {args.others}...")
            count = 0
            with_addr = 0

            with open(args.others, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if args.sample and count >= args.sample:
                        break

                    address_node_id = entity_to_address.get(row['node_id'])
                    address_record = addresses.get(address_node_id) if address_node_id else None
                    if address_record:
                        with_addr += 1

                    senzing_record = map_other(row, address_record)
                    outfile.write(json.dumps(senzing_record) + '\n')

                    count += 1
                    if count % 10000 == 0:
                        print(f"  {count:,} others processed...")

            print(f"  ✓ {count:,} others mapped ({with_addr:,} with registered address)")
            total_records += count
            total_with_address += with_addr
            print()

    print("=" * 70)
    print("MAPPING COMPLETE")
    print("=" * 70)
    print(f"Total records: {total_records:,}")
    print(f"With registered address: {total_with_address:,} ({total_with_address/total_records*100:.1f}%)")
    print(f"Output: {args.output}")
    print()


if __name__ == "__main__":
    main()
