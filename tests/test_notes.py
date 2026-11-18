import pytest

from quick_notes.notes import NoteHandler


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
        "  padded  ",
    ],
)
def test_sanitize_name_accepts_valid(handler, name):
    assert handler.sanitize_name(name) is True


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
    assert handler.sanitize_name(name) is False
