---
name: docs-site
description: Stands up, deploys, or fixes a documentation site on GitHub Pages - generator choice (MkDocs, Sphinx, Docusaurus, Starlight), the official Actions workflow, base-path/.nojekyll/custom-domain pitfalls, docs CI, versioning. Use for publishing docs to github.io or debugging a broken/unstyled Pages deploy. Not for writing the docs content, the README, or branch protections.
license: MIT
argument-hint: [generator or deploy problem]
---

# docs-site

Ships a documentation site that deploys correctly the first time. Models get
this wrong in predictable ways: stale `gh-pages`-branch workflows from old
blog posts, the official workflow but the Pages source never flipped (green
workflow, 404 site), base paths missed so the site works locally and renders
unstyled on github.io, and versioning bolted onto an incompatible deploy
model. This skill encodes the current official pipeline and the fixes.

## When NOT to use

- Writing or restructuring the documentation *content* → `docs-author`
  (the two compose: pipeline here, prose there).
- The README → `readme-author`.
- Branch rulesets, secret scanning, Actions hardening → `repo-protections`.
- Repo description/topics/social preview → `repo-discoverability`.
- Hosting on Read the Docs, Netlify, Vercel, or app deployments → out of
  scope by design; say so in one line and stop.

## Workflow

1. **Inspect.** Ecosystem and language, existing docs config and `docs/`
   tree, existing workflows, whether a `gh-pages` branch exists, current
   Pages state (`gh api repos/{owner}/{repo}/pages` when authenticated).
   Don't re-litigate a working generator — fix forward.
2. **Choose the generator** with `references/generator-choice.md`: by
   ecosystem and needs, not hosting; note the Material-for-MkDocs
   maintenance-mode caveat for new long-horizon sites. Below the
   navigational-need threshold, recommend staying README-only and stop.
3. **Configure with the base path first.** Project sites serve under
   `/<repo>/` — set the generator's `site_url`/`baseUrl`/`base` per the
   table in `references/pages-deploy.md`. Turn on strict builds
   (`mkdocs build --strict`, `sphinx-build -W`; Docusaurus throws on broken
   links by default). Shape the landing page per
   `references/generator-choice.md`: hero when visitors are still choosing,
   docs-first when they arrive convinced; ≤2 clicks (ideally 0) from landing
   to a runnable command.
4. **Pick ONE deploy model — never mix:**
   - Versioned MkDocs docs via `mike` → **branch publishing** (`gh-pages`),
     with `.nojekyll` and aliases (`mike deploy X latest --update-aliases`,
     `mike set-default latest`).
   - Everything else → the **official artifact workflow**: build job
     (`configure-pages` → strict build → `upload-pages-artifact`) then
     deploy job (`deploy-pages`) with `permissions: pages: write` +
     `id-token: write`, environment `github-pages`, deploying from the
     default branch only. Start from
     https://github.com/actions/starter-workflows/tree/main/pages for
     current action versions rather than hardcoding pins.
5. **Flip the source.** Settings → Pages → Source = "GitHub Actions" (or
   `gh api repos/{owner}/{repo}/pages -X POST -f build_type=workflow`;
   `-X PUT` if the site exists). A green workflow with a 404 site means
   this step was skipped. List every manual step you can't perform.
6. **Verify live, not locally.** Fetch the deployed `page_url`; check
   styling and a deep link. Symptom → cause → fix table in
   `references/pages-deploy.md` (base path, `.nojekyll`, permissions,
   entry file).
7. **Docs CI.** On PRs: strict build + internal link check, blocking,
   path-filtered to docs changes. External links: scheduled weekly with
   retries, non-blocking — flaky 403s train people to ignore CI. Deploy
   never runs from PRs.
8. **Optional extras, in order of value:** custom domain (verify-first
   order and exact DNS records in the reference), versioning only when
   released versions genuinely differ, `llms.txt` as a one-line build
   plugin (agent-readiness insurance, not SEO).
9. **Check.** Run and fix what it reports:
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/check_pages_setup.py"
   ```

## Output spec

A site reachable at its real URL with styling and working deep links; a
workflow with the exact required permissions deploying only from the default
branch; strict build + link check gating PRs; one deploy model, stated;
every manual settings step listed explicitly for the owner.

## Gotchas

- Green workflow, 404 site → Pages source not set to "GitHub Actions"
  (step 5).
- Works locally, broken on github.io → base path (the #1 failure).
- `.nojekyll` matters for **branch publishing only** — Actions artifacts
  skip Jekyll entirely; branch-mode Jekyll silently drops `_`-prefixed dirs
  (Sphinx `_static`, `_next`).
- Custom domain: with Actions publishing the domain lives in repo settings
  (CNAME files are ignored); with branch publishing the CNAME file must
  survive force-pushes. Verify the domain (TXT record) before DNS; a
  dangling CNAME record is a takeover.
- Branch-mode builds are not triggered by `GITHUB_TOKEN`-pushed commits —
  the site silently never updates.
- Hidden files (`.well-known/`) are excluded from Pages artifacts by
  default — the opt-out flag needs a current upload action (versions in the
  troubleshooting table).
- A Pages site is public even from a private repo (plan gating in the
  reference).
- Old pinned Pages actions hard-fail (artifacts-v4 cutoff); bump majors
  rather than debugging them.

## Files

- `references/generator-choice.md` — decision table, Material maintenance
  caveat, versioning mechanisms, generated API reference, mixed-language
  strategy, search, landing-page anatomy.
- `references/pages-deploy.md` — verified Pages facts: publishing sources,
  canonical workflow, base paths, custom domains/DNS, limits, llms.txt
  status, troubleshooting table.
- `scripts/check_pages_setup.py` — deterministic setup check: workflow
  permissions/triggers, base-path config, gh-pages/.nojekyll, CNAME-mode
  mismatches; non-zero exit on definite errors.
