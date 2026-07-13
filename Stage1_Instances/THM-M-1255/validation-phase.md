# THM-M-1255 validation-phase evidence

Item: `S56-M-1255-VALIDATION`. Base revision:
`bad90e2e2479d376609447202eb4f437789d0d11`.

The structured recipe in `validation-spec.json` used the existing pinned Lean artifacts without
updating or building dependencies. Each Lean invocation ran at trust level zero inside bubblewrap
with a read-only host root, cleared environment, fixed locale/timezone/thread count, no network,
and a disposable output directory. It separately replayed the canonical `Statement.lean` plus
`Validation.lean`, then `ObligationTree.lean` plus `Proof.lean`. Every printed declaration reported
exactly `propext`, `Classical.choice`, and `Quot.sound`. Kernel `assert_no_sorry` and a supplemental
comment-aware scan found no placeholder, new axiom, unsafe declaration, opaque body, external
implementation, or native oracle.

`Validation.lean` imports neither `Proof` nor `ObligationTree`; it independently reconstructs
coordinate commutation and polynomial-action existence directly over the canonical statement
definitions. This corroborates `M1255-L-COMMUTE` and `M1255-C-ACTION`, but the exact root remains
open. No Fourier division witness or `FundamentalSolutionsFor` body exists.

## Commands And Results

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, passed |
| `python3 scripts/stage1_target.py show THM-M-1255` | 0 | rank 160, planned lifecycle, theorem incomplete |
| `python3 Stage1_Instances/THM-M-1255/check_obligation_tree.py` | 0 | frozen 13-obligation, 25-edge graph passed; authoritative root remains open M3 |
| `python3 Stage1_Instances/THM-M-1255/check_proof.py` | 0 | proof receipt hashes, two provisional proof IDs, and open-root boundary passed |
| `python3 -I -B Stage1_Instances/THM-M-1255/check_validation.py` | 0 | trust-zero isolated replay, axiom parsing, canonical differential probe, source hygiene, hashes, pins, dependency cleanliness, graph state, and fail-closed release decisions passed |
| `python3 -m json.tool Stage1_Instances/THM-M-1255/validation-spec.json` | 0 | valid structured recipe JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1255/validation-receipt.json` | 0 | valid receipt JSON |
| `git diff --check -- Stage1_Instances/THM-M-1255 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Gate Decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Canonical statement, conditional composition, local proof bodies, and canonical differential reconstruction elaborate at `--trust=0`. |
| Placeholder and unsafe boundary | pass | `assert_no_sorry` plus comment-aware scanning found no prohibited mechanism in the four Lean modules. |
| Axiom observation | provisional pass | Checked declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`; no accepted complete foundation/TCB profile exists. |
| Local source provenance | partial | All local inputs are hash-bound; every manifest dependency source is at its pin and clean. Complete declaration, compiled-artifact, executable, SBOM, and license closure is absent. |
| Exact canonical linkage | fail closed | `ObligationTree.lean` redeclares the statement namespace instead of importing `Statement.lean`; its proof declarations cannot coexist with the canonical statement constants in one Lean environment. The independent canonical probe corroborates action existence but does not repair this linkage. |
| Exact root closure | fail | `M1255-N-FOURIER`, `M1255-L-DIVISION`, and `M1255-C-FUNDSOL` remain open. The package-level cut after proof acceptance is `M1255-C-FUNDSOL`; its leaf cut is the Fourier and division pair. |
| Source fidelity | fail closed | The frozen tempered-distribution target lacks accepted primary-source equivalence to the classical distributional claim. |
| Hermetic release replay | fail closed | The run reused shared warm compiled artifacts; there was no clean checkout, empty-cache cold dependency build, offline restoration, or complete archive. |
| Independent verification | fail closed | The differential module shares this worker, checkout, toolchain, and cache; no distinct identity, second signature, independent runner, or release verifier exists. |

This is a self-tested, truthful negative theorem-validation result and a provisional partial-proof
validation handoff. The accepted graph remains `H3/M3/R4` with cut
`{M1255-C-ACTION, M1255-C-FUNDSOL}`; accepting the predecessor proof could only propose `M2` with
`M1255-C-FUNDSOL` still open. `audit_complete=false` and `theorem_complete=false`. This receipt
grants no `M0`, `E0/E1`, release, or master-acceptance credit.
