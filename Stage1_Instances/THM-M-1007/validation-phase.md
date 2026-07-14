# THM-M-1007 validation-phase evidence

Item: `S56-M-1007-VALIDATION`

Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`

## Narrow validation

The validation recipe copies `Statement.lean`, `ObligationTree.lean`,
`Proof.lean`, and `Validation.lean` to a fresh temporary directory. It creates
only disposable local oleans and invokes the pinned Lean 4.29.0 executable at
`--trust=0 -t0`. Every Lean process runs in a Bubblewrap network namespace
with the host filesystem read-only except for that temporary directory, a
fresh `HOME`, fixed locale/timezone, and one Lean thread. The canonical pinned
`.lake` source and compiled dependency inputs are reused without mutation.
The structured wrapper applies a 900-second wall timeout and Bubblewrap
network namespace to the entire Python recipe; it clears the outer environment
and restores the fixed recipe `HOME`, `PATH`, locale, timezone, and thread
settings. Nested Lean subprocesses remain at trust level zero and use a fresh
temporary `HOME`.

The replay elaborates the exact frozen statement, the conditional
child-to-root composition, all 33 proof-phase declarations, an exact-type
probe for the proved sufficiency implication, and a separately expressed
explicit-premise reconstruction of that implication. The 36 distinct reported
declarations use exactly `propext`, `Classical.choice`, and `Quot.sound`.
Lean's transitive
`assert_no_sorry` check passes for the proof sufficiency declaration and both
validation probes, and a nested-comment-aware source scan finds no placeholder,
bodyless, unsafe, native, or external escape.

This is deliberately a negative-root result. The proof phase contains no
bounded independent-series necessity theorem and no inhabitant of the exact
biconditional root. Its immediate mathematical cut is
`M1007-L-BOUNDED-NEC`; the frozen graph remains open at `[H1, M3, R3]` with
no accepted closed obligations. The validation probe adds no mathematical
proof route and cannot convert the proved sufficiency direction into the
missing necessity direction.

## Commands and results

Commands ran from this worker clone on 2026-07-15 (`Asia/Shanghai`). No
`lake update`, `lake build`, dependency clone/fetch, checkout, or network
request was invoked.

| Command | Exit | Exact result summary |
|---|---:|---|
| `git status --short --untracked-files=all` | 0 | Before edits, only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; the run is nonrelease evidence. |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | HEAD `a1a7e939...aa04`; tree `d881fd96...dcf`. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1007` | 0 | Rank 287, planned, legacy artifacts unaccepted, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1007/check_obligation_tree.py` | 0 | 19 obligations, 54 typed edges, denominator `0a29c34a...e87cf`; frozen root open M3. |
| `python3 Stage1_Instances/THM-M-1007/check_statement.py` | 0 | Expression `3b1a82b3...cf38`; all four statement mutations distinguished. |
| `timeout 300s bash Stage1_Instances/THM-M-1007/check_proof.sh` | 124 | Historical proof script timed out without output; its absolute temporary source paths plus `--root` do not assign imported local modules consistently. It is not validation evidence. |
| `bash Stage1_Instances/THM-M-1007/run_validation.sh` | 0 | Whole-recipe network-isolated trust-zero replay, sorry/hygiene checks, selected provenance, receipt, and fail-closed root/release decisions passed. |
| `python3 -m json.tool Stage1_Instances/THM-M-1007/validation-spec.json` | 0 | Structured recipe parsed. |
| `python3 -m json.tool Stage1_Instances/THM-M-1007/validation-receipt.json` | 0 | Node receipt parsed. |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | Worker packet parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m1007-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-1007/check_validation.py` | 0 | Validator compiled outside the repository tree. |
| `git diff --check -- Stage1_Instances/THM-M-1007 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |

The prior proof-phase `check_proof.sh` was also run but is not a passing
validation recipe at this integrated snapshot: its absolute temporary source
paths plus `--root` do not assign the imported local modules consistently.
The validation checker therefore hash-binds the proof receipt and directly
replays the current Lean sources using correct relative module names. The
proof-phase `check_proof.py` is intentionally not invoked because it is bound
to the older proof worker's HEAD, DAG state, changed-path set, and root packet.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact local kernel replay | provisional pass | The frozen target and every extant proof/validation declaration elaborate at trust zero; exact sufficiency is checked, not the root. |
| Placeholder and unsafe boundary | provisional pass | Three transitive sorry checks and the parser-aware supplemental scan pass. |
| Axiom observation | provisional pass | Every report is the recorded classical trio; no accepted theorem-specific foundation profile or complete TCB closure exists. |
| Selected provenance | provisional pass | Current source/receipt/denominator hashes, tool identities, clean mathlib pin/tree/remote/license, and selected source/olean hashes agree. Full transitive declaration/import/artifact/SBOM provenance is open. |
| Proof dependency | fail closed | `S56-M-1007-PROOF` is only provisional `[_]`; its receipt is `accepted=false` and master acceptance is absent. |
| Exact root | fail closed | `M1007-L-BOUNDED-NEC`, necessity, assembly, and the canonical biconditional root have no proof body. |
| Human/readable acceptance | fail closed | Pinpoint independently reviewed H0 and R0 evidence is absent. |
| Hermetic release replay | fail closed | Network denial and fresh target outputs still reuse a shared warm dependency cache; there is no clean-checkout empty-cache cold build, offline restoration, deterministic evidence bundle, or complete SBOM/TCB archive. |
| Independent verification | fail closed | The differential probe shares this worker, checkout, Lean kernel, toolchain, and warm cache; there is no distinct identity, independently provisioned runner, second signature, or independent minimal release verifier. |

This node is self-tested only as truthful provisional validation evidence. It
grants no accepted obligation state, root closure, `M0-*`, `E0/E1`,
`AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or master acceptance.
