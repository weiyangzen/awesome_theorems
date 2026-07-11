# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` gives the title, attribution to Jean le Rond
d'Alembert, year 1746, and the phrase "general solution of the one-dimensional
wave equation". `Docs/Stage0_Blueprint.md` repeats this phrase but leaves exact
definitions, hypotheses, equivalent formulations, axioms, and machine status
open. No edition, theorem/page, translation, or errata record is attached.

No primary-source candidate is asserted at intake. The secondary metadata is
enough to identify a theorem family but not one exact proposition, so its
`已验证` label earns no H or M credit.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "one-dimensional" | one spatial coordinate | domain type and coordinate model | unresolved |
| "wave equation" | hyperbolic PDE family | derivative convention, equation, wave speed | unresolved |
| "general solution" | representation likely needs completeness | precise quantifiers and both-direction scope | unresolved |
| "d'Alembert formula" | named formula family | initial-data or traveling-wave encoding | unresolved |
| d'Alembert / 1746 | attribution metadata | primary edition, theorem/page, assumptions, errata | unverified |
| `已验证` | untrusted inventory status | inspectable proof or kernel receipt | no credit |

## Candidate statement families, not adopted

One common classical family states that twice differentiable traveling-wave
profiles yield a solution by `u(x,t)=F(x-ct)+G(x+ct)`, with a converse under
appropriate regularity and domain hypotheses. Another gives the Cauchy solution
from initial displacement and velocity, including an integral divided by
`2*c`. They are related but have different binders, hypotheses, boundary cases,
and proof obligations. A primary source and statement review must select and
crosswalk the intended claim before exact Lean elaboration.

The first downstream gate is therefore source identification and exact scope
freeze. H0 later requires edition/theorem/page/assumption/errata evidence and an
independent row-by-row review.
