# Choosing the Docs Generator — decision rules, versioning, API reference

Pick the generator by ecosystem and editorial needs; the deploy pipeline
(Pages via Actions) is the same for all of them. Tool facts below are as of
mid-2026 and drift — verify current status before pinning anything.

**Contents:** [Decision table](#decision-table) ·
[The MkDocs-Material caveat](#the-mkdocs-material-caveat) ·
[Versioned docs](#versioned-docs) · [Generated API reference](#generated-api-reference) ·
[Mixed-language projects](#mixed-language-projects) · [Search](#search) ·
[The landing page](#the-landing-page)

## Decision table

| Generator | Pick when | Pages gotcha |
| --- | --- | --- |
| **MkDocs + Material** | Python-ecosystem default; Markdown-first, excellent theme/search out of the box; `mkdocstrings` for API reference | maintenance-mode caveat below; `site_url` required; `mike` versioning forces branch publishing |
| **Sphinx** (+ Furo theme, MyST for Markdown) | API-reference-heavy or scientific Python; intersphinx cross-project links; PDF output; longest support horizon | `_static`/`_sources` need `.nojekyll` on branch publishing; no first-party Pages action — build then upload the artifact |
| **Docusaurus** | JS/TS/React ecosystem; the mature **built-in versioning**; big plugin ecosystem | `url` + `baseUrl` + `trailingSlash` must all be right; Node build chain is the heaviest here |
| **Astro Starlight** | Ecosystem-neutral modern default; fast zero-JS output, Pagefind search, i18n | still 0.x — minor releases break config occasionally; `site` + `base` both required for project pages |
| **VitePress** | Vue ecosystem or want the fastest dev loop | no built-in versioning; `base` required |
| **Jekyll (+ Just the Docs)** | smallest possible setup, GitHub-native branch publishing with zero build config | branch builds run frozen Jekyll 3.x with whitelisted plugins only — Jekyll 4.x or any plugin needs the Actions workflow |
| **mdBook** | book-style long-form (tutorial-heavy) docs, Rust ecosystem | starter workflow exists; not for API-reference sites |

Don't let hosting choose the authoring tool: anything that emits static HTML
deploys to Pages the same way. And don't stand up a generator at all below
the navigational-need threshold — a README-only project needs no site.

## The MkDocs-Material caveat

Material for MkDocs entered **maintenance mode**: 9.7.0 (Nov 2025) was the
final feature release (all former Insiders features went free/MIT), with
critical bug and security fixes committed for "12 months, at least" — patch
releases have continued through 2026. The team's successor project is
**Zensical** (mkdocs.yml-compatible, pre-1.0), and a separate MkDocs 2.0
rewrite is in progress that will break today's plugin/theme APIs.

Practical rule: Material remains a fine choice today for existing and
short-horizon sites; for a new site expected to live 5+ years, prefer Sphinx
(Python) or Starlight/Docusaurus (JS/neutral), or accept a future Zensical
migration. Verify current status: https://squidfunk.github.io/mkdocs-material/
before deciding.

## Versioned docs

First question: do published versions genuinely differ for users? If not,
one site + a changelog. Versioning multiplies maintenance and confuses
search; retire unsupported versions on a schedule.

- **MkDocs → `mike`**: deploys each version as a directory on the `gh-pages`
  branch with a `versions.json` the Material version selector reads.
  Release step: `mike deploy <version> latest --update-aliases --push`.
  Note: mike implies **branch publishing** (Settings → Pages → Source =
  gh-pages branch), not the Actions artifact path.
- **Docusaurus**: first-class built-in versioning (`docusaurus docs:version X`).
- **Sphinx**: `sphinx-multiversion`, or host on Read the Docs which does
  versioning, PR previews, and search natively for OSS.
- **VitePress/Starlight**: no native story — manual per-version builds into
  subdirectories; if versioning is a hard requirement, that's a point for
  Docusaurus.

The classic mistake: publishing `main`'s docs over the stable release's docs
so released users read unreleased behavior. Version the site (or gate deploys
to release tags) the moment released and development behavior diverge.

## Generated API reference

Never hand-write API reference — generate it from the source of truth:

- **Python**: `mkdocstrings[python]` (MkDocs) or `autodoc` + `napoleon`
  (Sphinx). Both import the package at build time — the docs build env must
  install the package, and imports must be side-effect-free. Pick Google or
  NumPy docstring style and never mix; don't repeat types that PEP 484
  annotations already carry.
- **TypeScript/JS**: TypeDoc reads types + TSDoc directly (signatures can't
  drift). Markdown output via `typedoc-plugin-markdown`, integrated with
  `starlight-typedoc` or `docusaurus-plugin-typedoc`.
- **HTTP APIs**: the OpenAPI spec is the contract — render with Redocly,
  Scalar, or Swagger UI; lint the spec (`redocly lint`) and contract-test it
  against the implementation in CI.

## Mixed-language projects

One site, not two: a single shell site (Starlight or Docusaurus, or MkDocs if
Python-led) holds all prose, with per-language generated reference sections
(mkdocstrings/Sphinx-built Markdown for Python + TypeDoc Markdown for TS)
under one nav, one search index, one Pages deployment, and a landing page
routing "Python SDK" / "JS SDK". Two separately themed sites are only
justified for genuinely disjoint audiences.

## Search

Built-in client-side search is fine to start: Material and VitePress ship
good ones; Starlight ships Pagefind (scales well). For large OSS sites,
Algolia DocSearch is free for qualifying projects and is the ecosystem
standard (first-class in Docusaurus). Wire search before versioning — a
searchable single-version site beats a versioned unsearchable one.

## The landing page

Distilled from the top live github.io docs sites (mdBook, Material for
MkDocs, Just the Docs, GoogleTest, LSP, Monaco, leaflet for R,
Sphinx-Gallery, VitePress):

- **Hero vs docs-first.** A marketing hero (tagline + ≤3 buttons + feature
  cards) earns its place when visitors ask "should I use this?" — tools
  competing in a crowded category. Projects whose visitors arrive already
  convinced (de-facto standards, specs, arrive-with-intent utilities) do
  better docs-first: title, one definitional sentence, grouped links.
- **The metric is clicks-to-runnable**: ≤2 from landing to a copy-pasteable
  command, and 0 is the ideal — put a one-line install or a live demo on the
  landing page itself. A "Get started" button is the fallback, not the goal.
- **Tagline**: one definitional sentence under the H1 — what it is + what
  you make with it. The H1 may state the benefit instead of the name
  ("Focus on writing good documentation").
- **Header kit**: search with a visible hotkey hint (`/` or `Ctrl/⌘-K`), a
  GitHub link (always the secondary CTA, never the primary), dark-mode
  toggle; a version switcher once more than one major is supported. Small
  shallow sites can skip search — a one-screen grouped index beats a search
  box.
- **Content-page furniture**: copy buttons on code blocks, edit-this-page
  links, prev/next pagination, per-page TOC. Split quickstarts by the
  user's toolchain (pip/docker tabs, Bazel vs CMake) rather than one
  generic path.
- **Prerender the landing page.** A client-rendered SPA shell is invisible
  to crawlers, link previews, and AI agents — every generator in the
  decision table emits static HTML; keep it that way.
- **Leaving github.io later?** Ship a redirect stub — a 404 with no pointer
  strands every inbound link, and the strongest projects have made exactly
  that mistake.
