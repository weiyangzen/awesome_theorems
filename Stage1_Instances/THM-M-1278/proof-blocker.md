# THM-M-1278 partial-proof boundary

Item: `S56-M-1278-PROOF`  
Base revision: `35d23d0193cd7c8fccb1d09f22534c6eba066b02`

## Verdict

This proof phase made genuine, self-tested partial progress but did not close the Onofri theorem.
`Proof.lean` constructs the smooth representative `subtractMean u`, proves the exact frozen
`M1278-N-SUBTRACT-MEAN` interface, and proves that this selected shift preserves tangential
gradients and Dirichlet energy. Thus `M1278-N-SUBTRACT-MEAN` and `M1278-N-ENERGY` have local proof
bodies pending master acceptance.

The energy theorem is deliberately specialized to `subtractMean u`; it does not assert an
invariant for an arbitrary unrelated representative. The supporting gradient lemmas receive no
additional obligation credit.

## Remaining Blocker

The first failed gate remains `M1278-L-SHARP-ONOFRI`. No repository-local, pinned-mathlib, or
audited immutable external Lean 4 declaration proves the exact sharp zero-mean estimate for the
frozen Hausdorff-area and tangential-gradient encoding. The sphere-area and finiteness/positivity
interfaces also remain in the root cut. Downstream zero-mean, exponential-shift, logarithmic
transport, complete `MeanShiftTransport`, and exact root composition cannot close until those
inputs have real bodies.

The remaining root cut is exactly `M1278-L-SHARP-ONOFRI`, `M1278-S-AREA`, and
`M1278-S-FINITE`. The root vector stays `[H2, M3, R4]`; `root_closed=false`,
`audit_complete=false`, and `theorem_complete=false`.

There is also a frozen architecture risk: `ObligationTree.lean` redeclares the statement's sphere
function structure in a different namespace rather than importing it. Lean structures are nominal,
and no checked transport currently connects `THM_M_1278_Obligations.Root` to the canonical
`THM_M_1278.OnofriInequality`. These partial bodies therefore close only the two frozen
obligation-tree nodes. A later root proof needs a checked bridge or shared definitions before it can
receive canonical-target credit.

## Replay Boundary

The narrow replay runs `bash Stage1_Instances/THM-M-1278/check_proof.sh`. It invokes the pinned
Lean 4.29.0 executable directly with `--trust=0`, one thread, explicit existing compiled-package
paths, and disposable output under `/tmp`. It does not invoke Lake, access the network, or run a
dependency update, build, clone, or fetch.

The worker's pre-existing untracked `.lake` symlink targets the shared canonical cache. An
incomplete `flt-regular` checkout from concurrent or earlier activity was observed there, so this
replay intentionally bypasses Lake and excludes that incomplete package. This is nonrelease worker
evidence, not a clean cold build.

Both credited declarations elaborate and report exactly `[propext, Classical.choice, Quot.sound]`.
Retry root execution only after a real exact sharp-estimate body is available and the remaining
area, side-condition, and transport obligations can be closed without placeholders.
