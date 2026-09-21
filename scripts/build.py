#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import zipfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCES = ("espuna", "presentation", "presentation-screen", "presenter-notes", "exposition")
BUILD_DIR = PROJECT_ROOT / "build"
OUT_DIR = PROJECT_ROOT / "out"
DIST_DIR = PROJECT_ROOT / "dist"
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


def build_pdf(stem: str) -> Path:
    if shutil.which("pdflatex") is None:
        raise SystemExit(
            "Required executable 'pdflatex' was not found. Install a TeX "
            "distribution with Beamer, TikZ, and Latin Modern fonts."
        )

    target_build_dir = BUILD_DIR / "latex" / stem
    target_build_dir.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # MiKTeX exposes latexmk.exe even when its required Perl engine is absent.
    # These documents need no BibTeX or external graphics-generation passes.
    if shutil.which("latexmk") and shutil.which("perl"):
        run(
            ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
             "-file-line-error", f"-outdir={target_build_dir}", f"{stem}.tex"],
            cwd=PROJECT_ROOT,
        )
    else:
        for _ in range(2):
            run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                 "-file-line-error", f"-output-directory={target_build_dir}",
                 f"{stem}.tex"],
                cwd=PROJECT_ROOT,
            )
    output = OUT_DIR / f"{stem}.pdf"
    shutil.copy2(target_build_dir / f"{stem}.pdf", output)
    print(f"Wrote {output.relative_to(PROJECT_ROOT)}")
    return output


def package_release(pdf_paths: list[Path]) -> Path:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = DIST_DIR / f"{PROJECT_ROOT.name}-release.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for pdf_path in pdf_paths:
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
    parser = argparse.ArgumentParser(description="Build the summary, slides, notes, and exposition.")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument(
        "--presentation-only", action="store_true",
        help="Build the audience deck, two-screen deck, and print-friendly notes only.",
    )
    selection.add_argument(
        "--exposition-only", action="store_true",
        help="Build only the standalone mathematical exposition.",
    )
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

    if args.exposition_only:
        sources = ("exposition",)
    elif args.presentation_only:
        sources = SOURCES[1:4]
    else:
        sources = SOURCES
    # The notes include thumbnails from out/presentation.pdf, so keep this order.
    pdf_paths = [build_pdf(stem) for stem in sources]
    if args.package:
        package_release(pdf_paths)


if __name__ == "__main__":
    main()
