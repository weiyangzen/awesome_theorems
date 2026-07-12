# THM-M-1143 proof-phase validation

Item: `S56-M-1143-PROOF`. Base revision:
`fcf07b444b4fc685fd4c015fff26d66c7354f325`.

## Verdict

`blocked`: this execution closes two genuine leaves of the frozen proof architecture, but no
eligible proof of the exact root exists in the repository or pinned dependency closure.
`Proof.lean` implements `M1143-N-BOUND` by extracting a uniform absolute-value bound from the
bounded range, and implements `M1143-L-CONSTANT` as the full
`ZeroDerivativeConstantPackage` using mathlib's mean-value theorem. It then kernel-checks the
exact root composition from an explicit `VanishingDerivativePackage` premise.

The remaining immediate root cut is `M1143-T-VANISH`. Its first unavailable substantive leaf is
`M1143-L-GRADIENT`, the arbitrary-positive-dimensional interior gradient estimate for harmonic
functions. Pinned mathlib provides harmonic-function Liouville only on the complex plane; its
general inner-product-space harmonic API contains definitions and elementary closure operations,
but no n-dimensional mean-value, gradient-estimate, or bounded-harmonic Liouville theorem. The
plane theorem cannot close a target quantified over every positive `n`.

No axiom, bodyless declaration, placeholder, unsafe declaration, or weakened/substituted target
was introduced. Because the requested proof phase is not complete, this attempt deliberately does
not create `.stage1-worker-selftest.json`.

## Narrow validation evidence

All commands ran in the worker clone on 2026-07-12 and reused the existing pinned Lake artifacts.
No update, build, dependency clone/fetch, or `.lake` mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets pass. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1143` | 0 | Rank 348, planned, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1143/check_obligation_tree.py` | 0 | Frozen obligation architecture passes. |
| Compile `Statement.lean` and `ObligationTree.lean` to temporary local oleans, then run `Proof.lean` with `lake env lean`; remove the temporary oleans | 0 | Both new proof bodies and conditional exact-root composition elaborate. `#print axioms` reports only `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg -n -i 'bounded.*harmonic\|harmonic.*constant\|gradient.*harmonic' --glob '*.lean' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis` | 0 | The only bounded-harmonic Liouville declaration is the complex-plane theorem; no arbitrary-dimensional gradient theorem is present. |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s|$)|\bunsafe\b' Stage1_Instances/THM-M-1143/Proof.lean` | 1 | No prohibited token found; exit 1 means no match. |
| `git diff --check -- Stage1_Instances/THM-M-1143` | 0 | No whitespace errors. |

The pinned mathlib revision is `8a178386ffc0f5fef0b77738bb5449d50efeea95`; the available
toolchain is Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.

## Reopen condition

Resume after a placeholder-free implementation or immutable eligible import of
`VanishingDerivativePackage`, including the n-dimensional interior gradient estimate and the
radius-to-infinity limit. Until then the exact root remains open at `M3`, downstream validation and
release remain ineligible, and theorem completion is false.
