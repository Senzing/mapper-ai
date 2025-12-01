**Total Schemas:** 6
**Total Fields:** 67

## Schema: nodes-addresses

**Record Count:** 402164
**Field Count:** 8

### Fields

| # | Field Name | Type | Records | Pop % | Unique % | Sample 1 | Sample 2 | Sample 3 |
|---|------------|------|---------|-------|----------|----------|----------|----------|
| 1 | node_id | str | 402164 | 100.0% | 100.0% | 24000001 (1) | 24000002 (1) | 24000003 (1) |
| 2 | address | str | 382225 | 95.0% | 98.7% | 2nd Floor (46) | 1st Floor (30) | 4th Floor (28) |
| 3 | name | str | 223408 | 55.6% | 99.1% |  PINFOLD STREET (34) |  HIGH STREET (32) |  ST. MICHAEL (31) |
| 4 | countries | str | 278437 | 69.2% | 0.6% | China (32492) | Hong Kong (28248) | United States (24350) |
| 5 | country_codes | str | 278464 | 69.2% | 0.6% | CHN (32492) | HKG (28262) | USA (24366) |
| 6 | sourceID | str | 401805 | 99.9% | 0.4% | Paradise Papers - Malta corporate registry (121801) | Panama Papers (93442) | Paradise Papers - Appleby (59169) |
| 7 | valid_until | str | 401091 | 99.7% | 0.4% | Malta corporate registry data is current through 2 (121801) | The Panama Papers  data is current through 2015 (93442) | Appleby data is current through 2014 (59169) |
| 8 | note | str | 2957 | 0.7% | 28.1% | On 8th of February 2024 ICIJ reclassified this add (352) | Paradise Papers - Malta corporate registry (339) |  ST. MICHAEL (189) |

## Schema: nodes-entities

**Record Count:** 814344
**Field Count:** 21

### Fields

| # | Field Name | Type | Records | Pop % | Unique % | Sample 1 | Sample 2 | Sample 3 |
|---|------------|------|---------|-------|----------|----------|----------|----------|
| 1 | node_id | str | 814344 | 100.0% | 100.0% | 10000001 (1) | 10000002 (1) | 10000003 (1) |
| 2 | name | str | 814315 | 100.0% | 96.0% | DE PALM TOURS N.V. - DE PALM TOURS (19) | RENTCAR N.V. - HERTZ (13) | KM BM-C-SEVEN LTD. (12) |
| 3 | original_name | str | 389534 | 47.8% | 94.7% | KM BM-C-SEVEN LTD. (12) |  S.A." (8) | POSITUM TWELVE LIMITED (8) |
| 4 | former_name | str | 6849 | 0.8% | 99.2% | EXTRANJERA (25) | IN PROCESS TO CHANGE THE NAME. (4) | INTERNATIONAL (3) |
| 5 | jurisdiction | str | 806769 | 99.1% | 0.0% | BAH (209631) | BVI (167841) | MLT (83929) |
| 6 | jurisdiction_description | str | 806770 | 99.1% | 0.0% | Bahamas (209710) | British Virgin Islands (172389) | Malta (83939) |
| 7 | company_type | str | 138769 | 17.0% | 0.1% | Standard International Company (40072) | Standard Company under IBC Act (26210) | Business Company Limited by Shares (25130) |
| 8 | address | str | 299326 | 36.8% | 6.9% | Portcullis TrustNet Chambers P.O. Box 3444 Road To (33841) | ORION HOUSE SERVICES (HK) LIMITED ROOM 1401; 14/F. (7012) | Unitrust Corporate Services Ltd. John Humphries Ho (5697) |
| 9 | internal_id | str | 390189 | 47.9% | 88.1% |  Severnaya Tower (659) |  1 PO BOX 2049 1211 GENEVE 1; SWITZERLAND; *S.I.*" (100) |  AVENUE CHARLES DE GAULLE L-1653 LUXEMBOURG" (12) |
| 10 | incorporation_date | str | 788459 | 96.8% | 2.4% | 02-JAN-1998 (1376) | 04-JAN-1999 (1211) | 04-JAN-2000 (1155) |
| 11 | inactivation_date | str | 145482 | 17.9% | 4.8% | 02-NOV-2009 (1723) | 06-NOV-2015 (1475) | 03-MAY-2010 (1398) |
| 12 | struck_off_date | str | 344498 | 42.3% | 2.6% | 31-AUG-2002 (18575) | 01-JAN-2000 (15896) | 31-JAN-2001 (13233) |
| 13 | dorm_date | str | 20015 | 2.5% | 1.9% | 01-MAY-2009 (2210) | 01-NOV-2009 (2046) | 01-NOV-2008 (1752) |
| 14 | status | str | 357890 | 43.9% | 0.1% | Active (115717) | Defaulted (100049) | Dissolved (24031) |
| 15 | service_provider | str | 343401 | 42.2% | 0.0% | Mossack Fonseca (213491) | Portcullis Trustnet (61123) | Commonwealth Trust Limited (43714) |
| 16 | ibcRUC | str | 561957 | 69.0% | 90.9% | 0 (1447) | 30 (719) | 80 (676) |
| 17 | country_codes | str | 504612 | 62.0% | 0.2% | MLT (84331) | VGB (54932) | HKG (38906) |
| 18 | countries | str | 504991 | 62.0% | 0.2% | Malta (84331) | British Virgin Islands (54932) | Hong Kong (38906) |
| 19 | sourceID | str | 814336 | 100.0% | 0.0% | Panama Papers (213491) | Bahamas Leaks (175886) | Offshore Leaks (104837) |
| 20 | valid_until | str | 814131 | 100.0% | 0.1% | The Panama Papers data is current through 2015 (213491) | The Bahamas Leaks data is current through early 20 (175886) | The Offshore Leaks data is current through 2010 (104837) |
| 21 | note | str | 42622 | 5.2% | 0.6% | Closed date stands for Cancelled date. (18210) | This is not an offshore entity even though it was  (8982) | Closed date stands for dissolved date. (8204) |

## Schema: nodes-intermediaries

**Record Count:** 25629
**Field Count:** 10

### Fields

| # | Field Name | Type | Records | Pop % | Unique % | Sample 1 | Sample 2 | Sample 3 |
|---|------------|------|---------|-------|----------|----------|----------|----------|
| 1 | node_id | str | 25629 | 100.0% | 100.0% | 11000001 (1) | 11000002 (1) | 11000003 (1) |
| 2 | name | str | 25628 | 100.0% | 95.5% | HUTCHINSON GAYLE A. (62) | SMITH JENNIFER G. (55) | CARMICHAEL TREVOR A. (43) |
| 3 | status | str | 12621 | 49.2% | 0.1% | ACTIVE (7062) | SUSPENDED (4756) | UNRECOVERABLE ACCOUNTS (382) |
| 4 | internal_id | str | 14651 | 57.2% | 97.5% | 1004 (2) | 1 (2) | 10 (2) |
| 5 | address | str | 8643 | 33.7% | 100.0% | ATLANTIQUE (BVI) LIMITED 3RD FLOOR; 37 ESPLANADE C (2) | KANFER INVESTISSEMENTS S.A. 12, RUE JEAN ENGLING L (2) | CAÑON & CAÑON ASESORES TRIBUTARIOS CALLE 99 NO 7 A (2) |
| 6 | countries | str | 22013 | 85.9% | 1.3% | Hong Kong (4719) | United Kingdom (1530) | United States (1432) |
| 7 | country_codes | str | 22013 | 85.9% | 1.3% | HKG (4719) | GBR (1530) | USA (1432) |
| 8 | sourceID | str | 25629 | 100.0% | 0.1% | Panama Papers (14106) | Offshore Leaks (8387) | Pandora Papers - Alemán, Cordero, Galindo & Lee (A (1023) |
| 9 | valid_until | str | 25629 | 100.0% | 0.0% | The Panama Papers  data is current through 2015 (14106) | The Offshore Leaks data is current through 2010 (8387) | Barbados corporate registry data is current throug (974) |
| 10 | note | str | 12 | 0.0% | 66.7% | The Panama Papers  data is current through 2015 (4) | The name of this intermediary is displayed as it o (2) | Mr. Ignacio Mañe lawyer from M&O Abogados told ICI (1) |

## Schema: nodes-officers

**Record Count:** 771236
**Field Count:** 7

### Fields

| # | Field Name | Type | Records | Pop % | Unique % | Sample 1 | Sample 2 | Sample 3 |
|---|------------|------|---------|-------|----------|----------|----------|----------|
| 1 | node_id | str | 771236 | 100.0% | 100.0% | 12000001 (1) | 12000002 (1) | 12000003 (1) |
| 2 | name | str | 771177 | 100.0% | 69.8% | THE BEARER (70873) | EL PORTADOR (9325) | Bearer 1 (2655) |
| 3 | countries | str | 468902 | 60.8% | 0.9% | Malta (44990) | Not identified (39450) | China (38275) |
| 4 | country_codes | str | 470179 | 61.0% | 1.0% | MLT (44939) | XXX (39450) | CHN (38261) |
| 5 | sourceID | str | 771236 | 100.0% | 0.0% | Panama Papers (238400) | Paradise Papers - Barbados corporate registry (127912) | Offshore Leaks (107190) |
| 6 | valid_until | str | 770697 | 99.9% | 0.0% | The Panama Papers data is current through 2015 (238400) | Barbados corporate registry data is current throug (127912) | The Offshore Leaks data is current through 2010 (107190) |
| 7 | note | str | 3775 | 0.5% | 0.8% | Not all beneficiaries are aware of offshore trusts (3382) | Record manually added from leaked documents (123) | The individual was a minor at the time of the publ (114) |

## Schema: nodes-others

**Record Count:** 2989
**Field Count:** 13

### Fields

| # | Field Name | Type | Records | Pop % | Unique % | Sample 1 | Sample 2 | Sample 3 |
|---|------------|------|---------|-------|----------|----------|----------|----------|
| 1 | node_id | str | 2989 | 100.0% | 100.0% | 85004929 (1) | 85008443 (1) | 85008517 (1) |
| 2 | name | str | 2989 | 100.0% | 99.6% | Flipflop International Limited (3) | Shampaign Investments Limited (3) | ANTAM ENTERPRISES N.V. (2) |
| 3 | type | str | 888 | 29.7% | 0.3% | LIMITED LIABILITY COMPANY (881) | SOLE OWNERSHIP (4) | FOREIGN FORMED CORPORATION (3) |
| 4 | incorporation_date | str | 888 | 29.7% | 93.9% | 28-DEC-1989 (3) | 21-DEC-1995 (3) | 18-NOV-1996 (3) |
| 5 | struck_off_date | str | 45 | 1.5% | 86.7% | 31-DEC-2000 (3) | 31-DEC-2002 (2) | 24-JUL-2000 (2) |
| 6 | closed_date | str | 117 | 3.9% | 95.7% | 24-SEP-2009 (3) | 08-APR-2011 (2) | 03-MAY-2011 (2) |
| 7 | jurisdiction | str | 958 | 32.1% | 0.6% | AW (888) | VGB (62) | BLZ (3) |
| 8 | jurisdiction_description | str | 958 | 32.1% | 0.6% | Aruba (888) | British Virgin Islands (62) | Belize (3) |
| 9 | countries | str | 386 | 12.9% | 16.3% | Isle of Man (105) | Cayman Islands (79) | United Kingdom (26) |
| 10 | country_codes | str | 386 | 12.9% | 16.3% | IMN (105) | CYM (79) | GBR (26) |
| 11 | sourceID | str | 2989 | 100.0% | 0.2% | Paradise Papers - Appleby (2031) | Paradise Papers - Aruba corporate registry (888) | Pandora Papers - Trident Trust (49) |
| 12 | valid_until | str | 2989 | 100.0% | 0.3% | Appleby data is current through 2014 (2031) | Aruba corporate registry data is current through 2 (888) | Provider data is current through 2017 (35) |
| 13 | note | str | 117 | 3.9% | 1.7% | Closed date stands for Cancelled date. (90) | Closed date stands for Liquidation date. (27) |  |

## Schema: relationships

**Record Count:** 3339267
**Field Count:** 8

### Fields

| # | Field Name | Type | Records | Pop % | Unique % | Sample 1 | Sample 2 | Sample 3 |
|---|------------|------|---------|-------|----------|----------|----------|----------|
| 1 | node_id_start | str | 3339267 | 100.0% | 33.9% | 54662 (36373) | 230000018 (35359) | 23000136 (14902) |
| 2 | node_id_end | str | 3339267 | 100.0% | 39.6% | 236724 (37338) | 240000001 (11962) | 81027146 (9268) |
| 3 | rel_type | str | 3339267 | 100.0% | 0.0% | officer_of (1720357) | registered_address (832721) | intermediary_of (598546) |
| 4 | link | str | 3338878 | 100.0% | 0.0% | shareholder of (589938) | registered address (566910) | intermediary of (512797) |
| 5 | status | str | 174946 | 5.2% | 0.0% | Resigned (131441) | Appointed (43505) |  |
| 6 | start_date | str | 946705 | 28.4% | 2.6% | 31-DEC-1969 (1848) | 24-AUG-2010 (1176) | 24-JUL-1997 (660) |
| 7 | end_date | str | 268867 | 8.1% | 5.0% | 30-SEP-2012 (9663) | 29-DEC-2009 (852) | 15-NOV-2014 (811) |
| 8 | sourceID | str | 2820285 | 84.5% | 0.0% | Paradise Papers - Malta corporate registry (776335) | Panama Papers (674102) | Offshore Leaks (561393) |
