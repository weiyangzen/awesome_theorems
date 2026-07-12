# Source-statement crosswalk

## Repository record and source lead

The repository inventory supplies only the label "Darboux transformation", Gaston Darboux, the
year 1882, and the gloss "transformation of the Schrodinger equation". Its `已验证` field is
untrusted under rev-5.6. It provides no equation, theorem number, page, hypotheses, or conclusion,
so it does not determine an exact proposition.

A historical primary-source lead is Gaston Darboux, *Sur une proposition relative aux equations
lineaires*, Comptes rendus de l'Academie des sciences, volume 94 (1882), commonly cited in the
literature on this transformation. This intake records it only as a discovery lead. An immutable
scan, exact pages/result, original wording, notation, assumptions, and corrections have not been
independently inspected here. The modern Schrodinger-operator formulation may be a later
specialization of Darboux's linear-equation result, so it must not be attributed to the source
without a checked historical crosswalk.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "Schrodinger equation" | second-order scalar spectral ODE and sign convention | interval functions, derivatives, potential multiplication, spectral equation | family identified; exact normal form open |
| seed solution | solution at a factorization energy and its nonvanishing domain | seed predicate, regularity, pointwise nonzero hypothesis | necessary construction input; source hypotheses open |
| "transformation" | first-order operator using the seed's logarithmic derivative | explicit function/operator definition with division domain | intended construction identified; formula convention open |
| transformed potential | potential changed by a seed-derived second-derivative term | explicit transformed-potential definition | included; coefficient and sign open |
| preservation of solutions | intertwining implies a transformed spectral equation | equality of differential expressions and mapped-solution theorem | intended conclusion family; exact strength open |
| Darboux / 1882 | bibliographic disambiguation from other Darboux theorems | no machine-proof credit | historical lead only |

## Human and machine boundary

The repository-wide search found no theorem-specific Lean artifact for `THM-M-1555`. The pinned
mathlib name search found `Mathlib/Analysis/Calculus/Darboux.lean`, but that module formalizes the
intermediate-value property of derivatives, not this transformation. This negative, name-oriented
search is intake evidence only and is not the later exhaustive anchor audit.

Before `H0`, an independent reviewer must inspect an immutable primary edition, select the exact
result and page, verify translation and errata, and approve every assumption and source-to-modern
specialization. Before statement credit, those components must map row by row to one elaborated
Lean expression without silently excluding seed zeros, changing the solution concept, or replacing
the source theorem by a convenient abstract intertwining premise.
