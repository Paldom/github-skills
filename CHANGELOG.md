# Changelog

All notable changes to this repository's skills are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning: [SemVer](https://semver.org) on the plugin manifest
(breaking skill-interface change → major, new skill → minor, fix → patch).

## [Unreleased]

## [0.4.0] - 2026-07-22

### Changed
- `readme-author` learned the exemplar layer, distilled from reading 20 of the
  best READMEs on GitHub (awesome-readme canon): centered hero stacks and nav
  rows, design-system badge strips, dark/light `<picture>` images,
  per-use-case collapsibles, persona routers, per-category exemplar study
  list — plus demo-GIF creation via the optional paldom/terminaltor and
  paldom/screenshooter subskills and a de-slop pass via paldom/noslop.
- `docs-site` learned docs-landing-page anatomy from 12 live github.io
  exemplar sites: hero vs docs-first decision rule, clicks-to-runnable
  metric, header kit, prerendered-landing rule, redirect-stub rule.
- `docs-author` gained the optional paldom/noslop de-slop pass on docs prose.

## [0.3.0] - 2026-07-21

### Added
- `docs-author` — plans/writes/restructures documentation content: Diátaxis-shaped
  structure applied iteratively (never four empty folders), minimal viable doc set,
  per-mode page recipes, verified runnable examples, README-to-docs graduation,
  drift prevention; deterministic `docs_lint.py` gate (links, orphans, structure).
- `docs-site` — GitHub Pages docs publishing: generator choice by ecosystem
  (incl. the Material-for-MkDocs maintenance-mode caveat), the official
  configure/upload/deploy-pages workflow with exact permissions, base-path and
  `.nojekyll` and custom-domain pitfalls, docs CI, mike-vs-artifact versioning
  decision; `check_pages_setup.py` static gate. Facts verified against
  docs.github.com July 2026.

### Changed
- `readme-author` and `repo-audit` now route documentation-set and docs-site work
  to the new docs skills; README and setup prompt say "six core skills" for the
  orchestrated set now that the catalog is larger.

### Fixed
- Portable `${CLAUDE_SKILL_DIR}` script paths and the owner-only git policy in
  the agent rules; setup prompt kept under its 4000-character limit.

## [0.2.0] - 2026-07-05

### Changed
- `readme-author` learned drift-sync: a code-change → README-section map
  (dependencies → Installation, env vars → Configuration, commands/endpoints →
  Usage, removals → prune), plus global-audience readability rules and
  GitHub alert callouts — distilled from an ecosystem survey of README skills.

### Fixed
- Modernized CI runtimes and broadened install channels.

## [0.1.0] - 2026-07-04

### Added
- skills.sh distribution: `npx skills add Paldom/github-skills` quick start, repo-page
  groupings (`skills.sh.json`), a `skills-sh` CI job mirroring the consumer
  install, `docs/deploying.md`, and the bundled `publish-repo` skill.
- `docs/setup-prompt.md` — paste-ready `/goal` prompt orchestrating the six
  core skills against a target repo (audit → four parallel fix agents →
  protections → re-audit), linked from the README quick start.
- `readme-author` — writes/restructures professional project READMEs (front-loaded
  structure, badge discipline, copy-pasteable quick start) with a deterministic
  `readme_lint.py` gate and per-type templates.
- `repo-discoverability` — GitHub-native findability: description, topics, social
  preview, name/H1 alignment; read-only `check_discoverability.py` audit.
- `community-health` — CONTRIBUTING/CODE_OF_CONDUCT/SECURITY/SUPPORT/GOVERNANCE/
  FUNDING/CODEOWNERS/LICENSE tailored to the repo; `check_health_files.py` gate.
- `issue-pr-templates` — YAML issue forms + config.yml routing + PR template +
  starter labels; schema validation via `validate_forms.sh`.
- `repo-protections` — rulesets, secret scanning/push protection, Dependabot,
  PVR, Actions hardening; read-only `check_protections.py` audit.
- `repo-audit` — scored six-category gap report with owner-skill routing;
  mechanical `collect_evidence.py` collector.
- Repository scaffolded from the skills template.
