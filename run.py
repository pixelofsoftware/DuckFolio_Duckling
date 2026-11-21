#!/usr/bin/env python3
"""Uruchom aplikację lub testy zbudowane przez build.py."""

import argparse
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", type=Path, default=ROOT / "build")
    parser.add_argument("--mode", choices=("native", "dvm"), default="native")
    parser.add_argument("--target", choices=("app", "tests"), default="app")
    parser.add_argument("--workdir", type=Path,
                        help="Katalog roboczy programu; domyślnie katalog budowy.")
    args = parser.parse_args()
    output = args.build.resolve()
    try:
        report_path = output / "budowa.json"
        if not report_path.is_file():
            raise ValueError(f"brak {report_path}; najpierw uruchom build.py.")
        report = json.loads(report_path.read_text(encoding="utf-8"))
        if not report.get("ok"):
            raise ValueError("budowa nie zakończyła się poprawnie.")
        command = report["commands"].get(f"{args.target}-{args.mode}")
        if command is None:
            raise ValueError(f"budowa nie zawiera {args.target} w trybie {args.mode}; "
                             "zbuduj je przez build.py z opcjami --target i --mode.")
        cwd = args.workdir.resolve() if args.workdir else output
        return subprocess.run(command, cwd=cwd).returncode
    except (OSError, ValueError) as error:
        parser.exit(1, f"Nie można uruchomić: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
