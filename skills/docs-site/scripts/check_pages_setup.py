#!/usr/bin/env python3
"""Deterministic GitHub Pages setup check for a docs site repo.

Static checks — no network beyond an optional `git ls-remote` fallback to the
repo's own origin. Catches the failure modes that produce a green workflow and
a broken site:

  ERRORS  (exit 1): no Pages publishing detected at all (no Pages workflow
          and no gh-pages branch, locally or on origin); a deploy workflow
          missing the required `pages: write` / `id-token: write` permissions.
  WARNS   (exit 0): deploy step reachable from pull_request triggers; no
          `github-pages` environment; no strict build flag; project-page base
          path missing from the generator config; gh-pages branch without
          `.nojekyll`; CNAME file alongside Actions publishing (ignored there).

Run from the repo root: python3 check_pages_setup.py [repo-root]
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

PAGES_ACTION_RE = re.compile(r"uses:\s*actions/(deploy-pages|upload-pages-artifact)@")
PERM_RES = {
    "pages: write": re.compile(r"pages\s*:\s*write"),
    "id-token: write": re.compile(r"id-token\s*:\s*write"),
}
WRITE_ALL_RE = re.compile(r"permissions\s*:\s*write-all")
STRICT_RE = re.compile(r"--strict|-W\b")

errors: list[str] = []
warnings: list[str] = []


def git(root: Path, *args: str) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True, text=True, timeout=15,
        )
        return out.stdout.strip() if out.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def repo_name(root: Path) -> str:
    url = git(root, "remote", "get-url", "origin")
    m = re.search(r"[:/]([^/:]+)/([^/]+?)(?:\.git)?/?$", url)
    return m.group(2) if m else ""


def gh_pages_ref(root: Path) -> str:
    """Local/remote-tracking gh-pages ref, or 'remote-only', or ''.

    Shallow/single-branch clones have no local ref for a real remote branch —
    fall back to asking origin so a working setup isn't reported as missing.
    """
    for ref in ("origin/gh-pages", "gh-pages"):
        if git(root, "rev-parse", "--verify", "--quiet", ref):
            return ref
    if git(root, "ls-remote", "--heads", "origin", "gh-pages"):
        return "remote-only"
    return ""


def pages_workflows(root: Path) -> list[Path]:
    wf_dir = root / ".github" / "workflows"
    if not wf_dir.is_dir():
        return []
    hits = []
    for p in sorted(wf_dir.glob("*.y*ml")):
        try:
            if PAGES_ACTION_RE.search(p.read_text(encoding="utf-8", errors="replace")):
                hits.append(p)
        except OSError:
            pass
    return hits


def check_workflow(p: Path) -> None:
    text = p.read_text(encoding="utf-8", errors="replace")
    rel = p.name
    deploys = "deploy-pages" in text
    if deploys and not WRITE_ALL_RE.search(text):
        for label, perm_re in PERM_RES.items():
            if not perm_re.search(text):
                errors.append(
                    f"ERROR {rel}: missing `{label}` — deploy-pages fails without it "
                    "(default token permissions do not include Pages)"
                )
    if deploys and "github-pages" not in text:
        warnings.append(f"WARN  {rel}: no `github-pages` environment on the deploy job — expected by deploy-pages")
    if deploys and re.search(r"^\s*pull_request\s*:", text, re.M):
        warnings.append(f"WARN  {rel}: pull_request trigger in a workflow that deploys — deploy must run only from the default branch")
    if "upload-pages-artifact" in text and not STRICT_RE.search(text):
        warnings.append(f"WARN  {rel}: no strict build flag found (mkdocs --strict / sphinx -W) — warnings rot silently without it")


def check_base_path(root: Path, name: str) -> None:
    if not name or name.endswith(".github.io"):
        return  # user/org site or unknown remote: served at /, no base needed
    configs = {
        "mkdocs.yml": r"site_url\s*:",
        "mkdocs.yaml": r"site_url\s*:",
        "docusaurus.config.js": r"baseUrl\s*:",
        "docusaurus.config.ts": r"baseUrl\s*:",
        "astro.config.mjs": r"\bbase\s*:",
        "astro.config.ts": r"\bbase\s*:",
        "docs/.vitepress/config.ts": r"\bbase\s*:",
        "docs/.vitepress/config.mts": r"\bbase\s*:",
        "docs/.vitepress/config.js": r"\bbase\s*:",
    }
    for fname, key_re in configs.items():
        p = root / fname
        if not p.is_file():
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        m = re.search(key_re + r".*$", text, re.M)
        if not m:
            warnings.append(
                f"WARN  {fname}: no base/site_url setting — a project site serves at /{name}/ "
                "and renders unstyled without it (fine if a custom domain serves at /)"
            )
        elif name.lower() not in m.group(0).lower():
            warnings.append(
                f"WARN  {fname}: base/site_url does not mention '/{name}' — verify it matches the "
                "served path (fine if a custom domain serves at /)"
            )


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not root.is_dir():
        print(f"ERROR {root}: not a directory", file=sys.stderr)
        return 1

    workflows = pages_workflows(root)
    ref = gh_pages_ref(root)

    if not workflows and not ref:
        errors.append(
            "ERROR no Pages publishing detected: no workflow using the official Pages actions "
            "and no gh-pages branch (local or on origin) — nothing here can deploy"
        )
    for wf in workflows:
        check_workflow(wf)

    if ref and ref != "remote-only":
        tree = git(root, "ls-tree", "--name-only", ref)
        if tree and ".nojekyll" not in tree.split("\n"):
            warnings.append(
                f"WARN  {ref}: no .nojekyll at the branch root — branch publishing runs Jekyll, "
                "which drops _-prefixed dirs (Sphinx _static etc.)"
            )

    if workflows:
        for cname in (root / "CNAME", root / "docs" / "CNAME"):
            if cname.is_file():
                warnings.append(
                    f"WARN  {cname.relative_to(root)}: CNAME file present but Actions publishing ignores "
                    "CNAME files — set the custom domain in Settings -> Pages instead"
                )

    check_base_path(root, repo_name(root))

    for line in errors + warnings:
        print(line, file=sys.stderr)
    print(f"{'FAIL' if errors else 'OK'}: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
