**File Type:** xml
**Root Records:** 8
**List Elements (Tables):** 38
**Total Fields:** 424

**XML Namespaces:**
- Default: `https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/ADVANCED_XML`

*Note: Generated code must handle these namespaces when parsing XML.*

**Data Elements (All Lists):**
- Location: 21,816 records
  - Location.LocationPart: 47,370 records
    - Location.LocationPart.LocationPartValue: 48,131 records
  - Location.FeatureVersionReference: 28,036 records
- IDRegDocument: 20,278 records
  - IDRegDocument.DocumentDate: 1,527 records
- SanctionsEntry: 17,969 records
  - SanctionsEntry.SanctionsMeasure: 39,492 records
  - SanctionsEntry.EntryEvent: 19,862 records
- DistinctParty: 17,815 records
  - DistinctParty.Profile.Identity.NamePartGroups.MasterNamePartGroup: 76,016 records
  - DistinctParty.Profile.Feature: 73,232 records
  - DistinctParty.Profile.Identity.Alias: 41,859 records
    - DistinctParty.Profile.Identity.Alias.DocumentedName: 47,473 records
      - DistinctParty.Profile.Identity.Alias.DocumentedName.DocumentedNamePart: 76,016 records
- ProfileRelationship: 7,731 records
- DetailReferenceValues.DetailReference: 205 records
- AreaCodeValues.AreaCode: 186 records
- CountryValues.Country: 186 records
- IDRegDocTypeValues.IDRegDocType: 105 records
- LegalBasisValues.LegalBasis: 83 records
- SanctionsProgramValues.SanctionsProgram: 74 records
- FeatureTypeValues.FeatureType: 72 records
- ScriptValues.Script: 12 records
- NamePartTypeValues.NamePartType: 10 records
- RelationTypeValues.RelationType: 10 records
- SanctionsTypeValues.SanctionsType: 10 records
- LocPartTypeValues.LocPartType: 8 records
- PartyTypeValues.PartyType: 5 records
- AliasTypeValues.AliasType: 4 records
- DetailTypeValues.DetailType: 4 records
- ListValues.List: 4 records
- PartySubTypeValues.PartySubType: 4 records
- RelationQualityValues.RelationQuality: 4 records
- ReliabilityValues.Reliability: 4 records
- DocNameStatusValues.DocNameStatus: 2 records
- IDRegDocDateTypeValues.IDRegDocDateType: 2 records
- ValidityValues.Validity: 2 records

## Document: sdn_advanced

### Fields

| # | Field Name | Type | Records | Pop % | Unique % | Table Context | Sample 1 | Sample 2 | Sample 3 | Sample 4 | Sample 5 |
|---|------------|------|---------|-------|----------|---------------|----------|----------|----------|----------|----------|
| 1 | CalendarTypeID | str | 1 | 12.5% | 100.0% | root (8) | 1 (1) |  |  |  |  |
| 2 | Year | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 3 | Year.text | str | 1 | 12.5% | 100.0% | root (8) | 2025 (1) |  |  |  |  |
| 4 | Month | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 5 | Month.text | str | 1 | 12.5% | 100.0% | root (8) | 8 (1) |  |  |  |  |
| 6 | Day | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 7 | Day.text | str | 1 | 12.5% | 100.0% | root (8) | 27 (1) |  |  |  |  |
| 8 | AliasTypeValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 9 | AliasTypeValues.AliasType | list | 1 |  |  | root (8) | 4 items (1) |  |  |  |  |
| 10 | AliasTypeValues.AliasType.ID | str | 4 | 100.0% | 100.0% | AliasType (4) | 1400 (1) | 1401 (1) | 1402 (1) | 1403 (1) |  |
| 11 | AliasTypeValues.AliasType.text | str | 4 | 100.0% | 100.0% | AliasType (4) | A.K.A. (1) | F.K.A. (1) | N.K.A. (1) | Name (1) |  |
| 12 | AreaCodeValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 13 | AreaCodeValues.AreaCode | list | 1 |  |  | root (8) | 186 items (1) |  |  |  |  |
| 14 | AreaCodeValues.AreaCode.ID | str | 186 | 100.0% | 100.0% | AreaCode (186) | 11029 (1) | 11030 (1) | 11031 (1) | 11033 (1) | 11034 (1) |
| 15 | AreaCodeValues.AreaCode.CountryID | str | 186 | 100.0% | 100.0% | AreaCode (186) | 11029 (1) | 11030 (1) | 11031 (1) | 11033 (1) | 11034 (1) |
| 16 | AreaCodeValues.AreaCode.Description | str | 186 | 100.0% | 100.0% | AreaCode (186) | Afghanistan (1) | Albania (1) | Algeria (1) | Angola (1) | Antigua and Barbuda (1) |
| 17 | AreaCodeValues.AreaCode.AreaCodeTypeID | str | 186 | 100.0% | 0.5% | AreaCode (186) | 1 (186) |  |  |  |  |
| 18 | AreaCodeValues.AreaCode.text | str | 180 | 96.8% | 100.0% | AreaCode (186) | AF (1) | AL (1) | DZ (1) | AO (1) | AG (1) |
| 19 | AreaCodeTypeValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 20 | AreaCodeTypeValues.AreaCodeType | dict | 1 |  |  | root (8) | 2 items (1) |  |  |  |  |
| 21 | AreaCodeTypeValues.AreaCodeType.ID | str | 1 | 12.5% | 100.0% | root (8) | 1 (1) |  |  |  |  |
| 22 | AreaCodeTypeValues.AreaCodeType.text | str | 1 | 12.5% | 100.0% | root (8) | ISO 3166 (2) (1) |  |  |  |  |
| 23 | CalendarTypeValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 24 | CalendarTypeValues.CalendarType | dict | 1 |  |  | root (8) | 2 items (1) |  |  |  |  |
| 25 | CalendarTypeValues.CalendarType.ID | str | 1 | 12.5% | 100.0% | root (8) | 1 (1) |  |  |  |  |
| 26 | CalendarTypeValues.CalendarType.text | str | 1 | 12.5% | 100.0% | root (8) | Gregorian (1) |  |  |  |  |
| 27 | CountryValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 28 | CountryValues.Country | list | 1 |  |  | root (8) | 186 items (1) |  |  |  |  |
| 29 | CountryValues.Country.ID | str | 186 | 100.0% | 100.0% | Country (186) | 11029 (1) | 11030 (1) | 11031 (1) | 11033 (1) | 11034 (1) |
| 30 | CountryValues.Country.ISO2 | str | 180 | 96.8% | 100.0% | Country (186) | AF (1) | AL (1) | DZ (1) | AO (1) | AG (1) |
| 31 | CountryValues.Country.text | str | 186 | 100.0% | 100.0% | Country (186) | Afghanistan (1) | Albania (1) | Algeria (1) | Angola (1) | Antigua and Barbuda (1) |
| 32 | CountryRelevanceValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 33 | CountryRelevanceValues.CountryRelevance | dict | 1 |  |  | root (8) | 2 items (1) |  |  |  |  |
| 34 | CountryRelevanceValues.CountryRelevance.ID | str | 1 | 12.5% | 100.0% | root (8) | 1413 (1) |  |  |  |  |
| 35 | CountryRelevanceValues.CountryRelevance.text | str | 1 | 12.5% | 100.0% | root (8) | PRIMARY (1) |  |  |  |  |
| 36 | DecisionMakingBodyValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 37 | DecisionMakingBodyValues.DecisionMakingBody | dict | 1 |  |  | root (8) | 3 items (1) |  |  |  |  |
| 38 | DecisionMakingBodyValues.DecisionMakingBody.ID | str | 1 | 12.5% | 100.0% | root (8) | 1 (1) |  |  |  |  |
| 39 | DecisionMakingBodyValues.DecisionMakingBody.OrganisationID | str | 1 | 12.5% | 100.0% | root (8) | 1 (1) |  |  |  |  |
| 40 | DecisionMakingBodyValues.DecisionMakingBody.text | str | 1 | 12.5% | 100.0% | root (8) | United States Treasury Department (1) |  |  |  |  |
| 41 | DetailReferenceValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 42 | DetailReferenceValues.DetailReference | list | 1 |  |  | root (8) | 205 items (1) |  |  |  |  |
| 43 | DetailReferenceValues.DetailReference.ID | str | 205 | 100.0% | 100.0% | DetailReference (205) | 702 (1) | 703 (1) | 704 (1) | 705 (1) | 91272 (1) |
| 44 | DetailReferenceValues.DetailReference.text | str | 205 | 100.0% | 98.0% | DetailReference (205) | General Cargo (2) | Landing Craft (2) | Passenger (2) | Roll-on Roll-off (2) | Bulk Carrier (1) |
| 45 | DetailTypeValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 46 | DetailTypeValues.DetailType | list | 1 |  |  | root (8) | 4 items (1) |  |  |  |  |
| 47 | DetailTypeValues.DetailType.ID | str | 4 | 100.0% | 100.0% | DetailType (4) | 1430 (1) | 1431 (1) | 1432 (1) | 1433 (1) |  |
| 48 | DetailTypeValues.DetailType.text | str | 4 | 100.0% | 100.0% | DetailType (4) | DATE (1) | LOOKUP (1) | TEXT (1) | COUNTRY (1) |  |
| 49 | DocNameStatusValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 50 | DocNameStatusValues.DocNameStatus | list | 1 |  |  | root (8) | 2 items (1) |  |  |  |  |
| 51 | DocNameStatusValues.DocNameStatus.ID | str | 2 | 100.0% | 100.0% | DocNameStatus (2) | 1 (1) | 2 (1) |  |  |  |
| 52 | DocNameStatusValues.DocNameStatus.text | str | 2 | 100.0% | 100.0% | DocNameStatus (2) | Primary Latin (1) | Others (1) |  |  |  |
| 53 | EntryEventTypeValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 54 | EntryEventTypeValues.EntryEventType | dict | 1 |  |  | root (8) | 2 items (1) |  |  |  |  |
| 55 | EntryEventTypeValues.EntryEventType.ID | str | 1 | 12.5% | 100.0% | root (8) | 1 (1) |  |  |  |  |
| 56 | EntryEventTypeValues.EntryEventType.text | str | 1 | 12.5% | 100.0% | root (8) | Created (1) |  |  |  |  |
| 57 | EntryLinkTypeValues | unk | 0 | 0.0% | 0% | root (8) |  |  |  |  |  |
| 58 | ExRefTypeValues | unk | 0 | 0.0% | 0% | root (8) |  |  |  |  |  |
| 59 | FeatureTypeValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 60 | FeatureTypeValues.FeatureType | list | 1 |  |  | root (8) | 72 items (1) |  |  |  |  |
| 61 | FeatureTypeValues.FeatureType.ID | str | 72 | 100.0% | 100.0% | FeatureType (72) | 1 (1) | 2 (1) | 3 (1) | 4 (1) | 5 (1) |
| 62 | FeatureTypeValues.FeatureType.FeatureTypeGroupID | str | 72 | 100.0% | 1.4% | FeatureType (72) | 1 (72) |  |  |  |  |
| 63 | FeatureTypeValues.FeatureType.text | str | 72 | 100.0% | 100.0% | FeatureType (72) | Vessel Call Sign (1) | VESSEL TYPE (1) | Vessel Flag (1) | Vessel Owner (1) | Vessel Tonnage (1) |
| 64 | FeatureTypeGroupValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 65 | FeatureTypeGroupValues.FeatureTypeGroup | dict | 1 |  |  | root (8) | 2 items (1) |  |  |  |  |
| 66 | FeatureTypeGroupValues.FeatureTypeGroup.ID | str | 1 | 12.5% | 100.0% | root (8) | 1 (1) |  |  |  |  |
| 67 | FeatureTypeGroupValues.FeatureTypeGroup.text | str | 1 | 12.5% | 100.0% | root (8) | Unknown (1) |  |  |  |  |
| 68 | IDRegDocDateTypeValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 69 | IDRegDocDateTypeValues.IDRegDocDateType | list | 1 |  |  | root (8) | 2 items (1) |  |  |  |  |
| 70 | IDRegDocDateTypeValues.IDRegDocDateType.ID | str | 2 | 100.0% | 100.0% | IDRegDocDateType (2) | 1480 (1) | 1481 (1) |  |  |  |
| 71 | IDRegDocDateTypeValues.IDRegDocDateType.text | str | 2 | 100.0% | 100.0% | IDRegDocDateType (2) | Issue Date (1) | Expiration Date (1) |  |  |  |
| 72 | IDRegDocTypeValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 73 | IDRegDocTypeValues.IDRegDocType | list | 1 |  |  | root (8) | 105 items (1) |  |  |  |  |
| 74 | IDRegDocTypeValues.IDRegDocType.ID | str | 105 | 100.0% | 100.0% | IDRegDocType (105) | 1570 (1) | 1571 (1) | 1572 (1) | 1573 (1) | 1574 (1) |
| 75 | IDRegDocTypeValues.IDRegDocType.text | str | 105 | 100.0% | 100.0% | IDRegDocType (105) | Cedula No. (1) | Passport (1) | SSN (1) | R.F.C. (1) | D.N.I. (1) |
| 76 | IdentityFeatureLinkTypeValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 77 | IdentityFeatureLinkTypeValues.IdentityFeatureLinkType | dict | 1 |  |  | root (8) | 2 items (1) |  |  |  |  |
| 78 | IdentityFeatureLinkTypeValues.IdentityFeatureLinkType.ID | str | 1 | 12.5% | 100.0% | root (8) | 1 (1) |  |  |  |  |
| 79 | IdentityFeatureLinkTypeValues.IdentityFeatureLinkType.text | str | 1 | 12.5% | 100.0% | root (8) | Unknown (1) |  |  |  |  |
| 80 | LegalBasisValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 81 | LegalBasisValues.LegalBasis | list | 1 |  |  | root (8) | 83 items (1) |  |  |  |  |
| 82 | LegalBasisValues.LegalBasis.ID | str | 83 | 100.0% | 100.0% | LegalBasis (83) | 1 (1) | 1807 (1) | 1810 (1) | 1811 (1) | 1817 (1) |
| 83 | LegalBasisValues.LegalBasis.LegalBasisShortRef | str | 83 | 100.0% | 100.0% | LegalBasis (83) | Unknown (1) | Executive Order 13566 (Libya) (1) | Executive Order 13441 (Lebanon) (1) | Executive Order 13382 (Non-proliferation) (1) | Executive Order 12947 (Terrorism) (1) |
| 84 | LegalBasisValues.LegalBasis.LegalBasisTypeID | str | 83 | 100.0% | 1.2% | LegalBasis (83) | 1 (83) |  |  |  |  |
| 85 | LegalBasisValues.LegalBasis.SanctionsProgramID | str | 83 | 100.0% | 1.2% | LegalBasis (83) | 1 (83) |  |  |  |  |
| 86 | LegalBasisValues.LegalBasis.text | str | 83 | 100.0% | 100.0% | LegalBasis (83) | Unknown (1) | Executive Order 13566 (Libya) (1) | Executive Order 13441 (Lebanon) (1) | Executive Order 13382 (Non-proliferation) (1) | Executive Order 12947 (Terrorism) (1) |
| 87 | LegalBasisTypeValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 88 | LegalBasisTypeValues.LegalBasisType | dict | 1 |  |  | root (8) | 2 items (1) |  |  |  |  |
| 89 | LegalBasisTypeValues.LegalBasisType.ID | str | 1 | 12.5% | 100.0% | root (8) | 1 (1) |  |  |  |  |
| 90 | LegalBasisTypeValues.LegalBasisType.text | str | 1 | 12.5% | 100.0% | root (8) | Unknown (1) |  |  |  |  |
| 91 | ListValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 92 | ListValues.List | list | 1 |  |  | root (8) | 4 items (1) |  |  |  |  |
| 93 | ListValues.List.ID | str | 4 | 100.0% | 100.0% | List (4) | 1550 (1) | 91243 (1) | 91507 (1) | 91512 (1) |  |
| 94 | ListValues.List.text | str | 4 | 100.0% | 100.0% | List (4) | SDN List (1) | Non-SDN Palestinian Legislative Council List (1) | Sectoral Sanctions Identifications List (1) | Consolidated List (1) |  |
| 95 | LocPartTypeValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 96 | LocPartTypeValues.LocPartType | list | 1 |  |  | root (8) | 8 items (1) |  |  |  |  |
| 97 | LocPartTypeValues.LocPartType.ID | str | 8 | 100.0% | 100.0% | LocPartType (8) | 1 (1) | 1450 (1) | 1451 (1) | 1452 (1) | 1453 (1) |
| 98 | LocPartTypeValues.LocPartType.text | str | 8 | 100.0% | 100.0% | LocPartType (8) | Unknown (1) | REGION (1) | ADDRESS1 (1) | ADDRESS2 (1) | ADDRESS3 (1) |
| 99 | LocPartValueStatusValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 100 | LocPartValueStatusValues.LocPartValueStatus | dict | 1 |  |  | root (8) | 2 items (1) |  |  |  |  |
| 101 | LocPartValueStatusValues.LocPartValueStatus.ID | str | 1 | 12.5% | 100.0% | root (8) | 1 (1) |  |  |  |  |
| 102 | LocPartValueStatusValues.LocPartValueStatus.text | str | 1 | 12.5% | 100.0% | root (8) | Main (1) |  |  |  |  |
| 103 | LocPartValueTypeValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 104 | LocPartValueTypeValues.LocPartValueType | dict | 1 |  |  | root (8) | 2 items (1) |  |  |  |  |
| 105 | LocPartValueTypeValues.LocPartValueType.ID | str | 1 | 12.5% | 100.0% | root (8) | 1 (1) |  |  |  |  |
| 106 | LocPartValueTypeValues.LocPartValueType.text | str | 1 | 12.5% | 100.0% | root (8) | Unknown (1) |  |  |  |  |
| 107 | NamePartTypeValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 108 | NamePartTypeValues.NamePartType | list | 1 |  |  | root (8) | 10 items (1) |  |  |  |  |
| 109 | NamePartTypeValues.NamePartType.ID | str | 10 | 100.0% | 100.0% | NamePartType (10) | 1520 (1) | 1521 (1) | 1522 (1) | 1523 (1) | 1524 (1) |
| 110 | NamePartTypeValues.NamePartType.text | str | 10 | 100.0% | 100.0% | NamePartType (10) | Last Name (1) | First Name (1) | Middle Name (1) | Maiden Name (1) | Aircraft Name (1) |
| 111 | OrganisationValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 112 | OrganisationValues.Organisation | dict | 1 |  |  | root (8) | 3 items (1) |  |  |  |  |
| 113 | OrganisationValues.Organisation.ID | str | 1 | 12.5% | 100.0% | root (8) | 1 (1) |  |  |  |  |
| 114 | OrganisationValues.Organisation.CountryID | str | 1 | 12.5% | 100.0% | root (8) | 11212 (1) |  |  |  |  |
| 115 | OrganisationValues.Organisation.text | str | 1 | 12.5% | 100.0% | root (8) | State (1) |  |  |  |  |
| 116 | PartySubTypeValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 117 | PartySubTypeValues.PartySubType | list | 1 |  |  | root (8) | 4 items (1) |  |  |  |  |
| 118 | PartySubTypeValues.PartySubType.ID | str | 4 | 100.0% | 100.0% | PartySubType (4) | 1 (1) | 2 (1) | 3 (1) | 4 (1) |  |
| 119 | PartySubTypeValues.PartySubType.PartyTypeID | str | 4 | 100.0% | 75.0% | PartySubType (4) | 4 (2) | 2 (1) | 1 (1) |  |  |
| 120 | PartySubTypeValues.PartySubType.text | str | 4 | 100.0% | 75.0% | PartySubType (4) | Unknown (2) | Vessel (1) | Aircraft (1) |  |  |
| 121 | PartyTypeValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 122 | PartyTypeValues.PartyType | list | 1 |  |  | root (8) | 5 items (1) |  |  |  |  |
| 123 | PartyTypeValues.PartyType.ID | str | 5 | 100.0% | 100.0% | PartyType (5) | 1 (1) | 2 (1) | 3 (1) | 4 (1) | 5 (1) |
| 124 | PartyTypeValues.PartyType.text | str | 5 | 100.0% | 100.0% | PartyType (5) | Individual (1) | Entity (1) | Location (1) | Transport (1) | Other Entity (1) |
| 125 | RelationQualityValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 126 | RelationQualityValues.RelationQuality | list | 1 |  |  | root (8) | 4 items (1) |  |  |  |  |
| 127 | RelationQualityValues.RelationQuality.ID | str | 4 | 100.0% | 100.0% | RelationQuality (4) | 1540 (1) | 1541 (1) | 1542 (1) | 1 (1) |  |
| 128 | RelationQualityValues.RelationQuality.text | str | 4 | 100.0% | 100.0% | RelationQuality (4) | High (1) | Low (1) | on OFAC's SDN list: (1) | Unknown (1) |  |
| 129 | RelationTypeValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 130 | RelationTypeValues.RelationType | list | 1 |  |  | root (8) | 10 items (1) |  |  |  |  |
| 131 | RelationTypeValues.RelationType.ID | str | 10 | 100.0% | 100.0% | RelationType (10) | 1555 (1) | 15001 (1) | 15002 (1) | 15003 (1) | 15004 (1) |
| 132 | RelationTypeValues.RelationType.Symmetrical | str | 10 | 100.0% | 10.0% | RelationType (10) | false (10) |  |  |  |  |
| 133 | RelationTypeValues.RelationType.text | str | 10 | 100.0% | 100.0% | RelationType (10) | Associate Of (1) | Providing support to (1) | Acting for or on behalf of (1) | Owned or Controlled By (1) | Family member of (1) |
| 134 | ReliabilityValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 135 | ReliabilityValues.Reliability | list | 1 |  |  | root (8) | 4 items (1) |  |  |  |  |
| 136 | ReliabilityValues.Reliability.ID | str | 4 | 100.0% | 100.0% | Reliability (4) | 1560 (1) | 1561 (1) | 91479 (1) | 1 (1) |  |
| 137 | ReliabilityValues.Reliability.text | str | 4 | 100.0% | 100.0% | Reliability (4) | Confirmed (1) | False (1) | Reported (1) | Unknown (1) |  |
| 138 | SanctionsProgramValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 139 | SanctionsProgramValues.SanctionsProgram | list | 1 |  |  | root (8) | 74 items (1) |  |  |  |  |
| 140 | SanctionsProgramValues.SanctionsProgram.ID | str | 74 | 100.0% | 100.0% | SanctionsProgram (74) | 1 (1) | 202 (1) | 203 (1) | 204 (1) | 205 (1) |
| 141 | SanctionsProgramValues.SanctionsProgram.SubsidiaryBodyID | str | 74 | 100.0% | 1.4% | SanctionsProgram (74) | 1 (74) |  |  |  |  |
| 142 | SanctionsProgramValues.SanctionsProgram.text | str | 74 | 100.0% | 100.0% | SanctionsProgram (74) | Unknown (1) | CUBA (1) | SDNTK (1) | FTO (1) | IRAN (1) |
| 143 | SanctionsTypeValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 144 | SanctionsTypeValues.SanctionsType | list | 1 |  |  | root (8) | 10 items (1) |  |  |  |  |
| 145 | SanctionsTypeValues.SanctionsType.ID | str | 10 | 100.0% | 100.0% | SanctionsType (10) | 1705 (1) | 1706 (1) | 91419 (1) | 91505 (1) | 91506 (1) |
| 146 | SanctionsTypeValues.SanctionsType.text | str | 10 | 100.0% | 100.0% | SanctionsType (10) | Block (1) | Reject (1) | NDAA Special Conditions (1) | 13662 Sectoral Directive 1 (1) | 13662 Sectoral Directive 2 (1) |
| 147 | ScriptValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 148 | ScriptValues.Script | list | 1 |  |  | root (8) | 12 items (1) |  |  |  |  |
| 149 | ScriptValues.Script.ID | str | 12 | 100.0% | 100.0% | Script (12) | 160 (1) | 230 (1) | 501 (1) | 502 (1) | 220 (1) |
| 150 | ScriptValues.Script.ScriptCode | str | 12 | 100.0% | 100.0% | Script (12) | Arab (1) | Armn (1) | Hans (1) | Hant (1) | Cyrl (1) |
| 151 | ScriptValues.Script.text | str | 12 | 100.0% | 100.0% | Script (12) | Arabic (1) | Armenian (1) | Chinese Simplified (1) | Chinese Traditional (1) | Cyrillic (1) |
| 152 | ScriptStatusValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 153 | ScriptStatusValues.ScriptStatus | dict | 1 |  |  | root (8) | 2 items (1) |  |  |  |  |
| 154 | ScriptStatusValues.ScriptStatus.ID | str | 1 | 12.5% | 100.0% | root (8) | 1 (1) |  |  |  |  |
| 155 | ScriptStatusValues.ScriptStatus.text | str | 1 | 12.5% | 100.0% | root (8) | Unknown (1) |  |  |  |  |
| 156 | SubsidiaryBodyValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 157 | SubsidiaryBodyValues.SubsidiaryBody | dict | 1 |  |  | root (8) | 4 items (1) |  |  |  |  |
| 158 | SubsidiaryBodyValues.SubsidiaryBody.ID | str | 1 | 12.5% | 100.0% | root (8) | 1 (1) |  |  |  |  |
| 159 | SubsidiaryBodyValues.SubsidiaryBody.Notional | str | 1 | 12.5% | 100.0% | root (8) | false (1) |  |  |  |  |
| 160 | SubsidiaryBodyValues.SubsidiaryBody.DecisionMakingBodyID | str | 1 | 12.5% | 100.0% | root (8) | 1 (1) |  |  |  |  |
| 161 | SubsidiaryBodyValues.SubsidiaryBody.text | str | 1 | 12.5% | 100.0% | root (8) | Office of Foreign Assets Control (1) |  |  |  |  |
| 162 | SupInfoTypeValues | unk | 0 | 0.0% | 0% | root (8) |  |  |  |  |  |
| 163 | TargetTypeValues | unk | 0 | 0.0% | 0% | root (8) |  |  |  |  |  |
| 164 | ValidityValues | dict | 1 |  |  | root (8) | 1 items (1) |  |  |  |  |
| 165 | ValidityValues.Validity | list | 1 |  |  | root (8) | 2 items (1) |  |  |  |  |
| 166 | ValidityValues.Validity.ID | str | 2 | 100.0% | 100.0% | Validity (2) | 1 (1) | 2 (1) |  |  |  |
| 167 | ValidityValues.Validity.text | str | 2 | 100.0% | 100.0% | Validity (2) | Valid (1) | Fraudulent (1) |  |  |  |
| 168 | Location | list | 1 |  |  | root (8) | 21816 items (1) |  |  |  |  |
| 169 | Location.ID | str | 21816 | 100.0% | 100.0% | Location (21816) | 1 (1) | 2 (1) | 25 (1) | 80 (1) | 81 (1) |
| 170 | Location.LocationAreaCode | dict | 21484 |  |  | Location (21816) | 1 items (21484) |  |  |  |  |
| 171 | Location.LocationAreaCode.AreaCodeID | str | 21484 | 98.5% | 0.8% | Location (21816) | 11171 (5825) | 11143 (1956) | 11109 (1912) | 11065 (1230) | 11291 (1147) |
| 172 | Location.LocationCountry | dict | 20344 |  |  | Location (21816) | 2 items (20344) |  |  |  |  |
| 173 | Location.LocationCountry.CountryID | str | 20344 | 93.3% | 0.9% | Location (21816) | 11171 (5825) | 11143 (1956) | 11109 (1912) | 11065 (1230) | 11210 (792) |
| 174 | Location.LocationCountry.CountryRelevanceID | str | 20344 | 93.3% | 0.0% | Location (21816) | 1413 (20344) |  |  |  |  |
| 175 | Location.FeatureVersionReference | list | 21636 |  |  | Location (21816) | 1 items (21505) | 2 items (15) | 4 items (9) | 3 items (8) | 7 items (8) |
| 176 | Location.FeatureVersionReference.FeatureVersionID | str | 28036 | 100.0% | 100.0% | FeatureVersionReference (28036) | 200001 (1) | 200002 (1) | 200025 (1) | 200080 (1) | 200081 (1) |
| 177 | Location.LocationPart | list | 17091 |  |  | Location (21816) | 2 items (6824) | 3 items (5656) | 4 items (3331) | 5 items (1127) | 6 items (153) |
| 178 | Location.LocationPart.LocPartTypeID | str | 47370 | 100.0% | 0.0% | LocationPart (47370) | 1454 (15658) | 1451 (13490) | 1456 (6776) | 1452 (4884) | 1455 (4633) |
| 179 | Location.LocationPart.LocationPartValue | list | 47370 |  |  | LocationPart (47370) | 5 items (46627) | 2 items (725) | 3 items (18) |  |  |
| 180 | Location.LocationPart.LocationPartValue.Primary | str | 48131 | 100.0% | 0.0% | LocationPartValue (48131) | true (47367) | false (764) |  |  |  |
| 181 | Location.LocationPart.LocationPartValue.LocPartValueTypeID | str | 48131 | 100.0% | 0.0% | LocationPartValue (48131) | 1 (48131) |  |  |  |  |
| 182 | Location.LocationPart.LocationPartValue.LocPartValueStatusID | str | 48131 | 100.0% | 0.0% | LocationPartValue (48131) | 1 (48131) |  |  |  |  |
| 183 | Location.LocationPart.LocationPartValue.Comment | dict | 738 |  |  | LocationPartValue (48131) | 1 items (738) |  |  |  |  |
| 184 | Location.LocationPart.LocationPartValue.Comment.text | str | 738 | 1.5% | 0.8% | LocationPartValue (48131) | Cyrillic (486) | Chinese Simplified (179) | Japanese (42) | Chinese Traditional (21) | Arabic (6) |
| 185 | Location.LocationPart.LocationPartValue.Value | dict | 48131 |  |  | LocationPartValue (48131) | 1 items (48131) |  |  |  |  |
| 186 | Location.LocationPart.LocationPartValue.Value.text | str | 48131 | 100.0% | 50.2% | LocationPartValue (48131) | Moscow (2127) | Tehran (1012) | Dubai (565) | Jalisco (467) | Hong Kong (455) |
| 187 | Location.IDRegDocumentReference | dict | 180 |  |  | Location (21816) | 1 items (180) |  |  |  |  |
| 188 | Location.IDRegDocumentReference.IDRegDocumentID | str | 180 | 0.8% | 100.0% | Location (21816) | 8264 (1) | 8311 (1) | 8438 (1) | 8835 (1) | 9049 (1) |
| 189 | IDRegDocument | list | 1 |  |  | root (8) | 20278 items (1) |  |  |  |  |
| 190 | IDRegDocument.ID | str | 20278 | 100.0% | 100.0% | IDRegDocument (20278) | 2 (1) | 3 (1) | 4 (1) | 5 (1) | 6 (1) |
| 191 | IDRegDocument.IDRegDocTypeID | str | 20278 | 100.0% | 0.5% | IDRegDocument (20278) | 1596 (4235) | 91761 (4197) | 1571 (2408) | 1584 (1478) | 1626 (1331) |
| 192 | IDRegDocument.IdentityID | str | 20278 | 100.0% | 60.5% | IDRegDocument (20278) | 7730 (13) | 1008 (11) | 21969 (10) | 6284 (9) | 16761 (9) |
| 193 | IDRegDocument.IssuedBy-CountryID | str | 17302 | 85.3% | 1.0% | IDRegDocument (20278) | 11171 (7686) | 11143 (1225) | 11109 (1171) | 11210 (653) | 11247 (580) |
| 194 | IDRegDocument.ValidityID | str | 20278 | 100.0% | 0.0% | IDRegDocument (20278) | 1 (19943) | 2 (335) |  |  |  |
| 195 | IDRegDocument.Comment | dict | 25 |  |  | IDRegDocument (20278) | 1 items (25) |  |  |  |  |
| 196 | IDRegDocument.Comment.text | str | 25 | 0.1% | 76.0% | IDRegDocument (20278) | Tazkera (3) | Expired (3) | IMO Number (3) | 1973 (1) | Alias ID card number (1) |
| 197 | IDRegDocument.IDRegistrationNo | dict | 20278 |  |  | IDRegDocument (20278) | 1 items (20278) |  |  |  |  |
| 198 | IDRegDocument.IDRegistrationNo.text | str | 20278 | 100.0% | 99.6% | IDRegDocument (20278) | 59536969 (3) | 6067015 (2) | 16215230 (2) | 29503761 (2) | 16209410 (2) |
| 199 | IDRegDocument.IssuingAuthority | dict | 76 |  |  | IDRegDocument (20278) | 1 items (76) |  |  |  |  |
| 200 | IDRegDocument.IssuingAuthority.text | str | 76 | 0.4% | 51.3% | IDRegDocument (20278) | OGRN (8) | INN (8) | International Maritime Organization (6) | Unified State Register of Legal Entities (5) | Russian National Classifier of Enterprises and Org (5) |
| 201 | IDRegDocument.DocumentedNameReference | dict | 20278 |  |  | IDRegDocument (20278) | 1 items (20278) |  |  |  |  |
| 202 | IDRegDocument.DocumentedNameReference.DocumentedNameID | str | 20278 | 100.0% | 60.6% | IDRegDocument (20278) | 17247 (13) | 1008 (11) | 41613 (10) | 6284 (9) | 33195 (9) |
| 203 | IDRegDocument.DocumentDate | list | 1189 |  |  | IDRegDocument (20278) | 2 items (1189) |  |  |  |  |
| 204 | IDRegDocument.DocumentDate.IDRegDocDateTypeID | str | 1527 | 100.0% | 0.1% | DocumentDate (1527) | 1481 (1046) | 1480 (481) |  |  |  |
| 205 | IDRegDocument.DocumentDate.DatePeriod | dict | 1527 |  |  | DocumentDate (1527) | 6 items (1527) |  |  |  |  |
| 206 | IDRegDocument.DocumentDate.DatePeriod.CalendarTypeID | str | 1527 | 100.0% | 0.1% | DocumentDate (1527) | 1 (1527) |  |  |  |  |
| 207 | IDRegDocument.DocumentDate.DatePeriod.YearFixed | str | 1527 | 100.0% | 0.1% | DocumentDate (1527) | false (1527) |  |  |  |  |
| 208 | IDRegDocument.DocumentDate.DatePeriod.MonthFixed | str | 1527 | 100.0% | 0.1% | DocumentDate (1527) | false (1527) |  |  |  |  |
| 209 | IDRegDocument.DocumentDate.DatePeriod.DayFixed | str | 1527 | 100.0% | 0.1% | DocumentDate (1527) | false (1527) |  |  |  |  |
| 210 | IDRegDocument.DocumentDate.DatePeriod.Start | dict | 1527 |  |  | DocumentDate (1527) | 6 items (1527) |  |  |  |  |
| 211 | IDRegDocument.DocumentDate.DatePeriod.Start.Approximate | str | 1527 | 100.0% | 0.1% | DocumentDate (1527) | false (1527) |  |  |  |  |
| 212 | IDRegDocument.DocumentDate.DatePeriod.Start.YearFixed | str | 1527 | 100.0% | 0.1% | DocumentDate (1527) | false (1527) |  |  |  |  |
| 213 | IDRegDocument.DocumentDate.DatePeriod.Start.MonthFixed | str | 1527 | 100.0% | 0.1% | DocumentDate (1527) | false (1527) |  |  |  |  |
| 214 | IDRegDocument.DocumentDate.DatePeriod.Start.DayFixed | str | 1527 | 100.0% | 0.1% | DocumentDate (1527) | false (1527) |  |  |  |  |
| 215 | IDRegDocument.DocumentDate.DatePeriod.Start.From | dict | 1527 |  |  | DocumentDate (1527) | 3 items (1527) |  |  |  |  |
| 216 | IDRegDocument.DocumentDate.DatePeriod.Start.From.Year | dict | 1527 |  |  | DocumentDate (1527) | 1 items (1527) |  |  |  |  |
| 217 | IDRegDocument.DocumentDate.DatePeriod.Start.From.Year.text | str | 1527 | 100.0% | 4.1% | DocumentDate (1527) | 2022 (82) | 2023 (80) | 2024 (76) | 2021 (73) | 2018 (71) |
| 218 | IDRegDocument.DocumentDate.DatePeriod.Start.From.Month | dict | 1527 |  |  | DocumentDate (1527) | 1 items (1527) |  |  |  |  |
| 219 | IDRegDocument.DocumentDate.DatePeriod.Start.From.Month.text | str | 1527 | 100.0% | 0.8% | DocumentDate (1527) | 5 (154) | 10 (147) | 9 (141) | 6 (137) | 3 (129) |
| 220 | IDRegDocument.DocumentDate.DatePeriod.Start.From.Day | dict | 1527 |  |  | DocumentDate (1527) | 1 items (1527) |  |  |  |  |
| 221 | IDRegDocument.DocumentDate.DatePeriod.Start.From.Day.text | str | 1527 | 100.0% | 2.0% | DocumentDate (1527) | 1 (74) | 28 (70) | 19 (66) | 12 (63) | 13 (60) |
| 222 | IDRegDocument.DocumentDate.DatePeriod.Start.To | dict | 1527 |  |  | DocumentDate (1527) | 3 items (1527) |  |  |  |  |
| 223 | IDRegDocument.DocumentDate.DatePeriod.Start.To.Year | dict | 1527 |  |  | DocumentDate (1527) | 1 items (1527) |  |  |  |  |
| 224 | IDRegDocument.DocumentDate.DatePeriod.Start.To.Year.text | str | 1527 | 100.0% | 4.1% | DocumentDate (1527) | 2022 (82) | 2023 (80) | 2024 (76) | 2021 (73) | 2018 (71) |
| 225 | IDRegDocument.DocumentDate.DatePeriod.Start.To.Month | dict | 1527 |  |  | DocumentDate (1527) | 1 items (1527) |  |  |  |  |
| 226 | IDRegDocument.DocumentDate.DatePeriod.Start.To.Month.text | str | 1527 | 100.0% | 0.8% | DocumentDate (1527) | 5 (154) | 10 (147) | 9 (141) | 6 (137) | 3 (129) |
| 227 | IDRegDocument.DocumentDate.DatePeriod.Start.To.Day | dict | 1527 |  |  | DocumentDate (1527) | 1 items (1527) |  |  |  |  |
| 228 | IDRegDocument.DocumentDate.DatePeriod.Start.To.Day.text | str | 1527 | 100.0% | 2.0% | DocumentDate (1527) | 1 (74) | 28 (70) | 19 (66) | 12 (63) | 13 (60) |
| 229 | IDRegDocument.DocumentDate.DatePeriod.End | dict | 1527 |  |  | DocumentDate (1527) | 6 items (1527) |  |  |  |  |
| 230 | IDRegDocument.DocumentDate.DatePeriod.End.Approximate | str | 1527 | 100.0% | 0.1% | DocumentDate (1527) | false (1527) |  |  |  |  |
| 231 | IDRegDocument.DocumentDate.DatePeriod.End.YearFixed | str | 1527 | 100.0% | 0.1% | DocumentDate (1527) | false (1527) |  |  |  |  |
| 232 | IDRegDocument.DocumentDate.DatePeriod.End.MonthFixed | str | 1527 | 100.0% | 0.1% | DocumentDate (1527) | false (1527) |  |  |  |  |
| 233 | IDRegDocument.DocumentDate.DatePeriod.End.DayFixed | str | 1527 | 100.0% | 0.1% | DocumentDate (1527) | false (1527) |  |  |  |  |
| 234 | IDRegDocument.DocumentDate.DatePeriod.End.From | dict | 1527 |  |  | DocumentDate (1527) | 3 items (1527) |  |  |  |  |
| 235 | IDRegDocument.DocumentDate.DatePeriod.End.From.Year | dict | 1527 |  |  | DocumentDate (1527) | 1 items (1527) |  |  |  |  |
| 236 | IDRegDocument.DocumentDate.DatePeriod.End.From.Year.text | str | 1527 | 100.0% | 4.1% | DocumentDate (1527) | 2022 (82) | 2023 (79) | 2024 (77) | 2021 (73) | 2018 (71) |
| 237 | IDRegDocument.DocumentDate.DatePeriod.End.From.Month | dict | 1527 |  |  | DocumentDate (1527) | 1 items (1527) |  |  |  |  |
| 238 | IDRegDocument.DocumentDate.DatePeriod.End.From.Month.text | str | 1527 | 100.0% | 0.8% | DocumentDate (1527) | 5 (154) | 10 (147) | 9 (141) | 6 (137) | 3 (129) |
| 239 | IDRegDocument.DocumentDate.DatePeriod.End.From.Day | dict | 1527 |  |  | DocumentDate (1527) | 1 items (1527) |  |  |  |  |
| 240 | IDRegDocument.DocumentDate.DatePeriod.End.From.Day.text | str | 1527 | 100.0% | 2.0% | DocumentDate (1527) | 28 (70) | 19 (66) | 12 (63) | 13 (60) | 14 (58) |
| 241 | IDRegDocument.DocumentDate.DatePeriod.End.To | dict | 1527 |  |  | DocumentDate (1527) | 3 items (1527) |  |  |  |  |
| 242 | IDRegDocument.DocumentDate.DatePeriod.End.To.Year | dict | 1527 |  |  | DocumentDate (1527) | 1 items (1527) |  |  |  |  |
| 243 | IDRegDocument.DocumentDate.DatePeriod.End.To.Year.text | str | 1527 | 100.0% | 4.1% | DocumentDate (1527) | 2022 (82) | 2023 (79) | 2024 (77) | 2021 (73) | 2018 (71) |
| 244 | IDRegDocument.DocumentDate.DatePeriod.End.To.Month | dict | 1527 |  |  | DocumentDate (1527) | 1 items (1527) |  |  |  |  |
| 245 | IDRegDocument.DocumentDate.DatePeriod.End.To.Month.text | str | 1527 | 100.0% | 0.8% | DocumentDate (1527) | 5 (154) | 10 (147) | 9 (141) | 6 (137) | 3 (129) |
| 246 | IDRegDocument.DocumentDate.DatePeriod.End.To.Day | dict | 1527 |  |  | DocumentDate (1527) | 1 items (1527) |  |  |  |  |
| 247 | IDRegDocument.DocumentDate.DatePeriod.End.To.Day.text | str | 1527 | 100.0% | 2.0% | DocumentDate (1527) | 28 (70) | 19 (66) | 12 (63) | 13 (60) | 14 (58) |
| 248 | IDRegDocument.IssuedIn-LocationID | str | 180 | 0.9% | 100.0% | IDRegDocument (20278) | 1008264 (1) | 1008311 (1) | 1008438 (1) | 1008835 (1) | 1009049 (1) |
| 249 | IDRegDocument.FeatureVersionReference | dict | 9 |  |  | IDRegDocument (20278) | 1 items (9) |  |  |  |  |
| 250 | IDRegDocument.FeatureVersionReference.FeatureVersionID | str | 9 | 0.0% | 88.9% | IDRegDocument (20278) | 4196 (2) | 28185 (1) | 28421 (1) | 28467 (1) | 36562 (1) |
| 251 | DistinctParty | list | 1 |  |  | root (8) | 17815 items (1) |  |  |  |  |
| 252 | DistinctParty.FixedRef | str | 17815 | 100.0% | 100.0% | DistinctParty (17815) | 36 (1) | 173 (1) | 306 (1) | 424 (1) | 475 (1) |
| 253 | DistinctParty.Comment | dict | 496 |  |  | DistinctParty (17815) | 1 items (496) |  |  |  |  |
| 254 | DistinctParty.Comment.text | str | 496 | 2.8% | 44.6% | DistinctParty (17815) | all offices worldwide (55) | ICTY indictee; (45) | For more information on directives, please visit t (41) | Member ETA; (28) | For more information on directives, please visit t (17) |
| 255 | DistinctParty.Profile | dict | 17815 |  |  | DistinctParty (17815) | 4 items (17813) | 3 items (2) |  |  |  |
| 256 | DistinctParty.Profile.ID | str | 17815 | 100.0% | 100.0% | DistinctParty (17815) | 36 (1) | 173 (1) | 306 (1) | 424 (1) | 475 (1) |
| 257 | DistinctParty.Profile.PartySubTypeID | str | 17815 | 100.0% | 0.0% | DistinctParty (17815) | 3 (8976) | 4 (7179) | 1 (1324) | 2 (336) |  |
| 258 | DistinctParty.Profile.Identity | dict | 17815 |  |  | DistinctParty (17815) | 6 items (17815) |  |  |  |  |
| 259 | DistinctParty.Profile.Identity.ID | str | 17815 | 100.0% | 100.0% | DistinctParty (17815) | 4375 (1) | 4310 (1) | 4314 (1) | 4322 (1) | 4330 (1) |
| 260 | DistinctParty.Profile.Identity.FixedRef | str | 17815 | 100.0% | 100.0% | DistinctParty (17815) | 36 (1) | 173 (1) | 306 (1) | 424 (1) | 475 (1) |
| 261 | DistinctParty.Profile.Identity.Primary | str | 17815 | 100.0% | 0.0% | DistinctParty (17815) | true (17815) |  |  |  |  |
| 262 | DistinctParty.Profile.Identity.False | str | 17815 | 100.0% | 0.0% | DistinctParty (17815) | false (17815) |  |  |  |  |
| 263 | DistinctParty.Profile.Identity.Alias | list | 17815 |  |  | DistinctParty (17815) | 5 items (8963) | 2 items (4387) | 3 items (2143) | 4 items (1159) | 6 items (359) |
| 264 | DistinctParty.Profile.Identity.Alias.FixedRef | str | 41859 | 100.0% | 42.6% | Alias (41859) | 10923 (96) | 7140 (51) | 10612 (47) | 7149 (43) | 4700 (40) |
| 265 | DistinctParty.Profile.Identity.Alias.AliasTypeID | str | 41859 | 100.0% | 0.0% | Alias (41859) | 1400 (23401) | 1403 (17815) | 1401 (625) | 1402 (18) |  |
| 266 | DistinctParty.Profile.Identity.Alias.Primary | str | 41859 | 100.0% | 0.0% | Alias (41859) | false (24044) | true (17815) |  |  |  |
| 267 | DistinctParty.Profile.Identity.Alias.LowQuality | str | 41859 | 100.0% | 0.0% | Alias (41859) | false (37623) | true (4236) |  |  |  |
| 268 | DistinctParty.Profile.Identity.Alias.DocumentedName | list | 41859 |  |  | Alias (41859) | 4 items (36326) | 2 items (5454) | 3 items (78) | 5 items (1) |  |
| 269 | DistinctParty.Profile.Identity.Alias.DocumentedName.ID | str | 47473 | 100.0% | 100.0% | DocumentedName (47473) | 13178 (1) | 4375 (1) | 12583 (1) | 4310 (1) | 12584 (1) |
| 270 | DistinctParty.Profile.Identity.Alias.DocumentedName.FixedRef | str | 47473 | 100.0% | 37.5% | DocumentedName (47473) | 10923 (96) | 7140 (51) | 10612 (47) | 7149 (43) | 4700 (40) |
| 271 | DistinctParty.Profile.Identity.Alias.DocumentedName.DocNameStatusID | str | 47473 | 100.0% | 0.0% | DocumentedName (47473) | 2 (29658) | 1 (17815) |  |  |  |
| 272 | DistinctParty.Profile.Identity.Alias.DocumentedName.DocumentedNamePart | list | 47473 |  |  | DocumentedName (47473) | 1 items (28098) | 2 items (10842) | 3 items (7946) | 4 items (551) | 5 items (26) |
| 273 | DistinctParty.Profile.Identity.Alias.DocumentedName.DocumentedNamePart.NamePartValue | dict | 76016 |  |  | DocumentedNamePart (76016) | 5 items (76016) |  |  |  |  |
| 274 | DistinctParty.Profile.Identity.Alias.DocumentedName.DocumentedNamePart.NamePartValue.NamePartGroupID | str | 76016 | 100.0% | 100.0% | DocumentedNamePart (76016) | 19387 (1) | 6700 (1) | 18519 (1) | 6625 (1) | 27627 (1) |
| 275 | DistinctParty.Profile.Identity.Alias.DocumentedName.DocumentedNamePart.NamePartValue.ScriptID | str | 76016 | 100.0% | 0.0% | DocumentedNamePart (76016) | 215 (66034) | 220 (7263) | 160 (1901) | 501 (479) | 502 (203) |
| 276 | DistinctParty.Profile.Identity.Alias.DocumentedName.DocumentedNamePart.NamePartValue.ScriptStatusID | str | 76016 | 100.0% | 0.0% | DocumentedNamePart (76016) | 1 (76016) |  |  |  |  |
| 277 | DistinctParty.Profile.Identity.Alias.DocumentedName.DocumentedNamePart.NamePartValue.Acronym | str | 76016 | 100.0% | 0.0% | DocumentedNamePart (76016) | false (76016) |  |  |  |  |
| 278 | DistinctParty.Profile.Identity.Alias.DocumentedName.DocumentedNamePart.NamePartValue.text | str | 76016 | 100.0% | 65.4% | DocumentedNamePart (76016) | Ali (344) | Muhammad (272) | Mohammad (216) | Vladimirovich (187) | Alexander (168) |
| 279 | DistinctParty.Profile.Identity.NamePartGroups | dict | 17815 |  |  | DistinctParty (17815) | 1 items (17815) |  |  |  |  |
| 280 | DistinctParty.Profile.Identity.NamePartGroups.MasterNamePartGroup | list | 17815 |  |  | DistinctParty (17815) | 1 items (4466) | 2 items (3888) | 3 items (2105) | 4 items (1797) | 6 items (1695) |
| 281 | DistinctParty.Profile.Identity.NamePartGroups.MasterNamePartGroup.NamePartGroup | dict | 76016 |  |  | MasterNamePartGroup (76016) | 2 items (76016) |  |  |  |  |
| 282 | DistinctParty.Profile.Identity.NamePartGroups.MasterNamePartGroup.NamePartGroup.ID | str | 76016 | 100.0% | 100.0% | MasterNamePartGroup (76016) | 6700 (1) | 19387 (1) | 6625 (1) | 18519 (1) | 18521 (1) |
| 283 | DistinctParty.Profile.Identity.NamePartGroups.MasterNamePartGroup.NamePartGroup.NamePartTypeID | str | 76016 | 100.0% | 0.0% | MasterNamePartGroup (76016) | 1525 (24555) | 1520 (19760) | 1521 (19371) | 1522 (8450) | 1526 (1622) |
| 284 | DistinctParty.Profile.Feature | list | 17813 |  |  | DistinctParty (17815) | 2 items (3661) | 3 items (3609) | 4 items (3524) | 5 items (2719) | 6 items (2571) |
| 285 | DistinctParty.Profile.Feature.ID | str | 73232 | 100.0% | 100.0% | Feature (73232) | 150025 (1) | 150129 (1) | 150199 (1) | 150200 (1) | 150201 (1) |
| 286 | DistinctParty.Profile.Feature.FeatureTypeID | str | 73232 | 100.0% | 0.1% | Feature (73232) | 25 (21484) | 504 (11051) | 8 (7863) | 10 (5370) | 224 (5000) |
| 287 | DistinctParty.Profile.Feature.FeatureVersion | dict | 73232 |  |  | Feature (73232) | 4 items (55660) | 5 items (17572) |  |  |  |
| 288 | DistinctParty.Profile.Feature.FeatureVersion.ID | str | 73232 | 100.0% | 100.0% | Feature (73232) | 200025 (1) | 200129 (1) | 200199 (1) | 200200 (1) | 200201 (1) |
| 289 | DistinctParty.Profile.Feature.FeatureVersion.ReliabilityID | str | 73232 | 100.0% | 0.0% | Feature (73232) | 1 (68753) | 1560 (3850) | 91479 (619) | 1561 (10) |  |
| 290 | DistinctParty.Profile.Feature.FeatureVersion.Comment | dict | 47 |  |  | Feature (73232) | 1 items (47) |  |  |  |  |
| 291 | DistinctParty.Profile.Feature.FeatureVersion.Comment.text | str | 47 | 0.1% | 80.9% | Feature (73232) | No associated forks. (5) | (NIV) (2) | This address is also associated with BCH and BSV f (2) | No forks. (2) | Fecha de Ingreso (2) |
| 292 | DistinctParty.Profile.Feature.FeatureVersion.VersionLocation | dict | 28036 |  |  | Feature (73232) | 1 items (28036) |  |  |  |  |
| 293 | DistinctParty.Profile.Feature.FeatureVersion.VersionLocation.LocationID | str | 28036 | 38.3% | 77.2% | Feature (73232) | 186171 (1928) | 186143 (660) | 186109 (585) | 186065 (193) | 186066 (171) |
| 294 | DistinctParty.Profile.Feature.FeatureVersion.VersionDetail | dict | 51748 |  |  | Feature (73232) | 2 items (34176) | 1 items (17572) |  |  |  |
| 295 | DistinctParty.Profile.Feature.FeatureVersion.VersionDetail.DetailTypeID | str | 51748 | 70.7% | 0.0% | Feature (73232) | 1431 (22239) | 1432 (11937) | 1430 (11020) | 1433 (6552) |  |
| 296 | DistinctParty.Profile.Feature.FeatureVersion.VersionDetail.text | str | 11937 | 16.3% | 60.1% | Feature (73232) | Member of the State Duma of the Federal Assembly o (446) | Russia (293) | Panama (219) | Iran (213) | Moscow, Russia (170) |
| 297 | DistinctParty.Profile.Feature.FeatureVersion.VersionDetail.DetailReferenceID | str | 22239 | 30.4% | 0.9% | Feature (73232) | 92764 (6397) | 91526 (4392) | 92084 (2819) | 91473 (2292) | 92077 (968) |
| 298 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod | dict | 11020 |  |  | Feature (73232) | 6 items (11020) |  |  |  |  |
| 299 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.CalendarTypeID | str | 11020 | 15.0% | 0.0% | Feature (73232) | 1 (11020) |  |  |  |  |
| 300 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.YearFixed | str | 11020 | 15.0% | 0.0% | Feature (73232) | false (11020) |  |  |  |  |
| 301 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.MonthFixed | str | 11020 | 15.0% | 0.0% | Feature (73232) | false (11020) |  |  |  |  |
| 302 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.DayFixed | str | 11020 | 15.0% | 0.0% | Feature (73232) | false (11020) |  |  |  |  |
| 303 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.Start | dict | 11020 |  |  | Feature (73232) | 6 items (11020) |  |  |  |  |
| 304 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.Start.Approximate | str | 11020 | 15.0% | 0.0% | Feature (73232) | false (10947) | true (73) |  |  |  |
| 305 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.Start.YearFixed | str | 11020 | 15.0% | 0.0% | Feature (73232) | false (11020) |  |  |  |  |
| 306 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.Start.MonthFixed | str | 11020 | 15.0% | 0.0% | Feature (73232) | false (11020) |  |  |  |  |
| 307 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.Start.DayFixed | str | 11020 | 15.0% | 0.0% | Feature (73232) | false (11020) |  |  |  |  |
| 308 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.Start.From | dict | 11020 |  |  | Feature (73232) | 3 items (11020) |  |  |  |  |
| 309 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.Start.From.Year | dict | 11020 |  |  | Feature (73232) | 1 items (11020) |  |  |  |  |
| 310 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.Start.From.Year.text | str | 11020 | 15.0% | 1.0% | Feature (73232) | 2022 (288) | 1964 (274) | 1970 (248) | 1969 (236) | 1967 (235) |
| 311 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.Start.From.Month | dict | 11020 |  |  | Feature (73232) | 1 items (11020) |  |  |  |  |
| 312 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.Start.From.Month.text | str | 11020 | 15.0% | 0.1% | Feature (73232) | 1 (2543) | 3 (898) | 9 (843) | 7 (794) | 12 (789) |
| 313 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.Start.From.Day | dict | 11020 |  |  | Feature (73232) | 1 items (11020) |  |  |  |  |
| 314 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.Start.From.Day.text | str | 11020 | 15.0% | 0.3% | Feature (73232) | 1 (2268) | 21 (346) | 15 (345) | 20 (334) | 23 (333) |
| 315 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.Start.To | dict | 11020 |  |  | Feature (73232) | 3 items (11020) |  |  |  |  |
| 316 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.Start.To.Year | dict | 11020 |  |  | Feature (73232) | 1 items (11020) |  |  |  |  |
| 317 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.Start.To.Year.text | str | 11020 | 15.0% | 1.0% | Feature (73232) | 2022 (288) | 1964 (274) | 1970 (248) | 1969 (236) | 1967 (235) |
| 318 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.Start.To.Month | dict | 11020 |  |  | Feature (73232) | 1 items (11020) |  |  |  |  |
| 319 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.Start.To.Month.text | str | 11020 | 15.0% | 0.1% | Feature (73232) | 1 (2467) | 3 (898) | 12 (865) | 9 (843) | 7 (794) |
| 320 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.Start.To.Day | dict | 11020 |  |  | Feature (73232) | 1 items (11020) |  |  |  |  |
| 321 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.Start.To.Day.text | str | 11020 | 15.0% | 0.3% | Feature (73232) | 1 (2186) | 21 (346) | 15 (345) | 20 (334) | 23 (333) |
| 322 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.End | dict | 11020 |  |  | Feature (73232) | 6 items (11020) |  |  |  |  |
| 323 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.End.Approximate | str | 11020 | 15.0% | 0.0% | Feature (73232) | false (10947) | true (73) |  |  |  |
| 324 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.End.YearFixed | str | 11020 | 15.0% | 0.0% | Feature (73232) | false (11020) |  |  |  |  |
| 325 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.End.MonthFixed | str | 11020 | 15.0% | 0.0% | Feature (73232) | false (11020) |  |  |  |  |
| 326 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.End.DayFixed | str | 11020 | 15.0% | 0.0% | Feature (73232) | false (11020) |  |  |  |  |
| 327 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.End.From | dict | 11020 |  |  | Feature (73232) | 3 items (11020) |  |  |  |  |
| 328 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.End.From.Year | dict | 11020 |  |  | Feature (73232) | 1 items (11020) |  |  |  |  |
| 329 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.End.From.Year.text | str | 11020 | 15.0% | 1.0% | Feature (73232) | 2022 (288) | 1964 (277) | 1970 (245) | 1969 (242) | 1967 (234) |
| 330 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.End.From.Month | dict | 11020 |  |  | Feature (73232) | 1 items (11020) |  |  |  |  |
| 331 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.End.From.Month.text | str | 11020 | 15.0% | 0.1% | Feature (73232) | 12 (2329) | 1 (1003) | 3 (896) | 9 (842) | 7 (794) |
| 332 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.End.From.Day | dict | 11020 |  |  | Feature (73232) | 1 items (11020) |  |  |  |  |
| 333 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.End.From.Day.text | str | 11020 | 15.0% | 0.3% | Feature (73232) | 31 (1827) | 1 (616) | 15 (345) | 21 (340) | 20 (338) |
| 334 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.End.To | dict | 11020 |  |  | Feature (73232) | 3 items (11020) |  |  |  |  |
| 335 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.End.To.Year | dict | 11020 |  |  | Feature (73232) | 1 items (11020) |  |  |  |  |
| 336 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.End.To.Year.text | str | 11020 | 15.0% | 1.0% | Feature (73232) | 2022 (288) | 1964 (277) | 1970 (245) | 1969 (242) | 1967 (234) |
| 337 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.End.To.Month | dict | 11020 |  |  | Feature (73232) | 1 items (11020) |  |  |  |  |
| 338 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.End.To.Month.text | str | 11020 | 15.0% | 0.1% | Feature (73232) | 12 (2405) | 1 (927) | 3 (896) | 9 (842) | 7 (794) |
| 339 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.End.To.Day | dict | 11020 |  |  | Feature (73232) | 1 items (11020) |  |  |  |  |
| 340 | DistinctParty.Profile.Feature.FeatureVersion.DatePeriod.End.To.Day.text | str | 11020 | 15.0% | 0.3% | Feature (73232) | 31 (1908) | 1 (534) | 15 (345) | 21 (340) | 20 (338) |
| 341 | DistinctParty.Profile.Feature.IdentityReference | dict | 73232 |  |  | Feature (73232) | 2 items (73232) |  |  |  |  |
| 342 | DistinctParty.Profile.Feature.IdentityReference.IdentityID | str | 73232 | 100.0% | 24.3% | Feature (73232) | 27840 (123) | 44520 (62) | 35045 (56) | 28694 (53) | 31217 (49) |
| 343 | DistinctParty.Profile.Feature.IdentityReference.IdentityFeatureLinkTypeID | str | 73232 | 100.0% | 0.0% | Feature (73232) | 1 (73232) |  |  |  |  |
| 344 | ProfileRelationship | list | 1 |  |  | root (8) | 7731 items (1) |  |  |  |  |
| 345 | ProfileRelationship.ID | str | 7731 | 100.0% | 100.0% | ProfileRelationship (7731) | 1 (1) | 2 (1) | 11 (1) | 12 (1) | 13 (1) |
| 346 | ProfileRelationship.From-ProfileID | str | 7731 | 100.0% | 92.9% | ProfileRelationship (7731) | 13377 (16) | 21031 (15) | 23883 (14) | 20251 (12) | 18108 (10) |
| 347 | ProfileRelationship.To-ProfileID | str | 7731 | 100.0% | 27.4% | ProfileRelationship (7731) | 15117 (132) | 10465 (126) | 25396 (124) | 4697 (104) | 8759 (98) |
| 348 | ProfileRelationship.RelationTypeID | str | 7731 | 100.0% | 0.1% | ProfileRelationship (7731) | 15003 (3475) | 15001 (1470) | 15002 (1276) | 92122 (865) | 91725 (369) |
| 349 | ProfileRelationship.RelationQualityID | str | 7731 | 100.0% | 0.1% | ProfileRelationship (7731) | 1 (7337) | 1540 (366) | 1542 (26) | 1541 (2) |  |
| 350 | ProfileRelationship.Former | str | 7731 | 100.0% | 0.0% | ProfileRelationship (7731) | false (7731) |  |  |  |  |
| 351 | ProfileRelationship.SanctionsEntryID | str | 7731 | 100.0% | 92.9% | ProfileRelationship (7731) | 13377 (16) | 21031 (15) | 23883 (14) | 20251 (12) | 18108 (10) |
| 352 | ProfileRelationship.Comment | dict | 3 |  |  | ProfileRelationship (7731) | 1 items (3) |  |  |  |  |
| 353 | ProfileRelationship.Comment.text | str | 3 | 0.0% | 100.0% | ProfileRelationship (7731) | Deputy Wakagashira of the Sumiyoshi-kai Yakuza org (1) | Property Of (1) | Property of (1) |  |  |
| 354 | ProfileRelationship.DatePeriod | dict | 7 |  |  | ProfileRelationship (7731) | 7 items (4) | 6 items (3) |  |  |  |
| 355 | ProfileRelationship.DatePeriod.CalendarTypeID | str | 7 | 0.1% | 14.3% | ProfileRelationship (7731) | 1 (7) |  |  |  |  |
| 356 | ProfileRelationship.DatePeriod.YearFixed | str | 7 | 0.1% | 14.3% | ProfileRelationship (7731) | false (7) |  |  |  |  |
| 357 | ProfileRelationship.DatePeriod.MonthFixed | str | 7 | 0.1% | 14.3% | ProfileRelationship (7731) | false (7) |  |  |  |  |
| 358 | ProfileRelationship.DatePeriod.DayFixed | str | 7 | 0.1% | 14.3% | ProfileRelationship (7731) | false (7) |  |  |  |  |
| 359 | ProfileRelationship.DatePeriod.Comment | unk | 0 | 0.0% | 0% | ProfileRelationship (7731) |  |  |  |  |  |
| 360 | ProfileRelationship.DatePeriod.Start | dict | 7 |  |  | ProfileRelationship (7731) | 6 items (7) |  |  |  |  |
| 361 | ProfileRelationship.DatePeriod.Start.Approximate | str | 7 | 0.1% | 14.3% | ProfileRelationship (7731) | false (7) |  |  |  |  |
| 362 | ProfileRelationship.DatePeriod.Start.YearFixed | str | 7 | 0.1% | 14.3% | ProfileRelationship (7731) | false (7) |  |  |  |  |
| 363 | ProfileRelationship.DatePeriod.Start.MonthFixed | str | 7 | 0.1% | 14.3% | ProfileRelationship (7731) | false (7) |  |  |  |  |
| 364 | ProfileRelationship.DatePeriod.Start.DayFixed | str | 7 | 0.1% | 14.3% | ProfileRelationship (7731) | false (7) |  |  |  |  |
| 365 | ProfileRelationship.DatePeriod.Start.From | dict | 7 |  |  | ProfileRelationship (7731) | 3 items (7) |  |  |  |  |
| 366 | ProfileRelationship.DatePeriod.Start.From.Year | dict | 7 |  |  | ProfileRelationship (7731) | 1 items (7) |  |  |  |  |
| 367 | ProfileRelationship.DatePeriod.Start.From.Year.text | str | 7 | 0.1% | 85.7% | ProfileRelationship (7731) | 2019 (2) | 2015 (1) | 2018 (1) | 2020 (1) | 2021 (1) |
| 368 | ProfileRelationship.DatePeriod.Start.From.Month | dict | 7 |  |  | ProfileRelationship (7731) | 1 items (7) |  |  |  |  |
| 369 | ProfileRelationship.DatePeriod.Start.From.Month.text | str | 7 | 0.1% | 71.4% | ProfileRelationship (7731) | 9 (2) | 4 (2) | 1 (1) | 3 (1) | 6 (1) |
| 370 | ProfileRelationship.DatePeriod.Start.From.Day | dict | 7 |  |  | ProfileRelationship (7731) | 1 items (7) |  |  |  |  |
| 371 | ProfileRelationship.DatePeriod.Start.From.Day.text | str | 7 | 0.1% | 100.0% | ProfileRelationship (7731) | 19 (1) | 1 (1) | 17 (1) | 15 (1) | 16 (1) |
| 372 | ProfileRelationship.DatePeriod.Start.To | dict | 7 |  |  | ProfileRelationship (7731) | 3 items (7) |  |  |  |  |
| 373 | ProfileRelationship.DatePeriod.Start.To.Year | dict | 7 |  |  | ProfileRelationship (7731) | 1 items (7) |  |  |  |  |
| 374 | ProfileRelationship.DatePeriod.Start.To.Year.text | str | 7 | 0.1% | 85.7% | ProfileRelationship (7731) | 2019 (2) | 2015 (1) | 2018 (1) | 2020 (1) | 2021 (1) |
| 375 | ProfileRelationship.DatePeriod.Start.To.Month | dict | 7 |  |  | ProfileRelationship (7731) | 1 items (7) |  |  |  |  |
| 376 | ProfileRelationship.DatePeriod.Start.To.Month.text | str | 7 | 0.1% | 71.4% | ProfileRelationship (7731) | 9 (2) | 4 (2) | 1 (1) | 3 (1) | 6 (1) |
| 377 | ProfileRelationship.DatePeriod.Start.To.Day | dict | 7 |  |  | ProfileRelationship (7731) | 1 items (7) |  |  |  |  |
| 378 | ProfileRelationship.DatePeriod.Start.To.Day.text | str | 7 | 0.1% | 100.0% | ProfileRelationship (7731) | 19 (1) | 31 (1) | 17 (1) | 15 (1) | 16 (1) |
| 379 | ProfileRelationship.DatePeriod.End | dict | 4 |  |  | ProfileRelationship (7731) | 6 items (4) |  |  |  |  |
| 380 | ProfileRelationship.DatePeriod.End.Approximate | str | 4 | 0.1% | 25.0% | ProfileRelationship (7731) | false (4) |  |  |  |  |
| 381 | ProfileRelationship.DatePeriod.End.YearFixed | str | 4 | 0.1% | 25.0% | ProfileRelationship (7731) | false (4) |  |  |  |  |
| 382 | ProfileRelationship.DatePeriod.End.MonthFixed | str | 4 | 0.1% | 25.0% | ProfileRelationship (7731) | false (4) |  |  |  |  |
| 383 | ProfileRelationship.DatePeriod.End.DayFixed | str | 4 | 0.1% | 25.0% | ProfileRelationship (7731) | false (4) |  |  |  |  |
| 384 | ProfileRelationship.DatePeriod.End.From | dict | 4 |  |  | ProfileRelationship (7731) | 3 items (4) |  |  |  |  |
| 385 | ProfileRelationship.DatePeriod.End.From.Year | dict | 4 |  |  | ProfileRelationship (7731) | 1 items (4) |  |  |  |  |
| 386 | ProfileRelationship.DatePeriod.End.From.Year.text | str | 4 | 0.1% | 100.0% | ProfileRelationship (7731) | 2020 (1) | 2019 (1) | 2018 (1) | 2021 (1) |  |
| 387 | ProfileRelationship.DatePeriod.End.From.Month | dict | 4 |  |  | ProfileRelationship (7731) | 1 items (4) |  |  |  |  |
| 388 | ProfileRelationship.DatePeriod.End.From.Month.text | str | 4 | 0.1% | 100.0% | ProfileRelationship (7731) | 4 (1) | 6 (1) | 9 (1) | 3 (1) |  |
| 389 | ProfileRelationship.DatePeriod.End.From.Day | dict | 4 |  |  | ProfileRelationship (7731) | 1 items (4) |  |  |  |  |
| 390 | ProfileRelationship.DatePeriod.End.From.Day.text | str | 4 | 0.1% | 100.0% | ProfileRelationship (7731) | 14 (1) | 27 (1) | 17 (1) | 16 (1) |  |
| 391 | ProfileRelationship.DatePeriod.End.To | dict | 4 |  |  | ProfileRelationship (7731) | 3 items (4) |  |  |  |  |
| 392 | ProfileRelationship.DatePeriod.End.To.Year | dict | 4 |  |  | ProfileRelationship (7731) | 1 items (4) |  |  |  |  |
| 393 | ProfileRelationship.DatePeriod.End.To.Year.text | str | 4 | 0.1% | 100.0% | ProfileRelationship (7731) | 2020 (1) | 2019 (1) | 2018 (1) | 2021 (1) |  |
| 394 | ProfileRelationship.DatePeriod.End.To.Month | dict | 4 |  |  | ProfileRelationship (7731) | 1 items (4) |  |  |  |  |
| 395 | ProfileRelationship.DatePeriod.End.To.Month.text | str | 4 | 0.1% | 100.0% | ProfileRelationship (7731) | 4 (1) | 6 (1) | 9 (1) | 3 (1) |  |
| 396 | ProfileRelationship.DatePeriod.End.To.Day | dict | 4 |  |  | ProfileRelationship (7731) | 1 items (4) |  |  |  |  |
| 397 | ProfileRelationship.DatePeriod.End.To.Day.text | str | 4 | 0.1% | 100.0% | ProfileRelationship (7731) | 14 (1) | 27 (1) | 17 (1) | 16 (1) |  |
| 398 | SanctionsEntry | list | 1 |  |  | root (8) | 17969 items (1) |  |  |  |  |
| 399 | SanctionsEntry.ID | str | 17969 | 100.0% | 100.0% | SanctionsEntry (17969) | 36 (1) | 173 (1) | 306 (1) | 424 (1) | 475 (1) |
| 400 | SanctionsEntry.ProfileID | str | 17969 | 100.0% | 99.1% | SanctionsEntry (17969) | 9647 (3) | 9659 (3) | 17013 (3) | 17015 (3) | 17016 (3) |
| 401 | SanctionsEntry.ListID | str | 17969 | 100.0% | 0.0% | SanctionsEntry (17969) | 1550 (17815) | 91512 (77) | 91507 (75) | 91243 (2) |  |
| 402 | SanctionsEntry.EntryEvent | list | 17969 |  |  | SanctionsEntry (17969) | 5 items (16284) | 2 items (1526) | 3 items (128) | 4 items (30) | 6 items (1) |
| 403 | SanctionsEntry.EntryEvent.ID | str | 19862 | 100.0% | 100.0% | EntryEvent (19862) | 36 (1) | 173 (1) | 306 (1) | 424 (1) | 475 (1) |
| 404 | SanctionsEntry.EntryEvent.EntryEventTypeID | str | 19862 | 100.0% | 0.0% | EntryEvent (19862) | 1 (19862) |  |  |  |  |
| 405 | SanctionsEntry.EntryEvent.LegalBasisID | str | 19862 | 100.0% | 0.4% | EntryEvent (19862) | 92049 (6542) | 1828 (2355) | 1 (1820) | 1811 (926) | 1849 (758) |
| 406 | SanctionsEntry.EntryEvent.Comment | unk | 0 | 0.0% | 0% | EntryEvent (19862) |  |  |  |  |  |
| 407 | SanctionsEntry.EntryEvent.Date | dict | 19862 |  |  | EntryEvent (19862) | 4 items (19862) |  |  |  |  |
| 408 | SanctionsEntry.EntryEvent.Date.CalendarTypeID | str | 19862 | 100.0% | 0.0% | EntryEvent (19862) | 1 (19862) |  |  |  |  |
| 409 | SanctionsEntry.EntryEvent.Date.Year | dict | 19862 |  |  | EntryEvent (19862) | 1 items (19862) |  |  |  |  |
| 410 | SanctionsEntry.EntryEvent.Date.Year.text | str | 19862 | 100.0% | 0.2% | EntryEvent (19862) | 2024 (3417) | 2023 (2721) | 2022 (2621) | 2025 (1846) | 2018 (1439) |
| 411 | SanctionsEntry.EntryEvent.Date.Month | dict | 19862 |  |  | EntryEvent (19862) | 1 items (19862) |  |  |  |  |
| 412 | SanctionsEntry.EntryEvent.Date.Month.text | str | 19862 | 100.0% | 0.1% | EntryEvent (19862) | 12 (2190) | 1 (1861) | 11 (1825) | 9 (1812) | 2 (1801) |
| 413 | SanctionsEntry.EntryEvent.Date.Day | dict | 19862 |  |  | EntryEvent (19862) | 1 items (19862) |  |  |  |  |
| 414 | SanctionsEntry.EntryEvent.Date.Day.text | str | 19862 | 100.0% | 0.2% | EntryEvent (19862) | 24 (1315) | 30 (1295) | 23 (1294) | 12 (1274) | 10 (1269) |
| 415 | SanctionsEntry.SanctionsMeasure | list | 17969 |  |  | SanctionsEntry (17969) | 2 items (15398) | 3 items (1748) | 4 items (692) | 5 items (109) | 6 items (17) |
| 416 | SanctionsEntry.SanctionsMeasure.ID | str | 39492 | 100.0% | 100.0% | SanctionsMeasure (39492) | 4716 (1) | 126005 (1) | 9029 (1) | 126014 (1) | 1616 (1) |
| 417 | SanctionsEntry.SanctionsMeasure.SanctionsTypeID | str | 39492 | 100.0% | 0.0% | SanctionsMeasure (39492) | 1 (21223) | 1705 (17963) | 91505 (150) | 92093 (53) | 91514 (42) |
| 418 | SanctionsEntry.SanctionsMeasure.DatePeriod | dict | 39492 |  |  | SanctionsMeasure (39492) | 4 items (39492) |  |  |  |  |
| 419 | SanctionsEntry.SanctionsMeasure.DatePeriod.CalendarTypeID | str | 39492 | 100.0% | 0.0% | SanctionsMeasure (39492) | 1 (39492) |  |  |  |  |
| 420 | SanctionsEntry.SanctionsMeasure.DatePeriod.YearFixed | str | 39492 | 100.0% | 0.0% | SanctionsMeasure (39492) | true (39492) |  |  |  |  |
| 421 | SanctionsEntry.SanctionsMeasure.DatePeriod.MonthFixed | str | 39492 | 100.0% | 0.0% | SanctionsMeasure (39492) | true (39492) |  |  |  |  |
| 422 | SanctionsEntry.SanctionsMeasure.DatePeriod.DayFixed | str | 39492 | 100.0% | 0.0% | SanctionsMeasure (39492) | true (39492) |  |  |  |  |
| 423 | SanctionsEntry.SanctionsMeasure.Comment | dict | 21223 |  |  | SanctionsMeasure (39492) | 1 items (21223) |  |  |  |  |
| 424 | SanctionsEntry.SanctionsMeasure.Comment.text | str | 21223 | 53.7% | 0.3% | SanctionsMeasure (39492) | RUSSIA-EO14024 (6545) | SDGT (2824) | SDNTK (1420) | IFSR (1323) | NPWMD (1058) |