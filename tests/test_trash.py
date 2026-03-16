import shutil
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

import trashcli.trash as trash_module
from trashcli.trash import (
    delete_item,
    empty_trash,
    list_trash,
    move_to_trash,
    restore_item,
)


@pytest.fixture
def trash_dirs(tmp_path):
    files_dir = tmp_path / "files"
    info_dir = tmp_path / "info"
    files_dir.mkdir()
    info_dir.mkdir()
    with (
        patch.object(trash_module, "FILES_DIR", files_dir),
        patch.object(trash_module, "INFO_DIR", info_dir),
        patch.object(trash_module, "TRASH_DIR", tmp_path),
    ):
        yield {"files": files_dir, "info": info_dir}


class TestMoveToTrash:
    def test_moves_file(self, trash_dirs, tmp_path):
        src = tmp_path / "file.txt"
        src.write_text("hello")
        move_to_trash(str(src))
        assert (trash_dirs["files"] / "file.txt").exists()
        assert not src.exists()

    def test_creates_trashinfo(self, trash_dirs, tmp_path):
        src = tmp_path / "file.txt"
        src.write_text("hello")
        move_to_trash(str(src))
        assert (trash_dirs["info"] / "file.txt.trashinfo").exists()

    def test_raises_if_not_found(self, trash_dirs, tmp_path):
        with pytest.raises(FileNotFoundError):
            move_to_trash(str(tmp_path / "ghost.txt"))

    def test_unique_name_on_conflict(self, trash_dirs, tmp_path):
        (trash_dirs["files"] / "file.txt").write_text("existing")
        src = tmp_path / "file.txt"
        src.write_text("new")
        move_to_trash(str(src))
        assert (trash_dirs["files"] / "file_1.txt").exists()

    def test_moves_directory(self, trash_dirs, tmp_path):
        src = tmp_path / "mydir"
        src.mkdir()
        (src / "a.txt").write_text("data")
        move_to_trash(str(src))
        assert (trash_dirs["files"] / "mydir").is_dir()
        assert not src.exists()


class TestListTrash:
    def test_empty_trash(self, trash_dirs):
        assert list_trash() == []

    def test_lists_items(self, trash_dirs, tmp_path):
        src = tmp_path / "file.txt"
        src.write_text("hello")
        move_to_trash(str(src))
        items = list_trash()
        assert len(items) == 1
        assert items[0]["name"] == "file.txt"
        assert items[0]["id"] == 1

    def test_ids_are_sequential(self, trash_dirs, tmp_path):
        for name in ["a.txt", "b.txt", "c.txt"]:
            f = tmp_path / name
            f.write_text(name)
            move_to_trash(str(f))
        items = list_trash()
        assert [i["id"] for i in items] == [1, 2, 3]

    def test_item_has_correct_path(self, trash_dirs, tmp_path):
        src = tmp_path / "file.txt"
        src.write_text("hello")
        move_to_trash(str(src))
        items = list_trash()
        assert items[0]["path"] == str(src)

    def test_item_has_deletion_date(self, trash_dirs, tmp_path):
        src = tmp_path / "file.txt"
        src.write_text("hello")
        move_to_trash(str(src))
        items = list_trash()
        assert items[0]["deleted"].startswith(datetime.now().strftime("%Y-%m-%d"))


class TestRestoreItem:
    def test_restores_file(self, trash_dirs, tmp_path):
        src = tmp_path / "file.txt"
        src.write_text("hello")
        move_to_trash(str(src))
        restore_item(1)
        assert src.exists()
        assert not (trash_dirs["files"] / "file.txt").exists()

    def test_removes_trashinfo(self, trash_dirs, tmp_path):
        src = tmp_path / "file.txt"
        src.write_text("hello")
        move_to_trash(str(src))
        restore_item(1)
        assert not (trash_dirs["info"] / "file.txt.trashinfo").exists()

    def test_raises_if_dest_exists(self, trash_dirs, tmp_path):
        src = tmp_path / "file.txt"
        src.write_text("hello")
        move_to_trash(str(src))
        src.write_text("already here")
        with pytest.raises(FileExistsError):
            restore_item(1)

    def test_raises_on_invalid_id(self, trash_dirs):
        with pytest.raises(ValueError):
            restore_item(99)


class TestDeleteItem:
    def test_deletes_file(self, trash_dirs, tmp_path):
        src = tmp_path / "file.txt"
        src.write_text("hello")
        move_to_trash(str(src))
        delete_item(1)
        assert not (trash_dirs["files"] / "file.txt").exists()
        assert not (trash_dirs["info"] / "file.txt.trashinfo").exists()

    def test_deletes_directory(self, trash_dirs, tmp_path):
        src = tmp_path / "mydir"
        src.mkdir()
        (src / "a.txt").write_text("data")
        move_to_trash(str(src))
        delete_item(1)
        assert not (trash_dirs["files"] / "mydir").exists()

    def test_raises_on_invalid_id(self, trash_dirs):
        with pytest.raises(ValueError):
            delete_item(99)


class TestEmptyTrash:
    def test_removes_all_files(self, trash_dirs, tmp_path):
        for name in ["a.txt", "b.txt"]:
            f = tmp_path / name
            f.write_text(name)
            move_to_trash(str(f))
        empty_trash()
        assert list(trash_dirs["files"].iterdir()) == []
        assert list(trash_dirs["info"].iterdir()) == []

    def test_empty_on_already_empty(self, trash_dirs):
        empty_trash()
        assert list_trash() == []
