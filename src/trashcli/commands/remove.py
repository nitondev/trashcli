from trashcli.trash import delete_item


def cmd_remove(item_id: str) -> None:
    try:
        delete_item(int(item_id))
        print(f"item {item_id} permanently deleted")
    except ValueError as e:
        print(f"error: {e}")
