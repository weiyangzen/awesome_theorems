# Anchor-audit validation record

Item: `S56-M-0001-ANCHOR_AUDIT`  
Base revision: `4fe35307a2ed7cb6e80278de2f6b6fd3866fcb12`

## Result

The pinned mathlib module supplies the connecting morphism, its two zero-composition lemmas, and
all three exactness families matching the frozen target. Narrow Lean adapters for each target
position elaborate at mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
The observed axiom set is `propext`, `Classical.choice`, and `Quot.sound`.

This is classified `M1`, not `M0-W`: the downstream proof phase must add the canonical root wrapper,
and the validation/release phases must establish full declaration provenance, accepted foundation
and TCB closure, hermetic replay, and independent evidence. The legacy local wrapper is `M3` because
its proposition is only one adjacent window. Anonymous GitHub repository searches found no other
candidate; unauthenticated code-search endpoints failed with HTTP 401/429, so exhaustive discovery
is not claimed.

## Commands and results

All commands ran in this worker clone. Lean ran from `Formalizations/Lean` against the existing
pinned Lake environment. No update, fetch, clone, or other `.lake` mutation command was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0001/AnchorAudit.lean` | 0 | six declarations typechecked; three exact-position adapters elaborated; axiom sets printed |
| `python3 ../../Stage1_Instances/THM-M-0001/check_anchor_audit.py` | 0 | immutable mathlib revision/tree/clean state and both candidate source hashes verified; root classification `M1` |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a1783...a95`, tree `bdc39a...c2b` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard and all 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets valid |
| `python3 scripts/stage1_target.py show THM-M-0001` | 0 | rank 96, planned, L0/rework-required, theorem incomplete |
| scoped forbidden-term scan over new Lean/Python artifacts | 1 | no proof-gap declaration found; 1 is ripgrep's no-match exit |
| `git diff --check -- Stage1_Instances/THM-M-0001 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This completes only the provisional anchor-audit phase pending master acceptance. It does not
complete the full target audit or theorem.
