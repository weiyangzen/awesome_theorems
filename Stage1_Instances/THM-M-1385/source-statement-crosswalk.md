# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:10090-10095` records only the title `Sturm comparison theorem`,
Jacques Sturm, the year 1836, and the gloss `comparison of zeros of solutions`. Those six catalog
lines originate at repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives
no bibliography, equation, interval, binders, coefficient hypotheses, solution definition, strict
or weak comparison direction, endpoint rule, multiplicity convention, proof, or formal artifact.
`Docs/Stage0_Blueprint.md:37668-37693` repeats the gloss while explicitly leaving exact definitions,
premises, proof route, dependencies, equivalent forms, axioms, and machine artifacts open.

## Inspected primary source

C. Sturm, *Memoire sur les Equations differentielles lineaires du second ordre*, *Journal de
Mathematiques Pures et Appliquees*, series 1, volume 1 (1836), pages 106-186. The stable NUMDAM
record is `JMPA_1836_1_1__106_0`; the inspected 82-page PDF was 3,056,791 bytes with SHA-256
`dac79254915e753884f6dd68865ef5c7165043599ac611558c6c4d6045feac96`.

Section XII, journal pages 125-126 (PDF pages 21-22), compares
`(d/dx)(K' dV'/dx) + G' V' = 0` and `(d/dx)(K'' dV''/dx) + G'' V'' = 0` on an interval.
The scan shows `G'' >= G'`, positive `K'` and `K''`, `K'' <= K'`, and a left-endpoint inequality
between `K'' (dV''/dx) / V''` and `K' (dV'/dx) / V'`. It concludes that `V''` vanishes and changes
sign at least as many times as `V'`, and that same-rank zeros of `V'`, ordered from the left, occur
later than those of `V''`. A footnote permits a leading coefficient to vanish at the left endpoint
under an additional compatibility condition that must be mapped before formalization.

Section XVI, journal pages 135-136 (PDF pages 31-32), retains the non-strict source orders
`G'' >= G'` and `K'' <= K'` but removes dependence on endpoint logarithmic derivatives. Between two
consecutive zeros of `V'` it places at least one zero of `V''`; between two consecutive zeros of
`V''` it permits at most one zero of `V'`. OCR drops the equality bars, so these inequalities were
read from the page scan. The catalog gloss does not choose section XII's full global theorem,
section XVI's local corollary, or a normalized equivalent form. Complete proof mapping,
translation, errata review, and independent review remain open, so this intake does not claim `H0`.

Crossref metadata also identifies the collected-works reprint at DOI
`10.1007/978-3-7643-7990-2_30`, pages 392-472. It is bibliographic corroboration, not a separately
inspected or selected edition.

Encyclopedia of Mathematics, `Sturm theorem`, immutable revision `51620`, was inspected through
the MediaWiki API. It states the polynomial Sturm-series theorem: under four conditions, the
number of distinct roots of a function on `[a,b]` equals the change in sign variations of a Sturm
series. It cites an 1829 publication. This is useful negative evidence: it is not the repository's
1836 ODE comparison-of-solution-zeros item and is expressly excluded as a substitute. The entry is
a secondary source and supplies no proof or formal credit for this target.

Crossref discovery for the phrase `Sturm comparison theorem` also returns materially different
extensions for difference equations, nonlinear problems, singular equations, and time scales.
This reinforces the need to fix the classical scalar ODE statement before selecting a Lean target;
the search results themselves are not source or anchor-audit completion evidence.

## Component crosswalk

| Catalog/source component | Candidate mathematical content | Prospective Lean surface | Intake status |
|---|---|---|---|
| "solutions" | nontrivial classical solutions of two second-order scalar linear ODEs | functions `Real -> Real`, `HasDerivAt`, `HasDerivWithinAt`, or `IsIntegralCurveOn` after first-order encoding | exact solution predicate and regularity open |
| "zeros" | points where a solution equals zero, often consecutive isolated zeros | set comprehension, equality to zero, interval membership | consecutiveness, isolation, endpoints, multiplicity open |
| "comparison" | source orders `G'' >= G'`, `K'' <= K'`; either global count/order plus endpoint flux or local consecutive-zero comparison | ordered coefficient functions, endpoint flux, zero-count/order or existential interval conclusion | source components identified; canonical passage and encoding open |
| interval | an interval on which coefficients and solutions satisfy the equations | `Set.Icc`, `Set.Ioo`, or another source-selected domain | endpoint and local/global convention open |
| ODE form | normal form or self-adjoint Sturm-Liouville form | derivative equations or a first-order system encoding | source form and checked transport open |
| catalog `verified` | inventory metadata only | no declaration or proof object | explicitly rejected as evidence |

## Source and Lean exit gate

The statement phase must independently approve one of the inspected source passages, including
every incorporated definition, hypothesis, inequality direction, endpoint convention, proof
boundary, translation, and erratum. It must then elaborate and
fingerprint the binder-complete Lean expression with minimal pinned imports, add checked transports
for any alternate ODE representation, and run the four required mutation classes. Until then the
provisional human-source status is `H1`, machine status is `M4`, readability status is `R4`, and no
statement or proof closure is claimed.
