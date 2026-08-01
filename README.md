# text-repeat-lines

Repeat each input line a fixed number of times.

Zero-dependency CLI. Like a per-line `yes` — useful for generating test
data, duplicating configuration entries or padding sample files.

## Features

- `-n/--times N` repetitions per line (default: 2)
- `-s/--separator S` separator line inserted between repetitions
- `--number` prefixes each repetition with its index
- `--number-format` custom prefix template with `{i}` placeholder
- File or stdin input, `--json` statistics report

## Install

```bash
pip install .
# or
pip install git+https://github.com/TataneSan/text-repeat-lines.git
```

## Usage

```bash
# duplicate every line
text-repeat-lines names.txt

# repeat each line 3 times
printf 'a\nb\n' | text-repeat-lines -n 3

# with a separator between repetitions
echo 'ping 8.8.8.8' | text-repeat-lines -n 2 -s 'sleep 1'

# numbered repetitions
echo 'task' | text-repeat-lines -n 3 --number
# 1: task
# 2: task
# 3: task
```

## Exit codes

| Code | Meaning          |
|------|------------------|
| 0    | success          |
| 1    | I/O or CLI error |

## License

MIT
