# Intake validation

Base revision: `e1e156a5ecde6311a98efe69be284ba9e7d11414`.

Validation ran on 2026-07-12 in the worker clone. It covers manifest consistency, the planned
dossier's structured invariants, pinned environment identity, and changed-file hygiene. No Lean
target was elaborated: the source record names an axiom system but does not determine whether the
formal root is a definition, a concrete-model theorem, or a characterization theorem. Elaborating
one of those choices at intake would substitute an invented target. The existing `.lake` artifacts
were only queried; no update, build, clone, fetch, or dependency mutation was run.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0538` | 0 | Rank 595, planned, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | SHA-256 `651c8acc...b1d2` and `321626c8...2d81` |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | 0 | Both structured artifacts parsed |
| scoped Python intake assertions | 0 | `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0538 .stage1-worker-selftest.json` | 0 | No whitespace errors |

## Known downstream failures

Primary-source pinpointing and independent review, resolution of the theorem-versus-definition
fork, the exact Lean expression and mutation tests, formal-candidate and trust audit, obligation
registry, proof, hermetic replay, and independent validation remain open. Accepted receipt IDs:
none. First downstream gate: `S56-M-0538-STATEMENT`. The remaining root cut set begins with exact
source assertion identity and a canonical statement; theorem completion is false.
