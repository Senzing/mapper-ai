# mapper-ai

This repository contains AI-ready Senzing documentation and instructions that guide you through the process of mapping your data to Senzing with AI.

## What's Inside

### Senzing Materials

All Senzing-specific materials are organized under the `senzing/` directory:

#### Prompts
- [senzing/prompts/senzing_mapping_assistant.md](senzing/prompts/senzing_mapping_assistant.md): master workflow prompt with 5-stage mapping process, rules, and anti-hallucination safeguards.

#### Reference Documents
- [senzing/reference/senzing_entity_specification.md](senzing/reference/senzing_entity_specification.md): authoritative, AI-ready Senzing Entity Spec (this repo is the source of truth).
- [senzing/reference/senzing_mapping_examples.md](senzing/reference/senzing_mapping_examples.md): curated reference examples that show correct Senzing JSON patterns.
- [senzing/reference/identifier_crosswalk.json](senzing/reference/identifier_crosswalk.json): canonical identifier types, aliases, and mapping guidance.
- [senzing/reference/usage_type_crosswalk.json](senzing/reference/usage_type_crosswalk.json): canonical name, address, phone types, aliases and mapping guidance.
- [senzing/reference/images/](senzing/reference/images/): diagrams and visual examples referenced in the entity specification.

#### Tools
- [senzing/tools/lint_senzing_json.py](senzing/tools/lint_senzing_json.py): JSON schema linter for validating generated Senzing JSON/JSONL.
- [senzing/tools/sz_json_analyzer.py](senzing/tools/sz_json_analyzer.py): Analyzes Senzing JSON/JSONL files for data quality issues.
- [senzing/tools/sz_schema_generator.py](senzing/tools/sz_schema_generator.py): Generates schema reports from CSV, JSON, JSONL, XML, and Parquet files.
- [senzing/SENZING_TOOLS_REFERENCE.md](senzing/SENZING_TOOLS_REFERENCE.md): Complete reference for all Senzing tools.

## How to Use This Repository

### Overview
This repository provides everything needed to guide an AI assistant through the Senzing mapping process:

1. **Workflow Prompt:** [senzing/prompts/senzing_mapping_assistant.md](senzing/prompts/senzing_mapping_assistant.md) contains the structured workflow that guides the AI through the 5-stage mapping process.
2. **Reference Documents:** The specification, examples, and linter provide the knowledge base the AI needs to make correct mapping decisions.
3. **Crosswalks:** Organization-wide standards for identifier and usage type transformations that ensure consistency across all mapping projects.

### Quick Start

The simplest way to use this repository is via URL fetching, which works with any AI platform (Claude Code, ChatGPT, Grok, etc.):

**Single-line start:**
```
Please fetch and follow the instructions at: https://raw.githubusercontent.com/senzing/mapper-ai/main/senzing/prompts/senzing_mapping_assistant.md
```

The prompt will automatically:
- Try to load reference files from your local workspace (if available)
- Fall back to fetching from GitHub URLs (if not local)
- Guide you through the 5-stage mapping process

### Setup Instructions (Alternative Methods)

#### Option A: URL-Based (Recommended)
Use the quick start command above. The prompt bootstrap section handles loading all 5 reference files automatically.

#### Option B: Local Files with IDE AI Assistant
1. Clone this repository or download files to your workspace
2. Reference the prompt in your AI assistant:
   - **Claude Code:** Use slash command or @ reference to `senzing/prompts/senzing_mapping_assistant.md`
   - **VS Code / Cursor / Windsurf:** Load prompt file and reference documents
3. The prompt will detect and use local files from `senzing/reference/` directory

#### Option C: Manual Upload (Web AI Platforms)
1. Download these files:
   - `senzing/prompts/senzing_mapping_assistant.md` — workflow instructions
   - `senzing/reference/senzing_entity_specification.md` — entity specification
   - `senzing/reference/senzing_mapping_examples.md` — mapping examples
   - `senzing/tools/lint_senzing_json.py` — validation tool
   - `senzing/reference/identifier_crosswalk.json` — identifier mappings
   - `senzing/reference/usage_type_crosswalk.json` — usage type mappings
2. Upload all 6 files to your AI platform (Claude Projects, ChatGPT, Grok, etc.)
3. Start with: "Begin the Senzing mapping assistant workflow"

### Customizing Crosswalks (Optional)
The crosswalk files contain standard transformations:
- **identifier_crosswalk.json:** Maps source identifier types (SSN, DL, PassportNo, etc.) to Senzing features
- **usage_type_crosswalk.json:** Maps source usage types (HOME, WORK, MAILING, etc.) to Senzing types

Update these as you encounter new source type values to ensure consistency across mapping projects.

### The 5-Stage Mapping Process

Once started, the AI will guide you through:

1. **Stage 1 - Init:** Verify all reference files loaded, test linter
2. **Stage 2 - Inventory:** Extract all field names with integrity checks (anti-hallucination)
3. **Stage 3 - Planning:** Identify entities, confirm DATA_SOURCE codes
4. **Stage 4 - Mapping:** Field-by-field disposition with confidence scoring and validation
5. **Stage 5 - Outputs:** Generate README, mapping spec, and Python implementation

Each stage has an explicit gate requiring your confirmation before proceeding.

## Related Resources

For a complete hands-on mapping workshop with sample data, tools, and step-by-step instructions, see the full [AI-Class repository](https://github.com/jbutcher21/aiclass).
