# S56-M-1023-PROOF worker validation

Item: `S56-M-1023-PROOF`  
Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`  
Validation date: `2026-07-15` (`Asia/Shanghai`)

## Implemented proof

`Vendor/LeanLevy` contains the 20-module transitive source closure needed by the immutable
`slink/LeanLevy@93b635fba23398bfb1f0db8d220f88172f6900b6` real-line Levy-Khinchin
characterization and unique-triplet proof. The full MIT license, per-file upstream and port hashes,
and the exactly reversible two-edit Lean 4.29 compatibility delta are recorded by
`VENDOR_PROVENANCE.md` and `vendor-manifest.json`.
The generator checks each reconstructed file against an independently pinned upstream SHA-256 and
recomputes the normalized compatibility patch. The exact archive endpoint is recorded for
provenance, but no validation command downloads it.

`Proof.lean` kernel-checks a term of the unchanged canonical target. It proves equivalence of the local and upstream
recursive convolution powers. For the convention mismatch, it proves integrability of `x` on
`{x | |x| = 1}`, transports the drift by that boundary moment, and checks equality of the open and
closed truncation exponents. The forward direction transports upstream representation and triplet
uniqueness. The reverse direction derives that the represented measure is a probability measure
from its characteristic function at zero, invokes the upstream characterization, and transports
the exact convolution roots back.

The isolated replay compiled all 20 vendored modules from source in a new temporary directory with
`--trust=0`; it did not use or create owned `.olean` files. Lean reported all four inspected
declarations sorry-free. The exact root and upstream representation, converse, and uniqueness
declarations depend only on `propext`, `Classical.choice`, and `Quot.sound`.

## Commands and results

All checks used the existing automation-provided `.lake` symlink read-only. No `lake update`,
`lake build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1023` | 0 | rank 499; planned hard-mathlib-anchor-and-wrapper lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1023/check_obligation_tree.py` | 0 | frozen 17-obligation, 46-edge architecture passed; denominator `d4c7d2a1...80c825`; pre-proof projection remains root-open |
| `python3 Stage1_Instances/THM-M-1023/build_vendor_manifest.py` | 0 | reconstructed 20 source streams, matched 20 independently pinned upstream hashes, recomputed the 1004-byte two-edit patch, and regenerated the manifest |
| `bash Stage1_Instances/THM-M-1023/check_proof.sh` | 0 | fresh trust-zero source compilation of 20 vendored modules, `Statement.lean`, and `Proof.lean`; four declarations sorry-free; all four axiom closures matched the allowed three axioms |
| `python3 Stage1_Instances/THM-M-1023/check_proof.py` | 0 | source/provenance/pin/receipt/self-test invariants and exact proof identity passed |
| `python3 -m json.tool` on `vendor-manifest.json`, `proof-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts parsed |
| `git diff --check -- Stage1_Instances/THM-M-1023 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

The final isolated replay ran from `2026-07-15T06:42:20+08:00` through
`2026-07-15T06:52:50+08:00`. Its 644-byte combined output had SHA-256
`c00758ddfd88696c9ddf7d0d79c579053cfd3ecfe1e58a04d0b9397edd013565`.

## Status boundary

This is proof-node evidence proposing only `[_]`, pending predecessor and master acceptance. It
establishes a placeholder-free kernel inhabitant of the exact canonical root in the current pinned
environment. The packet proposes only `M1023-ROOT`; it does not retroactively close the frozen
planned child route, whose declaration/fingerprint reconciliation belongs to the master. It does
not establish accepted graph reconciliation, complete transitive foundation
or TCB review, `H0`, `R0`, cold hermetic replay, independent verification, downstream validation or
release, audit completion, or theorem completion. The pre-existing untracked `.lake` symlink makes
this worker evidence nonrelease input.
