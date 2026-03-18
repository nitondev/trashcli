import sys

sys.dont_write_bytecode = True

import argparse  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trash",
        description="Safely move files to trash",
    )
    parser.add_argument("files", nargs="*", metavar="FILE", help="files to trash")
    parser.add_argument("-ls", action="store_true", help="list trash contents")
    parser.add_argument("-mv", metavar="ID", help="restore file by ID")
    parser.add_argument(
        "-rm", metavar="ID", nargs="?", const="", help="delete file by ID"
    )
    parser.add_argument(
        "--all", action="store_true", help="used with -rm to empty trash"
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="overwrite existing file when restoring (skips prompt)",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.ls:
        from trashcli.commands.list import cmd_list

        cmd_list()
    elif args.mv is not None:
        from trashcli.commands.restore import cmd_restore

        cmd_restore(args.mv, overwrite=args.overwrite)
    elif args.rm is not None:
        if args.all:
            from trashcli.commands.empty import cmd_empty

            cmd_empty()
        else:
            if not args.rm:
                parser.error("-rm requires an ID or --all")
            from trashcli.commands.remove import cmd_remove

            cmd_remove(args.rm)
    elif args.files:
        from trashcli.commands.trash import cmd_trash

        cmd_trash(args.files)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
