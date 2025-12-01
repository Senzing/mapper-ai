#!/usr/bin/env python3
"""
Employee to Senzing JSON Mapper

Maps US small employee CSV data to Senzing entity resolution format.
Generates two entity types:
  - PERSON (DATA_SOURCE: EMPLOYEE)
  - ORGANIZATION (DATA_SOURCE: EMPLOYER)

Usage:
    python3 employee_mapper.py input.csv -o output.jsonl [--sample N]
"""

import csv
import json
import hashlib
import argparse
import sys
from datetime import datetime


def normalize_for_hash(text):
    """Normalize text for deterministic hashing."""
    return text.strip().upper().replace("  ", " ")


def compute_employer_id(employer_name, employer_addr):
    """Compute deterministic RECORD_ID for employer from name and address."""
    normalized = f"{normalize_for_hash(employer_name)}|{normalize_for_hash(employer_addr)}"
    return hashlib.sha1(normalized.encode()).hexdigest()[:16]


def convert_date(date_str):
    """
    Convert M/D/YY format to YYYY-MM-DD.
    Year conversion: YY >= 50 -> 19YY, YY < 50 -> 20YY
    """
    if not date_str or date_str.lower() == 'null':
        return None

    try:
        parts = date_str.split('/')
        if len(parts) != 3:
            return None

        month, day, year = parts
        month = int(month)
        day = int(day)
        year = int(year)

        # Century inference
        if year >= 50:
            year += 1900
        else:
            year += 2000

        return f"{year:04d}-{month:02d}-{day:02d}"
    except (ValueError, IndexError):
        return None


def split_multi_value(value, delimiter=','):
    """Split multi-valued field and trim each value."""
    if not value or value.lower() == 'null':
        return []
    return [v.strip() for v in value.split(delimiter) if v.strip()]


def map_employee(row, employer_cache):
    """Map employee CSV row to Senzing PERSON record."""
    emp_num = row.get('emp_num', '').strip()
    if not emp_num:
        return None

    features = []

    # RECORD_TYPE
    features.append({"RECORD_TYPE": "PERSON"})

    # NAME
    name_obj = {}
    if row.get('first_name'):
        name_obj['NAME_FIRST'] = row['first_name'].strip()
    if row.get('last_name'):
        name_obj['NAME_LAST'] = row['last_name'].strip()
    if row.get('middle_name'):
        name_obj['NAME_MIDDLE'] = row['middle_name'].strip()
    if name_obj:
        features.append(name_obj)

    # DATE_OF_BIRTH
    dob = convert_date(row.get('dob', ''))
    if dob:
        features.append({"DATE_OF_BIRTH": dob})

    # ADDRESS
    addr_obj = {"ADDR_TYPE": "HOME"}
    if row.get('addr1'):
        addr_obj['ADDR_LINE1'] = row['addr1'].strip()
    if row.get('city'):
        addr_obj['ADDR_CITY'] = row['city'].strip()
    if row.get('state'):
        addr_obj['ADDR_STATE'] = row['state'].strip()
    if row.get('zip'):
        addr_obj['ADDR_POSTAL_CODE'] = row['zip'].strip()
    if len(addr_obj) > 1:  # More than just ADDR_TYPE
        features.append(addr_obj)

    # PHONE
    if row.get('home_phone'):
        features.append({
            "PHONE_TYPE": "HOME",
            "PHONE_NUMBER": row['home_phone'].strip()
        })

    # SSN
    if row.get('ssn') and row['ssn'].lower() != 'null':
        features.append({"SSN_NUMBER": row['ssn'].strip()})

    # IDENTIFIERS (id_type, id_number, id_country)
    id_type = row.get('id_type', '').strip().upper()
    id_number = row.get('id_number', '').strip()
    id_country = row.get('id_country', '').strip().upper()

    if id_type and id_number and id_type != 'NULL' and id_number != 'NULL':
        if id_type == 'DL':
            id_obj = {"DRIVERS_LICENSE_NUMBER": id_number}
            if id_country and id_country != 'NULL':
                id_obj['DRIVERS_LICENSE_STATE'] = id_country
            features.append(id_obj)
        elif id_type == 'PP':
            id_obj = {"PASSPORT_NUMBER": id_number}
            if id_country and id_country != 'NULL':
                id_obj['PASSPORT_COUNTRY'] = id_country
            features.append(id_obj)
        elif id_type == 'STUDENT_ID':
            id_obj = {
                "OTHER_ID_TYPE": "STUDENT_ID",
                "OTHER_ID_NUMBER": id_number
            }
            if id_country and id_country != 'NULL':
                id_obj['OTHER_ID_COUNTRY'] = id_country
            features.append(id_obj)

    # SHERIFF'S CARD (multi-valued)
    sherrifs_cards = split_multi_value(row.get('sherrifs_card', ''))
    for card_num in sherrifs_cards:
        features.append({
            "OTHER_ID_TYPE": "SHERIFFS_CARD",
            "OTHER_ID_NUMBER": card_num
        })

    # RELATIONSHIPS
    # Manager relationship
    manager_id = row.get('manager_id', '').strip()
    if manager_id and manager_id.lower() != 'null':
        features.append({
            "REL_POINTER_DOMAIN": "EMPLOYEE",
            "REL_POINTER_KEY": manager_id,
            "REL_POINTER_ROLE": "REPORTS_TO"
        })

    # Employer relationship
    employer_name = row.get('employer_name', '').strip()
    employer_addr = row.get('employer_addr', '').strip()
    if employer_name and employer_addr:
        employer_id = compute_employer_id(employer_name, employer_addr)

        # Track employer for later emission
        if employer_id not in employer_cache:
            employer_cache[employer_id] = {
                'name': employer_name,
                'address': employer_addr
            }

        features.append({
            "REL_POINTER_DOMAIN": "EMPLOYER",
            "REL_POINTER_KEY": employer_id,
            "REL_POINTER_ROLE": "EMPLOYED_BY"
        })

    # REL_ANCHOR (for manager relationships to point to)
    features.append({
        "REL_ANCHOR_DOMAIN": "EMPLOYEE",
        "REL_ANCHOR_KEY": emp_num
    })

    # Build final record
    record = {
        "DATA_SOURCE": "EMPLOYEE",
        "RECORD_ID": emp_num,
        "FEATURES": features
    }

    # Payload attributes
    if row.get('job_category') and row['job_category'].lower() != 'null':
        record['JOB_CATEGORY'] = row['job_category'].strip()
    if row.get('job_title') and row['job_title'].lower() != 'null':
        record['JOB_TITLE'] = row['job_title'].strip()
    if row.get('hire_date') and row['hire_date'].lower() != 'null':
        record['HIRE_DATE'] = row['hire_date'].strip()
    if row.get('salary') and row['salary'].lower() != 'null':
        record['SALARY'] = row['salary'].strip()

    return record


def map_employer(employer_id, employer_data):
    """Map employer data to Senzing ORGANIZATION record."""
    features = [
        {"RECORD_TYPE": "ORGANIZATION"},
        {"NAME_ORG": employer_data['name']},
        {
            "ADDR_TYPE": "BUSINESS",
            "ADDR_FULL": employer_data['address']
        },
        {
            "REL_ANCHOR_DOMAIN": "EMPLOYER",
            "REL_ANCHOR_KEY": employer_id
        }
    ]

    return {
        "DATA_SOURCE": "EMPLOYER",
        "RECORD_ID": employer_id,
        "FEATURES": features
    }


def process_csv(input_path, output_path, sample_limit=None):
    """Process CSV and generate JSONL output."""
    employer_cache = {}
    employee_records = []

    # Read CSV and build records
    print(f"Reading {input_path}...", file=sys.stderr)
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for idx, row in enumerate(reader, 1):
            if sample_limit and idx > sample_limit:
                break

            record = map_employee(row, employer_cache)
            if record:
                employee_records.append(record)

            if idx % 100 == 0:
                print(f"Processed {idx} rows...", file=sys.stderr)

    print(f"Processed {len(employee_records)} employees", file=sys.stderr)
    print(f"Found {len(employer_cache)} unique employers", file=sys.stderr)

    # Write output
    print(f"Writing to {output_path}...", file=sys.stderr)
    with open(output_path, 'w', encoding='utf-8') as f:
        # Emit employers first
        for employer_id, employer_data in employer_cache.items():
            employer_record = map_employer(employer_id, employer_data)
            f.write(json.dumps(employer_record) + '\n')

        # Emit employees
        for record in employee_records:
            f.write(json.dumps(record) + '\n')

    print(f"✓ Complete: {len(employer_cache)} employers + {len(employee_records)} employees written", file=sys.stderr)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Map employee CSV to Senzing JSON format'
    )
    parser.add_argument('input', help='Input CSV file path')
    parser.add_argument('-o', '--output', required=True, help='Output JSONL file path')
    parser.add_argument('--sample', type=int, help='Limit to first N records (for testing)')

    args = parser.parse_args()

    try:
        process_csv(args.input, args.output, args.sample)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
