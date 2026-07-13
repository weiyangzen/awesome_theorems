# THM-M-0325 proof-phase attempt

Item: `S56-M-0325-PROOF`  
Date: `2026-07-13` (`Asia/Shanghai`)  
Base revision: `bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`

## Verdict

`blocked`: no eligible proof body for the exact finite real Grothendieck
inequality exists in the repository or pinned dependency closure. The minimal
root cut remains `M0325-T-PACKAGE`. Its first unavailable substantive core is
`M0325-K-TRANSFORM`, the construction and universal bound for the real
Grothendieck/Krivine transform. The finite-span and Gram reductions, correlated
random-sign rounding, measurability and integrability, scalar-bound
application, and expectation estimate also remain open.

`ObligationTree.lean` defines `GrothendieckProofPackage` to be the canonical
target and proves only `target_of_proofPackage package := package`. That body is
a checked conditional identity, not a construction of `package`, so it receives
no root proof credit. The prerequisite anchor audit found only generic pinned
projective/injective tensor-seminorm substrate. In particular, the available
injective-to-projective comparison does not provide the missing universal
scalar-to-Hilbert estimate. A fresh bounded source scan likewise found no
Grothendieck/Krivine theorem or correlated Gaussian-sign identity in pinned
mathlib.

Closing the target would require a substantial new formalization of every open
analytic package above, or an immutable compatible terminal Lean 4 proof that
can be pinned and exact-type checked. Introducing the proof package as an axiom
or premise, or reporting the conditional composition as the theorem, would be
a placeholder or substituted theorem. Root debt therefore remains `M3`,
`root_closed=false`, and `theorem_complete=false`. Because the assigned proof
deliverable is incomplete, `.stage1-worker-selftest.json` is deliberately
absent.

## Narrow validation evidence

All commands ran in this worker clone using the existing canonical pinned Lake
artifacts. No `lake update`, `lake build`, dependency clone/fetch, or other
dependency mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0325` | 0 | rank 214; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0325/check_obligation_tree.py` | 0 | 15 obligations and 33 typed edges pass; denominator `4c41e44f32c7c300ac25319a49fd14dcf197599756525b2dec8dcdce4207703c`; root open `M3` because the analytic proof package remains `M4` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0325/Statement.lean` | 0 | exact canonical target, expanded-shape transport, mutations, and empty-index boundary elaborate; canonical target printed |
| scoped temporary `Statement.olean`, followed by `ObligationTree.lean` through `lake env lean` and the pinned `LEAN_PATH`; temporary olean removed | 0 | conditional composition elaborates; `#print axioms` reports only `propext`, `Classical.choice`, and `Quot.sound` |
| `rg -n -i '\\b(grothendieck.?inequal\|grothendieckinequality\|grothendieckconstant\|krivine\|random.?round\|gaussian.*sign\|sign.*gaussian\|arcsin.*expect\|expect.*arcsin)\\b' --glob '*.lean' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | hits are historical audit strings, an unrelated polynomial Gaussian comment, and an unrelated Levy-Khintchine statement comment; no terminal theorem or analytic rounding body |
| `rg -n '\\b(sorry\|admit\|sorryAx)\\b\|^[[:space:]]*axiom\\b\|^[[:space:]]*unsafe\\b' Stage1_Instances/THM-M-0325 --glob '*.lean'` | 1 | expected no-match exit; no prohibited Lean placeholder, axiom declaration, or unsafe declaration |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `sha256sum Stage1_Instances/THM-M-0325/{Statement.lean,ObligationTree.lean,obligation-registry.json,anchor-audit.json}` | 0 | `a24ef5cd...eb1e`; `224e289b...abf8`; `9afd6408...9587b`; `fb87d78f...0d6e` |

## Reopen condition

Resume only after a placeholder-free implementation of `M0325-T-PACKAGE` and
its frozen dependencies, or discovery of an immutable compatible Lean 4 proof
whose exact type, terminal body, dependency closure, and axioms can all be
validated in the pinned environment.
