# mapper-ai

AI-assisted toolkit for mapping any data source to Senzing entity resolution format.

## The Mapping Workflow

### 1. Analyze Your Source Data

Start by profiling your source file to understand its structure:

```bash
python senzing/tools/sz_schema_generator.py your_data.csv
python senzing/tools/sz_schema_generator.py your_data.jsonl
python senzing/tools/sz_schema_generator.py your_data.xml
```

This generates a schema report showing all fields, data types, value distributions, and cardinality — essential context for the AI mapping assistant.

### 2. Run the AI Mapping Assistant

Paste this into any AI assistant (Claude, ChatGPT, Grok, etc.):

```
Please fetch and follow the instructions at: https://raw.githubusercontent.com/senzing/mapper-ai/main/senzing/prompts/senzing_mapping_assistant.md
```

The AI guides you through the **5-stage mapping process**:

1. **Init** — Load references, verify tools work
2. **Inventory** — Extract all source fields (with anti-hallucination checks)
3. **Planning** — Identify entities, confirm DATA_SOURCE codes
4. **Mapping** — Classify each field: Feature / Payload / Ignore
5. **Outputs** — Generate mapping spec and Python mapper code

Each stage requires your approval before proceeding.

### 3. Validate Your Mapped Output

Before loading into Senzing, validate the JSON structure:

```bash
python senzing/tools/lint_senzing_json.py output.jsonl
```

This catches structural errors like missing DATA_SOURCE, invalid feature names, or malformed records.

### 4. Load into Senzing

Load the validated JSONL into your Senzing instance using the Senzing API or bulk loader.

### 5. Analyze the Loaded Data

After loading, analyze the data quality and entity resolution results:

```bash
python senzing/tools/sz_json_analyzer.py output.jsonl -o analysis.md
```

This generates a comprehensive report showing:
- Feature attribute coverage and distributions
- Data quality warnings (low population, low uniqueness)
- Potential mapping errors
- Recommendations for improvement

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
└── tools/
    ├── sz_schema_generator.py          # Profile source data
    ├── lint_senzing_json.py            # Validate JSON structure
    └── sz_json_analyzer.py             # Analyze data quality
```

## Alternative Setup Methods

**Local files (IDE integration):**
Clone this repo and reference `senzing/prompts/senzing_mapping_assistant.md` in your AI assistant.

**Manual upload (web platforms):**
Upload the 6 files from `senzing/prompts/`, `senzing/reference/`, and `senzing/tools/lint_senzing_json.py` to your AI platform.
