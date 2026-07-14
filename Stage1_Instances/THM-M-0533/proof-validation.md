# THM-M-0533 proof-phase validation

Item: `S56-M-0533-PROOF`

Date: `2026-07-15T05:19:00+08:00`

Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`

Base tree: `d881fd9641fa3e5f3ebe5082b35672981e90adcf`

## Implemented body

`Proof.lean` adds the genuine local theorem
`AwesomeTheorems.THM_M_0533.firstMap_comp_secondMap`. It proves, for every
space, pair of opens, and degree, that the frozen signed map from intersection
homology followed by the sum of the two inclusion maps is zero. The proof
identifies the two underlying composites into the ambient space and uses
functoriality plus cancellation of a map with its negative.

This is one field of `ConstructionPackage`, so it is partial progress toward
`M0533-T-CONSTRUCTION`. It does not construct the connecting maps or either of
their zero-composite laws. Because the frozen node is the complete package, no
whole frozen obligation is claimed closed.

## Open boundary

The first unavailable substantive leaf remains `M0533-C-SUBDIVISION`. Pinned
mathlib has the generic `ShortExact.δ` and `homology_exact₁/₂/₃`
machinery, but it has no cover-small singular-chain construction, subdivision
chain homotopy, excision bridge, relative singular homology, or singular
Mayer-Vietoris theorem. Its Mayer-Vietoris declarations concern sheaf
cohomology and cannot be transported to this covariant singular-homology
target.

Consequently the exact root remains `[H3, M3, R4]`. `ConstructionPackage`,
`ExactnessPackage`, and `MayerVietorisSequence` remain uninhabited. This is a
self-tested partial proof delta, not theorem completion.

## Narrow validation evidence

All commands ran in this worker clone using the existing canonical pinned Lake
artifacts. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0533` | 0 | rank 590; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0533/check_obligation_tree.py` | 0 | 19 obligations and 37 typed edges passed; denominator `238242df...8dfc`; root open M3 |
| `bash Stage1_Instances/THM-M-0533/check_proof.sh` | 0 | isolated trust-zero `Statement -> ObligationTree -> Proof` replay passed; the source/axiom scan found no prohibited device, and the new declaration reported exactly `propext`, `Classical.choice`, and `Quot.sound` |
| `rg -n '\b(sorry|admit|sorryAx|implemented_by|native_decide)\b|^[[:space:]]*(axiom|constant|opaque|unsafe|extern)[[:space:]]+' Stage1_Instances/THM-M-0533 --glob '*.lean'` | 1 | expected no-match exit; no prohibited proof device occurs in owned Lean sources |
| `python3 -m json.tool` on `proof-receipt.json`, `proof-blocker.json`, and `.stage1-worker-selftest.json` | 0 each | all structured artifacts parsed |
| `git diff --check -- Stage1_Instances/THM-M-0533 .stage1-worker-selftest.json` | 0 | no whitespace errors |

`check_proof.sh` writes all generated `.olean` and output files below a
temporary `/tmp/thm-m-0533-proof.*` directory and removes it on exit. The
automation-provided `.lake` symlink is pre-existing, untracked, and reused
read-only, so this is scoped nonrelease evidence.

## Reopen condition

Resume after implementing the frozen subdivision, small-chain quasi-isomorphism,
signed chain short exact sequence, boundary, naturality, recurring exactness,
and degree-zero endpoint packages without placeholders, or after locating an
immutable exact Lean 4 proof whose terminal bodies and dependencies validate in
the pinned environment.
