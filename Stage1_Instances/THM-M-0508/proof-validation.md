# THM-M-0508 proof-phase attempt

Item: `S56-M-0508-PROOF`  
Date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `e3d0fd205c9c81486cb86f68cdc66d4d4e5bb264`

## Verdict

`blocked`: no eligible proof body for the exact Vinogradov three-primes target exists in the
repository or pinned dependency closure. The immediate unavailable proof package is
`M0508-N-FOURIER`, the ternary exponential-sum integral identity for the frozen finite
representation count. The first open root cut also includes the arc partition, major-arc
asymptotic, positive singular-series estimate, and minor-arc bound.

`ObligationTree.lean` already contains genuine unconditional bodies for
`representationCount_pos_iff` and the child-to-root composition
`root_of_eventualPositiveRepresentationCount`. The latter requires
`EventualPositiveRepresentationCount` as an explicit premise and therefore does not prove it. The
prerequisite immutable anchor audit found no eligible terminal Lean proof: the only relevant
external declaration discovered was stronger but had a literal `sorry` body and was rejected.
A fresh bounded scan of pinned mathlib found no matching terminal theorem.

Closing the target requires a new formalization of the ternary circle method, including the
Fourier normalization, major/minor arc construction, major asymptotic, singular-series positivity,
minor estimate, and eventual-positivity assembly. Postulating any package, importing the rejected
placeholder, or presenting the conditional composition as the root proof would violate the frozen
target. Root debt remains `M4`, `root_closed=false`, and `theorem_complete=false`. Because the
assigned proof phase is incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Narrow validation evidence

All commands ran in this worker clone and reused the canonical pinned Lake artifacts. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0508` | 0 | rank 882; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0508/check_obligation_tree.py` | 0 | 17 obligations and 86 typed edges passed; denominator `79ff122b...53bc2`; root open M4 |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0508/Statement.lean)` | 0 | exact canonical threshold target elaborated and printed |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0508/ObligationTree.lean)` | 0 | count equivalence and conditional root composition elaborated; both axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; three nonfatal linter warnings |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b\|^[[:space:]]*unsafe\\b' Stage1_Instances/THM-M-0508 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder, axiom declaration, or unsafe declaration found |
| bounded `rg -n -i` scan for Vinogradov/three-primes/ternary-Goldbach/weak-Goldbach terms in pinned mathlib Lean sources | 0 | only broad-term elementary prime hits; no relevant terminal theorem |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `sha256sum` on statement, conditional assembly, registry, and anchor audit | 0 | `e27734b0...080da`; `576a3fc6...a172`; `1f5afb02...d695`; `dcb3df3d...53d00` |

## Reopen condition

Resume only after a placeholder-free implementation of the frozen circle-method packages, or
discovery of an immutable compatible Lean 4 proof that can be pinned, exact-type transported, and
validated in the repository closure.
