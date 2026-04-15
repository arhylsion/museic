import argparse
import sys
import os
from museic.utils.helpers import get_wsl_path

def cmd_extend(args):
    from museic.core.extender import process_extension
    path = get_wsl_path(args.input)
    if not os.path.exists(path):
        print("Error Input file not found")
        sys.exit(1)
        
    print(f"Executing target {os.path.basename(path)}")
    try:
        out = process_extension(
            input_path=path,
            start_sec=args.start,
            end_sec=args.end,
            auto=args.auto,
            repeat=args.repeat
        )
        print(f"Output finalized {out}")
    except Exception as e:
        print(f"Core Error {e}")
        sys.exit(1)

def cmd_separate(args):
    from museic.core.separator import process_separation
    path = get_wsl_path(args.input)
    if not os.path.exists(path):
        print("Error Input file not found")
        sys.exit(1)
        
    print(f"Executing target {os.path.basename(path)}")
    try:
        out_dir = process_separation(
            input_path=path,
            start_sec=args.start,
            end_sec=args.end,
            target_format=args.export
        )
        print(f"Output finalized {out_dir}")
    except Exception as e:
        print(f"Core Error {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        prog="museic",
        description="High performance audio manipulation utility",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", metavar="command")

    ep = subparsers.add_parser("extend", help="Extend an audio track")
    ep.add_argument("-i", "--input", required=True, metavar="FILE")
    ep.add_argument("-s", "--start", type=float, default=0.0, metavar="SEC")
    ep.add_argument("-e", "--end", type=float, default=0.0, metavar="SEC")
    ep.add_argument("-r", "--repeat", type=int, default=2, metavar="N")
    ep.add_argument("--auto", action="store_true")

    sp = subparsers.add_parser("separate", help="Isolate stems in efficient mode")
    sp.add_argument("-i", "--input", required=True, metavar="FILE")
    sp.add_argument("-s", "--start", type=float, default=0.0, metavar="SEC")
    sp.add_argument("-e", "--end", type=float, default=10.0, metavar="SEC")
    sp.add_argument("--export", choices=["wav", "mp3", "ogg"], default="mp3")

    args = parser.parse_args()

    if args.command == "extend":
        cmd_extend(args)
    elif args.command == "separate":
        cmd_separate(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()