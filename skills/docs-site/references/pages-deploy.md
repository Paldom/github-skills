# GitHub Pages Deployment — verified facts and failure modes

Verified against docs.github.com and the official actions' repos, July 2026.
Product facts drift: when something here contradicts the GitHub UI or the
starter workflows, trust those and update this file.

**Contents:** [How Pages serves](#how-pages-serves) ·
[Publishing sources](#publishing-sources) · [The canonical workflow](#the-canonical-workflow) ·
[Base paths](#base-paths-the-1-failure) · [.nojekyll](#nojekyll--branch-publishing-only) ·
[Custom domains](#custom-domains) · [Limits](#limits) ·
[Serving docs to AI agents](#serving-docs-to-ai-agents-llmstxt) ·
[Troubleshooting table](#troubleshooting-table)

## How Pages serves

- **User/org site**: repo named `<owner>.github.io`, served at
  `https://<owner>.github.io/`. One per account.
- **Project site**: any repo, served at `https://<owner>.github.io/<repo>/` —
  the subpath is the top cause of broken deployments (see Base paths).
- Entry file at the publish root must be `index.html`, `index.md`, or `README.md`.
- Static files only — no server-side execution, no custom headers.
- **A Pages site is public even if the repo is private.** On Free plans the
  repo must be public; private-repo Pages needs Pro/Team/Enterprise.

## Publishing sources

Settings → Pages → Build and deployment:

1. **GitHub Actions** (recommended, and the default choice for any real build
   step): a workflow builds the site and uploads it as a Pages artifact.
   No `gh-pages` branch, no Jekyll pass, no `.nojekyll` needed.
2. **Deploy from a branch** (classic): GitHub runs a frozen Jekyll 3.x build
   (Jekyll 4 has never been supported there; plugins are whitelist-only) over
   the branch/folder. Tools like `mkdocs gh-deploy` and `mike` use this mode
   by pushing built HTML to `gh-pages`.

Branch-mode gotchas that look like Pages being broken:

- Commits pushed by a workflow using `GITHUB_TOKEN` do **not** trigger a
  branch-mode Pages build — the site silently never updates.
- Even branch/external-CI publishing deploys through an Actions run now, so
  disabling Actions on the repo breaks all Pages publishing.

## The canonical workflow

Two jobs — build produces the artifact, deploy needs nothing but it:

```yaml
name: docs
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
  pages: write      # deploy to Pages
  id-token: write   # OIDC token deploy-pages verifies
concurrency:
  group: pages
  cancel-in-progress: false
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5   # exposes base_path / origin
      # …toolchain setup + strict site build…
      - uses: actions/upload-pages-artifact@v3
        with:
          path: site/        # the generator's output dir
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages     # the expected environment name
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

Version reality (as of July 2026 — verify before pinning): latest majors are
`configure-pages@v6`, `upload-pages-artifact@v5`, `deploy-pages@v5` (Node 24
bumps, March–April 2026); GitHub's own starter workflows still pin older
majors and work fine. `upload-pages-artifact` below v3 is hard-broken since
the artifacts-v4 cutoff (Jan 2025). The living source of truth is
https://github.com/actions/starter-workflows/tree/main/pages — nine
ready-made workflows (static HTML, Jekyll, Hugo, Astro, Next.js, mdBook, …)
also offered in the Pages settings UI.

Rules the workflow must respect:

- `pages: write` + `id-token: write` are **not** in the default token — omit
  them and the deploy job fails with a permissions error.
- Deploy only from the default branch; PRs run the build job for validation,
  never the deploy job.
- Hidden files are excluded from artifacts by default since
  `upload-pages-artifact@v4`; the `include-hidden-files: true` opt-out only
  exists from **v5** — pin v5+ when the site ships `.well-known/` and friends.
- Build with the generator's strict mode (`mkdocs build --strict`,
  `sphinx-build -W`, generator equivalents) so warnings fail the PR, not
  production.

## Base paths (the #1 failure)

A project site is served under `/<repo>/`. Every generator must be told,
or CSS/JS/links resolve to the domain root and the site renders unstyled
with 404 links — while working perfectly on localhost:

| Generator | Setting |
| --- | --- |
| MkDocs | `site_url: https://<owner>.github.io/<repo>/` |
| Docusaurus | `url` + `baseUrl: '/<repo>/'` (both slashes) + `trailingSlash` set explicitly |
| VitePress | `base: '/<repo>/'` |
| Astro/Starlight | `site: 'https://<owner>.github.io'` + `base: '/<repo>'` |
| Jekyll (Actions) | `--baseurl "${{ steps.pages.outputs.base_path }}"` from configure-pages |
| Sphinx | pathless-relative by default — usually safe |

User/org sites (`<owner>.github.io` repo) and custom domains serve at `/` —
drop the base path there. Case matters in URLs; Pages is case-sensitive.

## .nojekyll — branch publishing only

Branch-mode publishing runs Jekyll by default, which drops files and dirs
starting with `_` — breaking Sphinx (`_static/`, `_sources/`), Next.js
(`_next/`), and many themes. An empty `.nojekyll` at the publishing-source
root disables that pass. Actions-published artifacts skip Jekyll entirely —
no `.nojekyll` needed there.

## Custom domains

Order matters — verify first, DNS second, HTTPS last:

1. **Verify the domain** (Settings → Pages → verified domains, per
   account/org): add the `_github-pages-challenge-<owner>` TXT record. This
   blocks takeover attacks. Never use wildcard DNS (`*.example.com`) — it is
   takeover-exposed even when verified.
2. **DNS**: subdomain (`docs.example.com`) → CNAME to `<owner>.github.io`
   (never including the repo name). Apex → A records
   `185.199.108.153 / .109. / .110. / .111.153` and AAAA
   `2606:50c0:8000::153` … `8003::153`.
3. **Set the domain** in repo Settings → Pages. With Actions publishing the
   domain lives in settings — no CNAME file is created and any committed one
   is ignored. With branch publishing it's a `CNAME` file (one bare domain)
   at the publish root — generators that force-push the branch will destroy
   it unless it lives in the built sources (MkDocs: `docs_dir`; Astro:
   `public/`).
4. **HTTPS**: cert comes from Let's Encrypt (CAA records, if any, must allow
   `letsencrypt.org`). "Enforce HTTPS" can take up to 24 h to become
   available; if provisioning wedges, remove and re-add the domain.
5. A dangling CNAME pointing at a disabled Pages site is immediately
   claimable — remove DNS when tearing a site down.

## Limits

Official numbers (docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits):
published site ≤ 1 GB; source repo recommended ≤ 1 GB; soft 100 GB/month
bandwidth; soft 10 builds/hour (branch builds only — custom Actions workflows
are exempt); 10-minute deployment timeout; over-limit traffic gets HTTP 429.
Usage policy: no e-commerce/sensitive transactions. Pages gives one
production site per repo — PR preview deployments need a third-party host
(Cloudflare/Netlify/Read the Docs) or links to CI build artifacts.

## Serving docs to AI agents (llms.txt)

Status as of mid-2026 — contested, cheap, optional:

- `llms.txt` (llmstxt.org, Jeremy Howard) is a **proposal**, not a standard.
  Google Search states it does not use it; server-log studies show ~97% of
  deployed files never get fetched. The confirmed consumers are coding
  agents/tools (Claude Code, Cursor) fetching docs on demand — and Chrome
  Lighthouse now has an agentic-browsing check for it.
- If shipping one: a **sectioned, described index** (H1 + summary + H2 link
  groups, an "Optional" section for skippables) — never a flat thousand-URL
  dump an agent can't afford to parse. `llms-full.txt` = full concatenated
  Markdown. Many generators have plugins that emit both at build time.
- Higher-leverage than llms.txt: clean Markdown variants of pages (`.md` URL
  suffixes), self-contained sections, and an `AGENTS.md` in the repo. Treat
  all of it as agent-readiness insurance, not SEO.

## Troubleshooting table

| Symptom | Cause | Fix |
| --- | --- | --- |
| Unstyled site, internal links 404, works locally | base path not set for `/<repo>/` | set the generator's base/site_url (table above), rebuild |
| CSS/assets under `_static`/`_next` 404 | branch publishing ran Jekyll, `_` dirs dropped | add empty `.nojekyll` at publish root (or switch to Actions publishing) |
| Deploy job: "Resource not accessible" / OIDC error | missing `pages: write` + `id-token: write`, or wrong environment | add permissions block; environment `github-pages` |
| Site never updates (branch mode) | pushed by `GITHUB_TOKEN`, which doesn't trigger Pages builds | deploy via the Actions artifact path, or push with a user token/deploy key |
| Custom domain disappears after deploy | branch force-push overwrote the CNAME file | keep CNAME in built sources, or use Actions publishing (domain = settings) |
| "Enforce HTTPS" greyed out | cert not provisioned yet / CAA blocks Let's Encrypt | wait (≤24 h), fix CAA, or remove and re-add the domain |
| Workflow fails: artifact/action deprecated | `upload-pages-artifact` ≤ v2 pinned | bump to current majors (see Version reality) |
| `.well-known/` missing from the site | hidden files excluded since upload-pages-artifact v4 | bump the upload action to v5+ and set `include-hidden-files: true` |
| 404 on the site root | no `index.html`/`index.md`/`README.md` at publish root, or wrong artifact `path:` | fix the output dir passed to upload |
| Random 429s | soft bandwidth/build limits exceeded | trim assets, cut build frequency, consider a CDN/other host |
