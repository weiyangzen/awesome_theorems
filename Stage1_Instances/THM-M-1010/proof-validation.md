# THM-M-1010 partial proof validation

Item: `S56-M-1010-PROOF`

Base revision: `ff3db6d51326417873f49c410421f8f3e13be993`

## Implemented body

`Proof.lean` now defines `CommonMarginalData` and proves
`exists_common_space_exact_marginals`. For any sequence `muSeq` and limit law `mu`, the theorem
constructs one probability space in the required universe together with measurable random
variables having every prescribed law. It indexes all laws by `Option Nat` and applies pinned
mathlib's `exists_hasLaw_indepFun`, so the product sample type remains `Type u`.

This is substantive partial progress toward `M1010-C-COUPLING`, `M1010-L-MEASURABLE`, and
`M1010-L-LAWS`. It is not a Skorokhod coupling: the variables supplied by the library construction
are independent and no convergence relation is proved. Therefore this receipt claims zero new
frozen obligations closed. The pre-existing constant-law representation remains a valid boundary
body but does not close the universal root.

## Remaining blocker

The exact target still needs a convergence-compatible common-space construction. The first missing
frozen leaf is `M1010-N-PARTITIONS`, followed by compatible allocation and the one-null-set
stabilization argument. The remaining root cut set is:

```text
M1010-N-PARTITIONS
M1010-C-INTERVAL
M1010-L-MEASURABLE
M1010-L-LAWS
M1010-L-AE-STABILIZE
```

The last two remain in the cut set because the new marginal theorem proves their fields only for an
independent product realization, not for the future convergence-compatible Skorokhod construction.
The root vector stays `[H1, M3, R3]`; `proof_phase_complete=false` and
`theorem_complete=false`.

## Commands and exact results

Validation reused the automation-provided canonical pinned `.lake` symlink read-only. No `lake
update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. Lean objects were
written only below `/tmp` and removed by the validation script.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets at the L0/rework-required baseline passed. |
| `python3 scripts/stage1_target.py show THM-M-1010` | 0 | Rank 290; planned hard-mathlib anchor/wrapper lane; theorem incomplete. |
| `timeout 240 python3 -B Stage1_Instances/THM-M-1010/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges passed; root explicitly remained open M3. |
| `bash Stage1_Instances/THM-M-1010/check_proof.sh` | 0 | Statement, obligation composer, and proof module elaborated under `--trust=0`; all three proof declarations reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 -B Stage1_Instances/THM-M-1010/check_proof.py` | 0 | Item scope, source hashes, dependency pins, receipt, blocker boundary, and worker packet passed. |
| Prohibited-device scan over owned Lean sources | 1 expected | No executable `sorry`, `admit`, `sorryAx`, bodyless axiom/constant, unsafe/opaque/extern declaration, implementation escape, or native oracle matched. |
| `git diff --check -- Stage1_Instances/THM-M-1010 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |

The worker packet proposes `[_]` only for this self-tested partial proof contribution. It is not
master acceptance, validation or release evidence, a closed frozen obligation, a proof of `Target`,
or theorem completion.
