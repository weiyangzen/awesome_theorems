# THM-M-0590 proof-phase blocker

Item: `S56-M-0590-PROOF`  
Attempt date: 2026-07-12  
Base revision: `b6840b8306a1983491c1963271bd791635c42c3f`

## Verdict

The assigned proof phase is blocked and is not self-tested as complete. No
`.stage1-worker-selftest.json` is emitted.

The frozen exact root requires both `THMM0590.ForwardInvariantPackage` and
`THMM0590.BackwardClassificationPackage`. Neither package has a proof-bearing
declaration in this repository or the pinned mathlib closure. The existing
`root_of_directional_packages` body is real and kernel-checks the final logical
composition, but it consumes those two missing packages as premises and cannot
be credited as an unconditional BDF proof.

The predecessor anchor audit found only compact-operator, adjoint, and ordinary
spectrum support. It found no exact immutable Lean candidate and no pinned
Calkin algebra, general Fredholm-index, essential-spectrum, Busby-extension, or
BDF classification API. Consequently, honest root closure would require the
substantive formalization represented by the open Calkin, Atkinson, forward
invariance, Busby, extension-classification, and index-completeness obligations.
No axiom, placeholder, hidden premise, or broadened/substituted theorem was
introduced.

## Validation evidence

Commands ran in this worker clone with the existing pinned Lake artifacts. No
update, build, dependency clone/fetch, or `.lake` mutation was performed. The
temporary `Statement.olean` used for the dependent module check was written
under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok` for 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok` for 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0590` | 0 | Confirmed rank 630, lifecycle `planned`, hard-statement-first lane, and `theorem_complete: false`. |
| `python3 Stage1_Instances/THM-M-0590/check_obligation_tree.py` | 0 | Passed 17 obligations and 37 typed edges; denominator `2d5b17d...9a9e8`; root open at M4 and both directional packages M4. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0590/Statement.lean` | 0 | Printed `THMM0590.brownDouglasFillmoreTarget.{u_2, u_3} : Prop`. |
| `LEAN=$(cd Formalizations/Lean && lake env which lean); LP=$(cd Formalizations/Lean && lake env printenv LEAN_PATH); cd Stage1_Instances/THM-M-0590; LEAN_PATH="$LP" "$LEAN" -o /tmp/.../Statement.olean Statement.lean; LEAN_PATH="/tmp/...:$LP" "$LEAN" ObligationTree.lean` | 0 | Conditional composition elaborated; `#print axioms` reported `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg -n '^\\s*(sorry\|admit\|axiom)(\\s\|$)' Stage1_Instances/THM-M-0590 --glob '*.lean'` | 1 | Expected no-match result: no prohibited Lean declaration token. |
| `rg -n -i 'Brown.?Douglas.?Fillmore\|Calkin\|essentialSpectrum\|IsFredholm\|fredholmIndex\|essentiallyNormal\|Busby' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | Expected no-match result in pinned mathlib source. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |

The first failed proof gate is terminal proof-body availability for
`M0590-B-FORWARD` and `M0590-T-BACKWARD`; these are the remaining root cut set.
This record is blocker evidence only and claims no proof completion, M0 status,
validation, release, theorem completion, or master acceptance.
