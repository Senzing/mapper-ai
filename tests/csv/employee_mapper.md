# Employee Mapper Specification

This document is the complete mapping specification for transforming US small employee CSV data into Senzing JSON format. Any AI should be able to generate a working mapper implementation from this specification alone.

## Source Schema

**Format**: CSV
**File**: `us-small-employee-raw.csv`
**Records**: 38 employees
**Fields**: 24

### Field Inventory

| # | Field | Type | Populated | Unique | Sample Values |
|---|-------|------|-----------|--------|---------------|
| 1 | emp_num | str | 100% | 100% | 1, 2, 3, 4, 5 |
| 2 | last_name | str | 100% | 97% | Martin, Sheehan, Mcpherson |
| 3 | first_name | str | 100% | 84% | John, Lisa, Joseph |
| 4 | middle_name | str | 100% | 34% | J, M, C, H, A |
| 5 | addr1 | str | 100% | 100% | 2280 Stoney Lonesome Road |
| 6 | city | str | 100% | 97% | Anaheim, Pittston, Holden |
| 7 | state | str | 100% | 58% | CA, FL, NY, NC, MA |
| 8 | zip | str | 100% | 100% | 18640, 92806, 1520 |
| 9 | home_phone | str | 100% | 100% | 570-300-5826, 714-762-0551 |
| 10 | dob | str | 100% | 100% | 4/13/69, 10/13/70, 8/5/57 |
| 11 | ssn | str | 100% | 97% | 477-33-1025, 189-50-0966 |
| 12 | job_category | str | 100% | 16% | sales, key executive, management |
| 13 | job_title | str | 100% | 29% | Senior sales person, President |
| 14 | hire_date | str | 100% | 21% | 1/10/10, 2/20/12, 3/13/13 |
| 15 | salary | str | 100% | 8% | 75k, 50k, 100k |
| 16 | rehire_flag | str | 100% | 3% | null (all records) |
| 17 | employer_name | str | 100% | 8% | ABC Company, BNC Connections |
| 18 | employer_addr | str | 100% | 8% | 111 First St, anytown USA |
| 19 | id_type | str | 21% | 38% | DL, PP, student_id |
| 20 | id_number | str | 21% | 100% | N9123912, N676555, 123234568 |
| 21 | id_country | str | 18% | 43% | NV, US, CA |
| 22 | manager_id | str | 34% | 31% | 12, 2, 1, 3 |
| 23 | sherrifs_card | str | 16% | 100% | A224-5698, B232-4344 |

## Target Entities

### Entity 1: PERSON (Employee)

**DATA_SOURCE**: `EMPLOYEE`
**RECORD_ID**: `emp_num` (unique employee number from source)
**RECORD_TYPE**: `PERSON`

### Entity 2: ORGANIZATION (Employer)

**DATA_SOURCE**: `EMPLOYER`
**RECORD_ID**: SHA1 hash of normalized `employer_name + "|" + employer_addr`
**RECORD_TYPE**: `ORGANIZATION`

**Normalization for hash**:
- Trim whitespace
- Convert to uppercase
- Remove extra internal spaces
- Format: `{NAME}|{ADDRESS}`

Example:
```python
import hashlib
normalized = f"{employer_name.strip().upper()}|{employer_addr.strip().upper()}"
record_id = hashlib.sha1(normalized.encode()).hexdigest()[:16]
```

## Field Mappings

### Employee (PERSON) Entity

| Source Field | Disposition | Senzing Attribute | Transform | Notes |
|--------------|-------------|-------------------|-----------|-------|
| emp_num | Feature | RECORD_ID | As-is | Root attribute |
| — | Feature | RECORD_TYPE | Constant: "PERSON" | — |
| first_name | Feature | NAME_FIRST | Trim whitespace | In NAME feature object |
| middle_name | Feature | NAME_MIDDLE | Trim whitespace | In NAME feature object |
| last_name | Feature | NAME_LAST | Trim whitespace | In NAME feature object |
| dob | Feature | DATE_OF_BIRTH | Convert M/D/YY → YYYY-MM-DD | Separate feature object |
| addr1 | Feature | ADDR_LINE1 | Trim whitespace | In ADDRESS feature object |
| city | Feature | ADDR_CITY | Trim whitespace | In ADDRESS feature object |
| state | Feature | ADDR_STATE | Trim whitespace | In ADDRESS feature object |
| zip | Feature | ADDR_POSTAL_CODE | As-is | In ADDRESS feature object |
| — | Feature | ADDR_TYPE | Constant: "HOME" | In ADDRESS feature object |
| home_phone | Feature | PHONE_NUMBER | As-is | In PHONE feature object |
| — | Feature | PHONE_TYPE | Constant: "HOME" | In PHONE feature object |
| ssn | Feature | SSN_NUMBER | As-is | Separate feature object |
| id_type="DL" | Feature | DRIVERS_LICENSE_NUMBER | From id_number | Separate feature object |
| id_country (DL) | Feature | DRIVERS_LICENSE_STATE | From id_country | In DRLIC feature object |
| id_type="PP" | Feature | PASSPORT_NUMBER | From id_number | Separate feature object |
| id_country (PP) | Feature | PASSPORT_COUNTRY | From id_country | In PASSPORT feature object |
| id_type="student_id" | Feature | OTHER_ID_NUMBER | From id_number | Separate feature object |
| — | Feature | OTHER_ID_TYPE | Constant: "STUDENT_ID" | In OTHER_ID feature object |
| id_country (student_id) | Feature | OTHER_ID_COUNTRY | From id_country | In OTHER_ID feature object (optional) |
| sherrifs_card | Feature | OTHER_ID_NUMBER | Split on comma, create multiple | One feature object per value |
| — | Feature | OTHER_ID_TYPE | Constant: "SHERIFFS_CARD" | In each OTHER_ID feature object |
| manager_id | Feature | REL_POINTER_KEY | As-is | In REL_POINTER feature object |
| — | Feature | REL_POINTER_DOMAIN | Constant: "EMPLOYEE" | In REL_POINTER feature object |
| — | Feature | REL_POINTER_ROLE | Constant: "REPORTS_TO" | In REL_POINTER feature object |
| employer_name + employer_addr | Feature | REL_POINTER_KEY | Hash (see employer RECORD_ID) | In REL_POINTER feature object |
| — | Feature | REL_POINTER_DOMAIN | Constant: "EMPLOYER" | In REL_POINTER feature object |
| — | Feature | REL_POINTER_ROLE | Constant: "EMPLOYED_BY" | In REL_POINTER feature object |
| emp_num | Feature | REL_ANCHOR_KEY | From emp_num | In REL_ANCHOR feature object |
| — | Feature | REL_ANCHOR_DOMAIN | Constant: "EMPLOYEE" | In REL_ANCHOR feature object |
| job_category | Payload | JOB_CATEGORY | As-is | Root attribute |
| job_title | Payload | JOB_TITLE | As-is | Root attribute |
| hire_date | Payload | HIRE_DATE | As-is | Root attribute |
| salary | Payload | SALARY | As-is | Root attribute |
| rehire_flag | Ignore | — | — | All null values |

### Employer (ORGANIZATION) Entity

| Source Field | Disposition | Senzing Attribute | Transform | Notes |
|--------------|-------------|-------------------|-----------|-------|
| employer_name + employer_addr | Feature | RECORD_ID | SHA1 hash (16 chars) | Root attribute |
| — | Feature | RECORD_TYPE | Constant: "ORGANIZATION" | — |
| employer_name | Feature | NAME_ORG | Trim whitespace | Separate feature object |
| employer_addr | Feature | ADDR_FULL | Trim whitespace | In ADDRESS feature object |
| — | Feature | ADDR_TYPE | Constant: "BUSINESS" | In ADDRESS feature object |
| (computed) | Feature | REL_ANCHOR_KEY | Same as RECORD_ID | In REL_ANCHOR feature object |
| — | Feature | REL_ANCHOR_DOMAIN | Constant: "EMPLOYER" | In REL_ANCHOR feature object |

## Date Conversion Logic

Source format: `M/D/YY` (e.g., "4/13/69")
Target format: `YYYY-MM-DD` (e.g., "1969-04-13")

**Algorithm**:
1. Parse M/D/YY
2. Year conversion: YY >= 50 → 19YY; YY < 50 → 20YY
3. Zero-pad month and day to 2 digits
4. Format as YYYY-MM-DD

**Example**:
- "4/13/69" → "1969-04-13"
- "8/5/57" → "1957-08-05"
- "7/8/71" → "1971-07-08"

## Multi-Valued Field Handling

**Sheriff's Card** (`sherrifs_card`):
- Some records contain comma-separated values: "A224-5698, B232-4344"
- Split on comma
- Trim each value
- Create separate OTHER_ID feature object for each value

## Crosswalk Mappings Used

### Identifier Type Crosswalk

| Source Value | Senzing Feature | Type Attribute | Notes |
|--------------|-----------------|----------------|-------|
| DL | DRLIC | — | Driver's License |
| PP | PASSPORT | — | Passport |
| student_id | OTHER_ID | OTHER_ID_TYPE="STUDENT_ID" | Custom identifier |

### Usage Type Crosswalk

| Source Context | Senzing Type | Notes |
|----------------|--------------|-------|
| home_phone | PHONE_TYPE="HOME" | Derived from field name |
| addr1, city, state, zip | ADDR_TYPE="HOME" | Personal residence |
| employer_addr | ADDR_TYPE="BUSINESS" | Organization location |

## Sample JSON Output

### Sample 1: Employee with Driver's License and Sheriff's Cards

```json
{
  "DATA_SOURCE": "EMPLOYEE",
  "RECORD_ID": "1",
  "FEATURES": [
    {
      "RECORD_TYPE": "PERSON"
    },
    {
      "NAME_FIRST": "Robert",
      "NAME_LAST": "Smith",
      "NAME_MIDDLE": "J"
    },
    {
      "DATE_OF_BIRTH": "1969-04-13"
    },
    {
      "ADDR_TYPE": "HOME",
      "ADDR_LINE1": "2280 Stoney Lonesome Road",
      "ADDR_CITY": "Pittston",
      "ADDR_STATE": "PA",
      "ADDR_POSTAL_CODE": "18640"
    },
    {
      "PHONE_TYPE": "HOME",
      "PHONE_NUMBER": "570-300-5826"
    },
    {
      "SSN_NUMBER": "189-50-0966"
    },
    {
      "DRIVERS_LICENSE_NUMBER": "N9123912",
      "DRIVERS_LICENSE_STATE": "NV"
    },
    {
      "OTHER_ID_TYPE": "SHERIFFS_CARD",
      "OTHER_ID_NUMBER": "A224-5698"
    },
    {
      "OTHER_ID_TYPE": "SHERIFFS_CARD",
      "OTHER_ID_NUMBER": "B232-4344"
    },
    {
      "REL_POINTER_DOMAIN": "EMPLOYEE",
      "REL_POINTER_KEY": "12",
      "REL_POINTER_ROLE": "REPORTS_TO"
    },
    {
      "REL_POINTER_DOMAIN": "EMPLOYER",
      "REL_POINTER_KEY": "e7a3b9c4d5f6a1b2",
      "REL_POINTER_ROLE": "EMPLOYED_BY"
    },
    {
      "REL_ANCHOR_DOMAIN": "EMPLOYEE",
      "REL_ANCHOR_KEY": "1"
    }
  ],
  "JOB_CATEGORY": "sales",
  "JOB_TITLE": "Senior sales person",
  "HIRE_DATE": "1/10/10",
  "SALARY": "75k"
}
```

### Sample 2: Employer Organization

```json
{
  "DATA_SOURCE": "EMPLOYER",
  "RECORD_ID": "e7a3b9c4d5f6a1b2",
  "FEATURES": [
    {
      "RECORD_TYPE": "ORGANIZATION"
    },
    {
      "NAME_ORG": "ABC Company"
    },
    {
      "ADDR_TYPE": "BUSINESS",
      "ADDR_FULL": "111 First St, anytown USA"
    },
    {
      "REL_ANCHOR_DOMAIN": "EMPLOYER",
      "REL_ANCHOR_KEY": "e7a3b9c4d5f6a1b2"
    }
  ]
}
```

### Sample 3: Employee with Passport (No Manager)

```json
{
  "DATA_SOURCE": "EMPLOYEE",
  "RECORD_ID": "25",
  "FEATURES": [
    {
      "RECORD_TYPE": "PERSON"
    },
    {
      "NAME_FIRST": "Jennifer",
      "NAME_LAST": "Martinez",
      "NAME_MIDDLE": "A"
    },
    {
      "DATE_OF_BIRTH": "1980-03-22"
    },
    {
      "ADDR_TYPE": "HOME",
      "ADDR_LINE1": "456 Oak Avenue",
      "ADDR_CITY": "Los Angeles",
      "ADDR_STATE": "CA",
      "ADDR_POSTAL_CODE": "90012"
    },
    {
      "PHONE_TYPE": "HOME",
      "PHONE_NUMBER": "213-555-7890"
    },
    {
      "SSN_NUMBER": "555-66-7777"
    },
    {
      "PASSPORT_NUMBER": "N676555",
      "PASSPORT_COUNTRY": "US"
    },
    {
      "REL_POINTER_DOMAIN": "EMPLOYER",
      "REL_POINTER_KEY": "a1b2c3d4e5f6g7h8",
      "REL_POINTER_ROLE": "EMPLOYED_BY"
    },
    {
      "REL_ANCHOR_DOMAIN": "EMPLOYEE",
      "REL_ANCHOR_KEY": "25"
    }
  ],
  "JOB_CATEGORY": "accounting",
  "JOB_TITLE": "Senior accountant",
  "HIRE_DATE": "2/20/12",
  "SALARY": "75k"
}
```

## Implementation Requirements

### Output Format
- **JSONL** (JSON Lines): One JSON record per line
- Each employee generates one EMPLOYEE record
- Each unique employer generates one EMPLOYER record (deduplicated by hash)

### Processing Order
1. First pass: Read all employees, track unique employers (by hash)
2. Second pass: Emit all EMPLOYER records first
3. Third pass: Emit all EMPLOYEE records with relationship pointers

Alternative single-pass approach:
1. Maintain employer cache (hash → record)
2. For each employee row:
   - Compute employer hash
   - If not in cache, emit EMPLOYER record and add to cache
   - Emit EMPLOYEE record

### Command-Line Interface

```bash
python3 employee_mapper.py <input_csv> -o <output_jsonl> [--sample N]
```

**Arguments**:
- `input_csv`: Path to source CSV file (required)
- `-o/--output`: Path to output JSONL file (required)
- `--sample N`: Optional, emit only first N records for testing

**Example**:
```bash
python3 employee_mapper.py us-small-employee-raw.csv -o output.jsonl --sample 10
```

### Dependencies
- Python 3.7+
- Standard library only: `csv`, `json`, `hashlib`, `argparse`, `sys`

### Error Handling
- Missing required fields: Skip record, log warning
- Invalid date format: Log warning, omit DATE_OF_BIRTH feature
- Empty employer fields: Skip EMPLOYED_BY relationship
- Invalid manager_id: Skip REPORTS_TO relationship

### Progress Display
For files with >100 rows, print progress every 10% or 100 records:
```
Processing employees: 100/38 (100%)
Employers created: 3
Employees created: 38
```

## Validation

### Linter Validation (Development)
```bash
# Test a single record
echo '{"DATA_SOURCE":"EMPLOYEE",...}' | python3 ../../senzing/tools/lint_senzing_json.py
```

### Production Validation
```bash
# Analyze complete output
python3 ../../senzing/tools/sz_json_analyzer.py output.jsonl
```

Expected validation results:
- All records pass structural validation
- Two DATA_SOURCE values: EMPLOYEE, EMPLOYER
- RECORD_TYPE values: PERSON, ORGANIZATION
- All REL_POINTER references resolve to valid REL_ANCHOR records

## Decisions Made

1. **DATA_SOURCE codes**: EMPLOYEE (persons), EMPLOYER (organizations)
2. **Employer handling**: Create separate ORGANIZATION entities with EMPLOYED_BY relationships
3. **Manager relationships**: Use REL_POINTER with REPORTS_TO role
4. **Date conversion**: M/D/YY → YYYY-MM-DD with century inference (>=50 → 1900s)
5. **Identifier mapping**: DL→DRLIC, PP→PASSPORT, student_id→OTHER_ID
6. **Sheriff's cards**: Split multi-valued, map to OTHER_ID with type SHERIFFS_CARD
7. **Job fields**: Map to payload (not used for entity resolution)
8. **rehire_flag**: Ignored (all null)
9. **Employer RECORD_ID**: SHA1 hash (first 16 chars) of normalized name+address
10. **Address types**: HOME for employees, BUSINESS for employers

## Known Data Quality Issues

- **Duplicate SSN**: 477-33-1025 appears twice (records will likely resolve as same entity)
- **Sparse identifiers**: Only 21% have id_type/id_number
- **Missing managers**: 66% of employees have no manager_id
- **Sheriff's cards**: Only 16% populated, some multi-valued
- **All rehire_flag null**: Field provides no value
