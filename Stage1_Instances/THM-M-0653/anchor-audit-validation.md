# Anchor-audit validation

Item: `S56-M-0653-ANCHOR_AUDIT`  
Base revision: `3dfb8575e8f56f817e48b9846f7ff2fbd146b603`

## Result

The repository-local exact artifact is the elaborated proposition definition
`Stage1.THM_M_0653.BethDefinabilityTarget`, not a theorem with a proof body. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` provides formula definability, reduct and theory-map
machinery, compactness, and finite entailment APIs. The seven retained declarations elaborate in
`AnchorAudit.lean`, but none states the uniform implication from uniqueness over all common
reducts to one old-language defining formula.

No exact external Lean 4 proof candidate was found by the bounded public searches. Sourcegraph's
Beth/implicit-definability and Craig-interpolation alias queries both completed with zero matches;
GitHub repository searches completed with zero results. GitHub code search required authentication,
so that lane is a blocker rather than a negative result. The complete Git tree of
`google-deepmind/formal-conjectures@b2e608fc52d765510915a244bb69b1a2741acc3c` had 1204 entries and
no matching path. Search responses are dated and hashed discovery evidence, whereas mathlib and
the Formal Conjectures tree are bound to immutable commits.

The exact root therefore remains `M3`: an exact statement and useful interfaces exist, but no
terminal proof body was located. This finishes the bounded anchor-audit node only; it is not a
global absence claim and supplies no proof, full-audit, or theorem-completion credit.

## Commands and results

Commands ran on 2026-07-12 inside the worker clone. Existing `.lake` artifacts were used read-only;
no update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0653` | 0 | rank 698, planned, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0653/Statement.lean` | 0 | exact canonical target re-elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0653/AnchorAudit.lean` | 0 | seven pinned supporting declarations elaborated |
| `rg -n -i '\bbeth\b|implicitly[ _-]?defin|explicitly[ _-]?defin|craig.{0,30}interpolat|interpolat.{0,30}craig' Formalizations/Lean/.lake/packages/mathlib/Mathlib/ModelTheory --glob '*.lean'` | 1 | expected no-match exit; no terminal named candidate in pinned model-theory source |
| Sourcegraph Beth/implicit-definability alias query | 0 | `matchCount=0`; SHA-256 `9eae8c256c2aee252f94c48d01e98b7c299fa9d3c70c65eaec3f396d4d677222` |
| Sourcegraph Craig-interpolation alias query | 0 | `matchCount=0`; SHA-256 `93fdf2f44eb94c5cd0c18be408ceda30995e2c997a6e7fe93a55f04d02d6f7fa` |
| GitHub REST repository searches for Beth definability and Craig interpolation with Lean | 0 | both `total_count=0`, complete; identical response SHA-256 `08c082f...2600b2` |
| GitHub REST code search for `"Beth definability" language:Lean` | 0 | response captured; HTTP 401 blocker; SHA-256 `b7dbd173...5e29e` |
| GitHub immutable recursive-tree inspection of `formal-conjectures@b2e608...` | 0 | non-truncated 1204-entry tree, no matching path; response SHA-256 `76fa3f...efc61` |
| `python3 -m json.tool Stage1_Instances/THM-M-0653/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0653 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Open integration gate

Reopen integration only for a candidate with an immutable revision, exact declaration and type
mapping, toolchain and dependency graph, terminal-body provenance, license, placeholder and axiom
audit, and a successful repo-local wrapper check. Until then no `M0-P`, `M1`, audit-completion, or
theorem-completion credit is valid.
