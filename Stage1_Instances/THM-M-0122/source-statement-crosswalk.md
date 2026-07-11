# Source-statement crosswalk

## Primary source identified

Gerd Faltings, "Endlichkeitssatze fur abelsche Varietaten uber Zahlkorpern,"
*Inventiones Mathematicae* 73 (1983), 349-366. DOI:
`10.1007/BF01388432`.

This identification is not `H0`. The exact internal Satz/corollary and page,
the original German terminology, hypotheses used for the curve consequence,
later correction/errata history, and an independent review remain open. This
intake therefore records the article page range rather than inventing a precise
locator.

## Crosswalk

| Source-side concept | Frozen target meaning | Lean status at intake |
|---|---|---|
| Zahlkorper | number field `K` | mathlib carrier/API selection pending |
| nonsingular projective curve | smooth projective curve over `K`, with exact geometric connectedness/integrality convention to be audited | native conjunction unresolved |
| genus greater than one | geometric genus of the curve is strictly greater than one | native invariant unresolved |
| rational points | `K`-morphisms `Spec K -> C`, equivalently sections of the structure map | legacy checked encoding is discovery input only |
| finiteness | the full type/set of `K`-rational points is finite | exact `Finite`/`Set.Finite` target unresolved |

## Repository-source crosswalk

`Docs/researches/math_theorems.md` supplies only the label "Mordell conjecture's
proof" and is not a statement-level source. The generated legacy blueprint
narrows that label to rational-point finiteness. The primary-paper audit must
control the final statement rather than either metadata summary.

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_041.lean` checks useful
section and slice-category point encodings and a provisional curve condition.
Its `GeometricGenusSlot := Nat` is not computed from the curve, and its curve
condition deliberately omits a selected projectivity API. Consequently the
legacy `StatementShape` receives no exact-statement or theorem-proof credit.

## Fidelity risks

Older formulations may say nonsingular complete/projective curve and may build
geometric irreducibility or connectedness into the word "curve." The theorem
is also commonly called both Faltings' theorem and Mordell's conjecture. These
terminological choices must not change the quantified field, the curve's
geometric hypotheses, the genus boundary, or the full rational-point set.
