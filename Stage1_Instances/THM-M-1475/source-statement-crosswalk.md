# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10763-10768` supplies exactly the title
`龙格-库塔法的稳定性`, the attribution `众多数学家`, the period `20世纪`, the gloss
`RK方法的稳定性区域`, importance "high," and status `已验证`. Git provenance places all six
uncited lines in repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains
no equation, tableau, definition, binder, hypothesis, conclusion, proof, source locator,
correction record, or formal artifact.

`Docs/Stage0_Blueprint.md:40108-40133` repeats the catalog fields while explicitly leaving exact
definitions and premises, proof route, dependencies, equivalent forms, axioms, machine status,
and artifact links open. Its generic planning text is not source evidence. The rev-5.6 manifest
retains `已验证` only as `source_status_untrusted` and resets the target to
`L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| RK methods | a general tableau family or one named scheme | stage index, coefficient matrix, weights/nodes, and update equations | unspecified |
| stability | absolute, A-, L-, B-, algebraic, contractive, internal, or another notion | exact predicate and complete problem class | unspecified |
| stability region | a subset of complex step-eigenvalue products | parameter carrier, amplification map, domain/poles, modulus or norm criterion | unspecified |
| methods, plural | a theorem uniform in tableaux or a collection of examples | quantification over admissible schemes or an exact selected list | unspecified |
| many mathematicians / twentieth century | a source family | immutable edition and pinpoint proposition, definitions, proof, errata, reviewer | no locator |
| `已验证` | untrusted inventory status | reviewed human-source packet or kernel receipt would be required | no H or M credit |

The wording does not state whether the intended root defines a region, derives a stability function,
computes one method's region, or proves a property about a family. Combining these alternatives
would broaden the catalog rather than clarify it.

## Source-family leads

Ernst Hairer and Gerhard Wanner, *Solving Ordinary Differential Equations II: Stiff and
Differential-Algebraic Problems*, second revised edition, Springer, 1996, is a strong modern
source-family lead. The authors' table of contents locates "Stability Analysis for Explicit RK
Methods" in Chapter IV.2, pages 15-37, and "Stability Function of Implicit RK-Methods" in IV.3,
pages 40-49, followed by separate A- and L-stability material. The author-hosted correction sheet
for the 2010 printing includes an L-stability correction on page 98. This demonstrates that exact
method, definition, edition, and correction choices matter; the catalog does not cite the book or
select a proposition from it.

Tobin A. Driscoll and Richard J. Braun, *Fundamentals of Numerical Computation*, immutable source
commit `000839af87622138c210a6361ba05913705ffbe4`, Chapter 11 section "Absolute stability," is an
inspectable modern lead. Lines 37-76 reduce linear dynamics to the scalar test equation, define
absolute stability at a complex parameter, and define a solver's stability region; lines 78-145
give method-specific examples and discuss Runge-Kutta regions. The section treats Runge-Kutta and
multistep solvers and supplies definitions and examples rather than a catalog-identified theorem.
It therefore cannot be adopted as the root without an explicit target-selection and review step.

J. C. Butcher, *Numerical Methods for Ordinary Differential Equations*, third edition, Wiley,
2016, DOI `10.1002/9781119121534`, is another authoritative bibliographic lead. The repository
does not cite it, and no exact theorem/section/page, incorporated definitions, proof boundary,
errata, or independent review was admitted here.

These leads are discovery evidence only. No source is credited as `H0`, and no prose or formula
from them is silently installed as the canonical claim.

## Source exit gate

Before ordinary statement work, accountable reviewers must admit and hash one immutable source;
select one exact truth-valued proposition and every incorporated definition; map all ordered
binders, tableau constraints, equations, invertibility or domain hypotheses, stability predicates,
conclusions, constants, and exceptional cases; audit the relevant edition and corrections;
reconcile ownership with `THM-M-1396` and `THM-M-1474` through `THM-M-1478`; and obtain an
independent numerical-analysis source review. The H classification must then be recomputed.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded exact-topic
search found no named Runge-Kutta, Butcher-tableau, absolute-stability, stability-function, or
stability-region declaration. `IntakeProbe.lean` checks finite-matrix, complex-norm,
rational-function, and analytic ODE interfaces adjacent to a possible future encoding. This is not
an exhaustive anchor audit or a global absence claim.

The canonical module, declaration/expression, elaborated-expression hash, environment fingerprint,
checked transports, and statement mutations remain null. Adjacent APIs supply no exact statement,
H0, M0, or proof credit.
