# quick-notes

Quick-notes is a simple python tool for managing .md formatted notes. The project includes a CLI tool made with **Typer** and an MCP server made with **FastMCP**. The project also includes tests for the NoteHandler class from notes.py, which are also utilized in a GitHub Actions workflow.

## Tools

| Tool   | CLI command                     | MCP tool      |
| ------ | ------------------------------- | ------------- |
| Write  | `qnotes write <name> <content>` | `write_note`  |
| List   | `qnotes list`                   | `list_notes`  |
| Read   | `qnotes read <name>`            | `read_note`   |
| Delete | `qnotes delete <name>`          | `delete_note` |
## Quickstart

Requires Python 3.14+ and [uv](https://docs.astral.sh/uv/).

Note: It is recommended to set **QNOTES_PATH** environment variable pointing to a target directory. As a backup, .qnotes folder is created and used.

### Install Dependencies

```bash
uv sync
```
### CLI 

```bash
uv run qnotes write groceries "milk, eggs, coffee"
uv run qnotes list
uv run qnotes read groceries
uv run qnotes delete groceries
```

### MCP server

Register the MCP server with Claude code.

```bash
claude mcp add quick-notes -- uv run qnotes-mcp
```
### Tests

```bash
uv run pytest
```