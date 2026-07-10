# Setup prompt — professional GitHub setup in one run

One paste-ready `/goal` prompt orchestrating all six skills: audit → four parallel fix agents → protections → re-audit. `repo-audit` is read-only so it brackets the run; `repo-protections` goes last (its ruleset needs `community-health`'s CODEOWNERS and real CI check names); the middle four write disjoint files, so they parallelize.

## Prerequisites

```
/plugin marketplace add Paldom/github-skills
/plugin install github-skills@github-skills
```

(or copy `skills/*` into the target's `.claude/skills/`). Authenticated `gh` CLI (repo + workflow scopes).

## The prompt

Paste at the repo root:

```
/goal Set up this GitHub repo professionally with the github-skills skills — audit → parallel fixes → protections → re-audit — until the final repo-audit shows every category improved or deferred and all verifiers pass. Never run git commit or git push — every change stays in the working tree for my review. Work autonomously; stop only for decisions that are mine (visibility, paid features, deletions).

Verify first (stop if missing): the skills resolve (try /repo-audit); gh CLI authed (repo + workflow scopes); cwd is repo root; git status clean.

Method — order matters:
1. BASELINE (read-only): /repo-audit. Keep the scored gap report as the before picture and work list.
2. PARALLEL FIXES: four subagents in this working tree (disjoint file surfaces, no worktrees). Name each skill explicitly in the subagent instructions — auto-triggering in subagents is unreliable. Nobody runs git.
   - A → /readme-author: write/restructure README.md per baseline findings; readme_lint.py to 0 errors.
   - B → /community-health: CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, SUPPORT, CODEOWNERS covering .github/ and workflows (LICENSE if missing); files at root or .github/, never docs/. check_health_files.py clean (a missing-README error is Agent A's file in flight — defer to step 3).
   - C → /issue-pr-templates: YAML issue forms + config.yml routing + PR template + starter labels; validate_forms.sh clean.
   - D → /repo-discoverability: description, topics, homepage via gh repo edit; REPORT README/H1 misalignment, never edit README.md (Agent A owns it); social preview is a manual UI step — surface it. Re-run check_discoverability.py.
3. DEEP REVIEW (after all return): re-run each verifier; read the combined diff — names/links consistent; labels referenced by forms exist; no placeholders; no file touched by two agents. If /cross is available, cross-validate the diff and disposition every finding; else note its absence.
4. PROTECTIONS (after 2-3, never before): /repo-protections — ruleset with require-PR + code-owner review + required checks named exactly as CI reports them (CI must have run once; matrix CI wants one aggregator check), block force pushes; secret scanning + push protection; Dependabot (weekly, grouped, cooldown; no blanket bot auto-merge); private vulnerability reporting when public. Anything plan/privacy-blocked is reported with its unlock condition, never silently skipped.
5. VERIFY: re-run /repo-audit. Before/after table of the six category scores; stage-deferred items and the two manual blockers (secret-history scan, personal-file review) stay unchecked boxes — never passed.
6. HANDOFF: no git commit/push. Present the before/after table and changed-file list.

Definition of Done:
- Final repo-audit: every category improved or deferred with a reason; unknowns reported as unknowns.
- readme_lint.py, check_health_files.py, validate_forms.sh, check_discoverability.py exit 0; check_protections.py shows no FAIL (UNKNOWN with a plan-limit note is fine).
- Combined diff reviewed (cross-validated if available), findings dispositioned.
- All changes left uncommitted.
```

## Notes

- Drop agents the repo doesn't need (e.g. C); steps 1+5 = read-only assessment.
- Private free-plan repo: step 4 reports rulesets/PVR blocked — correct, not a failure.
