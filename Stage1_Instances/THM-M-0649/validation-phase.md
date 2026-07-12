# S56-M-0649-VALIDATION worker evidence

Date: `2026-07-12`. Base revision: `560c2540d43ab8a1495ff6772047b9ec8ea0f708`.

The narrow validator copied `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and the
proof-free `Validation.lean` exact-type wrapper into a fresh temporary module directory. It invoked
the pinned Lean executable directly through `lake env`, produced fresh oleans, and checked both the
proof-phase root and the independently elaborated wrapper. Both declarations report exactly
`propext`, `Classical.choice`, and `Quot.sound`; `sorryAx` is absent. The manifest and local mathlib
checkout agree at revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, and that dependency
worktree is clean. No recipe fetched or updated a dependency.

This is nonrelease evidence. The worker reused the canonical warm `.lake` symlink, host-level
network denial was not established, and no cold empty-cache replay, complete TCB/SBOM closure, or
distinct runner was available. The frozen obligation graph also predates `Proof.lean` and still
reports `M0649-T-TV` open, so master reconciliation is required before any accepted M0 state.
Human-source `H0` and readable-reconstruction `R0` reviews remain open. Consequently this phase is
self-tested but does not establish theorem completion or release.

## Commands and results

All commands ran from the repository root unless the working directory is stated explicitly.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0649` | 0 | rank 695; planned; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0649/check_obligation_tree.py` | 0 | 17 frozen obligations and 84 typed edges; graph root open M3 |
| `(cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0649/check_validation.py)` | 0 | fresh-module exact-root replay, exact axiom set, input hashes, hygiene, and pinned provenance passed |
| `rg -n "\\b(sorry\|admit\|sorryAx)\\b\|^[[:space:]]*(axiom\|unsafe)\\b\|\\bimplemented_by\\b"` over the four Lean sources | 1 | expected no-match result |
| `python3 -m json.tool` over validation spec and receipt | 0 | both artifacts are valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0649 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

First failed gate: `evidence.frozen_graph_freshness`. Further failed release gates are
`hermetic.cold_empty_cache`, `trust.complete_tcb_sbom`, `source.H0_independent_review`,
`readability.R0_independent_review`, and `independent.distinct_runner`.
