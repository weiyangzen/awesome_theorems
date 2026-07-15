# THM-M-1056 proof worker validation

Item: `S56-M-1056-PROOF`

Base revision: `118d66d1986768cd9a00e661ccf6447c26a53efb`

Validation date: `2026-07-15` (`Asia/Shanghai`)

## Implemented route

`External/Oseledets/ErgodicTheory` contains the complete 62-module source closure for
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`.
The Apache-2.0 license, immutable archive digest, per-file upstream and port hashes, frozen build
order, and reversible 26-file Lean 4.29 compatibility patch are bound by `vendor-manifest.json`,
`VENDOR_PROVENANCE.md`, and `check_vendor.py`. No compiled dependency artifact is vendored.

The target-local bridge conjugates arbitrary finite-dimensional real fibers to Euclidean
coordinates, transports both positive-log integrability assumptions and cocycle growth, invokes
`ErgodicTheory.oseledets_splitting`, constructs measurable oblique projectors from the measurable
internal sum, and pulls every splitting field back to the original fiber. `Proof.lean` exposes a
premise-free theorem whose type is exactly the frozen
`Stage1Instances.THM_M_1056.OseledetsMultiplicativeErgodicTarget`.

## Fresh replay

The final checked-in replay began with a new temporary tree containing zero oleans. It compiled all 62
vendored sources in `order.txt`, then `Statement.lean`, the eight bridge modules, and `Proof.lean`
with `LEAN_NUM_THREADS=1`, `lake env lean --trust=0 -t0`, and fresh output directories. It reused
only the existing pinned mathlib dependency artifacts, performed no update/build/fetch/clone, and
created no owned olean. Start was `2026-07-15T18:25:03+08:00`; end was
`2026-07-15T18:46:35+08:00`; exit was 0. Its complete 41,487-byte combined log has SHA-256
`6713bca4ed4554030a394c12bc85df28c0b6f284a96c2c9b2eab996ae894e0d5`.

The replay produced 62 external and 10 target oleans. The terminal olean SHA-256 was
`3f3165b7a9a58ab36f769fa03d68c4d520fec734dc45a7672c6733a3d3067197`; the proof olean SHA-256
was `1395882599505941aacb0351643f5236bec923b6e09661968e64401876eab176`. An exact probe checked
both public root names at the canonical target type. The external terminal, concrete wrapper, and
both root aliases were sorry-free and depended exactly on `propext`, `Classical.choice`, and
`Quot.sound`.

The historical olean ledger is provenance rather than a reproducibility gate. A fresh replay
matched 61 of its 62 hashes. `ErgodicTheory.Ergodic.Kingman.BlockSqueeze` repeatedly produced
SHA-256 `5115f2ae295b03503f97bdac623e52fa2c4927ef9716afc597878f9f134a5545` (1,170,672 bytes), while
the historical ledger records `5128ae1d5a9692d5d73229d23a6ab09e42c22352debd2cd0a145cf24108f7fc2`
(1,169,800 bytes). Its source hash matches exactly, repeated fresh outputs match each other, every
module kernel-checks, and the terminal olean reproduces exactly; no all-62 olean-hash reproduction
claim is made.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1056` | 0 | rank 248; planned; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1056/check_statement.py` | 0 | expression `8e1a96a...403b`; all four mutations distinguished |
| `python3 Stage1_Instances/THM-M-1056/check_obligation_tree.py` | 0 | 19 obligations, 49 typed edges, frozen denominator `5246a9d...b57828`; pre-proof graph remains open |
| `python3 Stage1_Instances/THM-M-1056/check_vendor.py` | 0 | 62 sources, 1,504,769 bytes, reversible 26-file port, no prohibited devices |
| `bash Stage1_Instances/THM-M-1056/check_proof.sh` | 0 | fresh copied-source trust-zero replay of 62 external and 10 target modules; exact root/axiom probe passed |
| `python3 Stage1_Instances/THM-M-1056/check_proof.py --require-receipt` | 0 | source, provenance, frozen scope, receipt, and no-completion boundaries passed |
| `python3 -m json.tool` on all new JSON artifacts | 0 | all structured artifacts parsed |
| parser-aware prohibited-device scan over all 75 owned Lean sources (72 active proof-replay inputs) | 0 | no placeholder, bodyless declaration, unsafe/extern hook, or native oracle |
| `git diff --check -- Stage1_Instances/THM-M-1056 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status boundary

This packet is self-tested proof-node evidence proposing only `[_]`. The frozen pre-proof graph
still names `M1056-T-CORE` as open and cannot be rewritten by this worker. The packet therefore
records an observed exact-root kernel inhabitant but proposes no accepted obligation closure or
debt-vector change. Dependency-ordered master reconciliation and acceptance, full transitive
foundation/TCB review, cold hermetic replay, independent signed validation, `H0`, `R0`, downstream
validation and release, `AUDIT-Z`, `THEOREM-Z`, and theorem completion remain open.
