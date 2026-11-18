import os
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


    def write(self) -> None:
        print(f"Writing")

    def read(self) -> None:
        print(f"Reading")

    def list(self) -> None:
        print(f"Listing")

    def delete(self) -> None:
        print(f"Deleting")