# trashcli

A modern command-line tool for safely deleting files by moving them to the system trash instead of permanently removing them.

Inspired by the original `trash-cli` but with a simpler interface, faster performance, and a modern Python codebase. Fully compatible with the [FreeDesktop Trash specification](https://specifications.freedesktop.org/trash-spec/latest/).

---

## Usage

### Move files to trash

```shell
trash file.txt
trash image.png folder/
trash file1 file2 file3
```

### List trash contents

```shell
trash -ls
```

Output:

```
ID   TYPE   NAME                           OWNER                DELETED
1    file   file.txt                       alice                2026-03-16
2    file   image.png                      alice                2026-03-15
3    dir    pictures                       bob                  2026-03-15
```

### Restore a file

```shell
trash -mv 1
```

Restores the file to its original location. If the destination already exists, you will be prompted to confirm before overwriting. Use `--overwrite` to skip the prompt:

```shell
trash -mv 1 --overwrite
```

### Permanently delete a file

```shell
trash -rm 1
```

### Empty the trash

```shell
trash -rm --all
```

---

## Installation

### Recommended

```shell
pipx install trashcli
```

### With pip

```shell
pip install trashcli
```

---

## Development

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Clone the project

```shell
git clone https://github.com/nitondev/trashcli
cd trashcli
```

### Set up the environment

```shell
uv venv
source .venv/bin/activate
uv pip install -e .
```

If `uv` is not available, bootstrap pip into the venv manually:

```shell
python -m venv .venv
source .venv/bin/activate
python -m ensurepip
.venv/bin/pip3 install -e . pytest
```

### Run the tool locally

```shell
.venv/bin/trash --help
```

Or add the venv to your PATH:

```shell
export PATH="$HOME/Dev/trashcli/.venv/bin:$PATH"
trash --help
```

### Run tests

```shell
.venv/bin/pytest tests/ -v
```

### Lint and format

```shell
ruff check .
ruff format .
```

---

## Project Structure

```
src/
  trashcli/
    cli.py          # entry point, argument parsing
    trash.py        # core trash logic (FreeDesktop spec)
    commands/
      trash.py      # trash <file>
      list.py       # trash -ls
      restore.py    # trash -mv <id>
      remove.py     # trash -rm <id>
      empty.py      # trash -rm --all
tests/
  test_trash.py
```

---

## Compatibility

Files are stored in `~/.local/share/Trash/` following the FreeDesktop Trash specification, making it compatible with GNOME, KDE, XFCE, Cinnamon, and other Linux desktop environments.
