# THM-M-1246 validation-phase result

Item `S56-M-1246-VALIDATION` was run against base revision
`18ff7447208231633bf2e01e8aad3111af56531a`. The exact frozen Hardy terminal
and public root replay at Lean trust level zero. Lean recursively reports all
six checked declarations sorry-free and observes exactly `propext`,
`Classical.choice`, and `Quot.sound`.

This is provisional nonrelease evidence, not theorem completion. The accepted
graph still records `M3`, `root_closed=false`, and cut set
`M1246-T-ANALYTIC`. The proof predecessor is only `[_]`, and its positive
denominator regularization still needs master reconciliation against the
frozen literal cutoff leaf architecture.

## Validation method

`check_validation.sh` copies the statement, composition module, four proof
modules, kernel audit, and source-replay module into a fresh `/tmp` directory.
Each Lean process runs with `--trust=0 -t0` inside Bubblewrap with an unshared
network namespace, read-only host root, fixed locale/timezone/thread count,
and only that temporary directory writable. No update, build, clone, fetch, or
dependency mutation occurs.

`ProofAudit.lean` uses Lean's recursive `assert_no_sorry` and `#print sorries`
commands, then prints exact axiom closures. `Validation.lean` does not import
`Proof`; before it is checked, the runner removes both `Proof.lean` and
`Proof.olean`. It mirrors the terminal assembly from the remaining support
modules. That verifies independence only from the `Proof` wrapper artifact, but
it is not independently reasoned proof or a distinct verifier.

## Gate decisions

| Gate | Decision | Evidence or boundary |
|---|---|---|
| Exact kernel replay | provisional pass | Statement, frozen composition, analytic terminal, and exact public root elaborate with trust zero. |
| Placeholder/unsafe audit | pass | Six recursive kernel sorry checks plus a comment-aware scan for prohibited constructs pass. |
| Axiom observation | provisional pass | All six declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`; foundation-policy acceptance and complete TCB review remain open. |
| Selected provenance | provisional pass | Local source hashes, clean pinned mathlib revision/tree/remote/license, three pivotal source blobs, compiled artifacts, and tool hashes agree before and after replay. |
| Proof dependency | fail closed | `S56-M-1246-PROOF` is provisional and lacks dependency-ordered master acceptance. |
| Structured state | fail closed | The frozen graph predates proof closure and remains `M3`/open; workers cannot reconcile its architecture or grant internal leaf credit. |
| Hermetic release replay | fail closed | The dependency cache is pinned and read-only during Lean runs, but it is shared and warm rather than a clean empty-cache build from an offline-restorable archive. |
| Independent verification | fail closed | The no-`Proof.olean` replay uses the same proof plan, worker identity, checkout, kernel, support modules, and cache; no second signed runner or independently implemented verifier exists. |
| Source/readability | fail closed | `H0` and `R0` require pinpoint source and independent reviews that this validation phase cannot supply. |

## Commands and results

Commands were run from the repository root on `2026-07-14`.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1246` | 0 | Rank 426, planned, theorem incomplete. |
| `bash Stage1_Instances/THM-M-1246/check_validation.sh` | 0 | Network-isolated trust-zero replay passed; output SHA-256 `cd4a55ba...27d4d3`, 30446 bytes, six sorry-free and six exact axiom reports. |
| `python3 -B Stage1_Instances/THM-M-1246/check_validation.py` | 0 | Hash, pin, graph, receipt, trust, provenance, scoped-status, and fail-closed boundary checks passed. |
| `python3 -m json.tool` on the validation spec, receipt, and worker packet | 0 | All three JSON artifacts parsed. |
| `git diff --check -- Stage1_Instances/THM-M-1246 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The first node gate that remains closed is
`dependency.S56-M-1246-PROOF.master_acceptance`. The first release gate is
`S56-10.6-HERMETIC-COLD-BUILD`. Therefore `audit_complete=false` and
`theorem_complete=false`; no accepted debt-vector or theorem state changes.
