# text-repeat-lines

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-%3E%3D3.9-blue.svg)](https://www.python.org/)

Repeat each input line N times. N can be global (`-n 3`) or read from a
numeric prefix on each line (`3 hello`). Output defaults to blocks
(`A A B B`) and can be round-robin interleaved (`A B A B`).

## Features

- Global repeat count with `-n/--times`
- Per-line counts via `--from-prefix` (`"3 hello"` → `hello` ×3)
- `--interleave` round-robin mode for test-data spreading
- `--json` machine-readable report, `--check` CI validation
- Streams from files or standard input

## Install

```sh
pip install .
# or directly from GitHub
pip install git+https://github.com/TataneSan/text-repeat-lines.git
```

## Usage

```
text-repeat-lines [FILE] [-n TIMES] [--from-prefix] [--interleave]
```

### Examples

Repeat each line three times:

```sh
$ printf 'ping\npong\n' | text-repeat-lines -n 3
ping
ping
ping
pong
pong
pong
```

Per-line counts:

```sh
$ printf '2 error: disk full\n1 ok\n3 retry\n' | text-repeat-lines --from-prefix
error: disk full
error: disk full
ok
retry
retry
retry
```

Interleaved (round-robin) output:

```sh
$ printf '2 a\n3 b\n' | text-repeat-lines -p --interleave
a
b
a
b
b
```

JSON report for pipelines:

```sh
$ printf '2 a\n1 b\n' | text-repeat-lines -p --json
{
  "input_lines": 2,
  "output_lines": 3,
  "times": null,
  "from_prefix": true,
  "interleave": false,
  "invalid_prefix_lines": [],
  "lines": ["a", "a", "b"]
}
```

CI validation of a count-prefixed fixture file:

```sh
text-repeat-lines -p --check -q fixtures.txt || echo "bad prefix"
```

## Exit codes

| Code | Meaning                                             |
|------|-----------------------------------------------------|
| 0    | Success (all prefixes valid, or `--check` not used) |
| 1    | I/O or CLI error                                    |
| 2    | `--check` mode and invalid count prefixes found     |

## License

MIT — see [LICENSE](LICENSE).
