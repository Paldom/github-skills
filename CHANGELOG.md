# Changelog

All notable changes to this repository's skills are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning: [SemVer](https://semver.org) on the plugin manifest
(breaking skill-interface change → major, new skill → minor, fix → patch).

## [Unreleased]

### Changed
- `readme-author` learned drift-sync: a code-change → README-section map
  (dependencies → Installation, env vars → Configuration, commands/endpoints →
  Usage, removals → prune), plus global-audience readability rules and
  GitHub alert callouts — distilled from an ecosystem survey of README skills.

### Added
- skills.sh distribution: `npx skills add Paldom/github-skills` quick start, repo-page
  groupings (`skills.sh.json`), a `skills-sh` CI job mirroring the consumer
  install, `docs/deploying.md`, and the bundled `publish-repo` skill.
- `docs/setup-prompt.md` — paste-ready `/goal` prompt orchestrating all six
  skills against a target repo (audit → four parallel fix agents → protections
  → re-audit), linked from the README quick start.
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
