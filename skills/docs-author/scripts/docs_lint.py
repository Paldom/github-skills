#!/usr/bin/env python3
"""Deterministic structure lint for a Markdown documentation tree.

Checks the mechanical rules from the docs playbook — everything judgment-free:

  ERRORS  (exit 1): missing/empty docs dir; no index page; broken relative
          links/images between files.
  WARNS   (exit 0): orphan pages (unreachable from index, other pages, or any
          generator nav config); >2 directory levels of nesting; non
          lowercase-hyphen filenames; zero/multiple H1s; skipped heading
          levels; emphasis over ~10% of a page's prose.

Not checked here: external URLs (use lychee in CI), anchor fragments,
site-root-absolute links like `/api/foo` (route-space, not file-space), prose
style (use Vale). Directories starting with `_` or `.` are generator-owned and
skipped.

Usage: python3 docs_lint.py [docs-dir]   (default: docs)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*(?:<([^>]+)>|([^)\s]+))")
FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^(#{1,6})\s+\S")
BOLD_RE = re.compile(r"(\*\*[^*]+\*\*|__[^_]+__)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
FILENAME_RE = re.compile(r"^[a-z0-9][a-z0-9.-]*$")
ROOT_NAV_NAMES = (
    "mkdocs.yml", "mkdocs.yaml", "sidebars.js", "sidebars.ts",
    "docusaurus.config.js", "docusaurus.config.ts", "astro.config.mjs",
    "astro.config.ts", "conf.py", "_sidebar.md", "SUMMARY.md",
)
VITEPRESS_NAV_NAMES = ("config.ts", "config.mts", "config.js")

errors: list[str] = []
warnings: list[str] = []


def strip_fences(text: str) -> list[str]:
    """Blank fenced code blocks, keeping line numbers.

    Tracks the opening fence's char and length so a ```` block containing
    literal ``` lines (how docs show fenced examples) doesn't toggle early;
    a fence closes only on the same char at >= the opening length.
    """
    out: list[str] = []
    fence: tuple[str, int] | None = None
    for line in text.splitlines():
        m = FENCE_OPEN_RE.match(line)
        if fence is None:
            if m:
                fence = (m.group(1)[0], len(m.group(1)))
                out.append("")
            else:
                out.append(line)
        else:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1] \
                    and not line.strip(fence[0] + " "):
                fence = None
            out.append("")
    return out


def md_files(root: Path) -> list[Path]:
    files = []
    for p in sorted(root.rglob("*.md")):
        rel = p.relative_to(root)
        if any(part.startswith(("_", ".")) for part in rel.parts[:-1]):
            continue
        files.append(p)
    return files


def rel_link_targets(path: Path, lines: list[str]):
    for line in lines:
        for m in LINK_RE.finditer(line):
            target = m.group(1) or m.group(2)
            if target.startswith(("http://", "https://", "mailto:", "#", "data:", "/")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            yield (path.parent / target).resolve()


def nav_config_text(root: Path) -> str:
    """Concatenated text of any generator nav/config near the docs tree."""
    candidates = [base / name for base in (root, root.parent) for name in ROOT_NAV_NAMES]
    candidates += [base / ".vitepress" / name
                   for base in (root, root.parent) for name in VITEPRESS_NAV_NAMES]
    chunks = []
    for p in candidates:
        if p.is_file():
            try:
                chunks.append(p.read_text(encoding="utf-8", errors="replace"))
            except OSError:
                pass
    return "\n".join(chunks)


def check_page(path: Path, root: Path) -> None:
    rel = path.relative_to(root)
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = strip_fences(text)

    if len(rel.parts) > 3:  # file more than 2 dirs below root
        warnings.append(f"WARN  {rel}: nested {len(rel.parts) - 1} levels deep — keep the tree at most 2 levels")
    if not FILENAME_RE.match(path.name):
        warnings.append(f"WARN  {rel}: filename not lowercase-with-hyphens")

    levels = [len(m.group(1)) for ln in lines if (m := HEADING_RE.match(ln))]
    h1s = levels.count(1)
    if h1s == 0:
        warnings.append(f"WARN  {rel}: no H1 — every page needs exactly one title")
    elif h1s > 1:
        warnings.append(f"WARN  {rel}: {h1s} H1s — one concept, one page, one title")
    for a, b in zip(levels, levels[1:]):
        if b > a + 1:
            warnings.append(f"WARN  {rel}: heading level jumps h{a} -> h{b} — screen readers and outlines break")
            break

    prose = INLINE_CODE_RE.sub("", "\n".join(lines))
    total = len(re.sub(r"\s", "", prose))
    if total > 400:
        bold = sum(len(m.group(0)) for m in BOLD_RE.finditer(prose))
        if bold / total > 0.10:
            warnings.append(f"WARN  {rel}: ~{bold * 100 // total}% of the page is emphasized — past ~10% nothing stands out")

    for target in rel_link_targets(path, lines):
        if not target.exists():
            try:
                shown = target.relative_to(root.resolve())
            except ValueError:
                shown = target
            errors.append(f"ERROR {rel}: broken relative link -> {shown}")


def check_orphans(root: Path, files: list[Path]) -> None:
    index = next((root / n for n in ("index.md", "README.md") if (root / n).is_file()), None)
    if index is None:
        errors.append(f"ERROR {root}: no index.md or README.md at the docs root — Pages needs an entry file")

    linked: set[Path] = set()
    for f in files:
        for t in rel_link_targets(f, strip_fences(f.read_text(encoding="utf-8", errors="replace"))):
            linked.add(t)
    nav = nav_config_text(root)
    for f in files:
        if f == index:
            continue
        if f.resolve() in linked:
            continue
        rel = f.relative_to(root)
        # Nav configs name pages by path ("guides/setup.md") or as a quoted
        # extensionless id ('guides/setup', link: '/guides/setup'). A bare
        # substring match on the id would let "api" hide inside "api-docs".
        page_id = rel.with_suffix("").as_posix()
        quoted = any(q in nav for q in (f"'{page_id}'", f'"{page_id}"', f"'/{page_id}'", f'"/{page_id}"'))
        if f.name in nav or rel.as_posix() in nav or quoted:
            continue
        warnings.append(f"WARN  {rel}: orphan — not linked from any page or nav config; unreachable content rots")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "docs")
    if not root.is_dir():
        print(f"ERROR {root}: not a directory", file=sys.stderr)
        return 1
    files = md_files(root)
    if not files:
        print(f"ERROR {root}: no Markdown files found", file=sys.stderr)
        return 1
    for f in files:
        check_page(f, root)
    check_orphans(root, files)
    for line in errors + warnings:
        print(line, file=sys.stderr)
    print(f"{'FAIL' if errors else 'OK'}: {len(errors)} error(s), {len(warnings)} warning(s) across {len(files)} page(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
