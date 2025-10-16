# mapper-ai

This repository contains AI-ready Senzing documentation and instructions that guide you through the process of mapping your data to Senzing with AI. 

## What's Inside

### RAG Documents

- [rag/senzing_mapping_assistant_prompt.md](rag/senzing_mapping_assistant_prompt.md): master mapping instructions/prompt with rules, templates, and examples.
- [rag/senzing_mapping_examples.md](rag/senzing_mapping_examples.md): curated reference examples that show correct Senzing JSON patterns.
- [rag/senzing_entity_specification.md](rag/senzing_entity_specification.md): authoritative, AI-ready Senzing Entity Spec (this repo is the source of truth).
- [rag/lint_senzing_json.py](rag/lint_senzing_json.py): JSON schema linter for validating generated Senzing JSON/JSONL.
- [rag/identifier_crosswalk.json](rag/identifier_crosswalk.json): canonical identifier types, aliases, and mapping guidance.
- [rag/usage_type_crosswalk.json](rag/usage_type_crosswalk.json): canonical name, address, phone types, aliases and mapping guidance. 

## How to Use This Repository

### Overview
This repository provides everything needed to guide an AI assistant through the Senzing mapping process:

1. **System Prompt:** [senzing_mapping_assistant_prompt.md](rag/senzing_mapping_assistant_prompt.md) contains the structured workflow that guides the AI through the 5-stage mapping process.
2. **Reference Documents:** The specification, examples, and linter provide the knowledge base the AI needs to make correct mapping decisions.
3. **Crosswalks:** Organization-wide standards for identifier and usage type transformations that ensure consistency across all mapping projects.

### Setup Instructions

#### 1. Load Reference Documents
Upload or load these files into your AI assistant or agentic workflow as **knowledge base/RAG documents**:
- `rag/senzing_entity_specification.md` — authoritative Senzing entity structure
- `rag/senzing_mapping_examples.md` — curated reference examples
- `rag/lint_senzing_json.py` — validation tool (must be executable)
- `rag/identifier_crosswalk.json` — your organization's identifier type mappings
- `rag/usage_type_crosswalk.json` — your organization's usage type mappings

#### 2. Configure System Prompt
Use the contents of `rag/senzing_mapping_assistant_prompt.md` as your **system prompt** (or initial instruction). This prompt guides the AI through:
- Stage 1: Initialization and verification
- Stage 2: Schema/data inventory (anti-hallucination)
- Stage 3: Planning (entity identification, DATA_SOURCE codes)
- Stage 4: Field-by-field mapping with validation
- Stage 5: Generate documentation and implementation code

#### 3. Customize Crosswalks (Optional)
The crosswalk files contain your organization's standard transformations:
- **identifier_crosswalk.json:** Maps source identifier types (SSN, DL, PassportNo, etc.) to Senzing identifier features
- **usage_type_crosswalk.json:** Maps source usage types (HOME, WORK, MAILING, etc.) to Senzing usage types

These ensure consistent mapping decisions across all your mapping projects. Update them as you encounter new source type values.

### Quick Start Options

#### Option A — Local IDE with AI Assistant (Recommended)
For most mapping projects, work locally with an AI-enabled IDE:
1. Open your project folder in your IDE (VS Code, Cursor, Windsurf, JetBrains, etc.)
2. Fetch the RAG files into your workspace (clone this repo, download files, or fetch via raw URLs)
3. Configure your AI assistant/agent to load the 5 RAG files as context/knowledge
4. Set `senzing_mapping_assistant_prompt.md` as the system prompt or initial instruction
5. Work interactively with your source schema/data files

**Why local?** Direct file access, ability to execute the linter, generate and test code, handle complex multi-file schemas, and iterate on mapper implementations.

#### Option B — Web-based AI Chat (Simple Schemas Only)
For quick exploration or simple single-file schemas:
1. Create a new project in a web-based AI platform:
   - **Claude.ai:** Create a Project and add documents
   - **ChatGPT:** Use ChatGPT web interface with file uploads
   - **Grok:** Use Grok web interface with file uploads
   - **Custom GPT:** Try the [Senzing Mapping Assistant GPT](https://chatgpt.com/g/g-68e7e7dd8b648191a082b4a0c2943499-senzing-mapping-assistant) (RAG files preloaded)
2. Upload the 5 RAG files as knowledge documents
3. Paste `senzing_mapping_assistant_prompt.md` content into your first message or system prompt
4. Upload your source schema/data file and begin

**Limitation:** Web interfaces can't execute the linter locally or handle complex multi-file schemas efficiently.

## Related Resources

For a complete hands-on mapping workshop with sample data, tools, and step-by-step instructions, see the full [AI-Class repository](https://github.com/jbutcher21/aiclass).
