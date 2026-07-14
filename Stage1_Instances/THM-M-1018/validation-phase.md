# THM-M-1018 validation-phase result

Item: `S56-M-1018-VALIDATION`. Base revision:
`718e166c56e53c552ebb861ee01427f9a606fc72`. Intent: `validate`.

## Narrow validation

The validator copied the frozen statement, conditional obligation composition, five partial proof
bodies, anchor audit, and three validation probes to a disposable directory. It replayed them with
pinned Lean 4.29.0, `--trust=0`, one Lean thread, fixed locale/timezone, a read-only host mount, and
network disabled by bubblewrap. The dependency closure was reused read-only; no `lake update`,
`lake build`, dependency clone/fetch, or `.lake` mutation was run.

`Validation.lean` does not import `Proof`. It independently reconstructs the endpoint-frontier and
conditional Portmanteau lemmas. It also checks that the frozen `ObligationTree.InversionFor`
interface is definitionally connected to `LevyInversionTarget`, but that bridge consumes the full
fixed-data analytic inversion premise. It therefore validates composition shape without creating
root proof content.

All five proof-phase declarations, `root_compose`, and the three probes report exactly `propext`,
`Classical.choice`, and `Quot.sound`. The three probes are machine-reported sorry-free; no Lean
output contains `sorryAx`; and the comment-aware source scan finds no placeholder, bodyless,
unsafe, external, native, or implemented-by escape. Local input hashes, the clean pinned mathlib
revision/tree/remote/license, and five selected terminal source/blob/olean identities agree.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Frozen kernel replay | provisional pass | Statement, conditional composition, five partial bodies, anchor checks, and three validation probes elaborate from disposable outputs at trust zero. |
| Placeholder and unsafe boundary | provisional pass | Machine sorry reports, exact axiom output, and a comment-aware scan find no forbidden proof device in checked owned sources. |
| Conditional canonical composition | pass | `conditionalCanonicalBridge` inhabits the canonical target only when given the exact still-open `M1018-T-ANALYTIC` premise. |
| Selected direct provenance | provisional pass | Local hashes, clean mathlib pin, license, and five source/blob/olean identities agree. |
| Structured proof authority | fail closed | `S56-M-1018-PROOF` remains provisional `[_]`, is not master-accepted, and closes no whole frozen obligation. |
| Exact root | fail closed | No premise-free local or pinned body inhabits `LevyInversionTarget`; `M1018-T-ANALYTIC` remains the root cut, with `M1018-L-DIRICHLET` the first missing analytic package. |
| Frozen recipes | fail closed for proof credit | All 17 old recipes rerun only `check_obligation_tree.py`; they validate architecture and cannot establish the named open mathematical obligations. |
| Complete trust and provenance | fail closed | The observed axioms and selected hashes are not an accepted foundation policy, serialized transitive declaration/import closure, or complete TCB/SBOM inventory. |
| Hermetic reproduction | fail closed | The replay used the shared warm dependency cache, not a new checkout, cold empty caches, or an offline-restored source/dependency archive. |
| Independent verification | fail closed | The probes share this worker, checkout, kernel, and cache; no distinct signed runner or independently implemented minimal release verifier exists. |

The first dependency-legal failure is
`dependency.S56-M-1018-PROOF.master_acceptance`. The accepted root vector remains
`[H2, M3, R4]`; `audit_complete=false` and `theorem_complete=false`.

## Commands and exact results

All commands ran on 2026-07-15 in this worker clone.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1018` | 0 | Rank 494; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1018/check_obligation_tree.py` | 0 | Frozen registry passed with 17 obligations and 34 typed edges; root open `M3`. |
| `bash Stage1_Instances/THM-M-1018/check_proof.sh` | 0 | Five partial proof declarations elaborated at trust zero with the recorded axiom trio. |
| `python3 -I -B Stage1_Instances/THM-M-1018/check_validation.py` | 0 | Network-isolated trust-zero replay, source hygiene, hashes, graph boundary, selected provenance, fail-closed decisions, receipt, and worker packet passed. |
| JSON parsing, Python syntax compilation outside the repository, scoped prohibited-device scan, and `git diff --check` | 0 | Structured artifacts parsed, the checker compiled, the scan found no forbidden construct, and whitespace checks passed. |

This node is self-tested as truthful validation work and proposes worker state `[_]`, while its
validation verdict is `blocked`. It grants no accepted receipt, exact-root credit, `E0/E1`, `M0`,
`AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or master acceptance.
