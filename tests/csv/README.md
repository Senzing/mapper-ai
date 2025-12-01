# US Small Employee Dataset - Senzing Mapper

This directory contains the mapper implementation for transforming US small employee CSV data into Senzing entity resolution format.

## Overview

The mapper processes employee records and creates two entity types:
- **PERSON (Employee)**: Individual employee records with personal information, job details, and relationships
- **ORGANIZATION (Employer)**: Employer organizations derived from employee records

## Data Sources

- `DATA_SOURCE`: **EMPLOYEE** - Employee person records
- `DATA_SOURCE`: **EMPLOYER** - Employer organization records

## Files

- `us-small-employee-raw.csv` - Source CSV data (38 employee records)
- `us-small-employee-schema.md` - Schema documentation
- `employee_mapper.md` - Complete mapping specification (source of truth)
- `employee_mapper.py` - Python mapper implementation

## Usage

### Basic Usage

```bash
# Map all records to JSONL output
python3 employee_mapper.py us-small-employee-raw.csv -o output.jsonl
```

### Testing with Sample Output

```bash
# Generate first 10 records only
python3 employee_mapper.py us-small-employee-raw.csv -o sample.jsonl --sample 10
```

### Validation

After generating output, validate the structure using the Senzing JSON analyzer:

```bash
# Validate and analyze the output
python3 ../../senzing/tools/sz_json_analyzer.py output.jsonl
```

The analyzer provides:
- Record count and validation status
- Feature usage statistics
- DATA_SOURCE distribution
- Structural validation

You can also use the linter during development to validate individual records:

```bash
# Validate a single record (development only)
echo '{"DATA_SOURCE":"EMPLOYEE",...}' | python3 ../../senzing/tools/lint_senzing_json.py
```

## Features Mapped

### Employee (PERSON) Features
- **Name**: First, middle, last name components
- **Date of Birth**: Converted from M/D/YY to YYYY-MM-DD format
- **Address**: Parsed home address (line1, city, state, ZIP)
- **Phone**: Home phone number
- **SSN**: Social Security Number
- **Identifiers**: Driver's license, passport, sheriff's card (when present)
- **Relationships**:
  - Manager reporting relationships (REPORTS_TO)
  - Employer relationships (EMPLOYED_BY)

### Employee Payload Attributes
- Job category
- Job title
- Hire date
- Salary

### Employer (ORGANIZATION) Features
- **Name**: Organization name
- **Address**: Business address
- **Relationship anchor**: For employee EMPLOYED_BY relationships

## Relationships

The mapper creates two types of disclosed relationships:

1. **Employee → Manager** (REPORTS_TO)
   - Uses `manager_id` field to link employees to their managers
   - Both source and target are in EMPLOYEE data source

2. **Employee → Employer** (EMPLOYED_BY)
   - Derives employer organizations from `employer_name` and `employer_addr` fields
   - Creates separate ORGANIZATION records in EMPLOYER data source
   - Links employees to their employers

## Record ID Strategy

### Employees
- Uses source field: `emp_num` (unique employee number)

### Employers
- No unique key in source data
- Uses deterministic SHA1 hash of normalized: `employer_name + employer_addr`
- Ensures consistent RECORD_ID across runs

## Implementation Notes

- **Stdlib only**: Uses only Python standard library (csv, json, hashlib)
- **Multi-valued fields**: Sheriff's cards with multiple values are split into separate feature objects
- **Date conversion**: Converts M/D/YY format to ISO YYYY-MM-DD
- **Sparse fields**: Handles optional identifiers (driver's license, passport, sheriff's card)
- **Progress display**: Shows progress for long-running operations

## Testing

1. **Schema validation**: Use `sz_schema_generator.py` to profile the source
2. **Sample run**: Test with `--sample 10` flag first
3. **Lint check**: Validate sample records during development
4. **Full validation**: Run `sz_json_analyzer.py` on complete output
5. **Relationship integrity**: Verify all REL_POINTER references resolve to valid REL_ANCHOR records

## Data Quality Notes

From schema analysis:
- 38 employee records
- 24 fields total
- 1 duplicate SSN detected (477-33-1025 appears twice)
- 3 distinct employers
- Sparse fields: id_type (21%), id_country (18%), manager_id (34%), sherrifs_card (16%)
- All rehire_flag values are null (ignored in mapping)
