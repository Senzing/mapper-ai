# Senzing Mapping — Shot Examples

This document provides short, end-to-end examples that show how to translate small source snippets into Senzing JSON, including a compact mapping table and linter usage.

Use these as patterns when building your own mappings. Always cite the spec in the Evidence column using the format: [Spec §<section-id>: "<attribute-name>"].

## Shot Example 1 — CSV (person) → Senzing JSON

Source Schema
- Shape: CSV
- Fields: `id`, `first_name`, `last_name`, `dob`, `email`, `last4ssn`, `status`, `create_date`
- Notes: `dob` is `YYYY-MM-DD`; `status` and `create_date` are payload attributes at the root; `last4ssn` is a partial SSN (last 4 digits).

Sample Input
```csv
id,first_name,last_name,dob,email,last4ssn,status,create_date
1001,Robert,Smith,1978-12-11,bob@example.com,1234,active,2020-06-15
```

Mapping (proposal)
| SourceField | SenzingAttribute | Transform | Evidence | Confidence |
|---|---|---|---|---|
| id | RECORD_ID | As-is | [Spec §Attributes for the Record Key: "RECORD_ID"] | High |
| first_name | NAME_FIRST | Trim | [Spec §Feature: NAME: "NAME_FIRST"] | High |
| last_name | NAME_LAST | Trim | [Spec §Feature: NAME: "NAME_LAST"] | High |
| dob | DATE_OF_BIRTH | As-is | [Spec §Feature: DOB: "DATE_OF_BIRTH"] | High |
| email | EMAIL_ADDRESS | Lowercase | [Spec §Feature: EMAIL: "EMAIL_ADDRESS"] | High |
| last4ssn | SSN_NUMBER | Last 4 only (partial accepted) | [Spec §Feature: SSN: "SSN_NUMBER"] | Medium |
| status | STATUS (root payload) | Capitalize first letter | [Spec §Payload Attributes (Optional): "STATUS"] | Medium |
| create_date | CREATE_DATE (root payload) | As-is | [Spec §Payload Attributes (Optional): "CREATE_DATE"] | Medium |

Output JSON (1 record)
```json
{
  "DATA_SOURCE": "CUSTOMERS",
  "RECORD_ID": "1001",
  "FEATURES": [
    { "RECORD_TYPE": "PERSON" },
    { "NAME_FIRST": "Robert", "NAME_LAST": "Smith" },
    { "DATE_OF_BIRTH": "1978-12-11" },
    { "EMAIL_ADDRESS": "bob@example.com" },
    { "SSN_NUMBER": "1234" }
  ],
  "STATUS": "Active",
  "CREATE_DATE": "2020-06-15"
}
```

---

## Shot Example 2 — CSV (typed customer) → Senzing JSON

Source Schema
- Shape: CSV
- Fields: `customer_id`, `type` (person/company), `name`, `address` (full), `status` (active/inactive)
- Notes: `type` controls RECORD_TYPE; `name` maps conditionally; `address` is full; `status` is a root payload attribute.

Sample Input
```csv
customer_id,type,name,address,status
P1001,person,Robert A Smith,123 Main St, Las Vegas, NV 89132,active
ORG2001,company,Acme Corporation,500 Industrial Way, Austin, TX 78701,inactive
U3001,,Chris Jordan,PO Box 19675, Las Vegas, NV 89111,active
```

Mapping (proposal)
| SourceField | SenzingAttribute | Transform | Evidence | Confidence |
|---|---|---|---|---|
| customer_id | RECORD_ID | As-is | [Spec §Attributes for the Record Key: "RECORD_ID"] | High |
| type | RECORD_TYPE | Map `person`→PERSON; `company`→ORGANIZATION; blank→omit | [Spec §FEATURE: RECORD_TYPE: "RECORD_TYPE"] | High |
| name (type=person) | NAME_FULL | As-is (full person name) | [Spec §Feature: NAME: "NAME_FULL"] | Medium |
| name (type=company) | NAME_ORG | As-is | [Spec §Feature: NAME: "NAME_ORG"] | High |
| name (type blank) | NAME_FULL | As-is (unknown type) | [Spec §Feature: NAME: "NAME_FULL"] | Medium |
| address | ADDR_FULL | As-is | [Spec §Feature: ADDRESS: "ADDR_FULL"] | High |
| type (company) | ADDR_TYPE | Set constant `BUSINESS` | [Spec §Feature: ADDRESS: "ADDR_TYPE"]; [Spec §Mapping Usage Types] | Medium |
| status | STATUS (root payload) | Uppercase first letter (Active/Inactive) | [Spec §Payload Attributes (Optional): "STATUS"] | Medium |

Output JSON (person)
```json
{
  "DATA_SOURCE": "CRM",
  "RECORD_ID": "P1001",
  "FEATURES": [
    { "RECORD_TYPE": "PERSON" },
    { "NAME_FULL": "Robert A Smith" },
    { "ADDR_FULL": "123 Main St, Las Vegas, NV 89132" }
  ],
  "STATUS": "Active"
}
```

Output JSON (organization)
```json
{
  "DATA_SOURCE": "CRM",
  "RECORD_ID": "ORG2001",
  "FEATURES": [
    { "RECORD_TYPE": "ORGANIZATION" },
    { "NAME_ORG": "Acme Corporation" },
    { "ADDR_TYPE": "BUSINESS", "ADDR_FULL": "500 Industrial Way, Austin, TX 78701" }
  ],
  "STATUS": "Inactive"
}
```

Output JSON (unknown type)
```json
{
  "DATA_SOURCE": "CRM",
  "RECORD_ID": "U3001",
  "FEATURES": [
    { "NAME_FULL": "Chris Jordan" },
    { "ADDR_FULL": "PO Box 19675, Las Vegas, NV 89111" }
  ],
  "STATUS": "Active"
}
```

## Shot Example 3 — Graph edges mapping (directors: person→org) → Senzing JSON

Source Schema
- Shape: Graph (nodes and edges)
- Nodes:
  - Person P1001: `first_name`, `last_name`, `address`
  - Person P1002: `first_name`, `last_name`, `address`
  - Org ORG3001: `name`, `address`
- Edges:
  - P1001 → ORG3001: DIRECTOR_OF
  - P1002 → ORG3001: DIRECTOR_OF

Sample Input (illustrative)
```json
{
  "nodes": [
    { "id": "P1001", "type": "person", "first_name": "David", "last_name": "Ng", "address": "12 King St, Boston, MA 02108" },
    { "id": "P1002", "type": "person", "first_name": "Hao", "last_name": "Ng", "address": "45 Beacon St, Boston, MA 02108" },
    { "id": "ORG3001", "type": "company", "name": "Beacon Analytics", "address": "100 Market St, Boston, MA 02109" }
  ],
  "edges": [
    { "from": "P1001", "to": "ORG3001", "role": "DIRECTOR_OF" },
    { "from": "P1002", "to": "ORG3001", "role": "DIRECTOR_OF" }
  ]
}
```

Mapping (proposal)
| SourceField | SenzingAttribute | Transform | Evidence | Confidence |
|---|---|---|---|---|
| id (person) | RECORD_ID | As-is | [Spec §Attributes for the Record Key: "RECORD_ID"] | High |
| first_name | NAME_FIRST | Trim | [Spec §Feature: NAME: "NAME_FIRST"] | High |
| last_name | NAME_LAST | Trim | [Spec §Feature: NAME: "NAME_LAST"] | High |
| address (person) | ADDR_FULL | As-is | [Spec §Feature: ADDRESS: "ADDR_FULL"] | High |
| id (org) | RECORD_ID | As-is | [Spec §Attributes for the Record Key: "RECORD_ID"] | High |
| name (org) | NAME_ORG | As-is | [Spec §Feature: NAME: "NAME_ORG"] | High |
| address (org) | ADDR_FULL | As-is | [Spec §Feature: ADDRESS: "ADDR_FULL"] | High |
| edge: person→org (DIRECTOR_OF) | REL_POINTER_ROLE=DIRECTOR_OF | Person → Organization | [Spec §Disclosed Relationship Mapping Guidance: "REL_POINTER_ROLE"]; [Spec §Format notes (how to spot masters, children, and disclosed relationships)] | High |
| any target node | REL_ANCHOR | Add one anchor per target | [Spec §Disclosed Relationship Mapping Guidance: "REL_ANCHOR_DOMAIN"]; [Spec §Format notes (how to spot masters, children, and disclosed relationships)] | High |

Output JSON (person P1001)
```json
{
  "DATA_SOURCE": "GRAPH",
  "RECORD_ID": "P1001",
  "FEATURES": [
    { "RECORD_TYPE": "PERSON" },
    { "NAME_FIRST": "David", "NAME_LAST": "Ng" },
    { "ADDR_FULL": "12 King St, Boston, MA 02108" },
    { "REL_POINTER_DOMAIN": "GRAPH", "REL_POINTER_KEY": "ORG3001", "REL_POINTER_ROLE": "DIRECTOR_OF" }
  ]
}
```

Output JSON (person P1002)
```json
{
  "DATA_SOURCE": "GRAPH",
  "RECORD_ID": "P1002",
  "FEATURES": [
    { "RECORD_TYPE": "PERSON" },
    { "NAME_FIRST": "Hao", "NAME_LAST": "Ng" },
    { "ADDR_FULL": "45 Beacon St, Boston, MA 02108" },
    { "REL_POINTER_DOMAIN": "GRAPH", "REL_POINTER_KEY": "ORG3001", "REL_POINTER_ROLE": "DIRECTOR_OF" }
  ]
}
```

Output JSON (organization ORG3001)
```json
{
  "DATA_SOURCE": "GRAPH",
  "RECORD_ID": "ORG3001",
  "FEATURES": [
    { "RECORD_TYPE": "ORGANIZATION" },
    { "NAME_ORG": "Beacon Analytics" },
    { "ADDR_FULL": "100 Market St, Boston, MA 02109" },
    { "REL_ANCHOR_DOMAIN": "GRAPH", "REL_ANCHOR_KEY": "ORG3001" }
  ]
}
```

---

## Shot Example 4 — JSON bidirectional relationships → Senzing JSON

Source Schema
- Shape: JSON list (array with per-person sublist of relationships)
- Arrays:
  - `people[]` with fields: `id`, `first_name`, `last_name`, `address`, `rels[]`
  - `rels[]` under each person with fields: `to`, `role` (FATHER_OF or SON_OF)

Sample Input
```json
{
  "people": [
    {
      "id": "P1001",
      "first_name": "David",
      "last_name": "Ng",
      "address": "12 King St, Boston, MA 02108",
      "rels": [ { "to": "P1002", "role": "FATHER_OF" } ]
    },
    {
      "id": "P1002",
      "first_name": "Hao",
      "last_name": "Ng",
      "address": "45 Beacon St, Boston, MA 02108",
      "rels": [ { "to": "P1001", "role": "SON_OF" } ]
    }
  ]
}
```

Mapping (proposal)
| SourceField | SenzingAttribute | Transform | Evidence | Confidence |
|---|---|---|---|---|
| people.id | RECORD_ID | As-is | [Spec §Attributes for the Record Key: "RECORD_ID"] | High |
| people.first_name | NAME_FIRST | Trim | [Spec §Feature: NAME: "NAME_FIRST"] | High |
| people.last_name | NAME_LAST | Trim | [Spec §Feature: NAME: "NAME_LAST"] | High |
| people.address | ADDR_FULL | As-is | [Spec §Feature: ADDRESS: "ADDR_FULL"] | High |
| people.rels[].to + role | REL_POINTER_* | Point to target with specific role (FATHER_OF or SON_OF) | [Spec §Disclosed Relationship Mapping Guidance: "REL_POINTER_ROLE"]; [Spec §Disclosed Relationship Mapping Guidance: "Uni- vs bi-directional"]; [Spec §Format notes (how to spot masters, children, and disclosed relationships)] | High |
| targets (each person) | REL_ANCHOR | Add one anchor per target | [Spec §Disclosed Relationship Mapping Guidance: "REL_ANCHOR_DOMAIN"] | High |

Output JSON (person P1001)
```json
{
  "DATA_SOURCE": "GRAPH",
  "RECORD_ID": "P1001",
  "FEATURES": [
    { "RECORD_TYPE": "PERSON" },
    { "NAME_FIRST": "David", "NAME_LAST": "Ng" },
    { "ADDR_FULL": "12 King St, Boston, MA 02108" },
    { "REL_POINTER_DOMAIN": "GRAPH", "REL_POINTER_KEY": "P1002", "REL_POINTER_ROLE": "FATHER_OF" },
    { "REL_ANCHOR_DOMAIN": "GRAPH", "REL_ANCHOR_KEY": "P1001" }
  ]
}
```

Output JSON (person P1002)
```json
{
  "DATA_SOURCE": "GRAPH",
  "RECORD_ID": "P1002",
  "FEATURES": [
    { "RECORD_TYPE": "PERSON" },
    { "NAME_FIRST": "Hao", "NAME_LAST": "Ng" },
    { "ADDR_FULL": "45 Beacon St, Boston, MA 02108" },
    { "REL_POINTER_DOMAIN": "GRAPH", "REL_POINTER_KEY": "P1001", "REL_POINTER_ROLE": "SON_OF" },
    { "REL_ANCHOR_DOMAIN": "GRAPH", "REL_ANCHOR_KEY": "P1002" }
  ]
}
```

---

## Shot Example 6 — Parquet (identifier sublist) → Senzing JSON

Source Schema
- Shape: Parquet
- Columns:
  - `company_id` (string)
  - `name` (string)
  - `identifiers` (list<struct>): each struct has `id_type` (string), `id_number` (string), `country` (string)
- Notes: Flatten each element of `identifiers` to one identifier feature object. Use the element’s `country` to set the issuer when needed.

Sample Input (row-like illustration)
```json
[
  {
    "company_id": "UK-0001",
    "name": "Albion Trading Ltd",
    "identifiers": [
      { "id_type": "CRN", "id_number": "01234567", "country": "UK" },
      { "id_type": "TIN", "id_number": "123456789", "country": "UK" },
      { "id_type": "WEBSITE", "id_number": "www.albion.com" }
    ]
  },
  {
    "company_id": "IT-0001",
    "name": "Italia Servizi S.p.A.",
    "identifiers": [
      { "id_type": "CODICE_FISCALE", "id_number": "RSSMRA80A01H501U", "country": "IT" },
      { "id_type": "FOO", "id_number": "MI-1234567", "country": "IT" },
      { "id_type": "LEI", "id_number": "5493001KJTIIGC8Y1R12" }
    ]
  }
]
```

Mapping (proposal)
| SourceField | SenzingAttribute | Transform | Evidence | Confidence |
|---|---|---|---|---|
| company_id | RECORD_ID | As-is | — | High |
| name | NAME_ORG | As-is | — | High |
| identifiers[id_type=CRN].country=UK | NATIONAL_ID_TYPE=CRN; NATIONAL_ID_NUMBER; NATIONAL_ID_COUNTRY=UK | Map CRN to NATIONAL_ID (org registration) | [Spec §Mapping Identifiers: "Identifier Classification Decision Tree"]; [Spec §Mapping Identifiers: "Required context"]; [Spec §Feature: NATIONAL_ID: "NATIONAL_ID_TYPE"] | High |
| identifiers[id_type=TIN].country=UK | TAX_ID_TYPE=TIN; TAX_ID_NUMBER; TAX_ID_COUNTRY=UK | Map TIN to TAX_ID | [Spec §Mapping Identifiers: "Identifier Classification Decision Tree"]; [Spec §Mapping Identifiers: "Required context"]; [Spec §Feature: TAX_ID: "TAX_ID_TYPE"] | High |
| identifiers[id_type=WEBSITE] | WEBSITE_ADDRESS | As-is | [Spec §Feature: WEBSITE: "WEBSITE_ADDRESS"] | High |
| identifiers[id_type=CODICE_FISCALE].country=IT | TAX_ID_TYPE=CODICE_FISCALE; TAX_ID_NUMBER; TAX_ID_COUNTRY=IT | Map Codice Fiscale to TAX_ID | [Spec §Mapping Identifiers: "Identifier Classification Decision Tree"]; [Spec §Mapping Identifiers: "Required context"]; [Spec §Feature: TAX_ID: "TAX_ID_TYPE"] | High |
| identifiers[id_type=FOO].country=IT | OTHER_ID_TYPE=FOO; OTHER_ID_NUMBER; OTHER_ID_COUNTRY=IT | Map FOO to OTHER_ID (issuer country provided) | [Spec §Mapping Identifiers: "Everything else (last resort)"]; [Spec §Feature: OTHER_ID: "OTHER_ID_TYPE"] | High |
| identifiers[id_type=LEI] | LEI_NUMBER | As-is | [Spec §Mapping Identifiers: "Identifier Classification Decision Tree"]; [Spec §Feature: LEI_NUMBER: "LEI_NUMBER"] | High |

Output JSON (organization, UK)
```json
{
  "DATA_SOURCE": "REGISTRY",
  "RECORD_ID": "UK-0001",
  "FEATURES": [
    { "RECORD_TYPE": "ORGANIZATION" },
    { "NAME_ORG": "Albion Trading Ltd" },
    { "NATIONAL_ID_TYPE": "CRN", "NATIONAL_ID_NUMBER": "01234567", "NATIONAL_ID_COUNTRY": "UK" },
    { "TAX_ID_TYPE": "TIN", "TAX_ID_NUMBER": "123456789", "TAX_ID_COUNTRY": "UK" },
    { "WEBSITE_ADDRESS": "www.albion.com" }
  ]
}
```

Output JSON (organization, Italy)
```json
{
  "DATA_SOURCE": "REGISTRY",
  "RECORD_ID": "IT-0001",
  "FEATURES": [
    { "RECORD_TYPE": "ORGANIZATION" },
    { "NAME_ORG": "Italia Servizi S.p.A." },
    { "TAX_ID_TYPE": "CODICE_FISCALE", "TAX_ID_NUMBER": "RSSMRA80A01H501U", "TAX_ID_COUNTRY": "IT" },
    { "OTHER_ID_TYPE": "FOO", "OTHER_ID_NUMBER": "MI-1234567", "OTHER_ID_COUNTRY": "IT" },
    { "LEI_NUMBER": "5493001KJTIIGC8Y1R12" }
  ]
}
```

References: [Spec §Mapping Identifiers: "Identifier Classification Decision Tree"]; [Spec §Mapping Identifiers: "Required context"]; [Spec §Mapping Identifiers: "Everything else (last resort)"]

---

## Shot Example 5 — Graph (shared address mapped to persons) → Senzing JSON

Source Schema
- Shape: Graph (nodes and edges)
- Nodes:
  - Person P7001: `first_name`, `last_name`
  - Person P7002: `first_name`, `last_name`
  - Address A9001: `address_full`
- Edges:
  - P7001 ↔ A9001 (HAS_ADDRESS)
  - P7002 ↔ A9001 (HAS_ADDRESS)
- Note: Edges from people to an address node map to ADDRESS features on the person records. The address itself is not a Senzing record.

Sample Input (illustrative)
```json
{
  "nodes": [
    { "id": "P7001", "type": "person", "first_name": "Eva", "last_name": "Lopez" },
    { "id": "P7002", "type": "person", "first_name": "Marco", "last_name": "Lopez" },
    { "id": "A9001", "type": "address", "address_full": "742 Evergreen Terrace, Springfield" }
  ],
  "edges": [
    { "from": "P7001", "to": "A9001", "role": "HAS_ADDRESS" },
    { "from": "P7002", "to": "A9001", "role": "HAS_ADDRESS" }
  ]
}
```

Mapping (proposal)
| SourceField | SenzingAttribute | Transform | Evidence | Confidence |
|---|---|---|---|---|
| person.id | RECORD_ID | As-is | [Spec §Attributes for the Record Key: "RECORD_ID"] | High |
| person.first_name | NAME_FIRST | Trim | [Spec §Feature: NAME: "NAME_FIRST"] | High |
| person.last_name | NAME_LAST | Trim | [Spec §Feature: NAME: "NAME_LAST"] | High |
| address.address_full | ADDR_FULL | As-is | [Spec §Feature: ADDRESS: "ADDR_FULL"] | High |
| address link role | (no REL_*) | Do not create disclosed relationships to features | [Spec §Format notes (graph): features vs disclosed relationships] | High |

Output JSON (person P7001)
```json
{
  "DATA_SOURCE": "GRAPH",
  "RECORD_ID": "P7001",
  "FEATURES": [
    { "RECORD_TYPE": "PERSON" },
    { "NAME_FIRST": "Eva", "NAME_LAST": "Lopez" },
    { "ADDR_FULL": "742 Evergreen Terrace, Springfield" }
  ]
}
```

Output JSON (person P7002)
```json
{
  "DATA_SOURCE": "GRAPH",
  "RECORD_ID": "P7002",
  "FEATURES": [
    { "RECORD_TYPE": "PERSON" },
    { "NAME_FIRST": "Marco", "NAME_LAST": "Lopez" },
    { "ADDR_FULL": "742 Evergreen Terrace, Springfield" }
  ]
}
```

---

## Shot Example 7 — Embedded entity (contact → employer org) → Senzing JSON

Source Schema
- Shape: CSV (embedded employer fields on a contact list)
- Fields: `surname`, `given_name`, `cell_phone`, `employer_name`, `employer_address`
- Goal: Create a separate ORGANIZATION entity for the employer and relate the person to it.
- RECORD_ID for employer: Deterministic hash of identifying attributes (NAME_ORG + ADDR_FULL).

Sample Input
```csv
surname,given_name,cell_phone,employer_name,employer_address
Ng,David,+1-617-555-0101,Beacon Analytics,100 Market St, Boston, MA 02109
```

Mapping (proposal)
| SourceField | SenzingAttribute | Transform | Evidence | Confidence |
|---|---|---|---|---|
| given_name | NAME_FIRST | Trim | — | High |
| surname | NAME_LAST | Trim | — | High |
| cell_phone | PHONE_NUMBER | As-is | — | High |
| employer_name | NAME_ORG (on separate org record) | As-is | — | High |
| employer_address | ADDR_FULL (on separate org record) | As-is | — | High |
| employer (NAME_ORG + ADDR_FULL) | RECORD_ID (org) | Deterministic hash of normalized values | [Spec §How to Map Them: deterministic RECORD_ID for referenced entities] | High |
| person → employer | REL_POINTER_ROLE=EMPLOYED_BY | Person → Organization | [Spec §Disclosed Relationship Mapping Guidance: "REL_POINTER_ROLE"]; [Spec §Format notes (how to spot masters, children, and disclosed relationships)] | High |
| employer (org) | REL_ANCHOR | Add one anchor on the organization | [Spec §Disclosed Relationship Mapping Guidance: "REL_ANCHOR_DOMAIN"] | High |

References: [Spec §How to Map Them]; [Spec §Disclosed Relationship Mapping Guidance]; [Spec §Format notes (how to spot masters, children, and disclosed relationships)]

Output JSON (person)
```json
{
  "DATA_SOURCE": "CONTACTS",
  "RECORD_ID": "P-0001",
  "FEATURES": [
    { "RECORD_TYPE": "PERSON" },
    { "NAME_FIRST": "David", "NAME_LAST": "Ng" },
    { "PHONE_NUMBER": "+1-617-555-0101" },
    { "REL_POINTER_DOMAIN": "CONTACTS", "REL_POINTER_KEY": "ORG-2a9e3c5f", "REL_POINTER_ROLE": "EMPLOYED_BY" }
  ]
}
```

Output JSON (organization)
```json
{
  "DATA_SOURCE": "CONTACTS",
  "RECORD_ID": "ORG-2a9e3c5f",
  "FEATURES": [
    { "RECORD_TYPE": "ORGANIZATION" },
    { "NAME_ORG": "Beacon Analytics" },
    { "ADDR_FULL": "100 Market St, Boston, MA 02109" },
    { "REL_ANCHOR_DOMAIN": "CONTACTS", "REL_ANCHOR_KEY": "ORG-2a9e3c5f" }
  ]
}
```

Notes
- The org RECORD_ID (`ORG-2a9e3c5f`) represents a deterministic hash of normalized `NAME_ORG` + `ADDR_FULL` (example value shown).
- Use a stable normalization recipe before hashing (trim/casefold/collapse whitespace/punctuation).
