# HOFA 2026 Kopp Summer School

## 45-minute presentation

The Beamer talk proves Jamneshan--Tao Theorem 1.6 through Lemmas 2.5 and
2.6. It includes a visual treatment of Example 2.3, precise statements and
references for the black boxes, and detailed notes unpacking the older
Green--Tao arguments.

Build just the presentation and notes:

```bash
python scripts/build.py --presentation-only
```

The build creates:

- `out/presentation.pdf`: audience slides (27 timed slides, references, five backups).
- `out/presentation-screen.pdf`: the same slides with notes on the right, for a
  PDF presenter that supports a two-screen layout.
- `out/presenter-notes.pdf`: printable notes with slide thumbnails, timing,
  and a preparation appendix containing the longer derivations and source checks.

The planned speaking time is **40 minutes 45 seconds**, leaving 4 minutes
15 seconds for pauses and questions. References and backup slides are not
part of that schedule. Timing checkpoints and suggested cuts are on the
first page of the notes.

Edit slide content and its matching speaker notes together in
[`talk/slides.tex`](talk/slides.tex); optional slides are in
[`talk/backup.tex`](talk/backup.tex). The additional mathematical preparation
is in [`talk/preparation.tex`](talk/preparation.tex). The entry points are
[`presentation.tex`](presentation.tex),
[`presentation-screen.tex`](presentation-screen.tex), and
[`presenter-notes.tex`](presenter-notes.tex). The existing proceedings summary
remains in `espuna.tex`.

Required: Python 3 and a TeX distribution with `pdflatex`, Beamer, TikZ,
Latin Modern, `mathtools`, and `enumitem`. The script uses `latexmk` when
Perl is available, otherwise it runs `pdflatex` twice. Build the audience
deck before compiling the printable notes, which use its PDF thumbnails.

In VS Code, the workspace configures LaTeX Workshop to run `pdflatex` twice,
so Perl is not required. Use **Build LaTeX project** (`Ctrl+Alt+B`); the PDF
is written to `build/vscode/` and previewed in a VS Code tab. This keeps
editor builds separate from PDFs in `out/`, which external viewers may lock
on Windows. Use the Python build script above to refresh `out/`, including
the audience deck needed for the printable notes. Close external viewers
of those PDFs before running the script. If the old recipe is still active, run
**Developer: Reload Window** and build again.

## Automated PDF build

GitHub Actions builds the summary, presentation, and notes on every push and
publishes the four PDFs and a source archive in the branch's `pdf-build-*` release.

Build locally with:

```bash
python scripts/build.py
```

Clean and create the release package with:

```bash
python scripts/build.py --clean --package
```

The generated PDFs are in `out/`. The release archive is
`dist/hofa-2026-kopp-summer-school-release.zip` and contains both PDFs and sources.
