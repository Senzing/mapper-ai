# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
[markdownlint](https://dlaa.me/markdownlint/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed 2026-02-10

- Align toolkit with January 2026 AWS workshop findings
  - Mapping assistant: better stage gating and improved multi-entity loop tracking
  - Entity specification: consolidated into text and tables, removed unused images
  - Tools reference: clarified tool usage, added multi-environment support (local/Docker/remote) via `senzing_server.json`
  - README: restructured with Getting Started, Environment Setup, and tool-agnostic context loading for AI IDEs
- Added `senzing_mcp_reference.md` for MCP server usage
