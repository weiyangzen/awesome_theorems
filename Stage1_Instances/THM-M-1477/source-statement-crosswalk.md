# THM-M-1477 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10777-10782` supplies exactly the title `A-稳定性`, attribution
to Germund Dahlquist, year 1963, gloss `数值方法的稳定性`, importance `high`, and status
`已验证`. All six uncited lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no method, formula,
definition, binder, hypothesis, conclusion, theorem/page locator, proof, correction record,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:40162-40187` repeats the gloss while explicitly leaving the formal system,
precise definitions and premises, proof route, dependencies, alternate forms, axioms, machine
status, and artifact links open. Its generic closed-result and leaf-audit wording is planning
metadata, not source evidence. Rev-5.6 retains `已验证` only as untrusted metadata and resets this
target to `L0 / rework_required`.

## Inspected primary-source lead

Crossref bibliographic metadata identifies Germund G. Dahlquist, *A special stability problem for
linear multistep methods*, BIT, volume 3, issue 1, pages 27-43, March 1963, DOI
`10.1007/BF01963532`. Semantic Scholar independently returns the same title, author, year, DOI, and
publication date while marking the full text closed. This is a strong primary-source lead matching
the catalog author and year.

It is not `H0`. The catalog does not cite this article; no exact theorem passage or complete
incorporated-definition chain was inspected; no statement, assumptions, transitions, conclusion,
proof boundary, corrections, or errata were mapped; and no independent source reviewer admitted a
root. Bibliographic identity and a DOI alone are `E5` discovery evidence under rev-5.6.

## Literal statement crosswalk

| Repository component | Required mathematical component | Prospective Lean component | Intake result |
|---|---|---|---|
| A-stability | exact property or theorem and its logical direction | exact `Prop` with ordered binders | label only; definition versus theorem open |
| numerical method | one-step/RK/general-linear/LMM class or concrete method | source-identical scheme structure and coefficient data | class and representation absent |
| stability | test equation, stability region, norm/root criterion, and boundary convention | quantified complex-region or root predicate | predicate and quantifiers absent |
| Dahlquist, 1963 | historical attribution and possible multistep source family | provenance only | no cited work or selected passage |
| verified | inventory screening label | accepted human-source/kernel receipt | explicitly rejected as evidence |

The literal record cannot populate a canonical domain, ordered binders, hypotheses, conclusion,
alternate encodings, excluded cases, or Lean expression fingerprint.

## Candidate-meaning boundary

For a one-step or Runge-Kutta method, a common formulation uses a rational stability function `R`
and asks whether the left half-plane lies in `{z | norm (R z) <= 1}`. For a linear multistep method,
stability is instead expressed through the roots of `rho(zeta) - z * sigma(zeta)`, including a
simple-root condition on the unit circle. A source may also prove a theorem about methods satisfying
that property, including the Dahlquist order barrier. These encodings need different data,
hypotheses, and conclusions. No checked equality, `Iff`, or implication between them is credited.

Choosing the second Dahlquist barrier solely from author and year would be conjectural source
reconstruction. Choosing a definition would not turn the catalog label into a theorem. Choosing
implicit Euler or trapezoidal rule would narrow an unidentified general target. Each is prohibited
until the source owner corrects and independently reviews the target.

## Pinned Lean crosswalk

| Candidate | What the pinned declaration supplies | Why it is not the target |
|---|---|---|
| `Polynomial.eval`, `Polynomial.eval₂` | polynomial evaluation in one semiring or through a homomorphism | no numerical-method or multistep polynomial-pair semantics |
| `Complex.normSq` | squared norm as a multiplicative map on complex numbers | no stability function, left-half-plane quantifier, or method theorem |
| `Metric.mem_closedBall` | membership characterization for a metric closed ball | no stability region or inclusion theorem |

`IntakeProbe.lean` checks these declarations at the pinned revision and reports axioms for two
adjacent library lemmas. A bounded exact-topic search located no numerical A-stability terminal
theorem. The probe and search are discovery evidence only, not a canonical target, proof body,
exhaustive anchor audit, or absence proof.

## Neighbor boundary

`THM-M-1475` separately names Runge-Kutta stability, `THM-M-1476` stiff stability, and
`THM-M-1478` L-stability. `THM-M-1472`, `THM-M-1473`, and `THM-M-1474` separately name Lax
equivalence, the CFL condition, and von Neumann finite-difference stability analysis. These records
confirm that none of those more specific or differently scoped propositions may be imported
silently as `THM-M-1477`.

## Source gate

The first downstream gate requires an accountable correction that selects and preserves one exact
immutable-source proposition; maps the method class and coefficients, test equation and sign,
stability representation and region, polynomial/root or rational-function conventions,
consistency/zero-stability/order assumptions, logical direction, constants, quantifier order,
arithmetic model, and degenerate cases; audits the incorporated proof and corrections; and receives
independent numerical-analysis and source review. Only then may the statement phase freeze the Lean
expression, minimal imports, checked transports, and required mutations.

Until then, `H5` records that the catalog target is not yet a stable truth-valued proposition,
`M4` records the lack of a source-identical usable formal artifact, and `R4` records the lack of an
anchorable proof reconstruction. These classifications do not say that established A-stability
results are false or open.
