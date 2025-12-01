# Senzing Tools Reference Guide

This document provides concise command-line reference for Senzing tools used in the workshop environment. Each tool section covers: what it does, when to run it, the exact command AI should use, and how to interpret the output.

## Tool Categories

**Workshop Development Tools:**
- `sz_schema_generator.py` - Analyze source data structure
- `lint_senzing_json.py` - Validate JSON format during development
- `sz_json_analyzer.py` - Analyze mapping quality before loading

**Senzing Core Tools:**
- `sz_configtool` - Configure data sources
- `sz_file_loader` - Load data into Senzing
- `sz_snapshot` - Export entity resolution statistics

**Environment Requirement:**
Senzing core tools require environment variables from `~/.bashrc`. When running via Bash tool, always use:
```bash
source ~/.bashrc && <senzing_tool> <args>
```

---

## sz_schema_generator.py

**Purpose:** Generate markdown documentation showing source data structure, field statistics, and sample values.

**When to run:** Before mapping, to understand source data structure.

**AI Command:**
```bash
python3 senzing/tools/sz_schema_generator.py <input_file> -o <source_filename>_schema.md
```

**Reading output:**
- Markdown file with field statistics table
- For each field: name, type, population %, uniqueness %, top 5 sample values
- Use this to understand what fields are available and their data quality
- Success indicator: Exit code 0 and message "markdown schema saved to <filename>"

**Example:**
```bash
python3 senzing/tools/sz_schema_generator.py customers.csv -o customers_schema.md
```

---

## lint_senzing_json.py

**Purpose:** Validate Senzing JSON structure against specification rules.

**When to run:** During mapping development as a self-test on sample JSON records created by AI. Used to verify JSON structure is correct before writing the full mapper code.

**AI Command:**
```bash
python3 senzing/tools/lint_senzing_json.py <file.jsonl>
```

**Reading output:**
- Exit code 0 = validation passed, ready to proceed
- Exit code 1 = errors found, must fix before loading
- Error format: `ERROR: filename:line: description`
- Warning format: `WARN: filename:line: description` (doesn't fail validation)
- Common errors:
  - Missing DATA_SOURCE or FEATURES array
  - Feature attributes at root level (must be in FEATURES array)
  - Mixed feature families in single object
  - Invalid NAME_FULL/ADDR_FULL combinations

**What to tell user:**
- If passed: "Validation passed - JSON structure is correct"
- If failed: "Found N errors - fix these structural issues before proceeding" (show error messages)

---

## sz_json_analyzer.py

**Purpose:** Analyze mapping quality, feature usage, and data quality issues before loading into Senzing.

**When to run:** After mapper code generates the complete JSONL output file, before loading. This is the critical pre-load check that provides comprehensive analysis of the entire mapped dataset.

**AI Command:**
```bash
python3 senzing/tools/sz_json_analyzer.py <input.jsonl> -o <analysis>.md
```

**IMPORTANT:** Always use `.md` extension for AI-friendly structured format.

**Reading output:**
After running, **AI MUST read the markdown file** and provide a summary covering:

1. **Critical Errors (❌)** - MUST fix before loading:
   - `DATA_SOURCE not found: <NAME>` → Run sz_configtool to add data source
   - Any other blocking issues

2. **Feature Attributes (✅)** - What's mapped:
   - Count of Senzing features used for matching
   - Population percentages for key features (NAME, ADDRESS, identifiers, etc.)

3. **Payload Attributes (ℹ️)** - What's stored but not matched:
   - Non-matching business data (e.g., ACCOUNT_STATUS, RISK_SCORE)
   - This is expected and normal

4. **Warnings (⚠️)** - Data quality issues:
   - Features with <25% population (may affect matching)
   - Features with <80% uniqueness (may indicate data quality problems)

5. **Informational (ℹ️)** - Minor issues:
   - Missing desired attributes (e.g., PASSPORT_COUNTRY for better matching)

**What to tell user:**
```
Analysis Results:

CRITICAL ERRORS: [count] found
❌ DATA_SOURCE not found: CUSTOMERS
   → ACTION: Run sz_configtool to add CUSTOMERS data source

FEATURE ATTRIBUTES: [count] Senzing features
✅ NAME (95%), ADDRESS (60%), EMAIL (37%), PHONE (17%)
✅ Identifiers: PASSPORT (11%), SSN (5%)

PAYLOAD ATTRIBUTES: [count] business fields
ℹ️ ACCOUNT_STATUS, CUSTOMER_TIER, etc. (stored but not matched)

WARNINGS: [count] data quality issues
⚠️ Low population: GENDER (16%), PHONE (17%)

NEXT STEPS:
- Fix critical errors → configure CUSTOMERS data source
- Review warnings → consider enriching source data
- Once fixed → proceed with sz_file_loader
```

---

## sz_configtool

**Purpose:** Configure Senzing data sources (required before loading data).

**When to run:** After analyzer shows "DATA_SOURCE not found" error, before loading.

**AI Command:**
```bash
# Create config file
cat > <project>_config.g2c << 'EOF'
addDataSource <DATA_SOURCE_NAME>
save
EOF

# Apply configuration
source ~/.bashrc && sz_configtool -f <project>_config.g2c
```

**Reading output:**
- Success: Shows "Configuration saved"
- Data source is now configured and ready for loading
- Verify with `listDataSources` command if needed

**What to tell user:**
"Added DATA_SOURCE '<NAME>' to Senzing configuration. Ready to load data with sz_file_loader."

**Example:**
```bash
cat > customers_config.g2c << 'EOF'
addDataSource CUSTOMERS
save
EOF
source ~/.bashrc && sz_configtool -f customers_config.g2c
```

---

## sz_file_loader

**Purpose:** Load validated Senzing JSONL into the entity resolution engine.

**When to run:** After linting passes, analyzer shows no critical errors, and all DATA_SOURCE values are configured.

**AI Command:**
```bash
source ~/.bashrc && sz_file_loader -f <file.jsonl>
```

**Reading output:**
- Exit code 0 = load successful
- Results section shows:
  - **Successful load records** - Records loaded successfully
  - **Error load records** - Records that failed to load
  - **Loading elapsed time (m)** - Load time in minutes
  - **Successful redo records** - Redo operations completed
  - **Error redo records** - Redo operations that failed
  - **Errors file** - Path to error log (if errors occurred)

**What to tell user:**
```
✅ Load completed: [N] records loaded successfully, [N] errors
⏱️ Completed in [X] minutes
📊 Redo processing: [N] successful, [N] errors

[If errors > 0:]
⚠️ Errors logged to: [error_log_path]

Next step: Run sz_snapshot to analyze entity resolution results
```

**Prerequisites checklist:**
- ✅ File passed lint_senzing_json.py
- ✅ Analyzer shows no critical errors
- ✅ All DATA_SOURCE values configured with sz_configtool

---

## sz_snapshot

**Purpose:** Analyze entity resolution results and export match statistics.

**When to run:** After loading data with sz_file_loader, to understand match quality and entity distribution.

**AI Command:**
```bash
source ~/.bashrc && sz_snapshot -o <project>-snapshot-$(date +%Y-%m-%d) -Q
```

**Note:** `-Q` flag prevents interactive prompts (recommended for automation).

**Reading output:**
- Creates JSON file with entity resolution statistics
- Terminal shows: entity count, processing time, completion message
- JSON file structure:
  - **TOTALS** - Overall database statistics with match categories
  - **DATA_SOURCES** - Per-source breakdown (CUSTOMERS, WATCHLIST, etc.)
  - **CROSS_SOURCES** - Cross-source pairs (e.g., "CUSTOMERS||WATCHLIST")
  - **ENTITY_SIZES** - Distribution by records per entity
- Each match category has PRINCIPLES containing match_keys with COUNTs and SAMPLE entity IDs
- Match categories: MATCH, POSSIBLE_MATCH, POSSIBLE_RELATION, AMBIGUOUS_MATCH, DISCLOSED_RELATION

**What to tell user:**

Show a simple table with per-data-source statistics:

| Data Source | Records | Entities | Compression | Relationships |
|-------------|---------|----------|-------------|---------------|
| CUSTOMERS   | 120     | 74       | 38.3%       | 33            |
| WATCHLIST   | 17      | 14       | 17.6%       | 4             |

Where:
- Records = DATA_SOURCES.{SOURCE}.RECORD_COUNT
- Entities = DATA_SOURCES.{SOURCE}.ENTITY_COUNT
- Compression = (Records - Entities) / Records * 100%
- Relationships = sum of AMBIGUOUS_MATCH + POSSIBLE_MATCH + POSSIBLE_RELATION counts

Then provide AI analysis of interesting findings:
```
✅ Snapshot complete: <filename>.json

[TABLE HERE]

ANALYSIS:
- CUSTOMERS shows 38% compression - significant duplicate detection
- CUSTOMERS||WATCHLIST has 5 cross-source matches - potential watchlist hits detected
- WATCHLIST has low relationship count - mostly definitive matches

INTERESTING AREAS TO EXPLORE:
1. CUSTOMERS high compression - see top match keys showing how duplicates were found?
2. CUSTOMERS||WATCHLIST cross-matches - review how customers matched to watchlist?
3. [Other notable findings based on the data]

Which would you like to explore, or something else?
```

**For drill-down requests:**
- Match keys: Extract from DATA_SOURCES.{SOURCE}.{CATEGORY}.PRINCIPLES, sort by COUNT descending, show top 10
- Cross-source match keys: Extract from CROSS_SOURCES."{SOURCE1||SOURCE2}".{CATEGORY}.PRINCIPLES
- Principles: Only show if user explicitly asks
- Entity examples: Use SAMPLE entity IDs to query with Senzing MCP server

---

## Standard Workflow

**Complete data mapping and loading process:**

```bash
# 1. Analyze source data
python3 senzing/tools/sz_schema_generator.py source.csv -o source_schema.md

# 2. Develop mapper (AI-assisted)
#    - AI creates sample JSON records
#    - AI runs linter on samples to validate structure
#    - AI generates mapper code once samples pass linting

# 3. Run mapper to generate complete output
python3 mapper.py source.csv output.jsonl

# 4. Analyze mapping quality on complete dataset
python3 senzing/tools/sz_json_analyzer.py output.jsonl -o analysis.md
# Read analysis.md and provide summary to user

# 5. Configure data sources (if needed)
cat > project_config.g2c << 'EOF'
addDataSource DATASOURCE_NAME
save
EOF
source ~/.bashrc && sz_configtool -f project_config.g2c

# 6. Load data
source ~/.bashrc && sz_file_loader -f output.jsonl
# Provide load summary to user

# 7. Analyze results
source ~/.bashrc && sz_snapshot -o project-snapshot-$(date +%Y-%m-%d) -Q
# Provide snapshot analysis summary to user
```

---

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| "DATA_SOURCE not found" in analyzer | Run sz_configtool to add data source |
| Linter reports format errors | Fix JSON structure (features in array, not at root) |
| sz_file_loader fails | Check: passed linting? analyzer clean? data sources configured? |
| Empty snapshot file | Load data first with sz_file_loader |
| SENZING_ROOT not set | Use `source ~/.bashrc && <command>` pattern |

---

*Last Updated: January 2025*
