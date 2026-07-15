# THM-M-0072 validation-phase result

Item: `S56-M-0072-VALIDATION`. Base revision:
`97cd9c492d95baa9b55d2d8b341844107f07e686` (tree
`bdd31de5f2fcd38078e4b5793b400a8105a3b8ba`).

Validation date: `2026-07-15` (`Asia/Shanghai`). No mathematical proof content
was added. `Validation.lean` only gives exact-type aliases for the existing
outside-transfer terminal and canonical root, then asks Lean to inspect their
trust closure.

## Narrow validation

The structured recipe copies `Statement.lean`, `ObligationTree.lean`,
`Proof.lean`, and `Validation.lean` into a fresh temporary output directory.
It invokes the hash-verified Lean 4.29.0 binary directly with `--trust=0 -t0`,
fixed locale, timezone, and thread count. Bubblewrap denies the network and
makes the host root, toolchain, and shared dependency cache read-only; only
the disposable output directory is writable.

The exact canonical root and outside branch replay through the frozen branch
composition. Fourteen proof, composition, helper, and alias declarations pass
`assert_no_sorry`; each reports exactly `propext`, `Classical.choice`, and
`Quot.sound`. Lean's transitive environment walk reaches 13,337 declarations
in 513 modules and observes no unexpected bodyless axiom declaration or unsafe
declaration. A nested-comment-and-string-aware supplemental scan rejects local
`sorry`, `admit`, `sorryAx`, bodyless declarations, unsafe/oracle escapes,
`extern`, `implemented_by`, `native_decide`, and `run_tac`.

Selected provenance binds the integrated local proof blob, all frozen dossier
inputs, the clean pinned mathlib revision/tree/remote/license, tool identities,
and source/olean pairs for the four direct proof imports plus the statement's
Sylow import. This is a bounded observation, not a complete serialized
declaration/import/source-origin graph, TCB inventory, or SBOM.

## Commands and results

Commands ran from the repository root. The automation-provided canonical
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, checkout, or `.lake` mutation was run.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0072` | 0 | rank 1102, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -I -B Stage1_Instances/THM-M-0072/check_validation.py --probe` | 0 | network-isolated trust-zero fresh-output replay and selected provenance checks passed |
| `python3 -I -B Stage1_Instances/THM-M-0072/check_validation.py --worker-packet .stage1-worker-selftest.json` | 0 | final recipe, receipt, worker packet, scoped changes, and fail-closed gate decisions passed |
| `python3 -m json.tool Stage1_Instances/THM-M-0072/validation-spec.json` and the receipt/packet equivalents | 0 | all validation JSON documents parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0072-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0072/check_validation.py` | 0 | checker syntax compiled outside the repository |
| `git diff --check -- Stage1_Instances/THM-M-0072 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The integrated predecessor checker is not cited as a current passing command.
It deliberately binds the proof worker's earlier base and execution-DAG hash,
so `python3 -B Stage1_Instances/THM-M-0072/check_proof.py` now fails closed with
`worker HEAD changed`. The validation checker instead hash-binds the integrated
proof receipt and directly replays the current Lean sources.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel and composition | provisional pass | Fresh outputs check the unchanged exact target, both maximal-subgroup branches, the outside-transfer body, and the frozen root composer at trust level zero. |
| Placeholder and unsafe boundary | provisional pass | Fourteen transitive sorry reports pass; parser-aware local scanning and the 13,337-declaration environment walk observe no prohibited local device, unexpected bodyless declaration, or unsafe declaration. |
| Axiom observation | provisional pass | Every checked declaration reports only the disclosed classical/quotient trio. The theorem-specific foundation policy is still planned, not accepted. |
| Selected provenance | provisional pass | Frozen local hashes, proof-body location, five source/olean boundaries, tool identities, mathlib pin/remote/license, and dependency cleanliness agree. Complete transitive provenance and TCB closure remain open. |
| Dependency legality and structured authority | fail closed | `S56-M-0072-PROOF` is only `[_]`, not master accepted. The planned instance and graph remain the honest pre-proof `H1/M3/R4`, `root_closed=false` snapshot. |
| Hermetic release replay | fail closed | The run reused a shared warm `.lake`; it is not a separate clean checkout, empty-cache cold build, content-addressed offline restoration, deterministic evidence bundle, or complete TCB/SBOM archive. |
| Independent verification | fail closed | The exact-type aliases import and reuse the existing proof in this worker, checkout, kernel, and cache. No distinct identity, independently provisioned runner, second signature, or independent minimal verifier exists. |
| Human source and readability | fail closed | The catalog date conflict remains H1 and no independently accepted source H0 or readable R0 receipt exists. |

The first node gate failure is
`dependency.S56-M-0072-PROOF.master_acceptance`; the first release-specific
failure is `S56-10.6-HERMETIC-COLD-EMPTY-CACHE`. The accepted vector remains
`H1/M3/R4`, with no accepted receipt or closed obligation. `AUDIT-Z`,
`THEOREM-Z`, release, and theorem completion remain false.

## Status boundary

This is a self-tested, nonrelease validation-node handoff for master review.
It records the narrow gates that passed and the assurance gates that failed.
It does not claim accepted `M0-L`, `E0`, complete trust/provenance, cold
hermetic evidence, distinct-runner independence, theorem completion, release,
or master acceptance.
