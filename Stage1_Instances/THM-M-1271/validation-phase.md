# THM-M-1271 validation-phase result

Item: `S56-M-1271-VALIDATION`. Base revision:
`557b928b377b386864527c9fb4831d45857837aa`; base tree:
`e677879a6eb4cb9d6795ba1bd78726af06ab9465`. Intent: `validate`.

## Narrow validation

The structured recipe copies the frozen statement, conditional composition,
partial proof, anchor probe, and a separate validation module to a disposable
directory. Pinned Lean 4.29.0 elaborates fresh target outputs at trust zero,
with one Lean thread, a read-only host root, fixed locale and timezone, and
network disabled by Bubblewrap. Existing pinned compiled dependencies are
reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
network operation, or `.lake` mutation is performed.

`Validation.lean` imports only `Statement`. It independently reconstructs
sphere crossing, the single-path lower bound, the geometric minimax barrier,
and the final conditional adapter. The adapter retains the analytic critical-
point package as an exact premise. It is same-workspace differential evidence,
not an independent runner and not an unconditional proof of the root.

The conditional composer, seven proof declarations, and four differential
probes all report exactly `propext`, `Classical.choice`, and `Quot.sound`.
A nested-comment-aware scan finds no placeholder, bodyless declaration,
unsafe/external escape, native decision shortcut, or implemented-by hook.
Frozen local hashes, the clean mathlib pin, license, executable identities,
and four selected source/blob/olean identities agree.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Frozen kernel replay | provisional partial pass | The exact statement, conditional composition, partial bodies, anchor interfaces, and differential probes elaborate at trust zero from fresh target outputs. |
| Placeholder and unsafe boundary | pass | Checked Lean sources and replay output contain no prohibited proof device or `sorryAx`. |
| Conditional canonical composition | pass | Both adapters reach `MountainPassTarget` only after consuming an exact unproved analytic package. |
| Trust observation | provisional pass | Twelve reports have the observed axiom trio; there is no accepted complete theorem-specific foundation or TCB profile. |
| Selected provenance | provisional pass | Frozen hashes, the mathlib revision/tree/remote/license, and selected source/blob/olean identities agree. Complete transitive provenance is open. |
| Proof dependency | fail closed | `S56-M-1271-PROOF` is only worker `[_]`; its receipt has `accepted=false`. |
| Exact root | fail closed | Value convergence is proved, but derivative-small convergence for `M1271-C-PS-SEQUENCE` is absent. `M1271-T-CRITICAL` and the root remain open. |
| Frozen obligation recipes | fail closed for proof credit | The old recipes validate structure or conditional composition and cannot prove open mathematical obligations. |
| Hermetic release replay | fail closed | The run uses the shared warm cache, not a clean checkout, empty caches, cold build, or offline-restored archive. |
| Independent verification | fail closed | The probes share this worker, clone, kernel, and cache; no distinct signed runner or independently implemented minimal verifier exists. |

The first dependency-legal failure is
`dependency.S56-M-1271-PROOF.master_acceptance`; the first theorem failure is
`proof.M1271-C-PS-SEQUENCE.kernel_closure`; the first release failure is
complete transitive provenance. The accepted root vector remains
`[H3, M3, R4]`, `audit_complete=false`, and `theorem_complete=false`.

## Commands and exact results

All commands ran on 2026-07-15 in this worker clone.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1271` | 0 | Rank 164; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1271/check_obligation_tree.py` | 0 | Frozen 13-obligation, 25-edge architecture passed; root remains open M3. |
| `python3 -I -B Stage1_Instances/THM-M-1271/check_validation.py` | 0 | Network-isolated trust-zero replay, hygiene, hashes, selected provenance, fail-closed decisions, receipt, and worker packet passed. |
| JSON parsing, isolated Python syntax compilation, and `git diff --check` | 0 | Structured artifacts parsed, checker syntax compiled outside the repository, and scoped whitespace checks passed. |

The successful Lean replay interval was `2026-07-15T08:12:15+08:00` through
`2026-07-15T08:14:12+08:00` (117 seconds). Its combined semantic output
SHA-256 is `2e0ba73325f3724b280cd538cd67c2b25dd77d0092ab721660ea30bfc01b3d1c`;
the receipt binds each module output separately.

This validation node is self-tested as truthful narrow work and proposes
worker state `[_]`, while its validation verdict is `blocked`. It grants no
accepted receipt, exact-root closure, M0/E0/E1, `AUDIT-Z`, `THEOREM-Z`,
release, theorem completion, or master acceptance.
