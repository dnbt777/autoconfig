import argparse

from autoconfig.commands import (
    cmd_clone,
    cmd_load,
    cmd_new,
    cmd_rm,
    cmd_save,
    cmd_track,
    cmd_untrack,
)


def main():
    parser = argparse.ArgumentParser(description="Automatically load and switch between configs across your system")
    sub = parser.add_subparsers(dest="command", required=True)

    p_save = sub.add_parser("save", help="Save configs from all tracked locations")
    p_save.add_argument("template")

    p_load = sub.add_parser("load", help="Load configs to all tracked locations")
    p_load.add_argument("template")

    p_track = sub.add_parser("track", help="Track a new path in a template")
    p_track.add_argument("template", help="Template name or 'all'")
    p_track.add_argument("path")

    p_untrack = sub.add_parser("untrack", help="Untrack a path from a template")
    p_untrack.add_argument("template", help="Template name or 'all'")
    p_untrack.add_argument("path")

    p_new = sub.add_parser("new", help="Create a new template")
    p_new.add_argument("template")

    p_rm = sub.add_parser("rm", help="Remove a template")
    p_rm.add_argument("template")

    p_clone = sub.add_parser("clone", help="Clone a template")
    p_clone.add_argument("old_template")
    p_clone.add_argument("new_template")

    args = parser.parse_args()

    if args.command == "save":
        cmd_save(args.template)
    elif args.command == "load":
        cmd_load(args.template)
    elif args.command == "track":
        cmd_track(args.template, args.path)
    elif args.command == "untrack":
        cmd_untrack(args.template, args.path)
    elif args.command == "new":
        cmd_new(args.template)
    elif args.command == "rm":
        cmd_rm(args.template)
    elif args.command == "clone":
        cmd_clone(args.old_template, args.new_template)


if __name__ == "__main__":
    main()
