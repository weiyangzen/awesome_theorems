# THM-M-0389 anchor audit

Item: `S56-M-0389-ANCHOR_AUDIT`  
Audit cutoff: 2026-07-12 (Asia/Shanghai)  
Base revision: `d20c5ace90ece18172510a4b9764b93d0ebfbecf`

## Result

The frozen root is the complete integer classification in `Statement.lean`,
not merely the Markov equation or existence of a solution. The audit found no
terminal theorem for that root in pinned mathlib or in the bounded external
Lean 4 searches. The root therefore remains `M3`; no external integration task
can truthfully be opened from this inventory.

The legacy repo-local file is useful but is not a root proof. Its
`StatementShape` is a statement-only `Prop` definition. Its actual theorem
bodies cover the zero and seed cases, equation symmetries, Vieta-move
soundness, generated-triple soundness, coordinate permutations, three small
descent bridges, and conditional packaging. They leave the positive-descent
converse, nonzero sign lift, and unconditional root composition open.

## Candidate table

| Surface | Immutable identity | Finding | Root credit |
|---|---|---|---|
| Repo-local legacy Lean | repository `d20c5a...`; `S1_M_020.lean` SHA-256 `b57e16...a7a4a` | Exact-shape statement candidate plus genuine partial proofs; no theorem inhabits `StatementShape` | none |
| mathlib4 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` | No Markov/Markoff equation/triple classification declaration in `Mathlib` or `Archive` | none |
| GitHub repository API | response hashes in `anchor-audit.json` | Exact phrase/alias repository queries returned zero relevant Lean projects; broader `markov lean4` hits were probability/category projects | none |
| Sourcegraph global Lean | response hashes in `anchor-audit.json` | Zero relevant matches for the exact name and equation queries | none |

GitHub's unauthenticated code-search endpoint returned HTTP 401, so that lane
is recorded as an access limitation rather than silently treated as a negative
result. Sourcegraph excluded forks and archived repositories by default. These
are bounded discovery results, not a claim that no formalization exists.

The Crossref lookup located Markoff's 1879 paper (DOI
`10.1007/BF02086269`) only as a bibliographic lead. No pinpoint theorem/page,
assumption mapping, errata review, or qualified review was established, so the
human-source status stays `H4`, not `H0`.

## Validation

All commands ran in this worker clone and reused the existing pinned `.lake`
artifacts. No dependency update, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0389/check_anchor.py` | 0 | legacy candidate compiled from source; exact axiom reports captured for six audited partial/bridge theorems (`propext`, with `Classical.choice` and `Quot.sound` on tactic-heavy algebra leaves) |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0389/Statement.lean` | 0 | frozen canonical target still elaborates |
| pinned mathlib `rg` query recorded in `anchor-audit.json` | 0 | only unrelated polynomial-shape hits; no Markov classification candidate |
| repo-local `rg` query recorded in `anchor-audit.json` | 0 | only the legacy `S1_M_020` candidate and metadata/source prose |
| GitHub and Sourcegraph queries recorded in `anchor-audit.json` | 0 except documented HTTP 401/404/403 limitations | no relevant external candidate; exact response hashes recorded |
| `python3 -m json.tool Stage1_Instances/THM-M-0389/anchor-audit.json >/dev/null` | 0 | audit inventory is valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure passes |
| `python3 scripts/stage1_target.py check` | 0 | 1546 ordered uniform-L0 targets pass |
| `git diff --check -- Stage1_Instances/THM-M-0389 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This phase is self-tested anchor-audit work pending master acceptance. It does
not claim proof, validation, release, `AUDIT-Z`, or theorem completion.
