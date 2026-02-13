# mapper-ai

AI-assisted toolkit for mapping any data source to Senzing entity resolution format.

> **Note:** This toolkit is designed for developing and testing mappers in a development or test environment, not for production data loading.

## Getting Started

This toolkit is designed to be used from an AI-powered IDE or command-line tool such as Claude Code, Cursor, or Windsurf.

Clone this repo once to a local directory and allow your AI environment access to it for each project. For example, in Claude Code you can add it to your allowed directories. The AI reads the reference files and runs the tools directly.

**Even better:** Configure the toolkit as persistent context so the AI always has it available. For example, in Claude Code:

- Add the mapper-ai directory as an additional working directory for each project
- Reference [senzing_tools_reference.md](senzing/senzing_tools_reference.md) and the mapping assistant prompt in your project's `CLAUDE.md` instructions
- Set up custom slash commands that load the mapping workflow or tools reference on demand

Other AI tools (Cursor, Windsurf) have similar mechanisms — `.cursorrules`, agent configs, or `@file` references that bring toolkit files into context automatically.

---

## What's Included

```
senzing/
├── prompts/
│   └── senzing_mapping_assistant.md   # 5-stage mapping workflow prompt
├── reference/
│   ├── senzing_entity_specification.md # Senzing entity format spec
│   ├── senzing_mapping_examples.md     # Correct JSON patterns
│   ├── identifier_crosswalk.json       # ID type mappings
│   └── usage_type_crosswalk.json       # Usage type mappings
├── tools/
│   ├── sz_schema_generator.py          # Profile source data structure
│   ├── lint_senzing_json.py            # Validate JSON structure
│   └── sz_json_analyzer.py             # Analyze mapping quality
└── senzing_tools_reference.md          # Complete tool & CLI reference
```

**Prompts** — The mapping assistant prompt drives the 5-stage workflow. Your AI fetches it and follows the instructions to guide you through mapping.

**Reference** — The entity spec, mapping examples, and crosswalk files give the AI the knowledge it needs to correctly map your data to Senzing format.

**Tools** — Python scripts the AI runs to profile source data, validate JSON structure, and analyze mapping quality.

**Tool guides** — [senzing_tools_reference.md](senzing/senzing_tools_reference.md) is the complete reference for all tools including Senzing core CLI tools (configtool, file loader, snapshot).

---

## Environment Setup

Different workflow steps have different requirements:

**Steps 1–4** (Profile, Map, Run, Validate) — No Senzing environment needed. Just this repo and an AI assistant.

**Step 5** (Configure, Load, Snapshot) — Requires a Senzing environment. Create a `senzing_server.json` config file in your project root to tell tools how to connect (local, Docker, or remote). See [senzing_tools_reference.md](senzing/senzing_tools_reference.md) for configuration details.

**Step 6 entity exploration** — Requires the [Senzing MCP Server](https://github.com/jbutcher21/senzing-mcp-server) installed in your Senzing environment and configured in your AI assistant's MCP settings. See that repo for installation and setup.

---

## The Mapping Workflow

Start each session by adding the `senzing/` folder to your AI's context. In most tools (Cursor, Windsurf, Claude Code) type `@senzing/` in the chat prompt; in GitHub Copilot use `#folder:senzing`. This gives the AI knowledge of all available tools, references, and prompts so every subsequent step just works.

If the AI seems unsure about a specific tool or format, add the relevant file to context directly — e.g., `@senzing/senzing_tools_reference.md` or `@senzing/reference/senzing_entity_specification.md`.

Then guide your AI through each step with prompts like these:

### 1. Profile Source Data

> *"Use the schema generator to profile customers.csv"*

The AI runs the schema generator (see [senzing_tools_reference.md](senzing/senzing_tools_reference.md)) and reports all fields, data types, population percentages, uniqueness, and sample values.

### 2. Develop the Mapper

> *"Follow the mapping assistant prompt to map customers.csv"*

The AI follows the workflow in [senzing_mapping_assistant.md](senzing/prompts/senzing_mapping_assistant.md) and guides you through the **5-stage mapping process**:

1. **Init** — Load references, verify tools
2. **Inventory** — Extract all source fields (with anti-hallucination checks)
3. **Planning** — Identify entities, confirm DATA_SOURCE codes
4. **Mapping** — Classify each field: Feature / Payload / Ignore
5. **Outputs** — Generate mapping spec and Python mapper code

During development, the AI validates sample JSON records with the linter automatically.

### 3. Run the Mapper

> *"Run the customer mapper on customers.csv to generate output.jsonl"*

The AI executes the generated mapper to produce the complete JSONL output.

### 4. Analyze Mapping Quality

> *"Use the JSON analyzer on output.jsonl and show me the results"*

The AI runs the analyzer (see [senzing_tools_reference.md](senzing/senzing_tools_reference.md)) and reports feature usage, data quality warnings, and critical errors to fix before loading.

### 5. Configure, Load, and Snapshot

> *"Use configtool, file loader, and snapshot to configure CUSTOMERS, load output.jsonl, and take a snapshot"*

**Requires:** Senzing environment + `senzing_server.json` (see [Environment Setup](#environment-setup))

The AI uses `sz_configtool`, `sz_file_loader`, and `sz_snapshot` to configure data sources, load data, and generate entity resolution statistics. See [senzing_tools_reference.md](senzing/senzing_tools_reference.md) for details.

### 6. Explore Results

**Snapshot analysis** — no additional setup needed:

> *"Show me the top match keys for CUSTOMERS"*
>
> *"What cross-source matches were found?"*

The AI analyzes the snapshot JSON from step 5 to show entity counts, match categories, and cross-source matches.

**Entity exploration** — requires [Senzing MCP Server](https://github.com/jbutcher21/senzing-mcp-server) (see [Environment Setup](#environment-setup)):

> *"Search for entities matching John Smith"*
>
> *"How was entity 1001 resolved?"*

The AI uses MCP tools to search, retrieve, and explain specific entities and their relationships. See the [Senzing MCP Server](https://github.com/jbutcher21/senzing-mcp-server) repo for available tools.
