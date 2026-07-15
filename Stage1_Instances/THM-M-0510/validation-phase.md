# THM-M-0510 validation-phase result

Item: `S56-M-0510-VALIDATION`. Base revision:
`472dc79eb4d406a6707691193fbe3ab58d0f0cc4`.

## Narrow validation

The structured recipe re-elaborates the exact statement and the five local
Euler-product declarations at trust level zero. `Validation.lean` imports
neither `Proof` nor `ObligationTree`; it separately reconstructs the ordinary
partition series and reciprocal Euler-product normalization from the pinned
`Partition.Glaisher` and power-series interfaces. This checks only
`M0510-N-EULER-PRODUCT`. It is not a proof of coefficient extraction, contour
estimates, the circle method, or the Hardy-Ramanujan root.

Every Lean subprocess runs inside a bubblewrap network namespace with a
read-only host root, a fresh writable temporary directory, fixed locale,
timezone, and thread count, and `--trust=0 -t0`. All seven checked proof bodies
report exactly `propext`, `Classical.choice`, and `Quot.sound`. The differential
module reports both declarations sorry-free; its observed closure has 16,524
declarations in 617 modules, with no unexpected bodyless nonaxiom or unsafe
declaration. Nested-comment-aware scans find no placeholder, bodyless local
declaration, unsafe declaration, native oracle, or implementation escape in
the checked local sources.

Selected direct provenance also agrees: Lean 4.29.0 commit `98dc76e3`, mathlib
revision `8a178386` and tree `bdc39a31`, canonical remote and license, and the
source blobs and compiled artifacts for `Partition.Basic`,
`Partition.Glaisher`, and `PowerSeries.PiTopology` are hash-bound. The
`Glaisher` dependency is important because the earlier anchor inventory did
not record the all-parts specialization later used by `Proof.lean`.

## Commands and results

Commands ran from the repository root on 2026-07-15 (Asia/Shanghai). The
automation-provided `.lake` symlink was reused read-only. No `lake update`,
`lake build`, dependency clone, dependency fetch, or `.lake` mutation was run.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0510` | 0 | rank 884, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0510/check_obligation_tree.py` | 0 | 17 obligations, 59 typed edges, denominator `59e9147c...167dd`; structured root open M3 |
| `bash Stage1_Instances/THM-M-0510/check_proof.sh` | 0 | fresh temporary trust-zero replay of `Statement.lean` and `Proof.lean`; five exact classical-trio axiom reports; root explicitly open |
| `python3 -I -B Stage1_Instances/THM-M-0510/check_validation.py --probe` | 0 | network-isolated fresh-output replay; output hashes `15b6b13d...104d3`, `2e9c6ee3...e8b2`, and `c32f2ad9...da2a`; closure 16,524/617 and selected provenance passed |
| `python3 -I -B Stage1_Instances/THM-M-0510/check_validation.py --worker-packet .stage1-worker-selftest.json` | 0 | the same replay plus receipt, structured-spec, state-boundary, and worker-packet checks passed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0510-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0510/check_validation.py` | 0 | checker syntax compiled outside the repository |
| JSON parsing for the validation spec, receipt, and worker packet | 0 | all three documents parsed |
| `git diff --check -- Stage1_Instances/THM-M-0510 .stage1-worker-selftest.json` | 0 | no whitespace errors |

`python3 Stage1_Instances/THM-M-0510/check_proof.py` is intentionally not
listed as a passing validation command. After proof integration it is not a
standalone recipe: it requires the removed proof-worker packet and hard-binds
the predecessor's old base revision and pre-integration DAG state.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | The exact statement and both implementations of the partial Euler-product package elaborate at trust level zero. |
| Placeholder and unsafe boundary | provisional pass | Source scans, `assert_no_sorry`, axiom output, and the differential declaration-closure walk pass for the checked boundary. |
| Axiom observation | provisional pass | Every checked body uses only the observed classical trio. The theorem-specific foundation policy and complete TCB remain unaccepted. |
| Selected direct provenance | provisional pass | Local inputs, dependency pin/cleanliness/origin/license, and three direct source/olean boundaries agree. Full transitive declaration, imported-artifact, bootstrap, and TCB provenance is absent. |
| Proof dependency | fail closed | The predecessor is only `[_]`; its receipt is `accepted=false`, root-kernel closure is false, and all analytic root obligations remain open. |
| Structured authority | fail closed | The accepted instance/graph remain `[H2,M3,R4]` with no accepted proof state. The Euler node remains planned M4 despite provisional proof evidence. |
| Terminal composition fidelity | fail closed | `M0510-T-ASYMPTOTIC` claims an M0-L relative-error transport, but `root_of_finalAsymptotic` merely takes a premise definitionally identical to the exact root and returns it. This is the dossier's explicitly excluded tautological-assumption shape. |
| Recorded predecessor recipes | fail closed | `validation-specs.json` belongs to the obligation-tree node and lacks executable `cwd`, `argv`, environment, timeout, output, and declaration fields. This validation phase supplies a runnable narrow replacement but cannot retroactively accept predecessor claims. |
| Human source and readability | fail closed | Primary-source pinpoint/assumption/errata review and independent H0/R0 review remain open. The graph's per-node readable fragments do not exist, and its copied one-line ledgers are not substantive reconstructions. |
| Hermetic release replay | fail closed | Network isolation and fresh local output are real, but the run reused the shared warm cache rather than a clean-checkout cold build with empty caches and offline archive restoration. |
| Independent verification | fail closed | The differential module shares this worker, checkout, toolchain, and cache; there is no second signed attestation, distinct runner, or independently implemented minimal release verifier. |

The validation node is self-tested only as an honest nonrelease blocked
receipt. It grants no accepted obligation state, root closure, `M0-*`,
`E0/E1`, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or master
acceptance. `audit_complete=false` and `theorem_complete=false` remain explicit.
