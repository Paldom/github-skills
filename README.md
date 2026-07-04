# Github Skills

[![CI](https://github.com/Paldom/github-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/Paldom/github-skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Agent Skills for professional GitHub repos - brief, structured, SEO-friendly READMEs that convert visitors into users, plus complete OSS scaffolding: community health files, templates, and discoverability best practices.

Agent Skills for [Claude Code](https://code.claude.com/docs/en/skills) (and any
[Agent Skills](https://agentskills.io)-compatible tool). Each skill is a folder under
[`skills/`](skills/) with a single-purpose `SKILL.md`, trigger evals, and optional
scripts/references — validated on every write, commit, and PR.

## Quick start

Install with the [skills CLI](https://skills.sh) — works with Claude Code, Cursor,
Codex, and any Agent Skills-compatible tool:

```bash
npx skills add Paldom/github-skills
```

Or as a Claude Code plugin:

```
/plugin marketplace add Paldom/github-skills
/plugin install github-skills@github-skills
```

Or copy a single skill into a project:

```bash
git clone https://github.com/Paldom/github-skills.git
cp -r github-skills/skills/<skill-name> your-project/.claude/skills/
```

Then just describe the task in Claude Code — the skill activates on its description —
or invoke it explicitly with `/<skill-name>`.

To professionalize a whole repository in one run, paste the
[setup prompt](docs/setup-prompt.md): it orchestrates all six skills
(audit → four parallel fix agents → protections → re-audit) with verifier
gates and a single reviewed commit.

## Skills

| Skill | Description |
| --- | --- |
| [readme-author](skills/readme-author/) | Writes or restructures a professional project README — front-loaded value prop, minimal badges, copy-pasteable quick start, per-type templates (library/CLI/web app). |
| [repo-discoverability](skills/repo-discoverability/) | Optimizes how the repo gets found — description, topics, social preview, name/H1 alignment, GitHub + web search levers. |
| [community-health](skills/community-health/) | Creates or completes community health files (CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, SUPPORT, GOVERNANCE, FUNDING, CODEOWNERS, LICENSE) tailored to the repo. |
| [issue-pr-templates](skills/issue-pr-templates/) | Builds structured intake — YAML issue forms with required fields, config.yml routing, PR template, starter labels. |
| [repo-protections](skills/repo-protections/) | Configures server-side protections — rulesets, secret scanning & push protection, Dependabot, private vulnerability reporting, Actions hardening. |
| [repo-audit](skills/repo-audit/) | Audits the repo against a professional-OSS checklist and returns a scored gap report routing each fix to the owning skill. |

## Repository structure

```
skills/                  # distributed skills, one folder per skill (SKILL.md + evals/ + scripts/)
docs/                    # skill-authoring guide, eval methodology, deployment guide
skills.sh.json           # skills.sh repo-page customization (groupings)
scripts/                 # deterministic validator used by hooks and CI
.claude/                 # agentic dev setup: hooks + bundled add-skill / publish-repo skills
.claude-plugin/          # plugin + marketplace manifests (makes this repo installable)
.local/                  # gitignored working area: sources, research, PROMPT.md (see below)
```

## Working on this repo with an agent

This repo is agent-native: canonical agent instructions live in
[AGENTS.md](AGENTS.md) (CLAUDE.md imports it), hooks validate every `SKILL.md` on
write, `make check` runs the full validator, and CI enforces the same gate on every
PR. The bundled `add-skill` skill walks the eval-first authoring workflow described
in [docs/skill-authoring.md](docs/skill-authoring.md). Maintainers drive sessions
with their own (gitignored, personal) `.local/PROMPT.md` goal prompt.

## Contributing

Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for the skill-proposal
process, the authoring workflow, and the PR checklist. Please note the
[Code of Conduct](CODE_OF_CONDUCT.md).

## Support

Questions, ideas, or something not working? Start with [SUPPORT.md](SUPPORT.md) —
bugs and skill proposals have [issue templates](../../issues/new/choose), and
security concerns go through [SECURITY.md](SECURITY.md) (never a public issue).

## License

[MIT](LICENSE) © 2026 Paldom
