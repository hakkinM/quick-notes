import typer

from quick_notes.notes import NoteHandler

app = typer.Typer(help="Quick notes from the terminal.")

handler = NoteHandler()

@app.command()
def hello() -> None:
    """Say hello."""
    print("Hello world!")


@app.command("write")
def write_note(name: str, content: str) -> None:
    """Write note"""
    handler.write()


@app.command("list")
def list_notes() -> None:
    """List notes"""
    handler.list()


@app.command("read")
def read_note(name: str) -> None:
    """Read note"""
    handler.read()


@app.command("delete")
def delete_note(name: str) -> None:
    """Delete note"""
    handler.delete()


def main() -> None:
    app()


if __name__ == "__main__":
    main()
