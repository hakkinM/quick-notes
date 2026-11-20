import pytest

from quick_notes.notes import InvalidNoteNameError, NoteHandler, NoteNotFoundError


@pytest.fixture
def handler(monkeypatch, tmp_path):
    monkeypatch.setenv("QNOTES_PATH", str(tmp_path))
    return NoteHandler()


@pytest.mark.parametrize(
    "name",
    [
        "todo",
        "Shopping list",
        "meeting-2026-11-18",
        "notes_v2",
        "Ääkköset",
    ],
)
def test_sanitize_name_accepts_valid(handler, name):
    assert handler._sanitize_name(name) is True


@pytest.mark.parametrize(
    "name",
    [
        "",
        "   ",
        ".hidden",
        ".obsidian",
        "..",
        "../escape",
        "a/b",
        "/etc/passwd",
        "back\\slash",
        "star*",
        'quote"',
        "less<",
        "greater>",
        "colon:",
        "pipe|",
        "question?",
        "hash#",
        "caret^",
        "[[link]]",
    ],
)
def test_sanitize_name_rejects_invalid(handler, name):
    assert handler._sanitize_name(name) is False


# write

def test_write_creates_note(handler, tmp_path):
    handler.write("todo", "buy milk")
    assert (tmp_path / "todo.md").read_text() == "buy milk\n"


def test_write_invalid_name_raises(handler):
    with pytest.raises(InvalidNoteNameError):
        handler.write("a/b", "x")


# read

def test_read_returns_content(handler, tmp_path):
    (tmp_path / "todo.md").write_text("buy milk\n")
    assert handler.read("todo") == "buy milk\n"


def test_read_missing_note_raises(handler):
    with pytest.raises(NoteNotFoundError):
        handler.read("nope")


# list

def test_list_returns_note_names(handler, tmp_path):
    (tmp_path / "a.md").write_text("")
    (tmp_path / "b.md").write_text("")
    assert sorted(handler.list()) == ["a", "b"]


def test_list_empty_returns_nothing(handler):
    assert handler.list() == []


# delete

def test_delete_removes_note(handler, tmp_path):
    (tmp_path / "todo.md").write_text("buy milk\n")
    handler.delete("todo")
    assert not (tmp_path / "todo.md").exists()


def test_delete_missing_note_raises(handler):
    with pytest.raises(NoteNotFoundError):
        handler.delete("nope")
