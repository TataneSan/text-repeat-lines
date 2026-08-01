#!/usr/bin/env python3
"""text-repeat-lines: repeat each input line N times.

Two repeat sources:

* global ``-n/--times N`` — every line is emitted N times;
* a per-line count taken from the line itself, e.g. "3 hello" — the
  numeric prefix is stripped and the remainder is emitted 3 times.

Blocks (all copies of line 1, then line 2, ...) are the default;
``--interleave`` round-robins one copy of each line until every count is
exhausted.

Exit codes:
    0  Success (all per-line counts valid, or --check not used).
    1  I/O or CLI error.
    2  --check mode and at least one per-line count prefix is invalid.
"""

import argparse
import json
import sys


def split_prefix(line):
    """Return (count, rest) if line starts with '<int><space>', else None."""
    stripped = line.lstrip()
    num, _, rest = stripped.partition(" ")
    if num.isdigit():
        return int(num), rest
    return None


def expand(pairs, interleave):
    """pairs: list of (text, count). Yield output lines."""
    if not interleave:
        for text, count in pairs:
            for _ in range(count):
                yield text
        return
    remaining = [[text, count] for text, count in pairs if count > 0]
    while remaining:
        nxt = []
        for text, count in remaining:
            yield text
            if count - 1 > 0:
                nxt.append([text, count - 1])
        remaining = nxt


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="text-repeat-lines",
        description="Repeat each input line N times (global -n or per-line "
        "count prefix, optional round-robin interleave).",
    )
    parser.add_argument(
        "file", nargs="?", default="-",
        help="input file (default: stdin; '-' = stdin)",
    )
    parser.add_argument(
        "-n", "--times", type=int, default=2,
        help="repeat count for every line (default: 2)",
    )
    parser.add_argument(
        "-p", "--from-prefix", action="store_true",
        help="read each repeat count from a numeric line prefix "
        "('3 hello' prints 'hello' three times)",
    )
    parser.add_argument(
        "--interleave", action="store_true",
        help="round-robin copies (A,B,A,B,...) instead of blocks (A,A,B,B)",
    )
    parser.add_argument(
        "--json", action="store_true", dest="as_json",
        help="emit a JSON report instead of the repeated lines",
    )
    parser.add_argument(
        "--check", action="store_true",
        help="CI mode: with --from-prefix, exit 2 when a line lacks a "
        "valid numeric prefix",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true",
        help="suppress line output (useful with --check)",
    )
    args = parser.parse_args(argv)

    if args.times < 0:
        print("error: --times must be >= 0", file=sys.stderr)
        return 1

    try:
        if args.file == "-":
            lines = sys.stdin.read().splitlines()
        else:
            with open(args.file, "r", encoding="utf-8") as fh:
                lines = fh.read().splitlines()
    except OSError as exc:
        print("error: cannot read %s: %s" % (args.file, exc), file=sys.stderr)
        return 1

    pairs = []
    bad = []
    if args.from_prefix:
        for i, line in enumerate(lines, 1):
            parsed = split_prefix(line)
            if parsed is None:
                bad.append({"line": i, "content": line})
                pairs.append((line, 0))
            else:
                pairs.append((parsed[1], parsed[0]))
    else:
        pairs = [(line, args.times) for line in lines]

    expanded = list(expand(pairs, args.interleave))

    if args.as_json:
        print(json.dumps({
            "input_lines": len(lines),
            "output_lines": len(expanded),
            "times": args.times if not args.from_prefix else None,
            "from_prefix": args.from_prefix,
            "interleave": args.interleave,
            "invalid_prefix_lines": bad,
            "lines": expanded,
        }, indent=2, ensure_ascii=False))
    elif not args.quiet:
        sys.stdout.write("\n".join(expanded))
        if expanded:
            sys.stdout.write("\n")

    if args.check and bad:
        print("check failed: %d line(s) without a valid count prefix"
              % len(bad), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
