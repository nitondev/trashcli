from trashcli.trash import restore_item


def cmd_restore(item_id: str) -> None:
    try:
        restore_item(int(item_id))
        print(f"item {item_id} restored")
    except ValueError as e:
        print(f"error: {e}")
    except FileExistsError as e:
        print(f"error: {e}")
