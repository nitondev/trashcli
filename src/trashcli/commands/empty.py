from trashcli.trash import empty_trash


def cmd_empty() -> None:
    empty_trash()
    print("trash emptied")
