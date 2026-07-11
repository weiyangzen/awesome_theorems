# THM-M-0579 proof-phase blocker

Item: `S56-M-0579-PROOF`  
Attempt date: 2026-07-12  
Base revision: `291aeb20bea9e3684c8de5cfca9373fcec398835`

## Verdict

The proof phase is blocked and is not self-tested as complete. No worker self-test
manifest is emitted.

The frozen root is the full three-dimensional topological Poincare theorem. Its
proof DAG requires both
`Stage1Instances.THMM0579.HomotopySphereRecognition` and
`Stage1Instances.THMM0579.HomotopySphereTopologicalRigidity`. Neither proposition
has a retained proof body in this clone's pinned Lean environment. The only exact
mathlib signature,
`SimplyConnectedSpace.nonempty_homeomorph_sphere_three`, occurs in
`Mathlib.Geometry.Manifold.PoincareConjecture` as a Batteries `proof_wanted`
command; importing that module does not add the declaration to the environment.
The immutable candidates already recorded in `anchor-audit.json` likewise contain
no admissible terminal body: the Lean Millennium candidate is statement-only and
the Formal Conjectures candidate uses `sorry`.

Consequently, filling either open package would amount to supplying the missing
formalization of Perelman's theorem, not a repo-local wrapper or import. Adding an
assumption, an axiom, or a proof of a weaker dimension/special case would not prove
the frozen target. The existing
`root_of_recognition_and_rigidity` declaration is a checked conditional
composition only; it truthfully leaves both mathematical packages as premises and
does not close `Stage1Instances.THMM0579.Statement`.

## Validation evidence

Commands ran in the worker clone using only the existing pinned Lake artifacts.
No `lake update`, `lake build`, clone, fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0579` | 0 | Rank 114; lifecycle `planned`; `theorem_complete` is `false` |
| `python3 Stage1_Instances/THM-M-0579/check_obligation_tree.py` | 0 | 16 obligations and 34 typed edges passed; root remains open at M3 and recognition/rigidity remain M4 |
| `cd Stage1_Instances/THM-M-0579 && LEAN=$(cd ../../Formalizations/Lean && lake env which lean) && LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) "$LEAN" -o Statement.olean Statement.lean && LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) "$LEAN" ObligationTree.lean` | 0 | Exact statement and conditional composition elaborated; `root_of_recognition_and_rigidity` reports only `[propext, Classical.choice, Quot.sound]`; temporary `Statement.olean` was removed |

The first failed proof gate is terminal proof-body availability for
`M0579-T-RECOGNITION` and `M0579-T-RIGIDITY`. The remaining root cut set is those
two obligations (with the recognition subtree's frozen analytic, surgery, and
normalization obligations). Reattempt only when a compatible, immutable,
license-acceptable Lean 4 implementation supplies these bodies, or when those
bodies are formally developed against the pinned environment.

