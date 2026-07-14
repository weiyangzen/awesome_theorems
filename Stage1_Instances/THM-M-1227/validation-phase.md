# THM-M-1227 validation-phase result

Item: `S56-M-1227-VALIDATION`. Base revision:
`a1a7e939e58f103f5ff5d23af51437fa8658aa04`. Intent: `validate`. Verdict:
`blocked`. Lifecycle: `planned -> planned`. Root vector: `[H2, M4, R4] -> [H2, M4, R4]`.

## Narrow validation

The node-specific validator copies `Statement.lean`, `Proof.lean`, and `Validation.lean` into a
disposable module directory. It invokes the pinned Lean 4.29.0 executable at trust zero, with one
Lean thread, a cleared fixed locale/timezone environment, a read-only host filesystem, and network
disabled by Bubblewrap. It rechecks the canonical Prop and conditional solution composer, the two
proof-phase zero-data declarations, and two separately written zero-data declarations that import
only the statement module.

The canonical `def : Prop` elaborates, and all five checked theorem declarations report exactly
`propext`, `Classical.choice`, and `Quot.sound`; the four executable branch declarations are
sorry-free. A supplemental comment-stripped source scan finds no placeholder, bodyless declaration,
unsafe/extern escape, or native oracle in the three hash-bound checked modules. Target hashes, the
frozen denominator, the clean immutable mathlib revision/tree,
three direct-import source/blob/olean identities, the mathlib license, and the Lean executable are
bound by the receipt. No `lake update`, `lake build`, clone, fetch, or `.lake` mutation is performed.

These checks validate only the local zero-data implementation candidate. The exact general
Leray-Hopf root has no proof body. `M1227-N-DATA`, `M1227-N-GLOBAL`, `M1227-C-GALERKIN`,
`M1227-C-BOUNDS`, and `M1227-C-COMPACT` remain the frozen root cut, and the structured graph remains
at `M4` with no accepted closed obligation.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | The frozen statement, conditional composer, proof zero branch, and a separately written zero branch elaborate at trust zero with network denied. |
| Placeholder and unsafe boundary | provisional pass | Kernel sorry output plus a supplemental comment-stripped scan find no prohibited proof device in the hash-bound checked modules. The scan is defense in depth, not a general Lean parser. |
| Trust observation | provisional pass | Five declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`. The accepted full foundation/TCB profile remains open. |
| Selected direct provenance | provisional pass | Exact local inputs, clean mathlib pin/tree/remote/license, three direct import source/blob/olean identities, and the Lean binary agree. This is not a transitive closure. |
| Dependency authority | fail closed | `S56-M-1227-PROOF` remains provisional `[_]`, its receipt is unaccepted, and it accepts no closed obligation. |
| Exact B-ZERO mapping | fail closed | The registry statement fingerprint is still `planned:v1`; only the master may map the checked declaration and accept node closure. |
| Exact root composition | fail closed | The proof contains only the zero-data branch; the nonzero/general construction and five-node cut are open. |
| Source fidelity | fail closed | Primary theorem/page/assumption/errata review is open. `scope-map.md` describes dimensions 2 or 3, optional forcing, and a weak source trace, while the frozen Prop is 3D, unforced, and uses a strong squared-L2 trace. |
| Complete trust and provenance | fail closed | Three direct imports are not a serialized transitive declaration/import closure, complete TCB inventory, or SBOM. |
| Hermetic release reproduction | fail closed | The run uses an automation-provided shared warm `.lake` cache, not a new clean checkout, empty-cache cold build, or offline-restored release closure. |
| Independent verification | fail closed | The differential implementation runs in this worker checkout and cache, not on a distinct signed independently provisioned runner. |

The first dependency-legal failure is
`dependency.S56-M-1227-PROOF.master_acceptance`. The first open theorem package is
`proof.M1227-N-DATA.kernel_closure`, and the first release failure is
`S56-10.6-HERMETIC-COLD-BUILD`. Root vector remains `[H2, M4, R4]`;
`audit_complete=false` and `theorem_complete=false`.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1227` | 0 | Rank 416; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1227/check_obligation_tree.py` | 0 | 21 obligations and 63 typed edges passed; root remained M4 with the five-node cut. |
| `python3 Stage1_Instances/THM-M-1227/check_proof.py` | 0 | The B-ZERO implementation candidate and bound proof hashes passed; root remained open. |
| `bash Stage1_Instances/THM-M-1227/check_proof.sh` | 0 | Isolated trust-zero replay passed; both proof declarations were sorry-free with the expected axiom set. |
| `python3 -I -B Stage1_Instances/THM-M-1227/check_validation.py` | 0 | Network-isolated trust-zero differential replay, hygiene, trust observation, selected provenance, receipt, and worker-packet checks passed while release gates failed closed. |
| JSON parsing, Python syntax compilation, scoped prohibited-device scan, and `git diff --check` | 0 | Structured artifacts parsed, the checker compiled, the scan was clean, and whitespace checks passed. |

This node is self-tested as truthful provisional validation work and proposes worker state `[_]`.
It grants no accepted receipt, exact-root credit, `E0/E1`, `M0`, `AUDIT-Z`, `THEOREM-Z`, release,
or master acceptance. Accepted receipt IDs: none.
