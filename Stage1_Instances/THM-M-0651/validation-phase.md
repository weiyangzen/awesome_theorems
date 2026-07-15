# THM-M-0651 validation-phase evidence

Item: `S56-M-0651-VALIDATION`. Base revision:
`9254a0ec0d0c71b346ae15a911721409e3ab3139`; base tree:
`a3de0086d55c8f209894b07409deeeed04c393a3`.

## Validation scope

The structured recipe re-elaborates disposable copies of `Statement.lean`,
`ObligationTree.lean`, `ProofLemmas.lean`, and `Validation.lean`. Every Lean
process runs with `--trust=0 -t0` in a Bubblewrap network namespace. The host
root, toolchain, and canonical pinned dependency cache are read-only; only a
fresh temporary output directory is writable.

`Validation.lean` imports the canonical statement but neither the proof module
nor the obligation-tree module. It separately reconstructs the omission
transport, the fair combined schedule, and the dense nonprincipality step.
This is same-worker differential evidence, not rev-5.6 independent
verification. It provides no Henkin construction, no proof that the resulting
model omits the types, and no unconditional canonical root declaration.

The validator binds the canonical expression, frozen denominator, partial
proof receipt, local source hashes, exact mathlib revision/tree/remote,
selected source and compiled-object hashes, license, and executable identities.
All checked partial bodies are sorry-free. Their observed axiom closure is
contained in `propext`, `Classical.choice`, and `Quot.sound`. The differential
closure contains 8384 declarations from 329 modules, with no unexpected
bodyless nonaxiom or unsafe declaration. This is a trust observation, not an
accepted foundation policy, serialized transitive provenance graph, or
complete release TCB inventory.

## Commands and results

All commands ran in this worker clone on 2026-07-15 (Asia/Shanghai). The
pre-existing canonical pinned `.lake` symlink was reused read-only. No `lake
update`, `lake build`, dependency clone, fetch, or dependency mutation was
performed.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0651` | 0 | rank 697, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0651/check_statement.py` | 0 | expression hash `789c281a...c43`; both frozen mutations killed |
| `python3 Stage1_Instances/THM-M-0651/check_obligation_tree.py` | 0 | 11 obligations and 21 typed edges passed; root open M4 |
| `bash Stage1_Instances/THM-M-0651/check_proof.sh` | 0 | eight partial bodies replayed at trust zero; exact root remained open |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0651/check_validation.py --worker-packet .stage1-worker-selftest.json` | 0 | network-isolated trust-zero Lean replay, selected provenance, receipt, and fail-closed decisions passed |
| `python3 -m json.tool` on the spec, receipt, and worker packet | 0 | all validation JSON documents parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0651-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0651/check_validation.py` | 0 | checker syntax compiled outside the repository |
| `git diff --check -- Stage1_Instances/THM-M-0651 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | Fresh outputs elaborate the exact statement, conditional tree, all eight partial proof bodies, and three no-import differential declarations. |
| Placeholder and unsafe boundary | provisional pass | Parser-aware source scans pass; `assert_no_sorry` passes; the differential closure has no bodyless nonaxiom or unsafe declaration. |
| Axiom observation | provisional pass | Checked bodies use only the selected classical trio, but no accepted theorem-specific foundation or complete TCB profile exists. |
| Selected provenance | provisional pass | Local hashes, pinned mathlib revision/tree/origin/license, and four selected source/olean boundaries agree. Complete transitive provenance remains open. |
| Proof dependency and exact root | fail closed | The proof receipt is unaccepted, closes zero frozen obligations, and supplies no joint Henkin/omission proof or checked cross-module canonical root composition. |
| Human source and readability | fail closed | Pinpoint primary-source H0 and independently reviewed R0 evidence are absent. |
| Hermetic release replay | fail closed | Shared warm artifacts are not a clean checkout, empty-cache cold build, offline restoration, or complete SBOM/TCB archive. |
| Independent verification | fail closed | The differential module shares this worker, checkout, toolchain, and cache; there is no distinct signed verifier or independently provisioned runner. |

The frozen root remains `[H1, M4, R3]`. Its cut set is
`M0651-L-ENUM`, `M0651-L-DENSE`, `M0651-L-HENKIN`, and
`M0651-L-OMIT`. The first unavailable terminal construction is the joint
Henkin package, and the frozen `AvoidanceInterface` is too strong because its
candidate retains no avoidance invariant. The available obligation-tree root
also duplicates the target definitions without a checked bridge to the
canonical statement.

This validation node is self-tested only as an honest, nonrelease blocked
receipt. It grants no accepted obligation closure, `M0-*`, `E0/E1`,
`AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or master acceptance.
