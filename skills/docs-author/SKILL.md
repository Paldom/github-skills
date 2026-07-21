---
name: docs-author
description: Plans, writes, or restructures project documentation - Diátaxis structure (tutorials, how-to guides, reference, explanation), minimal doc set, runnable examples, README-to-docs graduation, drift prevention. Use when the user asks to write, improve, or reorganize docs, guides, or tutorials. Not for the README itself, deploying a docs site, or community files.
license: MIT
argument-hint: [docs directory or what to document]
---

# docs-author

Produces a documentation set users can actually learn from. Default model
output fails at this in predictable ways — blended tutorial-reference hybrid
pages, navigation shaped like the module tree instead of user tasks, invented
code examples, and four empty "Tutorials/How-to/Reference/Explanation"
folders scaffolded as if structure were progress. This skill exists to
prevent exactly those failures.

## When NOT to use

- The README file itself → `readme-author`. Boundary: README = the front
  door; everything past it = this skill. "Turn our 800-line README into
  docs" uses this skill for the content and hands the README slimming to
  `readme-author`.
- Standing up, deploying, or fixing the docs *site* (generator, GitHub
  Pages, CI pipeline) → `docs-site`. The two compose: content here,
  pipeline there.
- CONTRIBUTING, SECURITY, CODE_OF_CONDUCT and other community files →
  `community-health`.
- Docstrings or inline code comments in source files → ordinary editing.

## Workflow

1. **Inspect before writing.** Read the repo: public API surface, existing
   README/docs/wiki, open issues and support questions (they reveal the
   missing how-tos). Classify every existing docs chunk by mode — tutorial /
   how-to / reference / explanation — before writing anything new. The
   framework's own author's rule: improve one page at a time and publish
   each step; never scaffold four empty sections.
2. **Scope the minimal viable set** (see `references/docs-playbook.md`):
   getting-started tutorial, how-tos for the top real tasks, generated
   reference, 1–3 concept pages, troubleshooting by symptom. Scale down for
   small projects — no empty or "coming soon" pages, ever. Below the
   navigational-need threshold, a good README is the whole answer.
3. **Structure task-first.** Navigation named by user tasks and topics
   (`authentication.md`), never by code modules; at most two levels deep;
   every page reachable from the index. Move content out of the README,
   don't copy it — duplicated content always forks. (`README.md` itself
   stays at the repo root for registry display.)
4. **Write each page in exactly one mode**, using the per-mode recipes and
   style rules in the playbook: second person, imperative, present tense,
   conditions before instructions, scannable structure, short sentences
   (~25-word check), no "simply/just/please", emphasis under ~10%.
   A sentence of inline explanation is fine; sustained explanation gets its
   own page and a link.
5. **Make every example runnable.** Complete as pasted (imports, setup,
   expected output), verified against the actual source in this repo —
   never written from memory. Label anything partial. Apply the
   clean-machine test to install/quickstart steps; wire doctest/CI example
   tests where the ecosystem supports them.
6. **Never hand-write what a tool can generate.** API reference comes from
   docstrings/types/OpenAPI (generation wiring belongs to `docs-site`);
   hand-write only what has no source of truth to generate from.
7. **Drift pass.** When syncing docs after code changes: search the whole
   docs tree for renamed/removed identifiers, not just the obvious page;
   mark deprecated-but-working features with their replacement instead of
   deleting; keep phrasing version-agnostic. Recommend the process fix —
   docs updated in the same PR as user-facing changes, enforced by a PR
   checkbox.
8. **Lint.** Run and fix errors, triage warnings:
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/docs_lint.py" docs
   ```
9. **Present the result**: the doc tree, what each page is (its mode), what
   was deliberately left out, and the signal that should trigger adding it.

## Output spec

Every page classified in exactly one Diátaxis mode; navigation task-shaped,
≤2 levels, no orphans; examples complete, runnable, and verified against the
repo; reference generated, not hand-written; README depth moved (not copied)
into docs; `docs_lint.py` exits 0.

## Gotchas

- The default LLM genre is the blended "guide" — classify the page's mode
  *before* writing it, not after.
- Docs are anti-DRY where repetition saves the reader a hunt between pages —
  but README↔docs duplication always drifts; link or include instead.
- An auto-generated API dump is not documentation — reference feeds the set;
  tutorials and how-tos are what drive adoption.
- FAQs fragment and rot; fold answers into findable pages and keep
  troubleshooting organized by symptom/error string.
- Coding agents are now a large, silent docs audience (they never file
  issues) — self-contained sections and text-over-screenshots serve them
  and human skimmers alike (playbook has the rules).
- Wrong docs are worse than no docs: when a fact can't be verified against
  the code, cut it or mark it unverified — never guess.

## Files

- `references/docs-playbook.md` — Diátaxis application, minimal doc set,
  per-mode page recipes, style rules, examples policy, drift prevention,
  contested points.
- `scripts/docs_lint.py` — deterministic tree lint: broken relative links,
  missing index, orphans, nesting depth, filename style, heading structure,
  emphasis budget; non-zero exit on errors.
