# Source-statement crosswalk

## Primary source identified

Gerd Faltings, "Endlichkeitssatze fur abelsche Varietaten uber
Zahlkorpern", *Inventiones Mathematicae* **73** (1983), 349-366,
DOI `10.1007/BF01388432`. The commonly cited Mordell-conjecture consequence is
associated with Satz 1 on page 349.

This intake has not inspected and archived a stable scan or checked later
corrections, exact German wording, every convention, or the derivation from the
paper's abelian-variety results. The locator is therefore a search lead, not
`H0` evidence. Independent review remains open.

## Crosswalk

| Canonical component | Source-side concept | Intake disposition |
|---|---|---|
| number field `K` | `Zahlkorper` | included; exact convention audit open |
| smooth proper geometrically connected curve | nonsingular complete curve over `K` under source conventions | included; convention transport open |
| genus at least two | genus greater than one | included |
| `K`-rational points | points rational over `K` | included; Lean section encoding open |
| finiteness | only finitely many `K`-rational points | included |

## Provenance and legacy boundary

Repository metadata contributes a Chinese theorem name, category, and the
untrusted label `已验证`; none establishes human fidelity or machine closure.
The legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_042.lean`
gives a useful quantifier skeleton and mathlib-backed smooth/proper structure,
but its genus field is an arbitrary proposition and it contains no terminal
proof of Faltings's theorem. It receives no rev-5.6 statement or proof credit.

The anchor audit must inspect the primary paper at the cited locator, record
assumptions and errata, distinguish a theorem stated directly for curves from a
corollary, and obtain independent source-to-target review.

