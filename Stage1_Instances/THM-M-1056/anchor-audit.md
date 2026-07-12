# Anchor audit record

Item: `S56-M-1056-ANCHOR_AUDIT`  
Base revision: `fc440f22c0e7587c75465d0dd18454622b2740db`

## Result

The complete pinned mathlib tree at `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains useful deterministic subadditivity, ergodicity, integrability-transport, flag, and
Grassmannian infrastructure, but no Kingman theorem or terminal Oseledets declaration. The legacy
`S1_M_248.lean` file is likewise a statement/infrastructure inventory and receives no proof credit.

A credible external Lean 4 candidate was found and frozen:
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`.
Its `ErgodicTheory.oseledets_splitting` is a substantive two-sided finite-matrix splitting theorem,
and its guarded source audit reports only `propext`, `Classical.choice`, and `Quot.sound`. It is not
an exact match for the canonical target: it uses matrices and Euclidean space and produces
measurable submodules, whereas the target is polymorphic in a finite-dimensional normed space and
requires strongly measurable complementary continuous projections. No checked transport exists.
Moreover, the upstream pin requires Lean `4.30.0-rc2` and mathlib `34f7a6cd...`, incompatible with
this clone's Lean `4.29.0` and mathlib `8a178386...`. Fetching/building it would violate worker
dependency policy. The honest classification is therefore `[H1, M3, R3]` / `E3`, not M0 or M1.

## Validation

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1056/AnchorAudit.lean` | 0 | all five pinned-mathlib infrastructure families resolve |
| `rg -l -i 'Oseledets|multiplicative ergodic|Lyapunov exponent|Kingman|subadditive ergodic' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | only nearby ergodic/function infrastructure; no terminal declaration |
| `git ls-remote https://github.com/marcmorningstar/lean4-ergodic-theory.git refs/heads/main` | 0 | immutable candidate revision `ed3fa6b8a30594eeb791160563942ba115581aa0` |
| immutable `raw.githubusercontent.com` reads of `MultiplicativeErgodic.lean`, `TwoSided/SplittingAssembly.lean`, `test/AxiomAudit.lean`, `lake-manifest.json`, and `lean-toolchain` at that SHA | 0 | declarations, types, trust guards, toolchain, and dependency revision inspected |
| `python3 -m json.tool Stage1_Instances/THM-M-1056/anchor-audit.json` | 0 | structured audit parses |
| `git diff --check -- Stage1_Instances/THM-M-1056` | 0 | no whitespace errors |

This phase audits candidates only. External integration, an exact wrapper, proof closure, and master
acceptance remain open.
