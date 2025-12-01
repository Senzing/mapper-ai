# mapper-ai

AI-assisted toolkit for mapping any data source to Senzing entity resolution format.

## Quick Start

Paste this into any AI assistant (Claude, ChatGPT, Grok, etc.):

```
Please fetch and follow the instructions at: https://raw.githubusercontent.com/senzing/mapper-ai/main/senzing/prompts/senzing_mapping_assistant.md
```

The AI will load the reference materials and guide you through mapping your data.

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
    ├── lint_senzing_json.py            # Validate JSON structure
    ├── sz_json_analyzer.py             # Analyze data quality
    └── sz_schema_generator.py          # Profile source data
```

## Tools

**Profile your source data:**
```bash
python senzing/tools/sz_schema_generator.py your_data.csv
python senzing/tools/sz_schema_generator.py your_data.jsonl --top_values 10
```

**Validate mapped output:**
```bash
python senzing/tools/lint_senzing_json.py output.jsonl
```

**Analyze mapping quality:**
```bash
python senzing/tools/sz_json_analyzer.py output.jsonl -o analysis.md
```

## The 5-Stage Mapping Process

The AI assistant guides you through:

1. **Init** — Load references, verify tools work
2. **Inventory** — Extract all source fields (with anti-hallucination checks)
3. **Planning** — Identify entities, confirm DATA_SOURCE codes
4. **Mapping** — Classify each field: Feature / Payload / Ignore
5. **Outputs** — Generate documentation and Python mapper code

Each stage requires your approval before proceeding.

## Alternative Setup Methods

**Local files (IDE integration):**
Clone this repo and reference `senzing/prompts/senzing_mapping_assistant.md` in your AI assistant.

**Manual upload (web platforms):**
Upload the 6 files from `senzing/prompts/`, `senzing/reference/`, and `senzing/tools/lint_senzing_json.py` to your AI platform.

## Use Cases

- Map CSV, JSON, XML, or any structured data to Senzing format
- Validate existing Senzing JSON files
- Analyze data quality before loading into Senzing
- Train AI assistants on Senzing entity resolution patterns
