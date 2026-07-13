# THM-M-0990 proof-phase attempt

Item: `S56-M-0990-PROOF`  
Date: `2026-07-14` (`Asia/Shanghai`)  
Base revision: `f3a2545c7e6634696c48f725a9581e7e248c8877`

## Verdict

`blocked`; no proof body was added and no proof credit is claimed.

The exact target `Stage1Instances.THM_M_0990.StatementShape` re-elaborates in the pinned Lean
environment. `ObligationTree.root_compose` also re-elaborates, but it merely returns an already
assumed inhabitant of the exact root. The frozen terminal `M0990-T-TRIANGULAR-BRIDGE` has no proof
body. The legacy `LyapunovData` route is equally conditional because it stores the missing
characteristic-function Taylor bridge as a `Prop` field.

Pinned mathlib's terminal central limit theorem is for one identically distributed sequence and
cannot prove the non-identically-distributed triangular-array target. Its finite independent-sum
factorization and Levy theorem are useful substrate. However, `taylor_charFun_two` supplies only a
qualitative little-o expansion for one fixed law, not the quantitative `2 + delta` remainder
uniformly summable over a growing triangular array.

The first unavailable analytic package is therefore `M0990-L-CHARFUN-ENTRY`. Closing the frozen
bridge also requires centering and variance normalization on the eventual positive tail, moment
and independence transport, Lyapunov infinitesimality, product convergence to the Gaussian
characteristic function, and Levy/Gaussian transport. No exact terminal declaration was found in
the pinned source closure or the prerequisite immutable-candidate audit. Assuming any of these
packages, using the iid theorem, or treating conditional composition as closure would be a
placeholder or substituted theorem.

The root stays `[H2, M3, R4]`, `root_closed=false`, and `theorem_complete=false`. Because the
assigned proof phase is incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Narrow validation

All commands used the existing automation-provided pinned `.lake` symlink read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0990` | 0 | rank 270; planned; L0/rework-required; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0990/Statement.lean` | 0 | exact canonical target and three mutation propositions elaborated and printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0990/ObligationTree.lean` | 0 | exact duplicated root and conditional composition elaborated; `#print axioms` reported `[propext, Classical.choice, Quot.sound]` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0990/AnchorAudit.lean` | 0 | iid CLT and supporting characteristic-function declarations elaborated at pinned types |
| `python3 Stage1_Instances/THM-M-0990/check_obligation_tree.py` | 0 | 18 obligations and 43 typed edges passed; denominator `fa799ae8...921f6`; root remains open M3 at `T-TRIANGULAR-BRIDGE` |
| pinned source search for `lyapunov`, `lindeberg`, and `triangular array` | 1 | no matching terminal or named supporting declaration in mathlib, its Archive, or flt-regular |
| forbidden-device scan over owned Lean files | 1 | expected no-match result: no `sorry`, `admit`, custom `axiom`, `sorryAx`, `unsafe`, or oracle |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

## Reopen condition

Resume after a placeholder-free implementation of the frozen triangular-array
characteristic-function packages, or after discovery of an immutable compatible Lean 4 terminal
proof that can be pinned, imported, exact-type transported, and checked without changing the
dependency lock. Until then the remaining root cut is `M0990-T-TRIANGULAR-BRIDGE`, downstream
validation and release are ineligible, and theorem completion remains false.
