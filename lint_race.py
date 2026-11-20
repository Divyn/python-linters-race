"""Lint the same unpacked source tree with ruff, flake8 and pylint.

Score: seconds to finish, median of 3 runs.
A non-zero exit from a linter is a findings report, not a failed run.
"""
import statistics
import subprocess
import sys
import time
from pathlib import Path

TARGET = "/root/exp/target"
RUNS = 3
PYBIN = str(Path(sys.executable).parent)

CMDS = {
    "ruff": [PYBIN + "/ruff", "check", TARGET, "--no-cache"],
    "flake8": [PYBIN + "/flake8", TARGET],
    "pylint": [PYBIN + "/pylint", TARGET, "--recursive=y", "--score=n"],
}


def run_once(name: str) -> tuple:
    start = time.perf_counter()
    res = subprocess.run(CMDS[name], capture_output=True, text=True)
    elapsed = time.perf_counter() - start
    code = res.returncode
    ok = False
    if name == "ruff" and code in (0, 1):
        ok = True
    elif name == "flake8" and code in (0, 1):
        ok = True
    elif name == "pylint" and 0 <= code < 32:
        ok = True
    if not ok:
        sys.stderr.write(res.stderr[-2000:] + "\n")
        raise SystemExit("%s exited %s" % (name, code))
    return elapsed, code


def main() -> None:
    count_path = Path("/root/exp/file_count.txt")
    nfiles = count_path.read_text().strip() if count_path.exists() else "?"
    print("# python_files=%s" % nfiles)
    print("name,median_seconds,run1,run2,run3,last_exit")
    for name in ("ruff", "flake8", "pylint"):
        times = []
        code = 0
        for _ in range(RUNS):
            secs, code = run_once(name)
            times.append(secs)
        med = statistics.median(times)
        runs = ",".join("%.6f" % t for t in times)
        print("%s,%.6f,%s,%s" % (name, med, runs, code), flush=True)


if __name__ == "__main__":
    main()
