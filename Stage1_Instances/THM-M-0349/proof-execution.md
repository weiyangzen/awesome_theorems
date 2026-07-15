# THM-M-0349 proof execution

Item: `S56-M-0349-PROOF`
Date: `2026-07-15`
Base revision: `3a40b1969f841e07036db5c4d7f03e97c7c57949`

## Implemented body

`Proof.lean` now contains a concrete candidate body for analytic obligation `M0349-L-L2`. It
transports an arbitrary period-one `L2` function through mathlib's Fourier Hilbert basis, multiplies
its square-summable coefficient sequence by `conjugateMultiplier`, and transports the sequence
back. The diagonal multiplier has modulus at most one, so the resulting function is an `L2`
contraction. The checked declaration `conjugate_l2_bound` supplies a conjugate function with the
all-integer Fourier identity and the sharp constant-one norm bound.

The frozen registry describes `M0349-L-L2` only as `planned exact L2 estimate`; it has no exact Lean
type, owned source, evidence ID, or terminal proof body. Consequently this worker cannot establish
an exact type/fingerprint match or a composition certificate. The body is substantive,
self-tested progress toward that node, not provisional node closure. Master reconciliation must
first freeze or approve the exact node interface.

The older one-mode body remains useful partial progress toward `M0349-C-POLYNOMIAL`, but that
planned polynomial interface is not claimed closed. The exact all-`p` root also remains open:
`M0349-L-WEAK11`, interpolation, extension, Fourier identification, and both root packages still
need proof bodies. The minimal open root cut remains `M0349-P-EXISTENCE` and `M0349-P-BOUND`;
`theorem_complete=false`.

## Validation

Validation reused the canonical pinned Lean artifacts without `lake update`, `lake build`, clone,
fetch, or other dependency mutation. The top-level Lake project was temporarily obstructed by an
unrelated incomplete `flt-regular` checkout, so `check_proof.sh` invokes `lake env lean` through the
pinned mathlib Lake project and constructs `LEAN_PATH` only from the canonical prebuilt package
directories. Compilation is isolated in `/tmp`, runs with `--trust=0 -t0`, and leaves no target
`.olean`.

| Command | Exit | Recorded result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0349` | 0 | Rank 842; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0349/check_obligation_tree.py` | 0 | Frozen 15-node registry and all 69 typed edges passed; predecessor root remains open. |
| `bash Stage1_Instances/THM-M-0349/check_proof.sh` | 0 | Pinned `lake env lean` replay elaborated `conjugate_l2_bound` and the two earlier declarations; every axiom report was exactly `[propext, Classical.choice, Quot.sound]`. |
| `python3 -I -B Stage1_Instances/THM-M-0349/check_proof.py` | 0 | Source hygiene, frozen-input mismatch boundary, pins, receipt, blocker, packet, and open root passed. |
| prohibited-construct scan over `Proof.lean` | 1, expected | No executable placeholder, declared axiom/constant, opaque/unsafe/extern declaration, implementation escape, or native oracle. |
| JSON parsing for receipt, blocker, and packet | 0 | All structured evidence parsed without duplicate keys. |
| `git diff --check -- Stage1_Instances/THM-M-0349 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |

This is warm-cache nonrelease worker evidence proposing `[_]` for the proof phase only. It is not
master acceptance, validation/release evidence, root closure, or theorem completion.

## Remaining blocker

The first failed mapping gate is the absence of an exact frozen Lean target for `M0349-L-L2`.
Beyond that reconciliation, the first central missing analytic body is `M0349-L-WEAK11`. The
pinned tree has the Fourier Hilbert basis and `L2` infrastructure used here, but no periodic weak
`(1,1)` conjugate-function estimate or Marcinkiewicz interpolation theorem. A bounded external
search found an immutable project at revision
`8e93bee110628f230e2b6e11611d231ede5981ab` contains relevant Hilbert-transform strong-type work,
but it targets Lean 4.31.0 and mathlib `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`, not this pinned
Lean 4.29.0/mathlib environment. It supplies an integration lead, not kernel proof credit here.
