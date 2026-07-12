# THM-M-1091 anchor-audit validation

Item: `S56-M-1091-ANCHOR_AUDIT`  
Theorem: `THM-M-1091`  
Base revision: `e7fc1469ef5eb468d13c2ccc07a94982bc51ab75`  
Validation date: 2026-07-12 (Asia/Shanghai)

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains both an
exact kernel-power anchor and its setwise integral form. `AnchorAudit.lean` checks direct bridges
at exact copies of both separately elaborated frozen expressions. The kernel bridge uses `Kernel.pow_add kappa n m` and normalizes `n+m`,
which is necessary because mathlib's displayed composition order and the frozen chronological
order name the step counts oppositely.

The bridge is an `M0-P` candidate, not proof-node credit. The audit remains `H1`: mathlib's
Meyn-Tweedie citation was not independently source-checked. No theorem completion is claimed.

## Commands and results

All commands ran in this worker clone using existing pinned Lake artifacts. No update, build,
clone, fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1091` | 0 | Rank 533, planned, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1091/AnchorAudit.lean` | 0 | Both exact bridges elaborated; both anchors and bridges reported only `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-1091/check_anchor_audit.py` | 0 | Pin, clean mathlib tree, exact source bodies, no source placeholder, and fail-closed classifications verified |
| `python3 -m json.tool Stage1_Instances/THM-M-1091/anchor-audit.json` | 0 | Structured audit parses |
| `rg -n -i 'chapman.?kolmogorov\|pow_add_apply_eq_lintegral' --glob '*.lean' --glob '*.md' --glob '*.json' . Formalizations/Lean/.lake/packages` | 0 | Located the pinned family and repo-local duplicate wrappers; no independent exact repo-local proof body |
| GitHub repository search API for `\"Chapman-Kolmogorov\" Lean` | 0 | Zero repositories; broader Markov-chain results were not admitted as candidates without exact declarations and immutable revisions |
| `git diff --check -- Stage1_Instances/THM-M-1091 .stage1-worker-selftest.json` | 0 | No whitespace errors |

## Status boundary

The candidate inventory, exact types, revisions, bodies, axioms, placeholder boundary,
integration feasibility, external-search limitation, source debt, and root decision are frozen.
Master acceptance is pending. Proof adoption, obligation graphs, kernel-closure credit, source
fidelity, hermetic replay, and independent validation remain downstream work.
