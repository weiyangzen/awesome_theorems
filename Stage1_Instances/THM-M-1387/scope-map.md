# Scope map

## Preserved catalog scope

The intake preserves the title `振荡理论`, the literal gloss `解的振荡性`, the ordinary-differential-
equations category, the collective attribution, and the twentieth-century date. It does not infer
one exact theorem. A later statement phase may select a root only from an immutable,
independently reviewed source passage.

Candidate mathematical components, none credited as the theorem, include:

- a scalar second-order ODE, a self-adjoint Sturm-Liouville equation, a higher-order equation, a
  system, or a source-selected nonlinear equation;
- a finite interval, half-line, whole line, singular endpoint, or another source-selected domain;
- a nontrivial real solution and a source-defined zero, sign-change, or phase predicate;
- oscillation as infinitely many zeros, arbitrarily large zeros, endpoint accumulation, repeated
  sign changes, or a property defined through a Pruefer angle;
- a universal claim about every nontrivial solution, existence of one oscillatory solution, or an
  equation/operator classification; and
- a comparison, separation, zero-count, eigenvalue, criterion, or asymptotic conclusion.

## Decisions required at statement freeze

1. Preserve one lawful complete source edition, exact theorem/definition/section/page, incorporated
   definitions, proof boundary, corrections or errata, and independent review.
2. Fix the differential equation, its order and form, dependent-variable codomain, independent-
   variable domain, coefficients, spectral parameters, and boundary conditions.
3. Fix coefficient regularity, positivity, integrability, local boundedness, endpoint, and
   self-adjointness assumptions, including every typeclass and coercion needed by Lean.
4. Define the solution notion and regularity: classical, weak, maximal local, global, real-valued,
   nontrivial, normalized, eigenfunction, or another source-selected class.
5. Define what counts as a zero and as oscillatory: distinct versus multiplicity-counted zeros,
   sign changes, infinitely many zeros in the domain, arbitrarily large zeros, accumulation at a
   finite or singular endpoint, or an equivalent source-approved phase formulation.
6. Fix quantifier polarity: every, some, or one normalized nontrivial solution; one parameter value
   or a range; one equation, a family, or an operator.
7. Select the exact conclusion: oscillatory/nonoscillatory classification, sufficient or necessary
   criterion, comparison implication, nodal count, spectral equivalence, or another result.
8. Freeze ordered binders, dependencies, all hypotheses, the exact conclusion, logical principles,
   and any checked alternate encodings.

## Degenerate and boundary cases

Source review must explicitly dispose of the zero solution; coefficients producing a degenerate or
first-order equation; empty, singleton, bounded, unbounded, open, closed, and half-open domains;
zeros at endpoints; repeated/tangent zeros without sign change; infinitely many zeros accumulating
inside the domain; solutions existing only locally; singular endpoints; identically zero
coefficients; zero or threshold spectral parameter; equality cases in comparison criteria; and
whether vacuity occurs when no nontrivial global solution exists.

## Neighbor and substitution exclusions

- `THM-M-1384` Sturm-Liouville theory, `THM-M-1385` Sturm comparison, `THM-M-1386` Sturm
  separation, `THM-M-1388` the eigenvalue problem, and `THM-M-1391` the Pruefer transform retain
  separate target ownership. Their statements or evidence cannot silently select this root.
- Teschl's zero-count theorem, Sturm comparison theorem, nodal theorem, Kneser criterion, or the
  half-line definition cannot replace the catalog phrase without an accountable source decision.
- Mathlib's pointwise `oscillation` of a function at a topological point is a different concept and
  is not an ODE oscillation theorem.
- A sinusoidal example, harmonic oscillator, numerical trajectory, plotted zero pattern, or
  special coefficient choice cannot substitute for a general source-selected theorem.
- A structure field or hypothesis that assumes the desired oscillatory classification is not a
  proof, and the catalog label `verified` carries no source or kernel credit.

No canonical Lean target, expression fingerprint, checked transport, discovery protocol,
obligation registry, or proof state is frozen at intake.
