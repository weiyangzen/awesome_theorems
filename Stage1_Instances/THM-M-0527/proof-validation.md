# THM-M-0527 proof-phase validation

Item: `S56-M-0527-PROOF`

Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`

## Implemented bodies

`Proof.lean` contains a placeholder-free proof of the full fiber-classification
branch for existing pointed connected covers. Its exact terminal declaration is

```lean
inducedSubgroup P = inducedSubgroup Q ↔ Isomorphic P Q
```

The forward proof constructs comparison lifts from the two range inclusions,
uses covering-lift uniqueness to prove the maps inverse, and assembles a
pointed homeomorphism over the base. The reverse proof explicitly composes the
induced-map naturality equality with surjectivity of the homomorphism induced
by the homeomorphism and then identifies ranges. Support lemmas also derive
local path-connectedness of covering total spaces.

The following frozen nodes receive substantive proof bodies or checked
composition: `M0527-FIB`, `M0527-FIB-FWD`, `M0527-FIB-LIFT-PQ`,
`M0527-FIB-LIFT-QP`, `M0527-FIB-INVERSE`, `M0527-FIB-HOME`,
`M0527-FIB-OVER`, `M0527-FIB-REV`, `M0527-FIB-REV-MAP`, and
`M0527-FIB-REV-RANGE`. Their registry interfaces are still planned
fingerprints and the predecessor graph has no composition certificates, so
this worker claims zero complete frozen obligations pending master
reconciliation.

## Boundary

The exact root remains open at `M3`. No pinned proof constructs the connected
cover associated to an arbitrary subgroup, and therefore `M0527-EX-COVER` and
`M0527-EX-RANGE` remain the proposed post-proof cut set. Pinned mathlib's
lifting criterion only compares covers already supplied. The audited Atlas
root contains `by sorry`; the inspected external universal-cover construction
does not quotient by arbitrary subgroups.

`typed-graphs.json` is the frozen predecessor snapshot and still includes
`M0527-FIB` in its cut set. It was not modified. Exact fingerprint and
child-to-parent receipt reconciliation belongs to the integration lane. Thus
`theorem_complete=false`, accepted state is unchanged, and downstream
validation/release gates remain open.

## Commands and exact results

Validation reused the pre-existing canonical pinned `.lake` artifacts. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0527` | 0 | Rank 584; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0527/check_obligation_tree.py` | 0 | Frozen registry passed with 34 obligations; predecessor root open M3. |
| `python3 Stage1_Instances/THM-M-0527/check_statement.py` | 0 | Exact expression fingerprint and all three killed mutations passed. |
| `bash Stage1_Instances/THM-M-0527/check_proof.sh` | 0 | Statement and all local proof declarations elaborated under `--trust=0`; each declaration reported exactly `[propext, Classical.choice, Quot.sound]`; packet, pin, and source checks passed. |
| prohibited-device scan over `Proof.lean` | 1 | Expected no-match exit; no executable placeholder, bodyless axiom/constant, unsafe/opaque/extern declaration, implementation escape, or native oracle. |
| JSON validation over receipt, blocker, and self-test | 0 | All three files parsed without error. |
| `git diff --check -- Stage1_Instances/THM-M-0527 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |

This packet proposes `[_]` only for the self-tested proof-phase contribution.
It is warm-cache nonrelease evidence, not master acceptance, a proof of the
surjectivity half, validation/release evidence, or theorem completion.
