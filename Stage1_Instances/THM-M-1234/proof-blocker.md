# THM-M-1234 proof-phase blocker

Item: `S56-M-1234-PROOF`  
Validation date: `2026-07-14` (`Asia/Shanghai`)  
Base revision: `bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`

## Verdict

`blocked`: no eligible proof body for the exact universal Yudovich existence
target exists in the repository or the pinned Lean dependency closure. The
root remains `M3`, the theorem is incomplete, and this attempt creates neither
a proof receipt nor `.stage1-worker-selftest.json`.

The checked declaration
`Stage1Rev56.THMM1234.root_of_construction_and_closure` consumes
`CandidateConstructionPackage` and `EquationAndTraceClosurePackage`; it does
not inhabit either package. The minimal frozen root cut therefore remains
`M1234-A-STRUCTURE` plus `M1234-E-CLOSURE`. Its first executable failure is
`M1234-A-APPROX`: neither repo-local Lean nor pinned mathlib constructs smooth
global Euler approximants for every frozen `InitialData` witness.

The existing `Proof.lean` bodies are real but narrower. They prove that zero
initial data is admissible and construct the identically zero solution. The
canonical root quantifies over every admissible `u0` and `omega0`, so the
zero-data body is a boundary case, not a substitute for the assigned target.
The replay reports `[propext, Classical.choice, Quot.sound]` for these bodies.

Closing the exact root requires placeholder-free proofs of smooth global
approximation, uniform energy and bounded-vorticity estimates,
nonlinear-compatible compactness, preservation of divergence and curl,
passage of the linear and quadratic momentum terms, and the one-sided initial
vorticity trace. The prerequisite audit found no exact immutable external Lean
body to pin. Assuming either package, adding an axiom, or weakening the
quantifiers would violate the frozen registry.

## Validation evidence

All commands ran in this worker clone using the existing canonical pinned Lake
artifacts. No `lake update`, `lake build`, dependency clone/fetch, network
search, or `.lake` mutation was performed. The pre-existing untracked `.lake`
symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1234` | 0 | Rank 158, planned lifecycle, hard mathlib-anchor lane, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1234/check_obligation_tree.py` | 0 | 14 obligations and 28 typed edges passed; denominator `cfa0a02c68993c8b3eefc0edfe7d3d7bd20e2b58d140f47a1f5444a8ba734c5d`; root open at M3. |
| `tmp=$(mktemp -d /tmp/thm-m-1234-replay.XXXXXX); cp Stage1_Instances/THM-M-1234/{Statement,ObligationTree,Proof}.lean "$tmp"; LEAN_BIN=$(cd Formalizations/Lean && lake env which lean); LEAN_PATH_PINNED=$(cd Formalizations/Lean && lake env printenv LEAN_PATH); cd "$tmp"; LEAN_PATH="$LEAN_PATH_PINNED" "$LEAN_BIN" -o Statement.olean Statement.lean; LEAN_PATH=".:$LEAN_PATH_PINNED" "$LEAN_BIN" -o ObligationTree.olean ObligationTree.lean; LEAN_PATH=".:$LEAN_PATH_PINNED" "$LEAN_BIN" Proof.lean` | 0 | Statement, conditional composition, and all three zero-data declarations elaborated. The conditional composition and zero-data declarations report `[propext, Classical.choice, Quot.sound]`. |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)\|^\s*unsafe\b\|sorryAx' Stage1_Instances/THM-M-1234 --glob '*.lean'` | 1 | Empty output: no prohibited declaration, placeholder, unsafe declaration, or `sorryAx`; exit 1 means no match. |
| `rg -ni 'yudovich\|incompressible[ -]?euler\|bounded vorticity\|vorticity' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | Empty output: no matching pinned mathlib source; exit 1 means no match. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |

## Reopen condition

Provide local placeholder-free bodies, or an immutable compatible pinned
dependency, for every obligation in the frozen analytic cut. The next proof
attempt must then check exact package types, terminal-body provenance, axiom
closure, and the existing child-to-root composition. Primary-source scope,
the weak-curl sign convention, and spacetime-integrability requirements also
remain review risks for the later source and release gates.
