#!/usr/bin/env python3
"""Install the public job-application workflow into another project."""

import argparse
from pathlib import Path
import shutil


SOURCE = Path(__file__).resolve().parents[1]
ROOT_FILES = (
    "AGENTS.md", "instruction.md", "shared-rules.md", "README.md", ".gitignore",
    "requirements.txt", "config.example.json",
    ".codex/config.toml", ".codex/hooks.json",
)


def bundle_files():
    files = [SOURCE / name for name in ROOT_FILES]
    for directory in (".agents/skills", ".codex/agents", ".codex/hooks", "scripts"):
        for item in (SOURCE / directory).rglob("*"):
            if "__pycache__" in item.parts or item.suffix == ".pyc":
                continue
            if item.is_symlink():
                raise ValueError(f"Source symlink is not supported: {item}")
            if item.is_file():
                files.append(item)
    files.extend(p for p in (SOURCE / "formatter").iterdir() if p.suffix in (".py", ".md"))
    return sorted(files)


def install(target):
    target = target.resolve(strict=True)
    if not target.is_dir():
        raise ValueError("Target must be an existing project directory.")
    pending = []
    for source in bundle_files():
        if source.is_symlink():
            raise ValueError(f"Source symlink is not supported: {source}")
        relative = source.relative_to(SOURCE)
        destination = target
        for part in relative.parts:
            destination /= part
            if destination.is_symlink():
                raise ValueError(f"Destination symlink: {relative}")
            if destination != target / relative and destination.exists() and not destination.is_dir():
                raise ValueError(f"Conflicting directory: {relative}")
        if destination.exists():
            if not destination.is_file() or destination.read_bytes() != source.read_bytes():
                raise ValueError(f"Conflicting file: {relative}. Reconcile it before installing.")
        else:
            pending.append((source, destination))

    # Preflight every file before copying, preserving customized projects on conflict.
    for source, destination in pending:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as output:
            output.write(source.read_bytes())
        shutil.copymode(source, destination)
    print(f"Installed job workflow in {target} ({len(pending)} new files).")
    print("Next: follow README.md to create the Python environment and local config.")
    print("Codex hooks require a Git repository; initialize one if needed, then start a new Codex session.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="existing target project directory")
    args = parser.parse_args()
    try:
        install(args.project)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Installation failed: {error}\n")


if __name__ == "__main__":
    main()
