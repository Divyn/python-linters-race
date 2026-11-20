# 3 Python linters on the same 376 files

ruff, flake8 and pylint each linted the same unpacked source tree: 376 Python files from pinned sdists (requests 2.32.3, urllib3 2.3.0, idna 3.10, charset-normalizer 3.4.1, httpx 0.28.1, httpcore 1.0.7, anyio 4.8.0, certifi 2024.12.14). Defaults, ruff with `--no-cache`, pylint with recursive yes and score off.

Score: seconds to finish, median of 3 runs. Lower is faster.

A non-zero exit is a findings report, not a failed run: ruff and flake8 may exit 0 or 1, pylint may exit 0 to 31.

| Linter | Seconds | Last exit |
|---|---|---|
| ruff 0.17.6 | 0.392721 | 1 |
| flake8 7.5.0 | 16.101970 | 1 |
| pylint 4.1.4 | 93.350376 | 30 |

flake8 / ruff = 41.0. pylint / ruff = 237.7. pylint / flake8 = 5.80.

Run 2026-11-20, 11:17 UTC, on a Vultr vc2-1c-1gb server (1 vCPU, 961 MB RAM, Intel Broadwell), Seattle, Debian 13, Python 3.13.5.

- `setup.sh`: creates a venv, installs the three linters, and unpacks the pinned sdists into `target/`.
- `lint_race.py`: the race.
- `results/`: raw output, logs, package versions, hardware and the file count.

## Run it yourself

1. Make a fresh Debian 13 server (these runs used Vultr `vc2-1c-1gb`: 1 vCPU, 1 GB, $5 a month).
2. Copy this folder to `/root/exp` on it, then run `cd /root/exp && sh run.sh`.
3. `run.sh` writes its state to `STATUS` (SETTING_UP, RUNNING, DONE, or SETUP_FAILED / RUN_FAILED). When it says DONE, the results are in `results.csv` and `run.log`.
