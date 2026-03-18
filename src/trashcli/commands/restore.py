from trashcli.trash import restore_item


def cmd_restore(item_id: str, overwrite: bool = False) -> None:
    try:
        restore_item(int(item_id), overwrite=overwrite)
        print(f"item {item_id} restored")
    except ValueError as e:
        print(f"error: {e}")
    except FileExistsError as e:
        answer = input(f"warning: {e}. Overwrite? [y/N]: ")
        if answer.strip().lower() == "y":
            try:
                restore_item(int(item_id), overwrite=True)
                print(f"item {item_id} restored")
            except ValueError as e2:
                print(f"error: {e2}")
        else:
            print("aborted")
