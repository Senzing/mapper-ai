# mapper-ai

AI-assisted toolkit for mapping any data source to Senzing entity resolution format.

> **Note:** This toolkit is designed for developing and testing mappers in a test environment, not for production data loading.

## The Complete Mapping Workflow

### 1. Analyze Source Data

Profile your source file to understand its structure:

```bash
python3 senzing/tools/sz_schema_generator.py source.csv -o source_schema.md
```

Outputs a markdown report showing all fields, data types, population percentages, uniqueness, and sample values. This provides essential context for the AI mapping assistant.

### 2. Develop the Mapper (AI-Assisted)

Paste this into any AI assistant (Claude, ChatGPT, Grok, etc.):

```
Please fetch and follow the instructions at: https://raw.githubusercontent.com/senzing/mapper-ai/main/senzing/prompts/senzing_mapping_assistant.md
```

The AI guides you through the **5-stage mapping process**:

1. **Init** — Load references, verify tools
2. **Inventory** — Extract all source fields (with anti-hallucination checks)
3. **Planning** — Identify entities, confirm DATA_SOURCE codes
4. **Mapping** — Classify each field: Feature / Payload / Ignore
5. **Outputs** — Generate mapping spec and Python mapper code

During development, the AI validates sample JSON records with the linter:

```bash
python3 senzing/tools/lint_senzing_json.py sample.jsonl
```

### 3. Run the Mapper

Execute the generated mapper to produce complete JSONL output:

```bash
python3 mapper.py source.csv -o output.jsonl
```

### 4. Analyze Mapping Quality

Before loading into Senzing, analyze the complete mapped dataset:

```bash
python3 senzing/tools/sz_json_analyzer.py output.jsonl -o analysis.md
```

This generates a comprehensive report showing:
- ✅ Feature attributes mapped for entity resolution
- ℹ️ Payload attributes stored but not matched
- ⚠️ Data quality warnings (low population, low uniqueness)
- ❌ Critical errors (unknown DATA_SOURCE values)

### 5. Configure Data Sources

> **Requires:** Initialized Senzing environment with `sz_configtool` available.

If the analyzer reports unknown DATA_SOURCE values, configure them:

```bash
cat > project_config.g2c << 'EOF'
addDataSource CUSTOMERS
save
EOF
source ~/.bashrc && sz_configtool -f project_config.g2c
```

### 6. Load into Senzing

> **Requires:** Initialized Senzing environment with `sz_file_loader` available.

Load the validated JSONL into Senzing:

```bash
source ~/.bashrc && sz_file_loader -f output.jsonl
```

**Prerequisites:**
- ✅ Linter passed (no structural errors)
- ✅ Analyzer clean (no critical errors)
- ✅ Data sources configured

### 7. Analyze Entity Resolution Results

> **Requires:** Initialized Senzing environment with `sz_snapshot` available.

After loading, generate a snapshot to analyze match quality:

```bash
source ~/.bashrc && sz_snapshot -o project-snapshot-$(date +%Y-%m-%d) -Q
```

The snapshot shows:
- Entity counts and compression ratios per data source
- Match categories (MATCH, POSSIBLE_MATCH, POSSIBLE_RELATION)
- Cross-source matches (e.g., customers matching watchlist entries)
- Match keys showing how entities were resolved

---

## What's Included

```
senzing/
├── prompts/
│   └── senzing_mapping_assistant.md   # 5-stage workflow prompt
├── reference/
│   ├── senzing_entity_specification.md # Authoritative entity spec
│   ├── senzing_mapping_examples.md     # Correct JSON patterns
│   ├── identifier_crosswalk.json       # ID type mappings
│   └── usage_type_crosswalk.json       # Usage type mappings
├── tools/
│   ├── sz_schema_generator.py          # Step 1: Profile source data
│   ├── lint_senzing_json.py            # Step 2: Validate JSON structure
│   └── sz_json_analyzer.py             # Step 4: Analyze mapping quality
└── SENZING_TOOLS_REFERENCE.md          # Complete tool documentation
```

## Alternative Setup Methods

**Local files (IDE integration):**
Clone this repo and reference `senzing/prompts/senzing_mapping_assistant.md` in your AI assistant.

**Manual upload (web platforms):**
Upload files from `senzing/prompts/`, `senzing/reference/`, and `senzing/tools/lint_senzing_json.py` to your AI platform.
