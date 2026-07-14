# THM-M-0559 validation-phase result

Item: `S56-M-0559-VALIDATION`. Base revision:
`6cf20c1ab97fcd6970455baa23022062ebc14fe1`. Intent: `validate`. Verdict: `blocked`.
Lifecycle: `planned -> planned`. Root vector: `[H3, M4, R4] -> [H3, M4, R4]`.

## Narrow validation

The node-specific validator copies `Statement.lean`, `Proof.lean`, and `Validation.lean` into a
fresh temporary module directory. It invokes the pinned Lean 4.29.0 executable at trust zero, with
one Lean thread, a cleared fixed locale/timezone environment, a read-only host filesystem, and
network disabled by Bubblewrap. It rechecks the printed canonical Prop, nine proof-phase component
and empty-branch declarations, and a separately implemented empty branch importing only the frozen
statement module.

All ten proof declarations are sorry-free and report exactly `propext`, `Classical.choice`, and
`Quot.sound`. A supplemental comment-aware source scan finds no placeholder, bodyless declaration,
unsafe/extern escape, or native oracle in the three hash-bound checked modules. Target hashes, the
frozen denominator, the clean immutable mathlib revision/tree, four selected source/blob/olean
identities, the mathlib license, and tool identities are bound by the receipt. No `lake update`,
`lake build`, clone, fetch, or `.lake` mutation was performed.

The separately written `empty_branch_direct` is useful differential evidence: it derives `IsEmpty
Y` directly from component surjectivity and then uses `Homeomorph.empty`, rather than importing or
calling the proof-phase branch. It ran in the same worker, checkout, kernel, and shared cache, so it
is not distinct-runner independent verification.

These checks do not reach any declaration proving `WhiteheadTarget`. The nonempty cellular branch,
skeleton construction, extension and colimit lemmas, component recomposition, and exact-forward
package remain absent. The frozen root cut is `M0559-N-COMPONENTS` plus `M0559-T-FORWARD`, and the
accepted root remains `M4`.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | The statement, nine partial proof declarations, and a differential empty branch elaborate at trust zero with network denied. |
| Placeholder and unsafe boundary | provisional pass | Kernel sorry output plus a supplemental comment-aware scan find no prohibited proof device in the hash-bound modules. |
| Trust observation | provisional pass | Ten declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`; theorem-specific foundation acceptance and complete TCB closure remain open. |
| Selected provenance | provisional pass | Exact local hashes, clean mathlib pin/tree/remote/license, four selected source/blob/olean identities, and tool hashes agree; this is not a transitive closure or SBOM. |
| Dependency authority | fail closed | `S56-M-0559-PROOF` is only `[_]`; its receipt is `accepted=false` and accepts no closed obligation. |
| Exact B-EMPTY mapping | fail closed | The registry fingerprint is still `planned:v1`; only the master may accept a checked implementation against the frozen node. |
| Exact root composition | fail closed | No local or pinned declaration proves the nonempty cellular construction or `WhiteheadTarget`. |
| Statement scope | fail closed for imported conventional proof credit | The frozen target has no `T2Space` assumptions although pinned `CWComplex` permits non-Hausdorff spaces; validation may not add Hausdorffness or substitute a narrower theorem. |
| Human source and readability | fail closed | Exact primary theorem/page/assumption/errata review and independent H0/R0 review remain open. |
| Complete trust and provenance | fail closed | Selected imports are not a complete transitive declaration/import closure, TCB inventory, or dependency SBOM. |
| Hermetic release reproduction | fail closed | The run uses the automation-provided shared warm `.lake` cache, not a clean checkout, empty-cache cold build, or offline-restored release closure. |
| Independent verification | fail closed | The differential implementation shares this worker identity and cache; no distinct signed runner or independent minimal verifier exists. |

The first dependency-legal failure is
`dependency.S56-M-0559-PROOF.master_acceptance`. The first open theorem gate is
`proof.M0559-N-COMPONENTS.kernel_closure`, and the first release failure is
`S56-10.6-HERMETIC-COLD-BUILD`. `audit_complete=false` and `theorem_complete=false`.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0559` | 0 | Rank 607; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0559/check_obligation_tree.py` | 0 | 18 obligations and 88 typed edges passed; denominator `040c9f0d...3446fc`; root remained M4. |
| `bash Stage1_Instances/THM-M-0559/check_proof.sh` | 0 | Isolated trust-zero replay passed for the nine proof declarations; output was 1413 bytes with SHA-256 `d336d5ec...9917`. |
| `python3 -I -B Stage1_Instances/THM-M-0559/check_validation.py` | 0 | Network-isolated trust-zero differential replay, hygiene, trust observation, selected provenance, receipt, and worker-packet checks passed while completion/release gates failed closed. |
| JSON parsing, Python syntax compilation, scoped prohibited-device scan, and `git diff --check` | 0 | Structured artifacts parsed, the checker compiled, the scan was clean, and whitespace checks passed. |

This node is self-tested as truthful provisional validation work and proposes worker state `[_]`.
It grants no accepted receipt, exact-root credit, `E0/E1`, `M0`, `AUDIT-Z`, `THEOREM-Z`, release,
theorem completion, or master acceptance. Accepted receipt IDs: none.
