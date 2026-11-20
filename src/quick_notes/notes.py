import os, glob
from pathlib import Path

ENVVAR = "QNOTES_PATH"
FALLBACK_DIR = ".qnotes"
INVALID_CHARS = set('*"\\/<>:|?#^[]')

class NoteHandler:
    def __init__(self) -> None:
        env_root = os.environ.get(ENVVAR)
        if env_root:
            self.root = Path(env_root).expanduser()
            self.root_fallback = False
        else:
            self.root = Path.cwd() / FALLBACK_DIR
            self.root_fallback = True

    def sanitize_name(self, name: str) -> bool:
        name = name.strip()
        return (
            bool(name)
            and not name.startswith(".")
            and not (INVALID_CHARS & set(name))
        )


    def write(self, note_name, content) -> None:
        if self.root_fallback:
            try:
                self.root.mkdir()
                print("Directory created")
            except FileExistsError:
                print("Directory already exists")

        print(f"Writing")
        Path(self.root / f"{note_name}.md").write_text(f"{content}\n")


    def read(self, note_name: str) -> None:
        print("Reading")
        try:
            content = Path(self.root / f"{note_name}.md").read_text()
            print("Read note. Content: " + content)
        except FileNotFoundError:
            print("Note not found")

    def list(self) -> None:
        print(f"Listing")
        for file in self.root.glob("*.md"):
            print(file.name)


    def delete(self, note_name) -> None:
        print(f"Deleting")
        Path(self.root / f"{note_name}.md").unlink()