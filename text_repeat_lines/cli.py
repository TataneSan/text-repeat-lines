"""text_repeat_lines - repeat each input line a fixed number of times.

Multiplies lines N times (like a per-line `yes`), with an optional blank
separator line between repetitions and per-line numbering. Reads a file or
stdin.

Exit codes:
  0  success
  1  I/O or CLI error
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def read_lines(path: str | None) -> tuple[str, list[str]]:
    if path in (None, "-"):
        return "<stdin>", sys.stdin.read().splitlines()
    p = Path(path)
    try:
        return str(p), p.read_text(encoding="utf-8").splitlines()
    except OSError as e:
        raise SystemExit(f"error: cannot read {p}: {e}")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="text-repeat-lines",
        description="Repeat each input line N times.",
    )
    ap.add_argument("file", nargs="?", default=None,
                    help="input file (default: stdin)")
    ap.add_argument("-n", "--times", type=int, default=2,
                    help="number of repetitions per line (default: 2)")
    ap.add_argument("-s", "--separator", default=None,
                    help="separator line inserted between repetitions")
    ap.add_argument("--number", action="store_true",
                    help="prefix each repetition with its 1-based index")
    ap.add_argument("--number-format", default="{i}: ",
                    help="prefix template with --number, {i} placeholder "
                         "(default: '{i}: ')")
    ap.add_argument("--json", action="store_true", help="JSON report on stderr")
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.times < 1:
        raise SystemExit("error: --times must be >= 1")

    name, lines = read_lines(args.file)

    out: list[str] = []
    for line in lines:
        for i in range(1, args.times + 1):
            body = line
            if args.number:
                body = args.number_format.replace("{i}", str(i)) + line
            out.append(body)
            if args.separator is not None and i < args.times:
                out.append(args.separator)

    sys.stdout.write("\n".join(out))
    if out:
        sys.stdout.write("\n")

    if args.json:
        print(json.dumps({
            "file": name, "input_lines": len(lines),
            "times": args.times, "output_lines": len(out),
        }), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
