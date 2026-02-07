# Senzing MCP Server Reference

This document describes the Senzing MCP Server for AI assistants with Model Context Protocol (MCP) support. The server provides read-only access to Senzing entity resolution results.

## When to Use

The MCP server is for **post-loading analysis** — after data has been mapped, loaded, and resolved by Senzing. It enables AI assistants to:

- Search and retrieve resolved entities
- Explore entity relationships and networks
- Understand WHY entities matched (matching explanation)
- Understand HOW entities resolved (resolution mechanics)

**Not for:** Data mapping, loading, or configuration. Use the CLI tools in [senzing_tools_reference.md](senzing_tools_reference.md) for those tasks.

---

## Available Tools

| Tool | Purpose | Use When |
|------|---------|----------|
| `search_entities` | Find entities by name, address, phone, email, identifiers | "Find entities matching..." |
| `get_entity` | Retrieve full entity details by entity ID | "Tell me about entity X" |
| `get_record` | Look up a specific source record | "Show record X from source Y" |
| `find_relationship_path` | Discover connection path between two entities | "How are X and Y connected?" |
| `find_network` | Map entity network up to 3 degrees of separation | "Show network around entity X" |
| `explain_relationship` | Explain why two entities are related (WHY) | "Why are X and Y related?" |
| `explain_entity_resolution` | Show how records resolved together (HOW) | "How was entity X resolved?" |

---

## Response Formatting Guide

### General Rules

**Do:**
- ✅ Start with a clear summary
- ✅ Use tables for comparisons
- ✅ Highlight matching features with ✅ and conflicts with ❌
- ✅ Show data sources with record counts (e.g., "CUSTOMERS:3, WATCHLIST:1")
- ✅ End with **➡️ Bottom line:** statement
- ✅ Reference only features from `match_key_details`

**Don't:**
- ❌ Show internal codes like `ERRULE_CODE`
- ❌ List every record ID in large groups (use "CUSTOMERS:1001 +3 more")
- ❌ Include features not part of the match process
- ❌ Dump raw JSON to users

---

### HOW Results (`explain_entity_resolution`)

Shows step-by-step how records merged into an entity.

**Format:**
```
## Summary
Entity [ID] resolved from [N] records through [N] merge steps.
Primary match drivers: [features]. [Conflicts if any].

## Resolution Steps

**Step 1: Merged [SOURCE:ID] with [SOURCE:ID]**
- ✅ EMAIL: user@example.com (Score: 95)
- ✅ PHONE: +1-555-0100 (Score: 90)
- Match Key: EMAIL+PHONE

**Step 2: Merged [SOURCE:ID] into existing entity**
- ✅ NAME: John Smith (Score: 85)
- Match Key: NAME+DOB

➡️ **Bottom line**: [Concise summary of resolution outcome]
```

**Step header verbs:**
- Both single records → "with"
- Single into group → "into"
- Group notation: `CUSTOMERS:1002 +3 more`

---

### WHY Results (`explain_relationship`)

Shows why two entities are or aren't related.

**Format:**
```
## Summary

**Comparison: Entity [ID1] vs Entity [ID2]**

✅ **Confirmations:** [matching features]
❌ **Denials:** [conflicting features]

**Match Key:** [key]
**➡️ Bottom line:** [Assessment]

## Feature Comparison

| Feature | Entity [ID1] | Entity [ID2] | Result |
|---------|--------------|--------------|--------|
| DATA_SOURCE | CUSTOMERS:3 | CUSTOMERS:2 | - |
| NAME | John Smith | Jon Smith | ❌ |
| EMAIL | user@example.com | user@example.com | ✅ |
```

---

### SEARCH Results (`search_entities`)

**Format:**
```
## Search Results: "[query]"

Found [N] entities. Score range: [X]% - [Y]%

### Strong Matches (90-100%)

| Entity ID | Name | Score | Data Sources | Key Matches |
|-----------|------|-------|--------------|-------------|
| 1001 | John Smith | 95% | CUSTOMERS:3 | Name, DOB, Phone |

### Good Matches (70-89%)
[table continues...]

**Analysis:** [Brief interpretation of results]
```

---

### ENTITY Details (`get_entity`)

**Format:**
```
## Entity [ID]: [Name]

**Overview:** [N] records from [N] data sources

## Source Records

**CUSTOMERS (3 records)**
- 1001: Name, DOB, Phone
- 1002: Name, Email, Address

## Resolved Features

**Identity:** Name, DOB, SSN
**Contact:** Email, Phone, Address
**[Other categories as relevant]**

## Related Entities (if any)
- Entity [ID]: [Name] - [Relationship reason]
```

---

### PATH Results (`find_relationship_path`)

**Format:**
```
## Path: Entity [ID1] → Entity [ID2]

**Summary:** [N] degrees of separation

## Path

**Entity [ID1]: [Name]**
    ↓ [Connection: Shared Phone +1-555-0100]
**Entity [ID2]: [Name]**
    ↓ [Connection: Shared Address]
**Entity [ID3]: [Name]**

**Analysis:** [What the path means]
```

---

### NETWORK Results (`find_network`)

**Format:**
```
## Network: Entity [ID]

**Summary:** [N] entities, [N] relationships, [N] degrees explored

## Direct Connections (1 degree)
- Entity [ID]: [Name] - [Connection type]

## Secondary Connections (2 degrees)
- Entity [ID]: [Name] - Through [intermediate]

## Clusters Identified
**[Cluster name]:** Entities [list] - [Common factor]

**Key Findings:** [Notable patterns]
```

---

## Reference Documentation

For detailed HOW and WHY output interpretation:
- [Senzing EDA Basic Exploration Guide](https://www.senzing.com/docs/tutorials/eda/eda_basic_exploration/) - See "Using How" and "Using Why" sections
