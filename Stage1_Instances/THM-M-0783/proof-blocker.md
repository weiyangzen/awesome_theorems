# THM-M-0783 proof-phase blocker

Item: `S56-M-0783-PROOF`  
Base revision: `1c5adf59c0f8176526cb4c9fb281b3ff340c9eeb`  
Assessment date: `2026-07-12` (`Asia/Shanghai`)

## Verdict

The proof phase is blocked and is not self-tested as complete. No proof body for
`Stage1Instances.THM_M_0783.MartinsAxiom` exists in the pinned dependency closure. The one open
machine leaf, `M0783-L-DENSE-FAMILY`, is definitionally the full expanded Martin's-axiom
proposition: for every `kappa < Cardinal.continuum`, nonempty ccc partial order, and suitably
bounded family of dense sets, it must construct a filter meeting the entire family.

Martin's axiom is an additional set-theoretic axiom, not a theorem available from the selected Lean
foundation. Introducing `MartinsAxiom` or `DenseFamilySolver` with `axiom`, `sorry`, a bodyless
declaration, or an extra premise would change the foundation or prove only a conditional theorem.
All of those routes are forbidden by the assigned gate. The existing
`root_of_denseFamilySolver` is an honest checked transport, but its `solve` argument is exactly the
open content and therefore supplies no root proof credit.

The frozen anchor audit found only cardinal and set infrastructure in pinned mathlib, and no exact
external Lean 4 proof candidate to pin or import. A scoped source scan reconfirmed that the pinned
mathlib tree has no Martin's-axiom declaration; its occurrences of "forcing" are unrelated model
theory documentation, order-ideal commentary, or incidental prose. No dependency update, fetch,
clone, or `.lake` mutation was attempted.

Accordingly, no Lean proof source was added and no `.stage1-worker-selftest.json` was written. The
first failed gate is exact root kernel closure without placeholders or an expanded foundation. The
remaining root cut set is `M0783-L-DENSE-FAMILY`. A retry requires a concrete Lean 4 proof body for
the exact frozen proposition, with immutable provenance and an acceptable axiom report, or a
master-approved correction that moves this additional axiom out of the theorem-proof queue. The
latter would be a target-policy change, not completion of this proof item.

## Narrow validation

All commands ran in the worker clone and reused only the existing pinned Lean artifacts.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0783` | 0 | rank 788; lifecycle `planned`; target lane `hard_statement_first_partial_verification`; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0783/check_obligation_tree.py` | 0 | 12 obligations and 28 typed edges passed; denominator `0581a4ed...25532c9`; root open at `M4` |
| `cd Formalizations/Lean && lake env lean -R ../.. -o /tmp/thm-m-0783-proof/Statement.olean ../../Stage1_Instances/THM-M-0783/Statement.lean` | 0 | exact canonical statement re-elaborated into an isolated temporary olean |
| `cd Formalizations/Lean && LEAN_PATH=/tmp/thm-m-0783-proof lake env lean -R ../.. ../../Stage1_Instances/THM-M-0783/ObligationTree.lean` | 0 | conditional composition elaborated; axiom report was `[propext, Classical.choice, Quot.sound]` |
| `rg -n -i "martin.?s axiom\|martinsaxiom\|forcing" Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | no Martin's-axiom declaration; only unrelated uses of "forcing" were found |
| `sha256sum Stage1_Instances/THM-M-0783/Statement.lean Stage1_Instances/THM-M-0783/ObligationTree.lean Stage1_Instances/THM-M-0783/obligation-registry.json` | 0 | `c7adfe1b...f757d40`, `64953151...07d361`, `099b0299...0fd07` |

The successful Lean checks validate only the exact statement and already frozen conditional
child-to-root composition. They are evidence for the blocker boundary, not a proof of Martin's
axiom. The theorem remains incomplete and this worker claims no master acceptance.
