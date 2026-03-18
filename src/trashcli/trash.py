import pwd
import shutil
from configparser import ConfigParser
from datetime import datetime
from pathlib import Path

TRASH_DIR = Path.home() / ".local" / "share" / "Trash"
FILES_DIR = TRASH_DIR / "files"
INFO_DIR = TRASH_DIR / "info"


def _ensure_trash_dirs() -> None:
    FILES_DIR.mkdir(parents=True, exist_ok=True)
    INFO_DIR.mkdir(parents=True, exist_ok=True)


def _unique_name(name: str) -> str:
    candidate = FILES_DIR / name
    if not candidate.exists():
        return name
    stem = Path(name).stem
    suffix = Path(name).suffix
    counter = 1
    while (FILES_DIR / f"{stem}_{counter}{suffix}").exists():
        counter += 1
    return f"{stem}_{counter}{suffix}"


def _write_trashinfo(
    trash_name: str, original_path: Path, deleted_at: datetime
) -> None:
    config = ConfigParser()
    config.optionxform = str
    config["Trash Info"] = {
        "Path": str(original_path),
        "DeletionDate": deleted_at.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    info_file = INFO_DIR / f"{trash_name}.trashinfo"
    with open(info_file, "w") as f:
        config.write(f)


def move_to_trash(path: str) -> None:
    _ensure_trash_dirs()
    src = Path(path).resolve()
    if not src.exists():
        raise FileNotFoundError(f"'{path}' does not exist")
    trash_name = _unique_name(src.name)
    _write_trashinfo(trash_name, src, datetime.now())
    shutil.move(str(src), FILES_DIR / trash_name)


def list_trash() -> list[dict]:
    _ensure_trash_dirs()
    items = []
    for info_file in sorted(INFO_DIR.glob("*.trashinfo")):
        config = ConfigParser()
        config.optionxform = str
        config.read(info_file)
        section = config["Trash Info"]
        trash_path = FILES_DIR / info_file.stem
        item_type = "dir" if trash_path.is_dir() else "file"
        try:
            uid = trash_path.stat().st_uid
            owner = pwd.getpwuid(uid).pw_name
        except (FileNotFoundError, KeyError):
            owner = ""
        items.append(
            {
                "id": len(items) + 1,
                "name": info_file.stem,
                "type": item_type,
                "path": section.get("Path", ""),
                "owner": owner,
                "deleted": section.get("DeletionDate", ""),
            }
        )
    return items


def _get_item_by_id(item_id: int) -> dict:
    items = list_trash()
    for item in items:
        if item["id"] == item_id:
            return item
    raise ValueError(f"no item with ID {item_id}")


def restore_item(item_id: int, overwrite: bool = False) -> None:
    item = _get_item_by_id(item_id)
    src = FILES_DIR / item["name"]
    dest = Path(item["path"])
    if dest.exists():
        if not overwrite:
            raise FileExistsError(f"'{dest}' already exists")
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), dest)
    (INFO_DIR / f"{item['name']}.trashinfo").unlink()


def delete_item(item_id: int) -> None:
    item = _get_item_by_id(item_id)
    src = FILES_DIR / item["name"]
    if src.is_dir():
        shutil.rmtree(src)
    else:
        src.unlink()
    (INFO_DIR / f"{item['name']}.trashinfo").unlink()


def empty_trash() -> None:
    _ensure_trash_dirs()
    for item in FILES_DIR.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()
    for info_file in INFO_DIR.glob("*.trashinfo"):
        info_file.unlink()
