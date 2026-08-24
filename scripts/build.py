#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import zipfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT_ROOT / "espuna.tex"
BUILD_DIR = PROJECT_ROOT / "build"
OUT_DIR = PROJECT_ROOT / "out"
DIST_DIR = PROJECT_ROOT / "dist"
OUTPUT = OUT_DIR / "espuna.pdf"
GENERATED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "build",
    "dist",
    "out",
}


def run(command: list[str], cwd: Path | None = None) -> None:
    print("+ " + " ".join(str(part) for part in command))
    subprocess.run(command, cwd=cwd, check=True)


def clean() -> None:
    for path in (BUILD_DIR, OUT_DIR, DIST_DIR):
        if path.exists():
            shutil.rmtree(path)


def build_pdf() -> Path:
    if shutil.which("latexmk") is None:
        raise SystemExit(
            "Required executable 'latexmk' was not found. Install a TeX "
            "distribution with latexmk and pdflatex available on PATH."
        )

    target_build_dir = BUILD_DIR / "latex" / "espuna"
    target_build_dir.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    run(
        [
            "latexmk",
            "-pdf",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            f"-outdir={target_build_dir}",
            SOURCE.name,
        ],
        cwd=PROJECT_ROOT,
    )
    shutil.copy2(target_build_dir / "espuna.pdf", OUTPUT)
    print(f"Wrote {OUTPUT.relative_to(PROJECT_ROOT)}")
    return OUTPUT


def package_release(pdf_path: Path) -> Path:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = DIST_DIR / f"{PROJECT_ROOT.name}-release.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(pdf_path, Path("pdfs") / pdf_path.name)
        for path in PROJECT_ROOT.rglob("*"):
            if not path.is_file():
                continue
            relative_path = path.relative_to(PROJECT_ROOT)
            if any(part in GENERATED_DIRS for part in relative_path.parts):
                continue
            archive.write(path, Path("source") / relative_path)
    print(f"Wrote {zip_path.relative_to(PROJECT_ROOT)}")
    return zip_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the LaTeX PDF.")
    parser.add_argument("--package", action="store_true", help="Create a release zip.")
    parser.add_argument("--clean", action="store_true", help="Clean before building.")
    parser.add_argument(
        "--clean-only", action="store_true", help="Remove generated files and exit."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.clean or args.clean_only:
        clean()
    if args.clean_only:
        return

    pdf_path = build_pdf()
    if args.package:
        package_release(pdf_path)


if __name__ == "__main__":
    main()
