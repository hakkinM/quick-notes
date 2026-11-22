import logging, sys

from fastmcp import FastMCP

from quick_notes.notes import NoteHandler

# stdout carries the MCP protocol over stdio, so logs must go to stderr
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s', stream=sys.stderr)

logger = logging.getLogger(__name__)

mcp = FastMCP("quick-notes")

handler = NoteHandler()

@mcp.tool
def write_note(note_name: str, content: str) -> str:
    """Write a note, overwriting it if it already exists."""
    handler.write(note_name, content)
    return f"Wrote note {note_name!r}"

@mcp.tool
def list_notes() -> list[str]:
    """List the names of all notes."""
    return handler.list()

@mcp.tool
def read_note(note_name: str) -> str:
    """Read the content of a note."""
    return handler.read(note_name)

@mcp.tool
def delete_note(note_name: str) -> str:
    """Delete a note."""
    handler.delete(note_name)
    return f"Deleted note {note_name!r}"


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
