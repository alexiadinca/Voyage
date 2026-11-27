#!/usr/bin/env python3
"""
Voyage – one-command development environment setup.

    Windows:        python setup.py
    macOS / Linux:  python3 setup.py

What it does (safe to run again at any time, e.g. after `git pull`):
  1. Checks that Python 3.12+, Node.js 20.9+, npm and git are installed.
  2. Creates the Python virtual environment in .venv/ and installs requirements.txt.
  3. Installs the frontend packages from frontend/package-lock.json (npm ci).
  4. Downloads the Playwright browser used for end-to-end tests.
  5. Creates backend/.env and frontend/.env.local from the .example templates
     (existing files are never overwritten).
  6. Runs the backend and frontend smoke tests to prove everything works.

Options:
  --skip-browsers   do not download the Playwright browser (~150 MB)
  --skip-tests      do not run the smoke tests at the end
  --recreate-venv   delete .venv and build it again from scratch

Note: this is a plain script, not a setuptools/pip package file.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV = ROOT / ".venv"
FRONTEND = ROOT / "frontend"
BACKEND = ROOT / "backend"
IS_WINDOWS = os.name == "nt"

MIN_PYTHON = (3, 12)
MIN_NODE = (20, 9)

ENV_FILES = [
    (BACKEND / ".env.example", BACKEND / ".env"),
    (FRONTEND / ".env.local.example", FRONTEND / ".env.local"),
]


# --------------------------------------------------------------------------- helpers
def _color(code: str, text: str) -> str:
    if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
        return text
    return f"\033[{code}m{text}\033[0m"


def step(n: int, total: int, msg: str) -> None:
    print("\n" + _color("1;36", f"[{n}/{total}] {msg}"))


def ok(msg: str) -> None:
    print(_color("32", "  OK  ") + msg)


def warn(msg: str) -> None:
    print(_color("33", "  !!  ") + msg)


def fail(msg: str) -> None:
    print("\n" + _color("1;31", "SETUP FAILED: ") + msg)
    sys.exit(1)


def run(cmd: list[str], cwd: Path = ROOT) -> None:
    print(_color("2", "  $ " + " ".join(cmd)))
    try:
        subprocess.run(cmd, cwd=cwd, check=True)
    except subprocess.CalledProcessError as exc:
        fail(f"command exited with code {exc.returncode}: {' '.join(cmd)}")


def tool(name: str) -> str | None:
    """Full path of an executable (handles npm.cmd / npx.cmd on Windows)."""
    return shutil.which(name)


def version_of(cmd: list[str]) -> tuple[int, ...] | None:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    match = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", out)
    return tuple(int(p) for p in match.groups() if p is not None) if match else None


def venv_python() -> Path:
    return VENV / ("Scripts/python.exe" if IS_WINDOWS else "bin/python")


# --------------------------------------------------------------------------- steps
def check_prerequisites() -> dict[str, str]:
    if sys.version_info < MIN_PYTHON:
        fail(
            f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ is required, you are running "
            f"{sys.version.split()[0]}.\n  Install it from https://www.python.org/downloads/ "
            "and run this script with the new version."
        )
    ok(f"Python {sys.version.split()[0]}")

    tools: dict[str, str] = {}
    hints = {
        "node": "Install Node.js LTS from https://nodejs.org/",
        "npm": "npm ships with Node.js – reinstall Node.js from https://nodejs.org/",
        "npx": "npx ships with Node.js – reinstall Node.js from https://nodejs.org/",
        "git": "Install Git from https://git-scm.com/downloads",
    }
    for name, hint in hints.items():
        path = tool(name)
        if not path:
            fail(f"'{name}' was not found on PATH.\n  {hint}\n  Then open a NEW terminal.")
        tools[name] = path

    node_version = version_of([tools["node"], "--version"])
    if not node_version or node_version[:2] < MIN_NODE:
        found = ".".join(map(str, node_version)) if node_version else "unknown"
        fail(
            f"Node.js {MIN_NODE[0]}.{MIN_NODE[1]}+ is required (found {found}).\n"
            "  Install the LTS version from https://nodejs.org/"
        )
    ok(f"Node.js {'.'.join(map(str, node_version))}")
    ok(f"npm {'.'.join(map(str, version_of([tools['npm'], '--version']) or ()))}")
    ok("git " + ".".join(map(str, version_of([tools["git"], "--version"]) or ())))
    return tools


def setup_python(recreate: bool) -> None:
    if recreate and VENV.exists():
        print("  Removing existing .venv ...")
        shutil.rmtree(VENV)

    if not venv_python().exists():
        print("  Creating virtual environment in .venv ...")
        venv.EnvBuilder(with_pip=True, upgrade_deps=False).create(VENV)
    else:
        ok(".venv already exists – reusing it")

    py = str(venv_python())
    run([py, "-m", "pip", "install", "--upgrade", "pip", "--disable-pip-version-check", "-q"])
    run([py, "-m", "pip", "install", "-r", "requirements.txt", "--disable-pip-version-check"])
    ok("Python packages installed")


def setup_frontend(tools: dict[str, str]) -> None:
    lockfile = FRONTEND / "package-lock.json"
    # `npm ci` installs EXACTLY what is in package-lock.json -> identical on every machine.
    run([tools["npm"], "ci" if lockfile.exists() else "install"], cwd=FRONTEND)
    ok("Frontend packages installed")


def setup_playwright(tools: dict[str, str]) -> None:
    run([tools["npx"], "playwright", "install", "chromium"], cwd=FRONTEND)
    ok("Playwright Chromium installed")
    if sys.platform.startswith("linux"):
        warn(
            "On Linux, Playwright may also need system libraries. If e2e tests fail, run:\n"
            "        cd frontend && sudo npx playwright install-deps chromium"
        )


def setup_env_files() -> list[Path]:
    created = []
    for example, target in ENV_FILES:
        rel = target.relative_to(ROOT)
        if target.exists():
            ok(f"{rel} already exists – left unchanged")
        elif example.exists():
            shutil.copyfile(example, target)
            created.append(target)
            ok(f"Created {rel} from {example.name}")
        else:
            warn(f"Template {example.relative_to(ROOT)} is missing – skipped")
    return created


def run_smoke_tests(tools: dict[str, str]) -> None:
    run([str(venv_python()), "-m", "pytest", "-q"])
    run([tools["npm"], "test"], cwd=FRONTEND)
    ok("Backend and frontend tests passed")


# --------------------------------------------------------------------------- main
def main() -> None:
    parser = argparse.ArgumentParser(description="Set up the Voyage development environment.")
    parser.add_argument("--skip-browsers", action="store_true", help="skip Playwright browser")
    parser.add_argument("--skip-tests", action="store_true", help="skip the final smoke tests")
    parser.add_argument("--recreate-venv", action="store_true", help="rebuild .venv from scratch")
    args = parser.parse_args()

    # Flush our messages immediately so they stay in order with pip/npm output.
    sys.stdout.reconfigure(line_buffering=True)
    os.chdir(ROOT)
    print(_color("1", "Voyage – development environment setup"))
    total = 6

    step(1, total, "Checking required tools")
    tools = check_prerequisites()

    step(2, total, "Python virtual environment + requirements.txt")
    setup_python(args.recreate_venv)

    step(3, total, "Frontend packages (Next.js, React, Leaflet, Supabase, test tools)")
    setup_frontend(tools)

    step(4, total, "Playwright browser for end-to-end tests")
    if args.skip_browsers:
        warn("Skipped (--skip-browsers)")
    else:
        setup_playwright(tools)

    step(5, total, "Environment files")
    created_env = setup_env_files()

    step(6, total, "Smoke tests")
    if args.skip_tests:
        warn("Skipped (--skip-tests)")
    else:
        run_smoke_tests(tools)

    activate = r".venv\Scripts\activate" if IS_WINDOWS else "source .venv/bin/activate"
    print("\n" + _color("1;32", "Setup complete!"))
    if created_env:
        print(_color("33", "\nFill in your keys before running the app:"))
        for path in created_env:
            print(f"  - {path.relative_to(ROOT)}")
    print(
        f"""
Run the project (two terminals):

  Backend   {activate}
            cd backend
            uvicorn app.main:app --reload      -> http://localhost:8000/docs

  Frontend  cd frontend
            npm run dev                        -> http://localhost:3000
"""
    )


if __name__ == "__main__":
    main()
