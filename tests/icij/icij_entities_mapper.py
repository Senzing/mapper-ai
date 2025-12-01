#!/usr/bin/env python3
"""
ICIJ Entities → Senzing Mapper

Denormalizes registered_address relationships onto entity records.
Maps ICIJ offshore entity data to Senzing JSON format.

Usage:
  python3 icij_entities_mapper.py
  python3 icij_entities_mapper.py --sample 100
  python3 icij_entities_mapper.py -o output.jsonl
"""

import csv
import hashlib
import json
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


def map_entity_to_senzing(entity, address_record=None):
    """Map ICIJ entity to Senzing JSON format.

    Args:
        entity: Entity record dict
        address_record: Optional address record dict

    Returns:
        dict: Senzing JSON record
    """
    senzing_record = {
        "DATA_SOURCE": "ICIJ",
        "RECORD_ID": entity['node_id']
    }

    # Build FEATURES array
    features = []

    # Record type
    features.append({"RECORD_TYPE": "ORGANIZATION"})

    # Name (primary)
    if entity.get('name'):
        features.append({
            "NAME_ORG": entity['name'],
            "NAME_TYPE": "PRIMARY"
        })

    # Original name
    if entity.get('original_name') and entity['original_name'] != entity.get('name'):
        features.append({
            "NAME_ORG": entity['original_name'],
            "NAME_TYPE": "ORIGINAL"
        })

    # Former name
    if entity.get('former_name'):
        features.append({
            "NAME_ORG": entity['former_name'],
            "NAME_TYPE": "FORMER"
        })

    # Tax ID (from ibcRUC)
    if entity.get('ibcRUC'):
        features.append({
            "TAX_ID_NUMBER": entity['ibcRUC'],
            "TAX_ID_COUNTRY": entity.get('jurisdiction', '')
        })

    # Registered address (denormalized from address node)
    if address_record:
        address_full = address_record.get('address', '')
        if address_full:
            features.append({
                "ADDR_FULL": address_full,
                "ADDR_TYPE": "REGISTERED",
                "ADDR_COUNTRY": address_record.get('country_codes', '')
            })

    # Entity's own address field (if present and different from registered)
    if entity.get('address'):
        features.append({
            "ADDR_FULL": entity['address'],
            "ADDR_TYPE": "PRIMARY"
        })

    # Incorporation date
    if entity.get('incorporation_date'):
        features.append({
            "DATE_OF_FORMATION": entity['incorporation_date']
        })

    senzing_record["FEATURES"] = features

    # Payload attributes (at root level)
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


def main():
    """Main mapping function."""
    import argparse

    parser = argparse.ArgumentParser(description='Map ICIJ entities to Senzing JSON format')
    parser.add_argument('-o', '--output', default='icij_entities.jsonl', help='Output JSONL file')
    parser.add_argument('--sample', type=int, help='Only process first N records (for testing)')
    parser.add_argument('--entities', default='nodes-entities.csv', help='Entities CSV file')
    parser.add_argument('--addresses', default='nodes-addresses.csv', help='Addresses CSV file')
    parser.add_argument('--relationships', default='relationships.csv', help='Relationships CSV file')
    args = parser.parse_args()

    print("ICIJ → Senzing Entity Mapper")
    print("=" * 60)
    print()

    # Load reference data
    addresses = load_addresses(args.addresses)
    entity_to_address = load_registered_addresses(args.relationships)
    print()

    # Process entities
    print(f"Processing entities from {args.entities}...")
    records_processed = 0
    records_with_address = 0

    with open(args.entities, 'r', encoding='utf-8') as infile, \
         open(args.output, 'w', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)

        for entity in reader:
            # Check sample limit
            if args.sample and records_processed >= args.sample:
                break

            # Get registered address if available
            address_node_id = entity_to_address.get(entity['node_id'])
            address_record = addresses.get(address_node_id) if address_node_id else None

            if address_record:
                records_with_address += 1

            # Map to Senzing format
            senzing_record = map_entity_to_senzing(entity, address_record)

            # Write JSONL
            outfile.write(json.dumps(senzing_record) + '\n')

            records_processed += 1
            if records_processed % 100000 == 0:
                print(f"  {records_processed:,} records processed...")

    print()
    print("Mapping complete!")
    print(f"  Total entities: {records_processed:,}")
    print(f"  With registered address: {records_with_address:,} ({records_with_address/records_processed*100:.1f}%)")
    print(f"  Output: {args.output}")


if __name__ == "__main__":
    main()
