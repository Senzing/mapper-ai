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

---

## Environment Configuration

Senzing core tools can run in three environments. You **MUST** create a `senzing_server.json` file in your project root before running any Senzing core tools. This file is **REQUIRED** - tools cannot run without it.

### Configuration File Format

```json
{
  "mode": "local",
  "senzingEnv": "/path/to/senzing/project/setupEnv",
  "docker_container": "senzing-tools",
  "docker_data_dir": "/data",
  "ssh_host": "user@remote-server",
  "ssh_data_dir": "/home/senzing/data"
}
```

### Configuration Attributes

| Attribute | Required For | Description |
|-----------|--------------|-------------|
| `mode` | All | Environment type: `local`, `docker`, or `remote` |
| `senzingEnv` | local, remote | Path to Senzing environment initialization script (e.g., setupEnv) |
| `docker_container` | docker | Name of the Docker container running Senzing |
| `docker_data_dir` | docker | Path inside container where data files are accessible |
| `ssh_host` | remote | SSH connection string (user@host) |
| `ssh_data_dir` | remote | Path on remote server where data files should be placed |

### Environment Modes

**Local** - Senzing installed directly on the machine:
```json
{
  "mode": "local",
  "senzingEnv": "/home/user/senzing/project/setupEnv"
}
```
Commands use: `source <senzingEnv> && <command>`

**Docker** - Senzing running in a Docker container:
```json
{
  "mode": "docker",
  "docker_container": "senzing-tools",
  "docker_data_dir": "/data"
}
```
Commands use: `docker exec <container> <command>`
Note: Docker containers have the Senzing environment already initialized.

**Remote (SSH)** - Senzing installed on a remote server:
```json
{
  "mode": "remote",
  "ssh_host": "senzing@192.168.1.100",
  "ssh_data_dir": "/home/senzing/data",
  "senzingEnv": "/home/senzing/project/setupEnv"
}
```
Commands use: `ssh <host> "source <senzingEnv> && <command>"`

### File Access (Docker and Remote)

**Docker - Detecting Volume Mounts:**

Before copying files, check if the project directory is already mounted:

1. **Verify with `ls`:** Run `docker exec <container> ls <docker_data_dir>`
   - If you see your project files, the directory is volume-mounted
   - If empty or "No such file", files must be copied

2. **Check the path mapping:** If `docker_data_dir` is `/project` and your local project files appear there, no copying needed

**Docker - File Access Rules:**
- **Volume mounted:** Files created locally are immediately accessible in container at `docker_data_dir` path
- **NOT mounted:** Must copy files before each command:
  docker cp local_file.jsonl <container>:<docker_data_dir>/local_file.jsonl

**Remote (SSH):**
- Files must always be transferred via `scp` before use:
  scp output.jsonl senzing@host:/home/senzing/data/

---

## Pre-flight Check for Senzing Core Tools

**BEFORE running any Senzing core tool (sz_configtool, sz_file_loader, sz_snapshot):**

1. **Read `senzing_server.json`** in the project root directory
   - If file does not exist → **STOP** and ask user to create it
2. **Identify the `mode`** value: `local`, `docker`, or `remote`
3. **For local/remote:** Verify `senzingEnv` path is specified
4. **Use the matching command pattern** from the tool's documentation

> ⚠️ **This config file is REQUIRED.** Tools cannot run without it. DO NOT skip this step.

---

## sz_schema_generator.py

**Purpose:** Generate markdown documentation showing source data structure, field statistics, and sample values.

**When to run:** Before mapping, to understand source data structure.

**AI Command:**
python3 senzing/tools/sz_schema_generator.py <input_file> -o <source_filename>_schema.md

**Reading output:**
- Markdown file with field statistics table
- For each field: name, type, population %, uniqueness %, top 5 sample values
- Use this to understand what fields are available and their data quality
- Success indicator: Exit code 0 and message "markdown schema saved to <filename>"

**Example:**
python3 senzing/tools/sz_schema_generator.py customers.csv -o customers_schema.md

---

## lint_senzing_json.py

**Purpose:** Validate Senzing JSON structure against specification rules.

**When to run:** During mapping development as a self-test on sample JSON records created by AI. Used to verify JSON structure is correct before writing the full mapper code.

**AI Command:**
python3 senzing/tools/lint_senzing_json.py <file.jsonl>

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
python3 senzing/tools/sz_json_analyzer.py <input.jsonl> -o <analysis>.md

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

> **Environment Check:** Read `senzing_server.json` first. This file is REQUIRED. See [Pre-flight Check](#pre-flight-check-for-senzing-core-tools).

**Purpose:** Configure Senzing data sources (required before loading data).

**When to run:** After analyzer shows "DATA_SOURCE not found" error, before loading.

**AI Command (by environment):**

First, create the config file locally:
cat > <project>_config.g2c << 'EOF'
addDataSource <DATA_SOURCE_NAME>
save
EOF

Then apply configuration based on environment:

**Local:**
source <senzingEnv> && sz_configtool -f <project>_config.g2c

**Docker:** *(See [File Access](#file-access-docker-and-remote) for volume mount check)*
docker cp <project>_config.g2c <container>:<docker_data_dir>/<project>_config.g2c
docker exec <container> sz_configtool -f <docker_data_dir>/<project>_config.g2c

**Remote (SSH):**
scp <project>_config.g2c <ssh_host>:<ssh_data_dir>/<project>_config.g2c
ssh <ssh_host> "source <senzingEnv> && sz_configtool -f <ssh_data_dir>/<project>_config.g2c"

**Reading output:**
- Success: Shows "Configuration saved"
- Data source is now configured and ready for loading
- Verify with `listDataSources` command if needed

**What to tell user:**
"Added DATA_SOURCE '<NAME>' to Senzing configuration. Ready to load data with sz_file_loader."

**Example (local):**
cat > customers_config.g2c << 'EOF'
addDataSource CUSTOMERS
save
EOF
source /home/user/senzing/project/setupEnv && sz_configtool -f customers_config.g2c

---

## sz_file_loader

> **Environment Check:** Read `senzing_server.json` first. This file is REQUIRED. See [Pre-flight Check](#pre-flight-check-for-senzing-core-tools).

**Purpose:** Load validated Senzing JSONL into the entity resolution engine.

**When to run:** After linting passes, analyzer shows no critical errors, and all DATA_SOURCE values are configured.

**AI Command (by environment):**

**Local:**
source <senzingEnv> && sz_file_loader -f <file.jsonl>

**Docker:** *(See [File Access](#file-access-docker-and-remote) for volume mount check)*
docker cp <file.jsonl> <container>:<docker_data_dir>/<file.jsonl>
docker exec <container> sz_file_loader -f <docker_data_dir>/<file.jsonl>

**Remote (SSH):**
scp <file.jsonl> <ssh_host>:<ssh_data_dir>/<file.jsonl>
ssh <ssh_host> "source <senzingEnv> && sz_file_loader -f <ssh_data_dir>/<file.jsonl>"

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

> **Environment Check:** Read `senzing_server.json` first. This file is REQUIRED. See [Pre-flight Check](#pre-flight-check-for-senzing-core-tools).

**Purpose:** Analyze entity resolution results and export match statistics.

**When to run:** After loading data with sz_file_loader, to understand match quality and entity distribution.

**AI Command (by environment):**

**Local:**
source <senzingEnv> && sz_snapshot -o <project>-snapshot-$(date +%Y-%m-%d) -Q

**Docker:** *(See [File Access](#file-access-docker-and-remote) for volume mount check)*
docker exec <container> sz_snapshot -o <docker_data_dir>/<project>-snapshot-$(date +%Y-%m-%d) -Q
docker cp <container>:<docker_data_dir>/<project>-snapshot-*.json ./

**Remote (SSH):**
ssh <ssh_host> "source <senzingEnv> && sz_snapshot -o <ssh_data_dir>/<project>-snapshot-$(date +%Y-%m-%d) -Q"
scp <ssh_host>:<ssh_data_dir>/<project>-snapshot-*.json ./

**Note:** `-Q` flag prevents interactive prompts (recommended for automation). For Docker/Remote, output files must be copied back to local machine for analysis.

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

> **Note:** Steps 1-4 run locally (development tools). Steps 5-7 use Senzing core tools and REQUIRE `senzing_server.json` to be configured. See [Environment Configuration](#environment-configuration).

1. Analyze source data
   python3 senzing/tools/sz_schema_generator.py source.csv -o source_schema.md

2. Develop mapper (AI-assisted)
   - AI creates sample JSON records
   - AI runs linter on samples to validate structure
   - AI generates mapper code once samples pass linting

3. Run mapper to generate complete output
   python3 mapper.py source.csv output.jsonl

4. Analyze mapping quality on complete dataset
   python3 senzing/tools/sz_json_analyzer.py output.jsonl -o analysis.md

4.5. **ENVIRONMENT CHECK** (REQUIRED before steps 5-7)
   Read `senzing_server.json` in project root. If missing → STOP and create it.
   Use the command pattern matching your environment (local/docker/remote).

5. Configure data sources (if needed) - use environment-specific commands
   Local:  source <senzingEnv> && sz_configtool -f project_config.g2c
   Docker: docker cp + docker exec
   Remote: scp + ssh with source <senzingEnv>

6. Load data - use environment-specific commands
   Local:  source <senzingEnv> && sz_file_loader -f output.jsonl
   Docker: docker cp + docker exec
   Remote: scp + ssh with source <senzingEnv>

7. Analyze results - use environment-specific commands
   Local:  source <senzingEnv> && sz_snapshot -o project-snapshot-$(date +%Y-%m-%d) -Q
   Docker: docker exec + docker cp (to retrieve output)
   Remote: ssh with source <senzingEnv> + scp (to retrieve output)

---

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| `senzing_server.json` not found | Create config file in project root - this is REQUIRED |
| `senzingEnv` path invalid | Verify the setupEnv file exists at the specified path |
| "DATA_SOURCE not found" in analyzer | Run sz_configtool to add data source |
| Linter reports format errors | Fix JSON structure (features in array, not at root) |
| sz_file_loader fails | Check: passed linting? analyzer clean? data sources configured? |
| Empty snapshot file | Load data first with sz_file_loader |
| Docker container not found | Verify container name in `senzing_server.json` matches running container |
| SSH connection refused | Verify `ssh_host` in `senzing_server.json` and SSH key access |
| File not found (Docker/Remote) | Ensure files are copied to `docker_data_dir` or `ssh_data_dir` before running commands |

---

## AI Integration

For AI assistants with MCP (Model Context Protocol) support, the **Senzing MCP Server** provides interactive access to entity resolution results after data is loaded.

See the [Senzing MCP Server](https://github.com/jbutcher21/senzing-mcp-server) repo for tools and response formatting.

---

*Last Updated: January 2025*
