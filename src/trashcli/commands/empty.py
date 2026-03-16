from trashcli.trash import empty_trash


def cmd_empty() -> None:
    answer = input("This will permanently delete all files in trash. Continue? [y/N] ")
    if answer.strip().lower() != "y":
        print("aborted")
        return
    empty_trash()
    print("trash emptied")
