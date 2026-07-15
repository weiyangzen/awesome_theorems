# THM-M-0321 proof-phase validation

Item: `S56-M-0321-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `5bb515438bd0e1d53584e5243c5d434dfde7158e`

## Implemented proof

`Proof.lean` now inhabits the exact frozen `MarkovKakutaniTarget`. For one continuous affine
self-map, it constructs Cesaro averages of an orbit. Convexity keeps those averages in `K`, while
a telescoping identity expresses their displacement as
`(n + 1)⁻¹ • (g^[n + 1] x - x)`. Compactness makes `K - K` von Neumann bounded, so this
displacement tends to zero. An ultrafilter cluster point supplied by compactness, continuity on
`K`, and Hausdorff uniqueness then give a genuine fixed point.

Finite induction applies that theorem to the compact convex common fixed locus of the maps already
inserted. Pairwise commutation makes this locus invariant. Finally,
`continuousCompactnessUpgrade` uses closed fixed loci and `IsCompact.inter_iInter_nonempty` to
upgrade all finite-family witnesses to a point fixed by the arbitrary family.
`markovKakutani_proof` has exactly the canonical target. The proof contains no `sorry`, `admit`,
custom axiom, unsafe/opaque declaration, native oracle, external implementation, or weakened
theorem. Lean reports only `propext`, `Classical.choice`, and `Quot.sound`.

## Frozen interface defect

The prerequisite obligation tree froze `ObligationTree.CompactnessUpgrade` without continuity or
closedness of the fixed loci. That proposition is false for arbitrary maps. On compact
`K = Set.Icc (0 : Real) 1`, maps can be chosen with fixed sets
`Set.Ioc 0 (1 / (n + 1))`; every finite intersection is nonempty, while their total intersection
is empty. The exact root is not affected because it already assumes continuity. The local proof
uses that assumption directly and does not inhabit the false helper.

Accordingly, no closure credit is proposed for the defective `M0321-N-INFINITE` interface or the
frozen `M0321-T-UPGRADE` composition route through it. The sound `continuousCompactnessUpgrade`
proves the intended root-scoped mathematical upgrade, and the exact root and other implemented
proof nodes are provisional machine-closure candidates. The architecture owner must reconcile the
defective intermediate interface. The worker did not edit
the frozen registry, typed graph, obligation tree, or authoritative state.

## Commands and results

All validation reused the automation-provided canonical pinned `.lake` artifacts. No `lake update`,
`lake build`, dependency clone/fetch, or `.lake` mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0321` | 0 | Rank 687; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0321/check_obligation_tree.py` | 0 | Frozen 30-obligation registry and 33 typed edges passed; its pre-proof accepted snapshot remained M3. |
| `bash Stage1_Instances/THM-M-0321/check_proof.sh` | 0 | Disposable mirrored modules elaborated with `--trust=0`; the exact root and all audited helpers used only the three allowed classical axioms or none; no `sorryAx` or error occurred. |
| `python3 Stage1_Instances/THM-M-0321/check_proof.py` | 0 | Exact root, source and input hashes, pinned environment, receipt, defect boundary, placeholder policy, and changed-path scope passed. |
| `python3 -m json.tool Stage1_Instances/THM-M-0321/proof-receipt.json` | 0 | Provisional exact-root proof receipt parsed. |
| `python3 -m json.tool Stage1_Instances/THM-M-0321/proof-blocker.json` | 0 | Frozen-interface defect record parsed. |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | Worker self-test packet parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0321 .stage1-worker-selftest.json` | 0 | No scoped whitespace diagnostics. |

The Lean replay derives the executable and `LEAN_PATH` through `lake env`, copies only the three
owned modules to a disposable mirrored tree, compiles the prerequisite oleans, and checks
`Proof.lean` with `LEAN_NUM_THREADS=1`, `--trust=0`, and `-t0`. It audits every expected
`#print axioms` report and deletes the tree on exit.

## Status boundary

This proof phase is self-tested and proposes repo-local exact-root `M0-L` only after master
acceptance. E0 acceptance remains downstream. Accepted state remains H2/M3/R4. Validation, release, H0, R0, complete
provenance and trust closure, cold hermetic replay, independent verification, AUDIT-Z, THEOREM-Z,
and theorem completion remain open.
