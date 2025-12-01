#!/usr/bin/env python3
"""
Map ICIJ data to use tax_id_number and tax_id_country fields.

Mappings:
  ibcRUC → tax_id_number
  jurisdiction → tax_id_country (and keep in payload)
"""

import csv
import sys


def map_entity_record(row):
    """Map a single entity record to new field names.

    Args:
        row: Dictionary with original field names

    Returns:
        Dictionary with mapped field names
    """
    mapped = {}

    # Map ibcRUC to tax_id_number
    if row.get('ibcRUC'):
        mapped['tax_id_number'] = row['ibcRUC']
        mapped['tax_id_country'] = row.get('jurisdiction', '')

    # Keep jurisdiction in payload (useful for context)
    if row.get('jurisdiction'):
        mapped['jurisdiction'] = row['jurisdiction']
        mapped['jurisdiction_description'] = row.get('jurisdiction_description', '')

    # Keep all other important fields
    field_mappings = {
        'node_id': 'node_id',
        'name': 'name',
        'original_name': 'original_name',
        'former_name': 'former_name',
        'company_type': 'company_type',
        'address': 'address',
        'internal_id': 'internal_id',
        'incorporation_date': 'incorporation_date',
        'inactivation_date': 'inactivation_date',
        'struck_off_date': 'struck_off_date',
        'dorm_date': 'dorm_date',
        'status': 'status',
        'service_provider': 'service_provider',
        'country_codes': 'country_codes',
        'countries': 'countries',
        'sourceID': 'sourceID',
        'valid_until': 'valid_until',
        'note': 'note'
    }

    for old_field, new_field in field_mappings.items():
        if row.get(old_field):
            mapped[new_field] = row[old_field]

    return mapped


def main():
    """Main mapping function."""
    input_file = 'nodes-entities.csv'
    output_file = 'nodes-entities-mapped.csv'

    print(f"Reading from: {input_file}")
    print(f"Writing to: {output_file}")
    print()

    records_processed = 0
    records_with_tax_id = 0

    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)

        # Determine output field order
        sample_row = next(reader)
        mapped_sample = map_entity_record(sample_row)
        fieldnames = list(mapped_sample.keys())

        # Reset to beginning
        infile.seek(0)
        reader = csv.DictReader(infile)

        with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                mapped_row = map_entity_record(row)
                writer.writerow(mapped_row)

                records_processed += 1
                if 'tax_id_number' in mapped_row:
                    records_with_tax_id += 1

                if records_processed % 100000 == 0:
                    print(f"  Processed {records_processed:,} records...")

    print(f"\nMapping complete!")
    print(f"  Total records: {records_processed:,}")
    print(f"  Records with tax_id_number: {records_with_tax_id:,} ({records_with_tax_id/records_processed*100:.1f}%)")
    print(f"  Output saved to: {output_file}")


if __name__ == "__main__":
    main()
