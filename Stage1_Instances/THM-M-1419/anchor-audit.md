# Anchor audit

Item: `S56-M-1419-ANCHOR_AUDIT`  
Base revision: `28be4ce7383f582503e6b54f645e2ca0e955d9de`

## Result

The complete pinned mathlib source tree at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` has useful deterministic
subadditivity, ergodicity, integrability transport, flag, and Grassmannian
infrastructure, but no named Kingman or terminal Oseledets declaration. The
repo-local `S1_M_248.lean` is a separately owned legacy statement and
infrastructure inventory; it explicitly leaves the terminal theorem open and
receives no proof credit.

A credible external Lean 4 candidate was found and frozen at
`marcmorningstar/lean4-ergodic-theory@3882faed7d0a9c332d3e7c0fb38a5f6d48f29864`.
Its `ErgodicTheory.oseledets_splitting` is a substantive two-sided finite-matrix
splitting theorem. Immutable source inspection also found a guarded axiom audit
for the declaration and the project's Apache-2.0 license.

The candidate is not an exact closure of this target. It uses a measurable
equivalence, pointwise measurability and invertibility, its own
`IntegrableLogNorm`, `EuclideanSpace`/L2 matrix action, measurable-subspace, and
cocycle APIs. The canonical statement instead uses a plain equivalence plus a
separate preservation hypothesis, AE strong measurability and invertibility,
the Pi-space norm, distance-to-fiber measurability, and its own forward product.
No checked transport between these interfaces exists. The external project is
also pinned to Lean `4.30.0-rc2` and mathlib `34f7a6cd...`, incompatible with
this clone's Lean `4.29.0` and mathlib `8a178386...`; it is absent from the Lake
closure and worker policy forbids fetching it. Thus the honest classification
is `[H2, M3, R3]` / `E3`, not M0.

## Validation

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 1546-target rev-5.6 standard is consistent |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered `L0/rework_required` targets |
| `python3 scripts/stage1_target.py show THM-M-1419` | 0 | rank 688, planned, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1419/AnchorAudit.lean)` | 0 | canonical statement and seven nearby pinned-mathlib declarations resolve |
| pinned-source `rg` searches recorded in `anchor-audit.json` | 1 for terminal-name query | no mathlib terminal Oseledets or Kingman declaration; exit 1 denotes no match |
| `git ls-remote https://github.com/marcmorningstar/lean4-ergodic-theory.git refs/heads/main` | 0 | candidate frozen at `3882faed7d0a9c332d3e7c0fb38a5f6d48f29864` |
| immutable raw GitHub reads at that SHA | 0 | theorem types, guarded trust record, license, toolchain, and mathlib pin inspected |
| `python3 -m json.tool Stage1_Instances/THM-M-1419/anchor-audit.json` | 0 | structured audit parses |
| `git diff --check -- Stage1_Instances/THM-M-1419 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This completes candidate discovery and classification only. It does not claim
source fidelity, external integration, a proof, audit completion, or theorem
completion. Master acceptance is still required.
