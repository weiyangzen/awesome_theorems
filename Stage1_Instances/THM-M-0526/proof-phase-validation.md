# THM-M-0526 proof-phase validation

Item: `S56-M-0526-PROOF`

Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`

## Implemented Bodies

`Proof.lean` retains the previously integrated proofs of `SVK-MAP-FUNCTORIALITY` and
`SVK-SQUARE`. This run adds `path_subdivision_of_two_open_cover`, a placeholder-free compactness
body for the frozen `SVK-LEBESGUE-NUMBER` leaf. It pulls the two open sets back along an arbitrary
path, applies mathlib's finite subdivision theorem for the unit interval, and proves that every
resulting subpath has range contained in the selected cover member.

The new result is strictly within the frozen route: it does not weaken or replace the exact based
pushout target. The proof receipt proposes provisional closure of three obligations, while accepted
state and the root vector remain unchanged pending master review.

## Validation

Validation reused the pre-existing canonical pinned `.lake` artifacts read-only. The replay copied
the three Lean inputs under a fresh `/tmp` module tree and wrote all `.olean` outputs there. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0526` | 0 | Rank 583; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0526/check_obligation_tree.py` | 0 | Frozen registry passed with 17 obligations, nine leaves, and 16 proof edges. |
| `bash Stage1_Instances/THM-M-0526/check_proof.sh` | 0 | Statement, composition harness, and all three local bodies elaborated with `--trust=0`; their axiom reports were subsets of `propext`, `Classical.choice`, and `Quot.sound`. |
| prohibited-device scan over `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` | 1 | Expected no-match exit; no executable forbidden proof device. |
| `python3 Stage1_Instances/THM-M-0526/check_proof.py` | 0 | Item scope, exact target and denominator, source hashes, dependency pins, receipt, blocker, worker packet, and open-root boundary passed. |
| `git diff --check -- Stage1_Instances/THM-M-0526 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |

## Boundary

The exact `SeifertVanKampenTarget` is still blocked. The next failed gate is
`SVK-CHANGE-BASEPATH`: segment endpoints must be transported to the common basepoint compatibly
inside `U`, `V`, and their intersection. Word definition, refinement and homotopy invariance, the
lift homomorphism, generation, and uniqueness also remain open. Consequently neither
`LiftExistence` nor `LiftUniqueness` is available, and the exact composition harness cannot close
the root.

This worker packet proposes `[_]` only for the self-tested partial proof contribution. It does not
claim master acceptance, validation or release, audit completion, root closure, or theorem
completion.
