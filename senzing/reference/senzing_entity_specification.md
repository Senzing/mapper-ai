# Senzing Entity Specification (v0.1.0 — 2025-09-22)

This document defines the Senzing Entity Specification — a detailed guide for mapping source data into Senzing's entity resolution engine.

The process of mapping is taking a source field name, like CustomerName, and transforming it into a target field name, by applying specific rules, such as renaming, reformatting, or combining fields based on predefined logic or conditions. It's like creating a bridge where data from one system is reshaped to fit the structure of another system, guided by those rules.

# Key Terms

## Entities, Features and Attributes:
- **Entity** — A real-world subject, primarily a PERSON or an ORGANIZATION, described by one record.
- **Feature** — A set of related attributes about the entity (e.g., NAME, ADDRESS, PHONE).
- **Attribute** — A single field within a feature (e.g., NAME_FIRST and NAME_LAST in NAME; ADDR_LINE1 in ADDRESS).

## Usage types and payload (optional attributes)
- **Usage Type** — A short label that distinguishes multiple instances of the same feature on one entity (e.g., HOME vs MAILING address, MOBILE vs HOME phone, PRIMARY vs ALIAS name). It helps explain "which one it is" when there are several.
- **Payload Attributes** — These are attributes that are not used for matching, but can be helpful in understanding matches or making quick decisions. (e.g., STATUS: Active|Inactive, RISK_CATEGORY, INDUSTRY_CODE)

# What Features to Map

Entity resolution works best when you have a name and as many other features as you can find. The more features on each record, the better the entity resolution! Below are feature lists to look for in your sources. Rank indicates typical importance to entity resolution.

| Feature | Description | Importance | Guidance |
| --- | --- | --- | --- |
| RECORD_TYPE | (e.g., PERSON, ORGANIZATION) | High | Include when known to prevent cross‑type resolution; omit if unknown. Use standardized kinds (PERSON, ORGANIZATION). Often used to determine icon/shape in graphs. |
| NAME (person) | Personal names | High | Look for: legal name, aliases/AKAs, maiden/former names, nickname/preferred name, transliterations/alternate scripts. Use parsed components (FIRST, MIDDLE, LAST, SUFFIX) only when the source provides separate fields; do NOT parse a single name field—use NAME_FULL instead. |
| NAME (organization) | Organization legal or trade name | High | Look for: legal/registered name, trade/DBA, former names, short/brand names, transliterations/alternate scripts. |
| DOB | Person date of birth | High | Full date preferred; partial values accepted. |
| ADDRESS (person) | Postal/physical address | High | Look for: residential/home, mailing/remittance, previous/old; prefer parsed components when available (LINE1/2, CITY, STATE/PROVINCE, POSTAL_CODE, COUNTRY). |
| ADDRESS (organization) | Organization location address | High | Look for: physical/business/registered office, mailing/remittance; prefer parsed components when available (LINE1/2, CITY, STATE/PROVINCE, POSTAL_CODE, COUNTRY). |
| PASSPORT | Passport identifier | High | Include issuing country. |
| DRLIC | Driver's license | High | Include issuing state/province/country. |
| SSN | US Social Security Number | High | Partial values accepted. |
| TAX_ID | Tax identifier | High | Look for: EIN, VAT, TIN/ITIN; include issuing country. |
| NATIONAL_ID (person) | National/person identifier | High | Look for country‑specific IDs; include issuing country. Common examples: SIN (CA), CURP (MX), NINO (UK), NIR/INSEE (FR). |
| NATIONAL_ID (organization) | National/company registration identifier | High | Look for company registry numbers (not tax/VAT); include issuing country. Common examples: Company Number/CRN (UK), SIREN/SIRET (FR), Corporation Number (CA), Folio Mercantil (MX). |
| PHONE | Telephone number | Medium | Look for all phone numbers; distinguish mobile if possible; personal mobile numbers carry additional weight. |
| EMAIL | Email address | Medium | — |
| Social handles | Social/media handles | Medium | Features include: LINKEDIN, FACEBOOK, TWITTER, SKYPE, ZOOMROOM, INSTAGRAM, WHATSAPP, SIGNAL, TELEGRAM, TANGO, VIBER, WECHAT. |
| DUNS_NUMBER | Company identifier | Medium | — |
| LEI_NUMBER | Legal Entity Identifier | Medium | — |
| NPI_NUMBER | US healthcare provider ID | Medium | — |
| ACCOUNT | Account or card number | Medium | Look for bank or other account numbers that can aid resolution, especially across data sources. |
| OTHER_ID | Other/uncategorized identifier | Medium | For identifier types that can't be mapped to one of Senzing's specific identifier features. Use sparingly; if an identifier is used frequently, create a dedicated feature for it. |
| GENDER | Person gender | Low-Medium | — |
| EMPLOYER | Name of a person's employer | Medium-Low | Can aid resolution on smaller companies; subject to generic thresholds; form of group association. |
| GROUP_ASSOCIATION | Other organization names an entity is associated with | Medium-Low | Can aid resolution on smaller domains, subject to generic thresholds. |
| GROUP_ASSN_ID | Group identifier | Medium-Low | Can aid resolution on smaller domains, subject to generic thresholds. |
| DOD | Person date of death | Medium-Low | When applicable. |
| REGISTRATION_DATE | Organization registration/incorporation date | Medium-Low | Full date preferred; partial values accepted. |
| REGISTRATION_COUNTRY | Organization registration country | Low | — |
| NATIONALITY | Person nationality | Low | — |
| CITIZENSHIP | Person citizenship | Low | — |
| PLACE_OF_BIRTH | Person place of birth | Low | Typically not well controlled. |
| WEBSITE | Organization website/domain | Low | Typically shared across the organization's hierarchy. |
| REL_ANCHOR | Relationship anchor for a source record | Relationship | Optional (recommended when other records will point here); at most one per record. |
| REL_POINTER | Pointer to another record's anchor | Relationship | Place on source record; include REL_POINTER_ROLE (e.g., EMPLOYED_BY, PRINCIPAL_OF, OWNER_OF, SPOUSE_OF, SON_OF, FATHER_OF, BRANCH_OF, DIRECT_PARENT, ULTIMATE_PARENT). |
| TRUSTED_ID | Curated control identifier | Control | Forces records together or apart; like a curated ID layered over source IDs. Use cautiously per guidance. |

## Payload Attributes (Optional)

The full details about a record should exist in your source systems. Senzing holds the features needed for entity resolution and acts as a pointer system to where the full details of their record can be found.

Payload attributes are optional because they are not used in matching. However, they can help a human reviewer quickly triage a match and decide whether looking up the full record is warranted.

Here are some examples of useful payload attributes:

- STATUS: Active/Inactive helps triage quickly (e.g., ignore inactive duplicates; focus on active customers).
- CREATE_DATE (or FIRST_SEEN): Helps sort duplicates and spot fraud risk (e.g., a new record with conflicting identifiers vs. an older established one).
- INDUSTRY_CODE/INDUSTRY: Codes and labels from data providers that describe the business (e.g., NAICS/SIC).
- JOB_TITLE: Role/title from HR or data providers; can inform risk, especially when matched to a watchlist entry.
- RISK_CATEGORY/RISK_SCORE: Watchlist-derived codes/scores that explain the type and severity of risk.

Performance note:
- Payload increases storage and I/O. Include only when it materially improves downstream understanding. On very large systems, evaluate impact before enabling broadly.
- If you do decide to include them, keep them minimal and only include what helps a human understand matches or an algorithm to triage them.
- You may decide to map a few during a proof of concept while you are analyzing matches and then remove them when you go to production.

Feature name collisions:
- When a source field name matches a Senzing feature attribute name, verify the source field's meaning matches the feature's definition. If it matches → map as that feature. If it differs → rename to a materially different payload attribute name (e.g., source field "registration_date" that means account signup date should become "signup_date", not "ACCOUNT_REGISTRATION_DATE" which still contains the reserved name).

# Recommended JSON Schema

In prior versions we allowed a flat JSON structure with a separate sub-list for each feature that had multiple values. While we still support that, we now recommend the following JSON schema that has just one list for all features. It is much cleaner, and if you standardize on it, you can write a single parser to extract values for downstream processes if needed.

Example (person)
```json
{
    "DATA_SOURCE": "CUSTOMERS",
    "RECORD_ID": "1001",
    "FEATURES":
    [
        {
            "RECORD_TYPE": "PERSON"
        },
        {
            "NAME_TYPE": "PRIMARY",
            "NAME_LAST": "Smith",
            "NAME_FIRST": "Robert"
        },
        {
            "NAME_TYPE": "NICKNAME",
            "NAME_FULL": "Bobby Smith"
        },
        {
            "DATE_OF_BIRTH": "1978-12-11"
        },
        {
            "ADDR_TYPE": "HOME",
            "ADDR_LINE1": "123 Main Street",
            "ADDR_CITY": "Las Vegas",
            "ADDR_STATE": "NV",
            "ADDR_POSTAL_CODE": "89132"
        },
        {
            "ADDR_TYPE": "MAILING",
            "ADDR_FULL": "PO Box 19675, Las Vegas, NV 89111"
        },
        {
            "PHONE_TYPE": "HOME",
            "PHONE_NUMBER": "702-919-3211"
        },
        {
            "PHONE_TYPE": "MOBILE",
            "PHONE_NUMBER": "702-919-1300"
        },
        {
            "DRIVERS_LICENSE_NUMBER": "112233",
            "DRIVERS_LICENSE_STATE": "NV"
        },
        {
            "EMAIL_ADDRESS": "bsmith@work.com"
        },
        {
            "REL_ANCHOR_DOMAIN": "CUSTOMERS",
            "REL_ANCHOR_KEY": "1001"
        },
        {
            "REL_POINTER_DOMAIN": "CUSTOMERS",
            "REL_POINTER_KEY": "ORG1001",
            "REL_POINTER_ROLE": "EMPLOYED_BY"
        }
    ],
    "CREATE_DATE": "2020-06-15",
    "STATUS": "Active"
}
```

Example (organization)
```json
{
    "DATA_SOURCE": "CUSTOMERS",
    "RECORD_ID": "ORG1001",
    "FEATURES":
    [
        {
            "RECORD_TYPE": "ORGANIZATION"
        },
        {
            "NAME_ORG": "Acme Corporation"
        },
        {
            "ADDR_TYPE": "BUSINESS",
            "ADDR_FULL": "500 Industrial Way, Austin, TX 78701, US"
        },
        {
            "PHONE_NUMBER": "+1-512-555-2000"
        },
        {
            "EMAIL_ADDRESS": "info@acme.example"
        },
        {
            "LEI_NUMBER": "5493001KJTIIGC8Y1R12"
        },
        {
            "TAX_ID_TYPE": "EIN",
            "TAX_ID_NUMBER": "12-3456789",
            "TAX_ID_COUNTRY": "US"
        },
        {
            "WEBSITE_ADDRESS": "https://www.acme.example"
        },
        {
            "REL_ANCHOR_DOMAIN": "CUSTOMERS",
            "REL_ANCHOR_KEY": "ORG1001"
        }
    ],
    "NAICS_CODE": "541511",
    "COMPANY_TYPE": "Corporation"
}
```

Schema Validation Rules
- Root keys
  - `DATA_SOURCE` (required, string): short, stable code naming the source system.
  - `RECORD_ID` (recommended, string): unique within the `DATA_SOURCE`; used for add/replace.
  - `FEATURES` (required, array): the only array allowed at root.
    - Contains only feature objects. Each object represents one instance of a feature's attributes
    - All attributes in a feature object must belong to the same feature
  - Optional root level attributes (Payload Attributes)
    - Must not be a registered feature attribute
    - Must be a scalar object (string, number, boolean), Not an array or nested object
  - Only registered feature attributes may appear inside feature objects. See "Registered Feature Attributes" below for the complete list and guidance.

*Note: If exporting Senzing JSON records to a file its best to flatten them to create an easy to consume JSONL file.*

# Source Schema Types

Sources vary — CSV/TSV and relational tables, JSON/JSONL, XML, Parquet, and graph exports.

## Unified terms (applies to all sources)
- Master entity: the master person or organization record (a master table row, a graph node, or a top‑level JSON/XML object). One master → one Senzing entity document.
- Identifying attributes: the attributes that identify/describe the entity (names, addresses, phones, emails, identifiers, websites, etc.). These may appear on the master itself or inside child lists/structures.
- Child lists: one‑to‑many data with ONE foreign key to the master. Depending on source, these appear as separate tables, JSON arrays under the master object, repeated XML elements, Parquet list<struct> columns, or graph attribute nodes. Usually each child record represents one (name, address, phone, identifier, etc.) and contains a type such as alias or dba for a name, home, mailing etc for an address, drivers license, passport, tax_id, etc for an identifier.
- Disclosed relationships: links between source records (masters) (person↔org, person↔person, org↔org). Depending on source, these appear as link/bridge tables, foreign keys to other master IDs, JSON pointers, XML references, Parquet join keys, or graph edges.

## Format notes (how to spot masters, children, and disclosed relationships)
- CSV/TSV/Relational: master tables for persons/organizations; child tables for names, addresses, phones, identifiers; link tables for relationships. Join on primary/foreign keys; each child row → one feature object.
- JSON/JSONL: master object per entity; child lists are arrays on the master (e.g., `names`, `addresses`, `phones`, `ids`). Flatten each array element into a separate feature object. Nested objects representing a single value map to a single feature; arrays map to multiple features.
- XML: master element per entity; child lists are repeated child elements; attributes may be XML attributes or elements. Treat repeated elements like JSON arrays: one repeated element → one feature object. Extract scalar values only inside a feature.
- Parquet: when normalized across files, treat like relational; when a single file contains list/struct columns on the master row, treat list<struct> as child lists (one struct → one feature) and struct as a single feature's values. Join across Parquet datasets on keys where needed.
- Graph: nodes representing persons or organizations are master entities; edges from a master to attribute nodes (e.g., address, phone, email, identifiers) represent features; edges between master nodes represent disclosed relationships.

## How to Map Them

- Master entity: each person/org row, node, or top‑level object → one Senzing record; include `RECORD_TYPE` (PERSON/ORGANIZATION) when known.
- Features: collect identifying attributes from the master and child lists/structures (tables, arrays/repeated elements, list<struct>, property nodes) and group them into features — `NAME_*`, `ADDR_*`, `PHONE_*`, `PASSPORT_*`, etc.
- Disclosed relationships: map links/edges/foreign keys between source records (masters) using `REL_*` features.
- Output: emit one JSON record per master entity with all FEATURES (attributes and disclosed relationships) included.
- For records that reference entities without unique keys (e.g., sender and receiver on transactions), extract identifying attributes and compute a deterministic RECORD_ID as a hash of normalized values. Stamp this ID on the source record before mapping to Senzing, and track these IDs on the source side as well.
- For records that have features that clearly do not belong to the primary entity (e.g., employer name and address on a contact list, reference name and phone number on a job application), consider creating a second entity related to the primary entity.
- Use a stable normalization recipe (fixed fields and order; trim/collapse whitespace; case‑fold; normalize punctuation/diacritics) before hashing.

# General mapping guidance

The following sections cover how Senzing treats record updates versus replacements, usage types, and identifier mapping.

Important: Decisions in this section affect matching behavior and whether records break or reinforce matches. Coordinate changes carefully and validate with sample runs.
- Updating vs Replacing determines which features are present at match time (no hidden history in Senzing).
- Usage types with special meaning (PRIMARY/BUSINESS/MOBILE) influence display/weighting.
- Identifier choices (specific vs NATIONAL_ID/TAX_ID/OTHER_ID) control break/no‑break behavior.

## Updating vs Replacing Records

Senzing always replaces records. It keeps governance and interpretation clear, avoids storing stale or unknown history in Senzing, and respects data‑provider and watchlist contracts that often forbid retaining prior values. It is also impossible for Senzing alone to know whether a prior address was corrected vs. a move, or whether a missing phone was removed on purpose.

Guidance
- Present all features you wish to retain (including historical values) in a single JSON record at update time.
- If the source keeps feature history, map that history as additional FEATURES.
- If the source lacks history, you may maintain your own small history table (DATA_SOURCE, RECORD_ID, FEATURE type, feature JSON) and merge as needed when producing the new record.

## Mapping Usage Types

Senzing matches across usage types because they are not well standardized and are often mislabeled across systems. Therefore, map usage types primarily for reference. However, three usage types do have special meaning that influences display or weighting.

Guidance
- Only include usage types when the source clearly provides them.
- Special meanings that influence resolution/display:
  - NAME_TYPE PRIMARY: Used to choose the best display name when multiple names exist.
  - ADDR_TYPE BUSINESS (organizations): Adds weight to an organization's physical location.
  - PHONE_TYPE MOBILE: Adds weight to personal mobile numbers.

## Mapping Identifiers

How identifiers arrive
- Direct fields: single columns like `SSN`, `LICENSE_NO`, `TIN`, `EIN`, `LEI`, etc.
- Child/type table: rows with `id_type`, `id_number`, and sometimes `id_country` or issuer (e.g., codes such as SSN, DRIVERS LICENSE, TIN).

Classification workflow (stop at first match)
1) Specific identifier
   - SSN → SSN
   - Passport → PASSPORT + PASSPORT_COUNTRY
   - Driver's License → DRLIC + DRIVERS_LICENSE_STATE
   - LEI → LEI_NUMBER
   - DUNS → DUNS_NUMBER
   - NPI → NPI_NUMBER

2) Tax-related identifier
   - VAT, TIN, INN, EIN/FEIN, other tax codes
   - Map to TAX_ID + TAX_ID_TYPE + TAX_ID_COUNTRY

3) Country-issued national identifier
   - Unique per person/org within a country (e.g., CEDULA, SIREN, OGRN)
   - Map to NATIONAL_ID + NATIONAL_ID_TYPE + NATIONAL_ID_COUNTRY

4) Unknown code? Research first
   - Look up the token; confirm whether it is tax, national, or organization-issued (e.g., LEI).
   - Maintain and consult a local crosswalk. Add aliases and verified findings to keep decisions consistent.

5) Everything else (last resort)
   - Only if it is truly an identifier and not covered above: OTHER_ID + OTHER_ID_TYPE [+ OTHER_ID_COUNTRY when relevant].
   - Do not default to OTHER_ID without research (see "dumping-ground" warning below).

Required context
- Always include issuer to scope uniqueness (e.g., PASSPORT_COUNTRY, DRIVERS_LICENSE_STATE, TAX_ID_COUNTRY). See "Identifiers → Principles" for uniqueness and issuer guidance.

Beware "dumping‑ground" identifier tables
- Some sources use code-driven "identifier" tables for anything lacking a dedicated field. You may encounter document dates (e.g., birth-certificate dates), risk categories/statuses, or free-text notes. Do not map these as identifiers (including OTHER_ID). Route to a registered feature when appropriate; otherwise use payload attributes or omit when no meaningful, spec-compliant placement exists.

Common identifier mappings reference

| Identifier | Countries    | Feature     | Type   | Example/Notes                               |
|-----------|---------------|-------------|--------|---------------------------------------------|
| OGRN      | RU            | NATIONAL_ID | OGRN   | RU business registration                    |
| INN       | RU            | TAX_ID      | INN    | Russian tax number                          |
| LEI       | International | LEI_NUMBER  | —      | Legal Entity Identifier                     |
| VAT       | EU/Global     | TAX_ID      | VAT    | Value Added Tax ID                          |
| CEDULA    | LATAM         | NATIONAL_ID | CEDULA | National ID card                            |
| SIREN     | FR            | NATIONAL_ID | SIREN  | FR business identifier                      |
| TIN       | US/Global     | TAX_ID      | TIN    | Taxpayer ID                                 |
| IMO       | International | OTHER_ID    | IMO    | Vessel identifier (no specific feature)     |
| Passport  | Any           | PASSPORT    | —      | Travel document                             |
| SSN       | US            | SSN         | —      | US Social Security Number                   |

## Mapping Group Associations (small groups only)

Purpose
- Use Group Associations only when the group is small and specific, materially narrowing the population.
- Intended for sparse data scenarios — when a person/organization is known primarily by a small group affiliation.

Use when the group is small/specific
- Examples: OWNER_EXEC of a company; BOARD_MEMBER of "ACME Corp"; CHAPTER_OFFICERS for "Local Chapter 42"; PROJECT_TEAM "AML 2024"; ALUMNI_COHORT "CS 2008".
- Provide both a precise type and a specific group/organization name.

Do not use for large/generic populations
- Not acceptable: political parties (e.g., REPUBLICAN, DEMOCRAT), religions, national populations, country/state "residents", mega social networks, extremely large unions or programs.
- Do not encode broad categories like "EMPLOYEE" as a group association unless the subgroup is small and well‑bounded.

Examples
- Good: GROUP_ASSOCIATION_TYPE=OWNER_EXEC; GROUP_ASSOCIATION_ORG_NAME="ACME Corp"
- Bad: GROUP_ASSOCIATION_TYPE=POLITICAL_PARTY; GROUP_ASSOCIATION_ORG_NAME="Democratic Party"
- Bad: GROUP_ASSOCIATION_TYPE=RESIDENTS; GROUP_ASSOCIATION_ORG_NAME="United States"

Notes
- Group Associations are optional and have limited utility; prefer them only when they add discriminative power in sparse contexts.

# Disclosed Relationship Mapping Guidance

What it is
- Disclosed relationships connect source records (masters), not features.
- Common pairs and examples:
  - Person ↔ Person: familial (e.g., SPOUSE_OF, SON_OF, FATHER_OF)
  - Person ↔ Organization: employment/ownership (e.g., EMPLOYED_BY, PRINCIPAL_OF, OWNER_OF)
  - Organization ↔ Organization: corporate hierarchy (e.g., BRANCH_OF, DIRECT_PARENT, ULTIMATE_PARENT)
- Extensible: if you add new `RECORD_TYPE`s (e.g., VEHICLE, VESSEL), apply the same pattern (e.g., OWNS_VESSEL, OPERATES_VEHICLE).

Direction and roles (how to assign anchor vs pointer)
- Single rule: the record doing the pointing holds `REL_POINTER_*`; the record being pointed to holds `REL_ANCHOR_*`.
- Role-driven direction examples:
  - EMPLOYED_BY: Person → Organization (person has REL_POINTER; organization has REL_ANCHOR)
  - BRANCH_OF: Branch org → Parent org (branch has REL_POINTER; parent has REL_ANCHOR)
  - PRINCIPAL_OF: Person → Organization (person has REL_POINTER; organization has REL_ANCHOR)
  - OWNER_OF: Person → Organization (person has REL_POINTER; organization has REL_ANCHOR)
  - DIRECT_PARENT: Parent org → Child org (parent has REL_POINTER; child has REL_ANCHOR)
  - ULTIMATE_PARENT: Top-level parent → Subsidiary (top-level has REL_POINTER; subsidiary has REL_ANCHOR)
  - SPOUSE_OF: Often symmetric; emitting a single direction is acceptable if that's what your source provides.
  - SON_OF / FATHER_OF (directional verbs): Follow the verb — SON_OF means child → parent; FATHER_OF means parent → child.

Anchors: avoid second passes
- Place at most one `REL_ANCHOR` on any record that could be a target of relationships.
- It's safe and recommended to add `REL_ANCHOR` proactively (even if pointers aren't known yet) so no second pass is required.

Model (anchor ↔ pointer)
- Anchor (target): add one `REL_ANCHOR` feature object; never more than one per record.
- Pointer (source): for each disclosed relationship leaving this record, add one `REL_POINTER` feature object with a role.
- Do not mix `REL_ANCHOR_*` and `REL_POINTER_*` keys in the same feature object.

Required fields
- Anchor: `REL_ANCHOR_DOMAIN`, `REL_ANCHOR_KEY` (uniquely identifies the target record).
- Pointer: `REL_POINTER_DOMAIN`, `REL_POINTER_KEY`, `REL_POINTER_ROLE` (e.g., SPOUSE_OF, SON_OF, FATHER_OF, EMPLOYED_BY, PRINCIPAL_OF, OWNER_OF, BRANCH_OF, DIRECT_PARENT, ULTIMATE_PARENT; standardize roles for filtering and display).

Map from common source shapes
- Link/bridge table: each link row → one `REL_POINTER` on the source record; ensure the target record has one `REL_ANCHOR`.
- Foreign key on a master: the record with the FK gets a `REL_POINTER`; the referenced record gets a `REL_ANCHOR`.
- JSON/XML references: treat object references as links; emit `REL_POINTER` on the referencing record and `REL_ANCHOR` on the referenced record.

Domain and key
- Prefer `REL_*_DOMAIN = DATA_SOURCE` and `REL_*_KEY = RECORD_ID` of the target record (or a stable link‑registry domain/key if you use one).
- Keys must be unique within the domain; keep formats stable and deterministic.

Cardinality and integrity
- One anchor per record (max). Zero or more pointers per record.
- One relationship → one `REL_POINTER` object (multiple relationships → multiple objects).
- Validate that every `REL_POINTER (DOMAIN, KEY)` resolves to a record that has (or will have) a matching `REL_ANCHOR`.

See also
- Full field definitions and examples: Feature: `REL_ANCHOR` and Feature: `REL_POINTER` later in this spec.

# Registered Feature Attributes

## Attributes for the Record Key

These attributes tie records in Senzing back to your source system. Place them at the root of each JSON record.

| Attribute | Required | Example | Guidance |
| --- | --- | --- | --- |
| DATA_SOURCE | Required | CUSTOMERS | Short, stable code naming the source (e.g., CUSTOMERS). If you have multiple similar sources, use distinct codes (e.g., BANKING_CUSTOMERS, MORTGAGE_CUSTOMERS). Prefer uppercase, no spaces. Used for retrieval and reporting — keep it consistent. |
| RECORD_ID | Strongly Recommended | 1001 | Must be unique within DATA_SOURCE; used to add/replace records. If the source lacks a primary key, construct a deterministic ID (e.g., hash of normalized identifying attributes). If omitted, Senzing generates a hash of features, making updates impractical. Do not duplicate RECORD_ID as a feature — retrieval uses DATA_SOURCE + RECORD_ID. |

Example
```json
{
  "DATA_SOURCE": "CUSTOMERS",
  "RECORD_ID": "1001",
}
```

### FEATURE: RECORD_TYPE
Importance: High

| Attribute | Required | Example | Guidance |
| --- | --- |  --- | --- |
| RECORD_TYPE | Recommended | PERSON | Prevents records of different types from resolving. Include when known to prevent cross‑type resolution; leave blank if unknown. Use standardized kinds (PERSON, ORGANIZATION). Often used to pick the icon/shape in graphs. |

Example
```json
{
  "FEATURES": [
    { "RECORD_TYPE": "PERSON" }
  ]
}
```

Tips for adding RECORD_TYPEs
- If you choose to add RECORD_TYPE, pick values that make sense for visualization too (e.g., a value that can map to a graph icon/shape).
- Avoid role labels as RECORD_TYPE (EMPLOYEE, VENDOR, CUSTOMER). Use intrinsic types (PERSON, ORGANIZATION) to preserve cross‑type resolution.
- Many watchlists have standardized on values such as VESSEL and AIRCRAFT. You do not need to register these in Senzing to use them as RECORD_TYPE.
- If you add such types, also include their appropriate identifiers as FEATURES so matching remains effective (e.g., `IMO_NUMBER`, `CALL_SIGN` for vessels; `AIRCRAFT_TAIL_NUMBER` for aircraft).

## Feature: NAME
Importance: High

| Attribute    | Example                 | Guidance |
| ---          | ---                     | --- |
| NAME_TYPE    | PRIMARY                 | Optional; include when the source provides it. Common values: PRIMARY, AKA (persons), DBA (organizations). |
| NAME_FIRST   | Robert                  | Person given name. |
| NAME_LAST    | Smith                   | Person surname. |
| NAME_MIDDLE  | A                       | Person middle name/initial (optional). |
| NAME_PREFIX  | Dr                      | Person title/prefix (optional). |
| NAME_SUFFIX  | Jr                      | Person suffix (optional). |
| NAME_ORG     | Acme Tire Inc.          | Organization name. |
| NAME_FULL    | Robert J Smith, Trust   | Single-field name when type (person vs org) is unknown or only a full name is provided. |

Rules
- Use parsed person names (NAME_FIRST/NAME_LAST/...) only when the source provides separate fields; do NOT attempt to parse a single name field—use NAME_FULL for single-field names (even if they appear parseable, like "Smith, Robert"). Use NAME_ORG for organizations.
- Keep each NAME feature object internally consistent: do not mix NAME_FULL with parsed name fields in the same object; do not mix NAME_ORG with parsed person fields in the same object.
- Use NAME_TYPE only when provided by the source (e.g., PRIMARY, AKA, DBA).
- When multiple names exist, NAME_TYPE=PRIMARY is special: it determines the best display name for the resolved entity (prefer PRIMARY over AKA).

Examples
- ✅ Person (parsed)
```json
{
  "FEATURES": [
    { "NAME_FIRST": "Robert", "NAME_LAST": "Smith", "NAME_MIDDLE": "A" }
  ]
}
```
- ✅ Organization
```json
{
  "FEATURES": [
    { "NAME_ORG": "Acme Tire Inc.", "NAME_TYPE": "PRIMARY" }
  ]
}
```
- ✅ Unknown type
```json
{
  "FEATURES": [
    { "NAME_FULL": "Robert J Smith, Trust" }
  ]
}
```

## Feature: ADDRESS
Importance: High

| Attribute       | Example                                   | Guidance |
| ---             | ---                                       | --- |
| ADDR_TYPE       | HOME                                      | Optional; include when provided by the source. Common values: HOME, MAILING (persons); BUSINESS (organizations). |
| ADDR_LINE1      | 111 First St                              | First address line (street, number). |
| ADDR_LINE2      | Suite 101                                 | Second address line (apt/suite). |
| ADDR_LINE3      |                                           | Third address line (optional). |
| ADDR_LINE4      |                                           | Fourth address line (optional). |
| ADDR_LINE5      |                                           | Fifth address line (optional). |
| ADDR_LINE6      |                                           | Sixth address line (optional). |
| ADDR_CITY       | Las Vegas                                 | City/locality. |
| ADDR_STATE      | NV                                        | State/province/region code. |
| ADDR_POSTAL_CODE| 89111                                     | Postal/ZIP code. |
| ADDR_COUNTRY    | US                                        | Country code. |
| ADDR_FULL       | 3 Underhill Way, Las Vegas, NV 89101, US  | Single-field address when parsed components are unavailable. |

Rules
- Prefer parsed address fields when available (ADDR_LINE1..ADDR_LINE6, ADDR_CITY, ADDR_STATE, ADDR_POSTAL_CODE, ADDR_COUNTRY).
- Use ADDR_FULL only when parsed components are unavailable.
- Do not mix ADDR_FULL with parsed address fields in the same object.
- For organizations, assign ADDR_TYPE=BUSINESS to at least one address when known (adds weight to the physical location).

Examples
- ✅ Parsed address
```json
{
  "FEATURES": [
    { "ADDR_TYPE": "HOME", "ADDR_LINE1": "111 First St", "ADDR_CITY": "Las Vegas", "ADDR_STATE": "NV", "ADDR_POSTAL_CODE": "89111" }
  ]
}
```
- ✅ Single-field address
```json
{
  "FEATURES": [
    { "ADDR_TYPE": "MAILING", "ADDR_FULL": "3 Underhill Way, Las Vegas, NV 89101, US" }
  ]
}
```

## Feature: PHONE
Importance: Medium

| Attribute    | Example       | Guidance |
| ---          | ---           | --- |
| PHONE_TYPE   | MOBILE        | Optional; include when provided by the source. Common values: MOBILE, HOME, WORK, FAX. MOBILE carries extra weight. |
| PHONE_NUMBER | 702-555-1212  | Telephone number. |

Rules
- Include PHONE_TYPE only when the source provides it (MOBILE carries extra weight).
- One PHONE object per number; represent multiple numbers as multiple PHONE objects.
- Do not put a list of numbers inside a single PHONE object.
- When a source uses clear prefixes (e.g., HOME_PHONE), you may derive PHONE_TYPE from the prefix.

Examples
```
{
  "FEATURES": [
    { "PHONE_TYPE": "MOBILE", "PHONE_NUMBER": "702-555-1212" },
    { "PHONE_NUMBER": "702-555-3434" }
  ]
}
```

## Simple Scalar Attributes

These single-value attributes follow the same pattern: `{ "ATTRIBUTE": "value" }`.

| Attribute | Importance | Example | Guidance |
| --- | --- | --- | --- |
| DATE_OF_BIRTH | High | 1980-05-14 | Complete dates preferred; partial dates accepted (YYYY-MM or MM-DD). |
| GENDER | Low-Medium | M | Only M, F, Male, Female are matched; other values ignored. |
| DATE_OF_DEATH | Low-Medium | 2010-05-14 | Complete dates preferred; partial dates accepted. |
| NATIONALITY | Low | US | Country of nationality (code or label). |
| CITIZENSHIP | Low | US | Country of citizenship (code or label). |
| PLACE_OF_BIRTH | Low | Chicago | City/region or country code/label. |
| REGISTRATION_DATE | Low-Medium | 2010-05-14 | Organization registration date. Complete dates preferred. |
| REGISTRATION_COUNTRY | Low | US | Organization country of registration (code or label). |

Example
```json
{
  "FEATURES": [
    { "DATE_OF_BIRTH": "1980-05-14" },
    { "GENDER": "F" },
    { "NATIONALITY": "US" }
  ]
}
```

## Identifiers

### Feature: PASSPORT
Importance: High

| Attribute          | Example     | Guidance |
| ---                | ---         | --- |
| PASSPORT_NUMBER    | 123456789   | Passport number. |
| PASSPORT_COUNTRY   | US          | Issuing country. Strongly recommended. |

Example
```json
{
  "FEATURES": [
    { "PASSPORT_NUMBER": "123456789", "PASSPORT_COUNTRY": "US" }
  ]
}
```

### Feature: DRLIC (Driver's License)
Importance: High

| Attribute               | Example | Guidance |
| ---                     | ---     | --- |
| DRIVERS_LICENSE_NUMBER  | 112233  | Driver's license number. |
| DRIVERS_LICENSE_STATE   | NV      | Issuing state/province/country. Strongly recommended. |

Example
```json
{
  "FEATURES": [
    { "DRIVERS_LICENSE_NUMBER": "112233", "DRIVERS_LICENSE_STATE": "NV" }
  ]
}
```

### Feature: SSN (US Social Security Number)
Importance: High

| Attribute   | Example      | Guidance |
| ---         | ---          | --- |
| SSN_NUMBER  | 123-12-1234  | US Social Security Number; partial accepted. |

Example
```json
{
  "FEATURES": [
    { "SSN_NUMBER": "123-12-1234" }
  ]
}
```

### Feature: NATIONAL_ID
Importance: High

| Attribute            | Example   | Guidance |
| ---                  | ---       | --- |
| NATIONAL_ID_TYPE     | CEDULA    | Use the type label from the source; standardize across sources. |
| NATIONAL_ID_NUMBER   | 123121234 | National identifier value. |
| NATIONAL_ID_COUNTRY  | FR        | Issuing country. Strongly recommended. |

Rules
- If the source type cannot be standardized and NATIONAL_ID_COUNTRY is present, leave NATIONAL_ID_TYPE blank.

Good/Bad
- ✅ Good
```json
{
  "FEATURES": [
    { "NATIONAL_ID_TYPE": "SIREN", "NATIONAL_ID_NUMBER": "552081317", "NATIONAL_ID_COUNTRY": "FR" }
  ]
}
```
- ❌ Bad (SSN mapped as NATIONAL_ID)
```json
{
  "FEATURES": [
    { "NATIONAL_ID_TYPE": "SSN", "NATIONAL_ID_NUMBER": "123-12-1234" }
  ]
}
```

### Feature: TAX_ID
Importance: High

| Attribute        | Example     | Guidance |
| ---              | ---         | --- |
| TAX_ID_TYPE      | EIN         | Use the type label from the source; standardize across sources. |
| TAX_ID_NUMBER    | 12-3456789  | Tax identification number. |
| TAX_ID_COUNTRY   | US          | Issuing country. Strongly recommended. |

Rules
- If the source type cannot be standardized and TAX_ID_COUNTRY is present, leave TAX_ID_TYPE blank.

Good/Bad
- ✅ Good
```json
{
  "FEATURES": [
    { "TAX_ID_TYPE": "EIN", "TAX_ID_NUMBER": "12-3456789", "TAX_ID_COUNTRY": "US" }
  ]
}
```
- ❌ Bad (EIN as NATIONAL_ID)
```json
{
  "FEATURES": [
    { "NATIONAL_ID_TYPE": "EIN", "NATIONAL_ID_NUMBER": "12-3456789", "NATIONAL_ID_COUNTRY": "US" }
  ]
}
```

### Feature: OTHER_ID
Importance: Medium

| Attribute         | Example  | Guidance |
| ---               | ---      | --- |
| OTHER_ID_TYPE     | ISIN     | Standardized source type strongly recommended as not always issued by a country |
| OTHER_ID_NUMBER   | 123121234| Identification number. |
| OTHER_ID_COUNTRY  | MX       | Optional as country often not known or issued by an organization |

- Use OTHER_ID sparingly; Prefer adding a specific feature for frequently used non‑country identifiers so matching behavior can be adjusted.
- Do NOT use OTHER_ID for values that are not unique to an entity within the domain.

Good/Bad
- ✅ Good
```json
{
  "FEATURES": [
    { "OTHER_ID_TYPE": "ISIN", "OTHER_ID_NUMBER": "123121234" }
  ]
}
```
- ❌ Bad (Category as an Identifier)
```json
{
  "FEATURES": [
    { "OTHER_ID_TYPE": "SDN Type", "OTHER_ID_NUMBER": "Sanctions List" }
  ]
}
```
- ❌ Bad (Date as an Identifier)
```json
{
  "FEATURES": [
    { "OTHER_ID_TYPE": "Certificate date", "OTHER_ID_NUMBER": "12/11/1980" }
  ]
}
```

### Feature: ACCOUNT
Importance: Medium

| Attribute        | Example                | Guidance |
| ---              | ---                    | --- |
| ACCOUNT_NUMBER   | 1234-1234-1234-1234    | Account number (e.g., bank, card). |
| ACCOUNT_DOMAIN   | VISA                   | Domain/system for the account number. |

Example
```json
{
  "FEATURES": [
    { "ACCOUNT_NUMBER": "1234-1234-1234-1234", "ACCOUNT_DOMAIN": "VISA" }
  ]
}
```

### Feature: DUNS_NUMBER
Importance: Medium

| Attribute    | Example | Guidance |
| ---          | ---     | --- |
| DUNS_NUMBER  | 123123  | Dun & Bradstreet company identifier. |

Example
```json
{
  "FEATURES": [
    { "DUNS_NUMBER": "123123" }
  ]
}
```

### Feature: NPI_NUMBER
Importance: Medium

| Attribute    | Example | Guidance |
| ---          | ---     | --- |
| NPI_NUMBER   | 123123  | US healthcare provider identifier. |

Example
```json
{
  "FEATURES": [
    { "NPI_NUMBER": "123123" }
  ]
}
```

### Feature: LEI_NUMBER
Importance: Medium

| Attribute    | Example | Guidance |
| ---          | ---     | --- |
| LEI_NUMBER   | 123123  | Legal Entity Identifier. |

Example
```json
{
  "FEATURES": [
    { "LEI_NUMBER": "123123" }
  ]
}
```

## Features: EMAIL and WEBSITE

| Attribute | Importance | Example | Guidance |
| --- | --- | --- | --- |
| EMAIL_ADDRESS | Medium | alex@example.com | Email address. |
| WEBSITE_ADDRESS | Low | acmetire.com | Website or domain; typically for organizations. |

## Features for Social Media Handles
Importance: Medium

Social handle features use the feature name as the attribute name.

| Feature/Attribute | Example           | Guidance |
| ---               | ---               | --- |
| LINKEDIN          | in/jane-doe       | Canonical handle/ID; no URL; no leading @. |
| FACEBOOK          | brand.page        | Canonical handle/ID; no URL; no leading @. |
| TWITTER           | john_doe          | Canonical handle/ID; no URL; no leading @. |
| SKYPE             | handle            | Canonical handle/ID; no URL. |
| ZOOMROOM          | room-id           | Canonical handle/ID; no URL. |
| INSTAGRAM         | jane.doe          | Canonical handle/ID; no URL; no leading @. |
| WHATSAPP          | +14155551234      | Canonical handle/ID; also map to PHONE. |
| SIGNAL            | +14155551234      | Canonical handle/ID; also map to PHONE. |
| TELEGRAM          | acme_support      | Canonical handle/ID; strip t.me/. |
| TANGO             | handle            | Canonical handle/ID; no URL. |
| VIBER             | +14155551234      | Canonical handle/ID; also map to PHONE. |
| WECHAT            | handle            | Canonical handle/ID; no URL. |

Rules
- Normalize values: store the canonical handle/ID, not a full URL. Strip `http(s)://`, `www.`, trailing slashes, query params, and a leading `@`.
- One handle per object: add one FEATURES object per platform handle; do not concatenate multiple handles.
- Prefer handle/ID over URL: if only a profile URL is provided, extract the handle/ID.
- Don't use content links: skip post/status URLs; only capture profile-level handles/IDs.
- Case handling: store handles lowercased for case‑insensitive platforms; preserve exact case if a platform is case‑sensitive.
- Phone‑based apps: when a handle is a phone number (e.g., WhatsApp, Signal, Viber), also map the number to PHONE in addition to the app‑specific feature.
- Persons vs organizations: map personal handles on person records and brand handles on organization records when known; avoid crossing them.
- Stability: handles can change; use alongside stronger identifiers (email, phone, gov IDs).

- Platform specifics
  - TWITTER (X): letters, numbers, underscores; length 1–15; case‑insensitive.
  - INSTAGRAM: letters, numbers, periods, underscores; length 1–30; case‑insensitive.
  - TELEGRAM: letters, numbers, underscores; 5–32; case‑insensitive; strip `t.me/`.
  - LINKEDIN: prefer the public slug (e.g., `in/jane-doe` or `company/acme`); if only a URL is provided, extract the slug.

Example
```json
{
  "FEATURES": [
    { "LINKEDIN": "in/john-smith" },
    { "TWITTER": "janedoe" }
  ]
}
```

## Group Associations

See 'Mapping Group Associations (small groups only)' for guidance and examples.

### Feature: EMPLOYER
Importance: Low-Medium

| Attribute | Example | Guidance |
| --- | --- | --- |
| EMPLOYER | ABC Company | This is the name of the organization the person is employed by. |

Rules
- When the source provides explicit employment relationships between person and organization records, prefer REL_POINTER/REL_ANCHOR to model the relationship; EMPLOYER can still be included for resolution.

Example
```json
{
  "FEATURES": [
    { "EMPLOYER": "ABC Company" }
  ]
}
```

### Feature: GROUP_ASSOCIATION
Importance: Low-Medium

| Attribute | Example | Guidance |
| --- | --- | --- |
| GROUP_ASSOCIATION_TYPE | OWNER_EXEC | Specific group/role within the organization; use precise categories (e.g., OWNER_EXEC, BOARD_MEMBER) to improve resolution. |
| GROUP_ASSOCIATION_ORG_NAME | Group name | Name of the associated organization; use the official or standardized name. |

Rules
- Provide GROUP_ASSOCIATION_TYPE to keep the group specific. Specific roles/groups (e.g., owners/executives of a company) are much smaller than the general population and therefore more discriminative.
- Only use when the group is small and specific; primarily useful in sparse data contexts.
- Do not set GROUP_ASSOCIATION for broad populations (e.g., political parties, religions, national populations, country/state residents, mega social networks).
- Provide a precise GROUP_ASSOCIATION_TYPE and a specific GROUP_ASSOCIATION_ORG_NAME.
- Example of discriminative power: the combination of a name with a small group (e.g., "George Washington" + "US President") is far rarer than the name alone.

Example
```json
{
  "FEATURES": [
    { "GROUP_ASSOCIATION_TYPE": "OWNER_EXEC", "GROUP_ASSOCIATION_ORG_NAME": "ABC Company" }
  ]
}
```

### Feature: GROUP_ASSN_ID
Importance: Low-Medium

| Attribute | Example | Guidance |
| --- | --- | --- |
| GROUP_ASSN_ID_TYPE | COMPANY_ID | The type of group identifier an entity is associated with. |
| GROUP_ASSN_ID_NUMBER | 12345 | The identifier the entity is associated with. If the group has a registered identifier, place it here. |

Rules
- Use when the group/organization has a registered identifier (e.g., DUNS). Include both type and number when available.

Example
```json
{
  "FEATURES": [
    { "GROUP_ASSN_ID_TYPE": "COMPANY_ID", "GROUP_ASSN_ID_NUMBER": "12345" }
  ]
}
```

## Disclosed relationships

See Disclosed Relationship Mapping Guidance above for model, direction, cardinality, and field‑population patterns.

### Feature: REL_ANCHOR
Category: Relationship

| Attribute | Example | Guidance |
| --- | --- | --- |
| REL_ANCHOR_DOMAIN | CUSTOMERS | This code helps keep the REL_ANCHOR_KEY unique.  This is a code (without dashes) for the data source or source field that is contributing the relationship.
| REL_ANCHOR_KEY | 1001 | This key should be a unique value for the record within the REL_ANCHOR_DOMAIN.  You can just use the current record's RECORD_ID here.|

Rules
- Include at most one REL_ANCHOR per record, only when other records will point to it.
- REL_ANCHOR identifies the target record for relationships using `REL_ANCHOR_DOMAIN` and `REL_ANCHOR_KEY`.
- Do not mix REL_ANCHOR and REL_POINTER attributes in the same feature object (separate objects in FEATURES are fine).
- Use a domain code without dashes to avoid confusion in downstream match key parsing.

Examples
```json
{
  "FEATURES": [
    { "REL_ANCHOR_DOMAIN": "CUSTOMERS", "REL_ANCHOR_KEY": "ACME-1001" }
  ]
}
```

- ❌ Incorrect (multiple REL_ANCHOR objects — only one allowed per record)
```json
{
  "FEATURES": [
    { "REL_ANCHOR_DOMAIN": "CUSTOMERS", "REL_ANCHOR_KEY": "ACME-1001" },
    { "REL_ANCHOR_DOMAIN": "CUSTOMERS", "REL_ANCHOR_KEY": "ACME-2002" }
  ]
}
```

### Feature: REL_POINTER
Category: Relationship

| Attribute | Example | Guidance |
| --- | --- | --- |
| REL_POINTER_DOMAIN | CUSTOMERS | See REL_ANCHOR_DOMAIN above. |
| REL_POINTER_KEY | 1001 | See REL_ANCHOR_KEY above.
| REL_POINTER_ROLE | SPOUSE | This is the role the pointer record has to the anchor record. Such as SPOUSE_OF, SON_OF, FATHER_OF, EMPLOYED_BY, PRINCIPAL_OF, OWNER_OF, BRANCH_OF, DIRECT_PARENT, ULTIMATE_PARENT. Standardize these role codes for display and filtering. |

Rules
- Place REL_POINTER on the source record for each disclosed relationship to a target record.
- Provide `REL_POINTER_DOMAIN` and `REL_POINTER_KEY` to point to the target's REL_ANCHOR; include a clear `REL_POINTER_ROLE`.
- Represent multiple relationships by adding multiple REL_POINTER objects in FEATURES (one per relationship).
- Do not mix REL_POINTER and REL_ANCHOR attributes in the same feature object.

Examples
```json
{
  "FEATURES": [
    { "REL_POINTER_DOMAIN": "CUSTOMERS", "REL_POINTER_KEY": "ACME-1001", "REL_POINTER_ROLE": "EMPLOYED_BY" }
  ]
}
```

- ❌ Incorrect (mixing REL_ANCHOR and REL_POINTER attributes in the same object)
```json
{
  "FEATURES": [
    { "REL_POINTER_DOMAIN": "CUSTOMERS", "REL_POINTER_KEY": "ACME-1001", "REL_POINTER_ROLE": "EMPLOYED_BY", "REL_ANCHOR_DOMAIN": "CUSTOMERS", "REL_ANCHOR_KEY": "ACME-1001" }
  ]
}
```

### Feature: TRUSTED_ID
Category: Control

Two records with the same TRUSTED_ID type and number will absolutely force records together even if all their other features are different.  Conversely, two records with a different TRUSTED_ID number of the same type will be forced apart even if all their other features are the same.

This feature can be used by data stewards to manually force records together or apart.  It can also be used for a source system identifier that is so trusted you want it to never be overruled by Senzing.

| Attribute | Example | Guidance |
| --- | --- | --- |
| TRUSTED_ID_TYPE | STEWARD | Short code for the identifier domain/system (e.g., STEWARD, MASTER_ID). |
| TRUSTED_ID_NUMBER | 1234-12345 | The identifier value shared by records that must resolve together. |

Example
```json
{
  "FEATURES": [
    { "TRUSTED_ID_TYPE": "STEWARD", "TRUSTED_ID_NUMBER": "1234-12345" }
  ]
}
```

# Additional configuration

Senzing comes pre-configured with all the features, attributes, and settings you will likely need to begin resolving persons and organizations immediately. The only configuration that really needs to be added is what you named your data sources.

Email support@senzing.com for assistance with custom features.

## How to add a data source

In your Senzing project's bin directory is an application called sz_configtool. Adding a new data source is as simple as registering the code you want to use for it.

```console
sz_configtool.py

Welcome to the Senzing configuration tool! Type help or ? to list commands

(szcfg) addDataSource CUSTOMERS

Data source successfully added!

(szcfg) save

Are you certain you wish to proceed and save changes? (y/n) y

Configuration changes saved!
```
