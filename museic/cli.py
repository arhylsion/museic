import argparse
import sys
import subprocess
from museic.core.extender import process_extension
from museic.core.separator import process_separation
from museic.tui import run_tui
from museic.utils.helpers import get_wsl_path

def get_wsl_path(path):
    """Helper to convert Windows paths to WSL paths dynamically."""
    if path and ":\\" in path:
        try:
            return subprocess.check_output(["wslpath", path]).decode().strip()
        except Exception:
            # Fallback if wslpath tool is missing
            drive = path[0].lower()
            remainder = path[3:].replace("\\", "/")
            return f"/mnt/{drive}/{remainder}"
    return path

def main():
    """Main entry point for the Museic CLI."""
    parser = argparse.ArgumentParser(
        description="Museic CLI: Advanced Audio Manipulation Tool",
        prog="museic"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command 1: TUI (Terminal User Interface)
    tui_parser = subparsers.add_parser("tui", help="Launch the interactive Terminal UI")

    # Command 2: Extend Track
    extend_parser = subparsers.add_parser("extend", help="Extend an audio track")
    extend_parser.add_argument("-i", "--input", required=True, help="Path to input audio file")
    extend_parser.add_argument("-s", "--start", type=float, help="Start time in seconds")
    extend_parser.add_argument("-e", "--end", type=float, help="End time in seconds")
    extend_parser.add_argument("--auto", action="store_true", help="Auto-detect chorus to extend")

    # Command 3: Separate Stems
    sep_parser = subparsers.add_parser("separate", help="Separate stems using Demucs")
    sep_parser.add_argument("-i", "--input", required=True, help="Path to input audio file")
    sep_parser.add_argument("-s", "--start", type=float, default=0.0, help="Start time in seconds (for targeted slicing)")
    sep_parser.add_argument("-e", "--end", type=float, default=10.0, help="End time in seconds (for targeted slicing)")
    sep_parser.add_argument("--export", choices=['wav', 'mp3', 'ogg'], default='mp3', help="Output format (default: mp3)")

    # Parse arguments
    args = parser.parse_args()

    # Pre-process: Handle Windows paths automatically for WSL compatibility
    if hasattr(args, 'input') and args.input:
        args.input = get_wsl_path(args.input)

    # Routing the commands
    if args.command == "tui":
        run_tui()
        sys.exit(0)
    
    elif args.command == "extend":
        print(f"[*] Initializing Extension pipeline for: {args.input}")
        try:
            process_extension(
                input_path=args.input,
                start_sec=args.start,
                end_sec=args.end,
                auto=args.auto
            )
        except Exception as e:
            print(f"[!] Extension Failed: {e}")

    elif args.command == "separate":
        print(f"[*] Initializing Separation pipeline for: {args.input}")
        try:
            # Slicing parameters are passed to maintain <100MB RAM and <30s runtime
            process_separation(
                input_path=args.input,
                start_sec=args.start,
                end_sec=args.end,
                target_format=args.export
            )
        except Exception as e:
            print(f"[!] Separation Failed: {e}")

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()