# mapper-ai

This repository contains AI-ready Senzing documentation and mapping instructions to guide you through the process of mapping your data to Senzing with AI. This is the documentation folder for the AI-Class: Senzing Mapping Assistant.

## What's Inside

### RAG Documents

- [rag/senzing_mapping_assistant_prompt.md](rag/senzing_mapping_assistant_prompt.md): master mapping instructions/prompt with rules, templates, and examples.
- [rag/senzing_mapping_examples.md](rag/senzing_mapping_examples.md): curated reference examples that show correct Senzing JSON patterns.
- [rag/senzing_entity_specification.md](rag/senzing_entity_specification.md): authoritative, AI-ready Senzing Entity Spec (this repo is the source of truth).
- [rag/lint_senzing_json.py](rag/lint_senzing_json.py): JSON schema linter for validating generated Senzing JSON/JSONL.
- [rag/identifier_crosswalk.json](rag/identifier_crosswalk.json): canonical identifier types, aliases, and mapping guidance.
- [rag/identifier_lookup_log.md](rag/identifier_lookup_log.md): template to record curated identifier lookups (no PII).

## Using These Documents with AI

### Data Handling Guidance
- Do not upload full datasets to an AI. Share schema extracts, field lists, small samples, or analyzer summaries instead.
- If you don't already have a schema, use a file analyzer to produce a schema and stats summary, then provide that summary to the assistant during mapping.

### Tips for Collaborating with AI
- Ask it questions if you don't understand something. One of my favorites is: `what does the senzing spec say about that`
- If it gives you options, ask it for the pros and cons.
- Correct it when it gets something wrong. It will learn from you.
- Keep it on track: AI's hallucinate. See: [ChatGPT Common Issues And Solutions](https://www.geeky-gadgets.com/chatgpt-5-common-issues-and-solutions/)
  - Telling it to `go back to strict mode` will get it back on track.

**Above all: Don't use it to replace your judgement or expertise. It's just your assistant. You are the decision maker.**

## Loading These Documents into Your AI Assistant

### Option A — Prebuilt GPT
Open [Senzing Mapping Assistant](https://chatgpt.com/g/g-68d471ea99a08191a4fbe2cf42bdc0d1-senzing-mapping-assistant) and click "Help me map my schema or data file." The mapping docs are preloaded.

### Option B — Your AI's Chat Interface
Create a new project/workspace and load the core references as project documents before you start chatting:
- Upload these files so the assistant can cite them:
  - `rag/senzing_mapping_examples.md`
  - `rag/lint_senzing_json.py`
  - `rag/senzing_entity_specification.md`
- Paste the contents of `rag/senzing_mapping_assistant_prompt.md` into the system prompt (or the first message if no system field exists).

### Option C — IDE Workflow
Open VS Code (or your IDE) on your project folder and connect your AI assistant extension. Pull the reference files into the workspace using these raw URLs:
```
https://raw.githubusercontent.com/Senzing/mapper-ai/main/rag/senzing_mapping_assistant_prompt.md
https://raw.githubusercontent.com/Senzing/mapper-ai/main/rag/senzing_mapping_examples.md
https://raw.githubusercontent.com/Senzing/mapper-ai/main/rag/senzing_entity_specification.md
https://raw.githubusercontent.com/Senzing/mapper-ai/main/rag/lint_senzing_json.py
```

## Important Links

- SenzingGPT (ChatGPT): https://chatgpt.com/g/g-679d39f4717c819192476201873ebc21-senzinggpt
- Senzing Mapping Assistant (ChatGPT): https://chatgpt.com/g/g-68d471ea99a08191a4fbe2cf42bdc0d1-senzing-mapping-assistant
- JSON Analyzer Docs (Senzing Garage): https://github.com/senzing-garage/sz-json-analyzer
- ChatGPT Common Issues And Solutions: https://www.geeky-gadgets.com/chatgpt-5-common-issues-and-solutions/

## Related Resources

For a complete hands-on mapping workshop with sample data, tools, and step-by-step instructions, see the full [AI-Class repository](https://github.com/jbutcher21/aiclass).
