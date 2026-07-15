# THM-M-0996 proof-phase validation

Item: `S56-M-0996-PROOF`

Base revision: `718e166c56e53c552ebb861ee01427f9a606fc72`

## Implemented proof bodies

`Proof.lean` adds placeholder-free bodies for several parts of the frozen
positive-dimensional route. The canonical orthonormal coordinate isometry
preserves standard Gaussian measure and open metric thickenings. It also
transports a unit half-space and its complete profile formula, so the
coordinate child is consumed by a checked half-space composition.

The Riesz representer of a unit functional gives the exact identity

```text
Metric.thickening r {x | L x <= c} = {x | L x < c + r}
```

for `0 < r`. Projection of `stdGaussian` along `L`, together with Gaussian
atomlessness, computes both the original half-space mass and every positive
open thickening. Continuity and strict monotonicity of the real Gaussian CDF
prove that its finite-threshold masses have range exactly `Set.Ioo 0 1`.
This supports a total inverse-CDF `halfspaceProfile` and the exact local
inhabitant `halfspaceEnlargementFormula`.

The source also retains the zero-dimensional vacuity proof, positive-finrank
consequence, conditional dimension recomposition, and exact conditional
composer from `GeneralSetEnlargementBound halfspaceProfile` to the canonical
target. The isolated replay checks 34 proof declarations and one obligation-tree declaration
under `--trust=0`.

## Classification boundary

These are genuine partial proof bodies, but the frozen obligation registry
records `planned:v1` fingerprints rather than exact elaborated obligation
types. It does not bind terminal bodies, dependency provenance, and exact
child-to-parent composition for these nodes. No frozen obligation is
provisionally closed by this packet. All six supported IDs are classified as
partial progress.

The frozen registry and typed graphs are untouched. Their authoritative open
cut remains `M0996-L-HALFSPACE` and `M0996-L-GENERAL`. In particular, this
packet does not replace that cut with an informal mathematical estimate.
`GeneralSetEnlargementBound halfspaceProfile` is not proved, so the canonical
root remains M3 and `theorem_complete=false`.

No external proof body is credited. The existing `anchor-audit.json` records
no exact external candidate and discovery searches with zero repository
results. Current receipt, blocker, and validation evidence make no unsupported
external-project assertion.

`ObligationTree.lean` now imports the canonical `Statement` module instead of
duplicating `IsUnitHalfspace` and `GaussianIsoperimetricTarget`. This is the
correct module boundary, but it changes the predecessor source bytes. The
earlier obligation-tree evidence is therefore stale and requires integration
re-review; its DAG state is merely observed, never accepted or inherited.

## Commands and exact results

Validation reused the automation-provided canonical pinned `.lake` symlink
without dependency update, build, clone, fetch, or intentional mutation. The
tree is dirty and the replay is warm-cache nonrelease worker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `bash -n Stage1_Instances/THM-M-0996/check_proof.sh` | 0 | Shell syntax passed. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0996` | 0 | Rank 276; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0996/check_obligation_tree.py` | 0 | The frozen 19-obligation, seven-graph architecture passed; authoritative root remains open M3. This structural check does not refresh the changed predecessor Lean evidence. |
| `nice -n 19 bash Stage1_Instances/THM-M-0996/check_proof.sh` | 0 | Isolated `Statement -> ObligationTree -> Proof` replay passed under `--trust=0`; 1 tree and 34 proof declarations each reported exactly `propext`, `Classical.choice`, and `Quot.sound`. Exact replay hashes are bound in `proof-receipt.json`. |
| `python3 Stage1_Instances/THM-M-0996/check_proof.py` | 0 | Scope, pins, module chain, dynamic declaration inventory, hashes, zero-closure boundary, stale predecessor boundary, changed paths, and open root passed. |
| prohibited-device scan over `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` | 1 | Expected no-match exit; no executable placeholder, declared axiom, unsafe/opaque/extern body, implementation escape, or native oracle. |
| `git diff --check -- Stage1_Instances/THM-M-0996 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |

The `[_]` packet records self-tested partial proof work. It is not predecessor
or master acceptance, a validation/release result, root closure, audit
completion, or theorem completion.
