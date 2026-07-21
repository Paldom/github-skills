# Docs Playbook — structure, page types, style, drift

Rules for planning and writing a project documentation set. Verified against
primary sources (diataxis.fr, Google/Microsoft style guides, Write the Docs,
kapa.ai) as of mid-2026; practices here are stable unless marked.

**Contents:** [Diátaxis in practice](#diátaxis-in-practice) ·
[The minimal viable doc set](#the-minimal-viable-doc-set) ·
[Page-type recipes](#page-type-recipes) · [Style rules](#style-rules-that-matter) ·
[Code examples](#code-examples) · [Writing for humans and AI readers](#writing-for-humans-and-ai-readers) ·
[Drift prevention](#drift-prevention) · [Contested points](#contested-points--decide-dont-assume)

## Diátaxis in practice

Four documentation forms (diataxis.fr), one per user need — the axes are
practical↔theoretical and study↔work:

| Form | Reader is… | Serves | Tone | Classic failure |
| --- | --- | --- | --- | --- |
| Tutorial | learning, on rails | acquisition of skill | "Follow me" — instructor owns success | digresses into theory or options |
| How-to guide | working, has a goal | a real task | "To do X: 1, 2, 3" — assumes competence | re-teaches basics, becomes a tutorial |
| Reference | working, looking up | facts | dry, complete, consistent | breaks into narrative or tasks |
| Explanation | studying, wants why | understanding | discursive, connective | turns into instructions |

How to actually apply it (Procida's own guidance):

- **Iterate, don't scaffold.** Do NOT create four empty sections and fill them.
  Choose one existing page → classify it → make one improvement → publish.
  Structure emerges "from the inside". Every step in the right direction is
  worth publishing immediately.
- **Skeleton, not law.** A sentence or two of inline explanation inside a
  tutorial is fine; *sustained* explanation gets its own page with a link.
  Rigid page-per-quadrant separation causes fragmentation fatigue.
- **Mode drift is the maintenance failure**: over time how-tos bloat with
  explanation and reference accretes steps. Re-classify pages during reviews.
- The framework is contested at the edges (see [Contested points](#contested-points--decide-dont-assume));
  use it as the default map, not a completeness proof.

## The minimal viable doc set

Scale the set to the project — a big framework's IA on a small library is a
maintenance trap and a burnout vector. Start minimal; automate before you
hand-author more.

For a typical small/medium package:

1. **Getting started** — one install path + one quickstart tutorial ending in
   visible success.
2. **How-to guides** — one page (or a few) for the top real tasks: the things
   support/issues actually get asked.
3. **Reference** — generated from docstrings/types/spec wherever possible
   (mkdocstrings, TypeDoc, OpenAPI renderers). Never hand-write what a tool
   can generate; hand-written reference is drift with a delay.
4. **Concepts** — 1–3 pages of why: architecture, mental model, terminology.

Supporting pages as needed: troubleshooting (organized by symptom/error
string, not by feature), changelog (link `CHANGELOG.md`), contributing,
migration/upgrade guides.

README ↔ docs boundary:

- The README is the front door, not the docs: what it is, why care, install,
  one minimal runnable example, links to everything else. README work itself
  belongs to a README-focused workflow, not this skill.
- **Graduate to a docs set when content needs navigation** — multiple guides,
  real API surface, troubleshooting depth. There is no line-count threshold in
  any authoritative source; the trigger is navigational need.
- Graduation is a move, not a copy: README depth moves into `docs/` pages and
  the README keeps pitch + quickstart + links. Duplicated content in both
  places drifts apart.
- Packaging constraint: `README.md` must stay at the package root for
  npm/PyPI registry display.

Information architecture rules:

- Nest at most two directory levels. One main concept per page.
- Name files by topic (`authentication.md`), lowercase-with-hyphens — never by
  type (`misc.md`, `other.md`).
- Every page must be reachable from the index/nav; orphans are dead content.
- Some duplication across pages is fine when it saves the reader a hunt —
  docs are deliberately anti-DRY (Write the Docs).
- FAQs are not documentation: they fragment content and rot. Fold answers
  into findable pages; keep troubleshooting symptom-organized.

## Page-type recipes

**Tutorial (getting started):** state prerequisites and the end result up
front; one happy path, no branches or options; every step is an action with
its expected output shown; end with visible, checkable success and "where to
go next". The instructor is responsible for the learner's success — nothing
may fail if followed literally.

**How-to guide:** title is the task ("Configure webhook retries"); assume a
working setup and basic competence; numbered steps, minimal context, no
teaching; link to concepts/reference instead of inlining them; cover the one
realistic variation that actually occurs, not every possibility.

**Reference:** each entry is a complete standalone lookup unit — readers land
directly from search and leave. For an API entry: purpose, parameters with
types/required flags, return/response with real status codes, error codes
with meanings, one runnable example. Consistent structure across all entries
matters more than prose quality.

**Explanation:** answers "why is it like this" — design decisions, trade-offs,
background. No instructions. If you feel a numbered list forming, it's a
how-to trying to escape.

## Style rules that matter

The highest-leverage rules Google's and Microsoft's guides agree on:

- The basics both guides agree on, in one line: second person, active voice,
  present tense, imperative instructions, scannable structure, sentence-case
  headings, descriptive link text, alt text on images.
- **Conditions before instructions**: "If X, do Y" — never "Do Y if X".
- Short sentences. No authority endorses one number; ~25 words is the common
  check-threshold (GOV.UK) — split anything longer unless splitting hurts it.
- Put commands in code blocks even when trivial; never assume prerequisite
  steps happened.
- Don't pre-announce ("in this section we will…") — just say the thing.
- Word-level traps: no "please" in instructions; avoid "easy"/"simply"/"just"
  (what's easy for you isn't for the reader); "sign in" not "log in";
  precise terms over metaphors for a global audience.
- Emphasis budget: keep bold/highlighted text under ~10% of a page — past
  that, nothing stands out.
- Contractions are prescribed by Microsoft, merely permitted by Google —
  house choice, not canon.

## Code examples

Examples are product surface, and the #1 trust signal:

- **Complete and runnable as pasted**: includes imports and setup, shows
  expected output, and error cases where they teach. Label anything partial
  ("… rest of config omitted").
- **Clean-machine test**: follow your own install + quickstart on a fresh
  machine/container with literal obedience; fix every place you improvised.
  Repeat at every release (dogfood the quickstart).
- Keep examples tested where the ecosystem allows: doctest / pytest-run
  snippets for Python, type-checked example files for TS, CI smoke tests for
  `examples/` directories. An untested example is a future bug report.
- Introduce every block with one task sentence ("The following configures…").

## Writing for humans and AI readers

A growing share of docs consumption is by coding agents (Cursor, Claude Code,
Copilot) — and agents fail silently: they never file issues, users just churn.
The same properties that help RAG/agents help human skimmers (kapa.ai):

- Make sections **self-contained**: restate product/component/version context
  instead of relying on the page above; chunked retrieval reads sections in
  isolation.
- Strict heading hierarchy; keep related information adjacent.
- Prefer text over screenshots for anything an agent must act on; define
  acronyms on first use per page.
- Q&A-format troubleshooting entries match how both users and agents query.
- An `AGENTS.md` at the repo root guides AI-assisted contributors (and cuts
  AI-slop PRs). Serving docs to agents (llms.txt, Markdown endpoints) is a
  publishing concern → the docs-site skill.

## Drift prevention

CI can catch broken builds and links, **not semantic staleness** — drift is a
process problem:

- Docs change in the **same PR** as any user-facing change; a PR-template
  checkbox ("docs updated?") and a `docs-needed` label make it enforceable.
- Generate reference from source so it cannot drift; keep prose
  version-agnostic where possible ("the CLI prints…", not "as of v2.3…").
- On any rename/removal: search the whole docs tree for old identifiers, not
  just the obvious page. Deprecated-but-working features are marked with
  their replacement, not silently deleted.
- Wrong docs are worse than no docs — when in doubt, cut or mark unverified.
- Mine signals for gaps: zero-result searches, high-exit pages, repeated
  support questions → each is a missing how-to.

## Contested points — decide, don't assume

Where authorities disagree, state the trade-off instead of encoding a fake
consensus:

- **Diátaxis universality**: Procida presents four forms as complete; critics
  (Hillel Wayne) show real docs that don't fit (ADRs, onboarding). Default to
  it; don't force-fit.
- **Sentence-length numbers**: GOV.UK 25-word check, Oxford 15–20 average,
  Google/Microsoft refuse numbers. Encode "short, ~25-word check", no limit.
- **"AI makes IA matter less"** vs "structure matters more for chunked
  retrieval" — both current; self-contained sections win either way.
- **Docs-as-code vs docs-as-product**: tooling philosophy vs management
  philosophy — complementary, not rivals.
- **Delete-most-docs minimalism** (code as source of truth) vs full doc sets:
  real position for small utilities; a README-only strategy is legitimate
  below the navigational-need threshold.

Templates for every page type above: The Good Docs Project
(thegooddocsproject.dev) maintains ~28 community templates (as of mid-2026;
verify: https://thegooddocsproject.dev/template/).
