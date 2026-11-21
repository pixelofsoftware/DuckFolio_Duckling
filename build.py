#!/usr/bin/env python3
"""Zbuduj aplikację i testy; komendy uruchomienia zapisz w budowa.json."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parent
TEST_ENTRY = ROOT / "tests/testy.dk"
REPORT = "budowa.json"


def execute(command, cwd):
    command = [str(part) for part in command]
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=180)


def find_tool(path, name, option):
    """Zwróć ścieżkę podaną wprost albo narzędzie z PATH (instalacja według tutoriala)."""
    if path is None:
        found = shutil.which(name)
        if found is None:
            raise ValueError(f"Nie znaleziono {name} w PATH. Zainstaluj Ducklinga według "
                             f"tutoriala albo wskaż narzędzie przez {option}.")
        path = Path(found)
    path = path.resolve()
    if not path.is_file():
        raise ValueError(f"Nie znaleziono {name}: {path}")
    return path


def version(tool, option):
    result = execute([tool, option], ROOT)
    if result.returncode != 0:
        raise ValueError(f"{tool} {option} zwrócił kod {result.returncode}:\n{result.stderr}")
    return result.stdout


def prepare_output(output):
    """Usuń poprzednią budowę albo pusty katalog; katalogu z innymi plikami nie ruszaj."""
    if output.is_dir() and ((output / REPORT).is_file() or not any(output.iterdir())):
        shutil.rmtree(output)
    elif output.exists():
        raise ValueError(f"{output} nie jest katalogiem budowy; wybierz inny --output.")
    output.mkdir(parents=True)


def package(output, target):
    """Zwróć katalog pakietu: źródła aplikacji albo ich kopię z punktem wejścia testów."""
    if target == "app":
        return ROOT / "app"
    path = output / "pakiet-testow" / "app"
    shutil.copytree(ROOT / "app", path)
    shutil.copy2(TEST_ENTRY, path / "app.dk")
    return path


def build(args):
    modes = ("native", "dvm") if args.mode == "both" else (args.mode,)
    targets = ("app", "tests") if args.target == "all" else (args.target,)
    duckc = find_tool(args.duckc, "duckc", "--duckc")
    vm = find_tool(args.vm, "VM_tc", "--vm") if "dvm" in modes else None
    report = {"ok": False, "tools": {}, "compilation": {}, "commands": {}}
    report["tools"]["duckc"] = version(duckc, "--version-verbose")
    if vm:
        report["tools"]["VM"] = version(vm, "--version")

    output = args.output.resolve()
    prepare_output(output)
    try:
        for target in targets:
            source = package(output, target)
            for mode in modes:
                name = f"{target}-{mode}"
                artifacts = output / name
                command = [duckc, "compile_package", source, "-n", "app", "-a", artifacts,
                           "--custom-std-artifacts-path", output / "std"]
                if args.std:
                    command += ["--custom-std-path", args.std.resolve()]
                if mode == "dvm":
                    command.append("--dvm-backend")
                result = execute(command, output)
                report["compilation"][name] = result.stderr + result.stdout
                binary = artifacts / ("package_dvm.dbc" if mode == "dvm" else "package_llvm.exe")
                passed = result.returncode == 0 and binary.is_file()
                print(("PASS " if passed else "FAIL ") + name, flush=True)
                if not passed:
                    raise ValueError(f"kompilacja {name} nie powiodła się.\n"
                                     f"{result.stderr}{result.stdout}")
                run = [vm, "run", binary] if mode == "dvm" else [binary]
                report["commands"][name] = [str(part) for part in run]
        report["ok"] = True
    finally:
        text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        (output / REPORT).write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duckc", type=Path, help="Kompilator; domyślnie duckc z PATH.")
    parser.add_argument("--vm", type=Path, help="Maszyna DVM; domyślnie VM_tc z PATH.")
    parser.add_argument("--std", type=Path,
                        help="Źródła zgodnej biblioteki standardowej, jeśli nie są ustawione "
                             "w duckc.")
    parser.add_argument("--mode", choices=("native", "dvm", "both"), default="native")
    parser.add_argument("--target", choices=("app", "tests", "all"), default="app")
    parser.add_argument("--output", type=Path, default=ROOT / "build",
                        help="Katalog wyników; poprzednia budowa w nim zostanie zastąpiona.")
    args = parser.parse_args()
    try:
        build(args)
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        parser.exit(1, f"Błąd budowania: {error}\n")


if __name__ == "__main__":
    main()
