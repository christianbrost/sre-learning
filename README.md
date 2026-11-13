# sre-learning

small python scripts for learning python as a scripting language for sre / automation work. covers venv, `pathlib`, `argparse` and `logging`. the scripts only use the standard library.

## setup

1. create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   (`requirements.txt` is left over from venv practice, the scripts themselves don't need it)

## scripts

- `inventar.py` – counts the files in a folder by extension
  ```bash
  python inventar.py testdaten
  ```
- `aufraeumen.py` – sorts the files in a folder into category subfolders (`bilder`, `dokumente`, `archive`, `sonstiges`) based on their extension
  ```bash
  python aufraeumen.py spielwiese --dry-run
  python aufraeumen.py spielwiese
  ```

both scripts take the same flags:

- `-i`, `--include-hidden` – also include hidden files (names starting with `.`)
- `-v`, `--verbose` – debug logging (why a file was skipped etc.)

`aufraeumen.py` additionally has `-d`, `--dry-run` – only show what would be moved, change nothing.

`aufraeumen.py` imports `list_files` from `inventar.py`, so the filtering logic only exists once.

## example

```
$ python aufraeumen.py spielwiese --dry-run
INFO     folder spielwiese will be sorted
INFO     Proceeding with dry run
INFO     [DRY-RUN] would move spielwiese/urlaub.JPG -> spielwiese/bilder/urlaub.JPG
INFO     [DRY-RUN] would move spielwiese/backup.tar.gz -> spielwiese/archive/backup.tar.gz
INFO     [DRY-RUN] would move spielwiese/README -> spielwiese/sonstiges/README
INFO     [DRY-RUN] would move spielwiese/foto.jpg -> spielwiese/bilder/foto.jpg
INFO     [DRY-RUN] would move spielwiese/bericht.pdf -> spielwiese/dokumente/bericht.pdf
INFO     [DRY-RUN] would move spielwiese/notizen.txt -> spielwiese/dokumente/notizen.txt
INFO     [DRY-RUN] would move spielwiese/scan.PDF -> spielwiese/dokumente/scan.PDF
INFO     Skipped 0, would move 7
```

(timestamps removed)

## safety

- `--dry-run` goes through the exact same code as a real run, only the actual move is skipped. so the dry run shows what will really happen
- never overwrites: if a file with the same name already exists in the target folder, it logs a warning and skips the file
- hidden files are skipped unless `-i` is set
- only files directly in the folder are touched, subfolders are left alone. running the script twice does nothing the second time
- logs go to stderr, results to stdout, so `python inventar.py testdaten > report.txt` only saves the result

for testing, work on a copy instead of `testdaten`:

```bash
rm -rf spielwiese && cp -r testdaten spielwiese
```

## known limitations

- only the last extension counts (`backup.tar.gz` is treated as `.gz`)
- categories are hardcoded in `CATEGORIES` at the top of `aufraeumen.py`
- errors during moving (e.g. missing permissions) aren't caught yet, the script stops at the first one
- folder names are german (`bilder`, `dokumente`, ...), everything else is english
