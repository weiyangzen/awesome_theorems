# Scope map

## Frozen repository boundary

- Target: `THM-M-1386`, `Sturm分离定理`, in ordinary differential equations.
- Literal claim: zeros of linearly independent solutions interlace.
- Attribution/date: Jacques Sturm, 1836, both catalog metadata rather than a citation.
- Baseline: `L0 / rework_required`; no legacy slot or accepted legacy artifact.
- Intake decision: the title and gloss identify the Sturm separation family, but the canonical
  statement and Lean expression remain null until an independently reviewed source is selected.

## Source-family decisions still open

The statement phase must select and justify all of the following before elaboration:

- Classical compact-interval theorem, Beesack Theorem 1(b), the entire singular-endpoint Theorem 1,
  or another pinpointed source result.
- Self-adjoint equation `(r y')' + s y = 0`, normal form `y'' + p y' + q y = 0`, a parameterized
  Sturm-Liouville equation, or a checked equivalence between selected forms.
- Open, closed, compact, bounded, or extended-real interval; interior versus endpoint zeros; and
  the source definition of a nonsingular endpoint.
- Continuity, differentiability, local integrability, and positivity or nonvanishing assumptions on
  coefficients, including which assumptions guarantee the intended solution regularity.
- A source-faithful solution predicate for the second-order equation, including whether derivatives
  are ordinary, within-set, weak, or almost-everywhere derivatives.
- Real-valued versus complex-valued solutions and linear independence as functions on which domain.
- Nontriviality, simplicity and isolation of zeros, the exact consecutive-zero predicate, and the
  endpoint behavior needed for existence.
- `At least one`, `precisely one`, reciprocal separation, or a globally indexed strict-alternation
  conclusion, with exact quantifier order.

## Boundary and degenerate cases

No case is excluded at intake because no canonical proposition is selected. Source review must
dispose of an empty, singleton, disconnected, or unbounded domain; equal or reversed zero endpoints;
zeros outside the equation's carrier; zeros accumulating at a singular endpoint; coefficients with
`r = 0` or a sign change; solutions that vanish identically; linearly dependent solutions; common
zeros; nonsimple zeros; only one or no zero of the reference solution; singular finite endpoints;
infinite endpoints; and complex-valued solutions whose `zero interlacing` lacks an order-theoretic
reading.

Beesack's Theorem 1 shows why endpoint conditions cannot be elided: part (b) gives precisely one
interior zero when consecutive zeros of the first solution are nonsingular, while parts (c)-(e)
classify several different behaviors when one or both endpoints are singular.

## Neighbor and substitution exclusions

- `THM-M-1384` owns the broader Sturm-Liouville theory entry; it supplies no proof credit here.
- `THM-M-1385` owns Sturm's comparison theorem, involving different equations or coefficient
  inequalities; comparison cannot replace separation for two independent solutions of one equation.
- `THM-M-1387` owns the broader oscillation-theory entry.
- `THM-M-1388` owns Sturm-Liouville eigenvalue problems. Interlacing consecutive eigenfunctions is
  not automatically the same theorem as separation of arbitrary independent solutions of one fixed
  equation; in particular, eigenfunctions for distinct eigenvalues solve different equations.
- Polynomial Sturm sequences, polynomial or matrix eigenvalue interlacing, and root-counting Sturm
  theorems are distinct targets.
- A structure field or hypothesis that directly stores the desired intermediate zero is not a proof.
- Generic derivative, Rolle, intermediate-value, ODE, or linear-independence APIs are substrate only.
- The catalog's untrusted `verified` label and the intake probe provide no source or proof credit.

## Formal boundary

A likely Lean encoding will need a chosen representation of the second-order equation, a solution-on-
interval predicate, `LinearIndependent ℝ ![y1, y2]` or a checked equivalent, a consecutive-zero
predicate, and a conclusion such as `∃! x ∈ Set.Ioo x1 x2, y2 x = 0`. That sketch is not the target:
its exact types, binders, hypotheses, conclusion, and imports remain deliberately unfrozen.

Pinned mathlib exposes derivative algebra, monotonicity from derivative signs, Rolle and intermediate-
value results, and pairwise linear independence. The probe authenticates only those adjacent APIs.
No canonical Lean expression, expression fingerprint, checked transport, mutation suite, or proof
body is claimed at intake.
