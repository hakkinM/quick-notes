import typer

app = typer.Typer(help="Quick notes from the terminal.")

@app.command()
def hello() -> None:
    """Say hello."""
    print("Hello world!")

@app.command()
def write(path: str) -> None:
    """Write note"""
    print(f"Writing")

@app.command()
def list(path: str) -> None:
    """List notes"""
    print(f"Listing")

@app.command()
def read(path: str) -> None:
    """Read note"""
    print(f"Reading")


def main() -> None:
    app()
