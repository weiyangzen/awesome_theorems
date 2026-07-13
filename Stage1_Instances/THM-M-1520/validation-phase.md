# THM-M-1520 validation-phase result

Item: `S56-M-1520-VALIDATION`. Base revision:
`ed9e08c4aa5d18cb58fa54e74867f38999a92a14`. Intent: `validate`.

## Narrow validation

The validator copied all nine owned Lean modules to a disposable directory and replayed the frozen
statement, eight local partial or conditional proof declarations, and two independently written
boundary probes with pinned Lean 4.29.0, `--trust=0`, one Lean thread, fixed locale/timezone, and
network disabled by bubblewrap. `Validation.lean` imports only `Statement`; it reconstructs the
time-zero and inverse-time flow facts without importing or invoking their proof-phase bodies.

Every checked proof declaration reports exactly `propext`, `Classical.choice`, and `Quot.sound`.
All declarations carrying `#print sorries` are sorry-free, no output contains `sorryAx`, and the
comment-stripped owned-source scan finds no placeholder, bodyless, unsafe, external, or native
escape. The validator also binds the canonical expression and denominator, all proof inputs, the
clean immutable mathlib revision/tree, three direct terminal source/blob/olean identities, the Lean
executable, and the structured recipe. No `lake update`, `lake build`, dependency clone/fetch, or
`.lake` mutation was run.

These are genuine narrow passes, not a proof of Liouville's theorem. The exact root has no
premise-free body: `liouvilleStatement_of_analyticPackage` still consumes an unconstructed
`LiouvilleAnalyticPackage`. The graph therefore retains only `M1520-T-ASSEMBLE` as closed, leaves
the root at `M3`, and reports `M1520-T-ALL-TIMES` as the remaining root cut. The first analytic
failure is `M1520-C-VARIATION`.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Frozen kernel replay | provisional pass | Nine copied modules and ten local proof declarations elaborate at trust zero; the canonical target itself elaborates as `Prop`. |
| Placeholder and unsafe boundary | provisional pass | Machine `#print sorries`, exact axiom output, and supplemental comment-stripped scans find no forbidden proof device in the checked owned sources. |
| Direct provenance | provisional pass | Local-source hashes, clean mathlib revision/tree/remote/license, and three terminal source/blob/olean identities agree with the receipt. |
| Structured authority | fail closed | The proof dependency remains only provisional `[_]`; it has no master acceptance and closes no whole new obligation. |
| Exact root composition | fail closed | The conditional composer consumes `LiouvilleAnalyticPackage`; spatial differentiability, divergence cancellation, the variational equation, and determinant-one evolution remain open. |
| Complete trust and provenance | fail closed | The classical axiom observation and three direct terminal identities are not a serialized transitive declaration/import closure or complete accepted foundation/TCB inventory. |
| Hermetic reproduction | fail closed | The replay used a shared warm writable `.lake` cache, not a new checkout, cold empty caches, or an offline-restored dependency/source/SBOM archive. |
| Independent verification | fail closed | The differential probes use the same worker, checkout, and cache; there is no second signed independently provisioned runner or independent minimal release verifier. |

The first dependency-legal failure is `dependency.S56-M-1520-PROOF.master_acceptance`. Root vector
remains `[H2, M3, R3]`; `audit_complete=false` and `theorem_complete=false`.

## Commands and exact results

All commands ran on 2026-07-14 in this worker clone.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1520` | 0 | Rank 189; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1520/check_obligation_tree.py` | 0 | Frozen registry passed with 16 obligations and 32 typed edges; root open M3 and analytic package open M4. |
| `cd Formalizations/Lean && lake env which lean && lake env lean --version` | 0 | Resolved pinned Lean 4.29.0 at commit `98dc76e3`; direct Lake environment access was available. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1520/AnchorAudit.lean` | 0 | Credited pinned substrate declarations and both typed examples elaborated. |
| initial disposable probe using `lake env lean` on a source outside the Lake root | 1 | Lake rejected the output path as outside its root and the dependent import was unavailable; this attempt carries no validation credit. The final structured validator uses `lake env` only for pinned tool discovery, then invokes that executable on disposable sources. |
| `python3 -I -B Stage1_Instances/THM-M-1520/check_validation.py` | 0 | Network-isolated trust-zero replay, exact axiom checks, source hygiene, hashes, graph boundary, direct provenance, fail-closed release decisions, receipt, and worker packet passed. |
| JSON parsing, Python syntax compilation outside the repository, scoped prohibited-device scan, and `git diff --check` | 0 | Structured artifacts parsed, checker compiled, scan found no forbidden construct, and whitespace checks passed. |

This node is self-tested as truthful validation work and proposes worker state `[_]`. It grants no
accepted receipt, exact-root credit, `E0/E1`, `M0`, `AUDIT-Z`, `THEOREM-Z`, release, or theorem
completion; only the integration lane may accept it.
