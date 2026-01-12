# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

mapper-ai is an AI-assisted toolkit for mapping any data source to Senzing entity resolution JSON format. It provides reference documentation, validation tools, and a structured 5-stage workflow prompt for AI assistants to generate mappers.

## Build and Development Commands

```bash
# Install all dependencies (development, lint, test, docs)
python -m pip install --group all .

# Run pylint on all Python files
pylint $(git ls-files '*.py' ':!:docs/source/*')

# Run the linter self-test
python3 senzing/tools/lint_senzing_json.py --self-test

# Validate a Senzing JSON/JSONL file
python3 senzing/tools/lint_senzing_json.py <file.jsonl>

# Profile source data structure
python3 senzing/tools/sz_schema_generator.py <input_file> -o <output>.md

# Analyze mapped data quality
python3 senzing/tools/sz_json_analyzer.py <input.jsonl> -o <analysis>.md
```

## Code Style

- Line length: 120 characters (black, flake8)
- Import sorting: isort with black profile
- Type hints: mypy enabled
- Security: bandit enabled (B101 skipped for asserts)

## Architecture

### Directory Structure

```console
senzing/
├── prompts/
│   └── senzing_mapping_assistant.md   # 5-stage AI workflow prompt
├── reference/
│   ├── senzing_entity_specification.md # Authoritative entity spec
│   ├── senzing_mapping_examples.md     # Correct JSON patterns
│   ├── identifier_crosswalk.json       # ID type mappings
│   └── usage_type_crosswalk.json       # Usage type mappings
└── tools/
    ├── lint_senzing_json.py            # JSON structure validator
    ├── sz_json_analyzer.py             # Mapping quality analyzer
    ├── sz_schema_generator.py          # Source data profiler
    └── sz_default_config.json          # Default Senzing config
```

### Tool Purposes

- **lint_senzing_json.py**: Development-time validator for Senzing JSON structure. Validates against entity spec rules (DATA_SOURCE, FEATURES array, feature families, attribute rules).

- **sz_json_analyzer.py**: Pre-load analyzer for complete mapped JSONL files. Reports feature usage, data quality warnings, and validates DATA_SOURCE values against Senzing configuration.

- **sz_schema_generator.py**: Profiles source files (CSV, JSON, JSONL, Parquet, XML) generating markdown reports with field statistics, types, population %, uniqueness %, and sample values.

### Senzing JSON Format

Records must have:

- `DATA_SOURCE` (string): Source identifier
- `RECORD_ID` (string): Unique record identifier (recommended)
- `FEATURES` (array): List of feature objects, each containing attributes from a single feature family

Feature families include: NAME, ADDRESS, PHONE, EMAIL, DOB, PASSPORT, SSN, NATIONAL_ID, TAX_ID, etc.

### 5-Stage Mapping Workflow

The AI mapping assistant (`senzing/prompts/senzing_mapping_assistant.md`) follows:

1. **Init** — Load references, verify tools
2. **Inventory** — Extract all source fields with integrity checks
3. **Planning** — Identify entities, confirm DATA_SOURCE codes
4. **Mapping** — Classify each field (Feature/Payload/Ignore), validate with linter
5. **Outputs** — Generate README, mapping spec, and Python mapper

## Custom Commands

- `/senzing` — Fetches and executes Senzing-specific instructions from senzing-factory/claude
