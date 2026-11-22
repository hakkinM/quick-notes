import os, logging
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
            logging.info(f"Set root as {ENVVAR}")
        else:
            self.root = Path.cwd() / FALLBACK_DIR
            self.root_fallback = True
            logging.info(f"Using backup root in {self.root}")

    def _sanitize_name(self, note_name: str) -> bool:
        note_name = note_name.strip()
        return (
            bool(note_name)
            and not note_name.startswith(".")
            and not (INVALID_CHARS & set(note_name))
        )

    def _require_root(self) -> None:
        if self.root.exists():
            return
        if self.root_fallback:
            raise RootDirMissingError(
                f"Notes directory not found: {self.root}. "
                f"Without {ENVVAR} set, notes are stored in "
                f"'{FALLBACK_DIR}' in the current directory."
            )
        else:
            raise RootDirMissingError(
                f"Notes directory not found: {self.root} "
                f"(set by {ENVVAR}). Create it or change {ENVVAR}."
            )


    def _note_path(self, note_name: str, create_dir_if_missing: bool = False) -> Path:
        if not self._sanitize_name(note_name):
            raise InvalidNoteNameError(
                f"Invalid note name {note_name!r}: names must not be empty, "
                f"start with '.', or contain any of: {' '.join(sorted(INVALID_CHARS))}"
            )

        if create_dir_if_missing and not self.root.exists():
            self.root.mkdir()
            logging.info(f"Created root folder {FALLBACK_DIR} in {self.root}")
        else:
            self._require_root()

        return Path(self.root / f"{note_name}.md")


    def write(self, note_name, content) -> None:
        self._note_path(note_name, True).write_text(f"{content}\n")
        logging.info(f"Wrote note {note_name!r} to {self.root}")

    def read(self, note_name: str) -> str:
        note = self._note_path(note_name)
        if note.exists():
            content = note.read_text()
            logging.info(f"Read note {note_name!r} from {self.root}")
            return content
        else:
            raise NoteNotFoundError(
                f"Note {note_name!r} not found in {self.root}. "
                f"Run 'list' to see existing notes."
            )

    def list(self) -> list[str]:
        self._require_root()
        logging.info(f"Listing .md notes in {self.root}")
        return [file.name[0:len(file.name)-3] for file in self.root.glob("*.md")]


    def delete(self, note_name) -> None:
        note_path = self._note_path(note_name)
        if note_path.exists():
            note_path.unlink()
            logging.info(f"Deleted note {note_name!r} from {self.root}")
        else:
            raise NoteNotFoundError(
                f"Note {note_name!r} not found in {self.root}. "
                f"Run 'list' to see existing notes."
            )

class NoteError(Exception):
    """Base class for all quick-notes errors."""

class InvalidNoteNameError(NoteError):
    """The note name failed validation."""

class RootDirMissingError(NoteError):
    """The notes directory does not exist."""

class NoteNotFoundError(NoteError):
    """No note with the given name exists."""
