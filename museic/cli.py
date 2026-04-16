import argparse
import sys
import os
import difflib
from museic.utils.helpers import get_wsl_path
from museic.core.plugin_manager import load_plugins

def execute_command(func, *args, **kwargs):
    try:
        out = func(*args, **kwargs)
        if out:
            print(f"Output finalized {out}")
    except Exception as e:
        print(f"Core Error {e}")
        sys.exit(1)

def get_custom_help():
    return """
MUSEIC CLI - High Performance Audio Manipulation Utility

Usage: museic <command> [options]

Commands:
  extend    Extend an audio track automatically or manually
            args: -i (input), -s (start), -e (end), -r (repeat), --auto
  
  separate  Isolate stems (vocals & instrumental) in efficient mode
            args: -i (input), -s (start), -e (end), --export (mp3/wav/ogg)
            
  extract   Smart extract the best chorus slice
            args: -i (input), --length (seconds), --export (mp3/wav/ogg)
            
  mix       Auto-duck BGM under voice track
            args: -v (voice), -b (bgm)
            
  optimize  Normalize to broadcast LUFS standards
            args: -i (input), --lufs (target lufs, default: -14.0)
            
  watch     Automated directory monitoring
            args: -d (directory)
            
  enhance   Denoise and boost audio clarity
            args: -i (input), --denoise, --boost

  trim      Auto-remove dead silence from podcasts or voice
            args: -i (input), --aggressive
            
  vibe      Apply social media audio trends
            args: -i (input), --slowed, --nightcore

Examples:
  museic extend -i track.mp3 --auto -r 4
  museic separate -i track.mp3 -s 0 -e 30 --export mp3
  museic vibe -i song.mp3 --slowed
"""

class MuseicParser(argparse.ArgumentParser):
    valid_commands = ["extend", "separate", "extract", "mix", "optimize", "watch", "enhance", "trim", "vibe"]

    def error(self, message):
        if "invalid choice" in message:
            user_cmd = sys.argv[1] if len(sys.argv) > 1 else ""
            matches = difflib.get_close_matches(user_cmd, self.valid_commands, n=1, cutoff=0.5)
            
            print(f"Error Command '{user_cmd}' is invalid")
            if matches:
                print(f"Did you mean: '{matches[0]}'?")
            print("\nRun 'museic --help' to see all available commands.")
        else:
            print(f"Error {message}")
        sys.exit(1)
        
    def print_help(self, file=None):
        print(get_custom_help())

def main():
    if len(sys.argv) == 1 or sys.argv[1] in ["-h", "--help"]:
        print(get_custom_help())
        sys.exit(0)

    parser = MuseicParser(add_help=False)
    subparsers = parser.add_subparsers(dest="command", metavar="command")

    ep = subparsers.add_parser("extend")
    ep.add_argument("-i", "--input", required=True)
    ep.add_argument("-s", "--start", type=float, default=0.0)
    ep.add_argument("-e", "--end", type=float, default=0.0)
    ep.add_argument("-r", "--repeat", type=int, default=2)
    ep.add_argument("--auto", action="store_true")

    sp = subparsers.add_parser("separate")
    sp.add_argument("-i", "--input", required=True)
    sp.add_argument("-s", "--start", type=float, default=0.0)
    sp.add_argument("-e", "--end", type=float, default=10.0)
    sp.add_argument("--export", choices=["wav", "mp3", "ogg"], default="mp3")

    ex = subparsers.add_parser("extract")
    ex.add_argument("-i", "--input", required=True)
    ex.add_argument("--length", type=int, default=30)
    ex.add_argument("--export", choices=["wav", "mp3", "ogg"], default="mp3")

    mx = subparsers.add_parser("mix")
    mx.add_argument("-v", "--voice", required=True)
    mx.add_argument("-b", "--bgm", required=True)

    op = subparsers.add_parser("optimize")
    op.add_argument("-i", "--input", required=True)
    op.add_argument("--lufs", type=float, default=-14.0)

    wt = subparsers.add_parser("watch")
    wt.add_argument("-d", "--dir", required=True)

    en = subparsers.add_parser("enhance")
    en.add_argument("-i", "--input", required=True)
    en.add_argument("--denoise", action="store_true")
    en.add_argument("--boost", action="store_true")

    tr = subparsers.add_parser("trim")
    tr.add_argument("-i", "--input", required=True)
    tr.add_argument("--aggressive", action="store_true")

    vb = subparsers.add_parser("vibe")
    vb.add_argument("-i", "--input", required=True)
    vb.add_argument("--slowed", action="store_true")
    vb.add_argument("--nightcore", action="store_true")

    loaded_plugins = load_plugins(parser, subparsers)
    
    for plugin in loaded_plugins:
        parser.valid_commands.append(plugin["command"])

    args = parser.parse_args()

    plugin_executed = False
    for plugin in loaded_plugins:
        if args.command == plugin["command"]:
            plugin["execute"](args)
            plugin_executed = True
            break
            
    if plugin_executed:
        sys.exit(0)

    if args.command == "extend":
        from museic.core.extender import process_extension
        execute_command(process_extension, input_path=get_wsl_path(args.input), start_sec=args.start, end_sec=args.end, auto=args.auto, repeat=args.repeat)
    elif args.command == "separate":
        from museic.core.separator import process_separation
        execute_command(process_separation, input_path=get_wsl_path(args.input), start_sec=args.start, end_sec=args.end, target_format=args.export)
    elif args.command == "extract":
        from museic.core.extractor import process_extraction
        execute_command(process_extraction, input_path=get_wsl_path(args.input), duration=args.length, export_format=args.export)
    elif args.command == "mix":
        from museic.core.ducker import process_ducking
        execute_command(process_ducking, voice_path=get_wsl_path(args.voice), bgm_path=get_wsl_path(args.bgm))
    elif args.command == "optimize":
        from museic.core.optimizer import process_optimization
        execute_command(process_optimization, input_path=get_wsl_path(args.input), target_lufs=args.lufs)
    elif args.command == "watch":
        from museic.core.watcher import start_watching
        execute_command(start_watching, input_dir=get_wsl_path(args.dir))
    elif args.command == "enhance":
        from museic.core.enhancer import process_enhancement
        execute_command(process_enhancement, input_path=get_wsl_path(args.input), denoise=args.denoise, boost=args.boost)
    elif args.command == "trim":
        from museic.core.trimmer import process_trimming
        execute_command(process_trimming, input_path=get_wsl_path(args.input), aggressive=args.aggressive)
    elif args.command == "vibe":
        from museic.core.vibe import process_vibe
        execute_command(process_vibe, input_path=get_wsl_path(args.input), slowed=args.slowed, nightcore=args.nightcore)

if __name__ == "__main__":
    main()