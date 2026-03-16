from trashcli.trash import list_trash


def cmd_list() -> None:
    items = list_trash()
    if not items:
        print("trash is empty")
        return
    print(f"{'ID':<4} {'NAME':<30} {'DELETED'}")
    for item in items:
        deleted = item["deleted"][:10] if item["deleted"] else ""
        print(f"{item['id']:<4} {item['name']:<30} {deleted}")
