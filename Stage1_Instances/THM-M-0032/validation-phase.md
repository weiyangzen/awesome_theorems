# THM-M-0032 validation-phase evidence

Item: `S56-M-0032-VALIDATION`. Base revision:
`289e3709a4204b41baa98cb95e0548b9811b26bb`; base tree:
`6adc6103dba02e89467851fce1b2f6e301490938`.

## Verdict

`blocked`, with a self-tested fail-closed validation packet proposed as `[_]`. The structured
recipe replays the exact statement, frozen conditional composition, and the real proof-phase
regular-local domain package at Lean trust level zero. Every Lean process has a fresh temporary
working directory, a read-only host root, a fixed cleared environment, and an unshared network
namespace.

This does not validate the Auslander-Buchsbaum UFD theorem. The root composer still consumes
`RegularLocalPrimeElementPackage` as an explicit premise, and no inhabitant of that package exists.
The proof receipt is worker-provisional and not master-accepted, while the frozen registry and graph
truthfully retain an open root. The accepted root vector therefore stays H1/M3/R4.

## Commands and results

Commands ran in this isolated worker clone on 2026-07-15 (`Asia/Shanghai`). No `lake update`,
`lake build`, dependency clone/fetch/checkout, or `.lake` mutation was performed.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0032` | 0 | rank 1076; planned; L0/rework-required; theorem incomplete |
| `bash Stage1_Instances/THM-M-0032/check_proof.sh` | 0 | fresh Statement, ObligationTree, and DomainProof outputs elaborated at trust zero; both domain declarations are sorry-free and expose only the three expected axioms |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0032/check_validation.py --probe` | 0 | network-isolated trust-zero replay produced deterministic output hashes and observed four roots, 22572 transitive constants, 841 modules, only the three expected axioms, no unexpected bodyless declaration, and no unsafe declaration |
| execute `validation-spec.json` `argv` without shell interpolation | 0 | frozen inputs, partial kernel/trust observations, selected provenance, fail-closed gate decisions, receipt/blocker/spec, and worker packet agree |
| `python3 -m json.tool` over validation spec, receipt, blocker, and worker packet | 0 | all four structured artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0032-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0032/check_validation.py` | 0 | checker syntax passed outside the repository |
| `git diff --check -- Stage1_Instances/THM-M-0032 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

The replay uses the installed pinned Lean 4.29.0 executable and existing compiled package paths
from the automation-provided canonical `.lake` symlink. Bubblewrap denies network and exposes the
host read-only except for a fresh temporary directory. This is stronger than an ordinary warm
replay, but it is shared-cache nonrelease evidence, not section 10.6 cold hermetic evidence.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | Exact statement, conditional composition, two domain declarations, and the validation closure probe elaborate at trust zero with network denied. |
| Placeholder and observed trust boundary | provisional pass | Lean's `assert_no_sorry`, `#print sorries`, parser-aware source scanning, and the transitive constant walk agree; all four roots expose only `propext`, `Classical.choice`, and `Quot.sound`. This is observation, not accepted complete TCB closure. |
| Selected provenance | provisional pass | Frozen local hashes, clean pinned mathlib revision/tree/remote/license, four selected source/blob/olean triples, and executable identities agree. |
| Proof dependency and exact root | fail closed | `S56-M-0032-PROOF` is only `[_]`, its receipt is unaccepted, and `RegularLocalPrimeElementPackage` has no body. A conditional composer does not prove its premise. |
| Complete trust and provenance | fail closed | No complete declaration/import/object/compiler/bootstrap/plugin/TCB/SBOM/archive closure exists. |
| Hermetic reproduction | fail closed | Shared warm cache; no immutable clean checkout, empty-cache cold build, offline archive restoration, or deterministic release bundle. |
| Independent verification | fail closed | The closure probe is a same-worker replay in the same checkout, toolchain, and cache, not a distinct signed runner or independently implemented minimal verifier. |
| Human and readable review | fail closed | No independently accepted H0 primary-source crosswalk or R0 reconstruction exists. |

The first node gate is `dependency.S56-M-0032-PROOF.master_acceptance`; the first mathematical gate
is `M0032-A-PRIME-ELEMENT`; and the first release gate is
`S56-10.6-HERMETIC-COLD-EMPTY-CACHE-REPLAY`. The remaining machine proof cut is
`M0032-A-PRIME-ELEMENT`.

The packet itself is genuinely replayed and self-tested, so the handoff proposes only `[_]` for
review. It grants no accepted frozen obligation, exact root, M0, validation completion, `AUDIT-Z`,
`THEOREM-Z`, release, theorem completion, or master acceptance.
