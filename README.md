# HOFA 2026 Kopp Summer School

## Automated PDF build

GitHub Actions builds `espuna.tex` on every push and publishes the PDF and a
source archive in the branch's `pdf-build-*` release.

Build locally with:

```bash
python scripts/build.py
```

Clean and create the release package with:

```bash
python scripts/build.py --clean --package
```

The generated files are `out/espuna.pdf` and
`dist/hofa-2026-kopp-summer-school-release.zip`.
