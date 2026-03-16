from trashcli.trash import move_to_trash


def cmd_trash(files: list[str]) -> None:
    for path in files:
        try:
            move_to_trash(path)
            print(f"'{path}' moved to trash")
        except FileNotFoundError as e:
            print(f"error: {e}")
