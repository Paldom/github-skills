# Setup prompt — professional GitHub setup in one run

A paste-ready `/goal` prompt that orchestrates all six skills against a target
repository: **audit → four parallel fix agents → protections → re-audit**, with
deterministic verifier gates and a single orchestrator commit.

Why this order: `repo-audit` is read-only, so it brackets the run (baseline +
verification); `repo-protections` must go last because its ruleset wants the
CODEOWNERS that `community-health` creates and required-check names that CI has
actually reported; the middle four write disjoint file surfaces, so they
parallelize safely.

## Prerequisites (once per target repo)

Install the skills in the target repo's Claude Code session:

```
/plugin marketplace add Paldom/github-skills
/plugin install github-skills@github-skills
```

(needs read access while this repo is private), or copy `skills/*` into the
target's `.claude/skills/`. You also need an authenticated `gh` CLI
(repo + workflow scopes).

## The prompt

Open Claude Code at the target repo's root and paste:

```
/goal Professionally set up this GitHub repository end to end with the github-skills skills — audit → parallel fixes → protections → re-audit — until the final repo-audit shows every category improved or explicitly deferred, all verifier scripts pass, and the changes are pushed. Work autonomously; stop only for decisions that are genuinely mine (visibility flip, paid-plan features, deleting anything).

Prerequisites (verify first; stop and tell me if missing):
- The github-skills skills resolve in this session (try /repo-audit) — install the plugin or copy skills/ into .claude/skills/ if not.
- gh CLI authenticated (repo + workflow scopes); cwd is the repo root; git status is clean.

Method — ordering matters, respect it:
1. BASELINE (read-only): run /repo-audit. Keep the scored gap report as the before picture and the work list.
2. PARALLEL FIXES: launch four parallel subagents in this working tree — their file surfaces are disjoint, so no worktrees are needed. Name each skill explicitly in the subagent's instructions (auto-triggering inside subagents is unreliable; headless mode never auto-triggers). No subagent commits — the orchestrator owns git.
   - Agent A → /readme-author: write or restructure README.md per the baseline's README findings; finish by running the skill's readme_lint.py to 0 errors.
   - Agent B → /community-health: CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, SUPPORT, and a CODEOWNERS that covers .github/ and workflows (plus LICENSE if missing). Place files at the root or .github/ — never docs/ (Agent A may create docs/ files while restructuring). Finish with the skill's check_health_files.py; if its only error is a missing README on a README-less repo, that is Agent A's file in flight — defer that one error to step 3's re-run.
   - Agent C → /issue-pr-templates: YAML issue forms + config.yml routing + PR template + starter labels; finish with the skill's validate_forms.sh clean.
   - Agent D → /repo-discoverability: description, topics, homepage via gh repo edit; REPORT any README/H1 misalignment instead of editing README.md (Agent A owns that file); social preview is a manual UI step — surface it. Finish by re-running the skill's check_discoverability.py.
3. DEEP REVIEW (after all four return): re-run each verifier from the orchestrator; read the combined diff as a whole — names/links consistent across README, health files, and templates; labels referenced by forms exist; no placeholder tokens; no file touched by two agents. If /cross is available, cross-validate the combined diff and disposition every finding (fix or reject with evidence); if not, note its absence explicitly.
4. PROTECTIONS (must run after 2-3, never before): run /repo-protections — ruleset with require-PR + code-owner review (CODEOWNERS now exists) + required checks named exactly as CI reports them (CI must have run at least once; read the real check name from gh run/checks output, matrix CI wants a single aggregator check), block force pushes; secret scanning + push protection; Dependabot (weekly, grouped, cooldown; never blanket auto-merge bot PRs); private vulnerability reporting when public. Anything blocked by plan limits or privacy (rulesets on a private free-plan repo, PVR while private) is reported with its unlock condition — never silently skipped.
5. VERIFY: re-run /repo-audit. Produce a before/after table of the six category scores; mark stage-deferred items and the two manual blockers (secret-history scan, personal/private-file review) as unchecked boxes for me — never as passed.
6. COMMIT: one orchestrator commit (or one per surface if the diff is huge) with the before/after score summary in the message; push. Never use git commit --no-verify; never force-push.

Definition of Done:
- Final repo-audit: every category improved or explicitly deferred with a reason; unknowns reported as unknowns, not failures.
- readme_lint.py, check_health_files.py, validate_forms.sh, check_discoverability.py all exit 0; check_protections.py shows no FAIL (UNKNOWN with a plan-limit note is acceptable).
- Combined diff reviewed (and /cross-validated if available) with findings dispositioned.
- Changes pushed by the orchestrator with the before/after audit summary in the commit message or PR description.
```

## Notes

- Adjust the agent list to what the repo needs — e.g. drop Agent C for a repo
  that intentionally keeps intake minimal, or run only steps 1 and 5 for a
  read-only assessment.
- The two manual blockers (full-history secret scan, personal-file review) stay
  yours: no evidence the agents collect can honestly tick those boxes.
- On a private free-plan repo, expect step 4 to report rulesets/PVR as blocked
  with their unlock conditions — that is correct behavior, not a failure.
