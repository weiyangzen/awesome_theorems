# Scope map

## Preserved repository scope

The repository fixes target `THM-M-1438`, the label `Lanford证明`, Oscar Lanford, the year 1982,
and the gloss `Feigenbaum猜想的计算机辅助证明`. This identifies Lanford's computer-assisted
Feigenbaum proof family in one-dimensional period-doubling dynamics. Importance "high" and status
`已验证` are catalog metadata, not theorem or proof evidence.

The matching primary source is Oscar E. Lanford III, "A computer-assisted proof of the Feigenbaum
conjectures," *Bulletin (New Series) of the American Mathematical Society* 6(3), May 1982,
pp. 427-435 in Crossref metadata, DOI `10.1090/S0273-0979-1982-15008-X`. The inspected publisher
scan contains the physical article on printed pages 427-434, and the next article in the issue
starts on p. 435; Crossref's boundary-style range is retained as metadata, not treated as physical
article pagination. The paper says it announces a proof of "essentially all" the relevant conjectures and gives
four distinct numbered theorems, not a single theorem called "the Lanford proof."

## Source-suite candidates not selected

The source defines a renormalization operator on normalized even unimodal interval maps and states
the following candidate clauses:

- Theorem 1: existence of an even analytic fixed point `g` of the renormalization operator on
  `{z : C | |z| < sqrt(8)}`, with negative Schwarzian derivative on `[-1, 1]`.
- Theorem 3: hyperbolicity of `DT(g)` on a specified Banach subspace, with a one-dimensional
  expanding subspace and positive expanding eigenvalue.
- Theorem 4: an iterate of the source's starred point on a chosen local unstable manifold lies on
  the simple period-doubling bifurcation surface.
- Theorem 5: for the quadratic family `x |-> 1 - mu * x^2`, an iterate of the parameter curve
  crosses a chosen local stable manifold transversally at a parameter in a stated interval.

Theorem 1 alone, Theorems 1 and 3 as the computer-estimate core, and the conjunction of Theorems
1, 3, 4, and 5 are inequivalent targets. No candidate is selected or credited at intake.

## Proposition-changing decisions

An approved source-to-target decision must freeze:

- which numbered result or exact conjunction constitutes the canonical root;
- the source's space of continuously differentiable even unimodal maps, normalizations at zero,
  strict monotonicity condition, and the precise domain of the renormalization operator;
- the definitions and signs of the scale parameters and the exact renormalization formula;
- the complex disk or source domain, analytic and reality conditions, evenness convention,
  restriction to `[-1, 1]`, fixed-point equation, and Schwarzian derivative convention;
- for hyperbolicity, the analytic-function Banach space and norm, second-order vanishing
  condition, Fréchet derivative, scalar field, compactness, spectrum, unit-circle convention,
  invariant splitting, eigenvalue multiplicity, and positivity;
- for the bifurcation clauses, the selected local stable and unstable manifolds, the definition of
  the period-doubling surface, the starred point notation, domain of the iterated operator, iterate
  indexing, quadratic-family notation, parameter interval, neighborhood quantifiers, and the exact
  transversality predicate; and
- whether Propositions 2, Estimates 1 and 2, interval-arithmetic certificates, invariant-manifold
  theory, cone estimates, and kneading arguments are hypotheses, proof obligations, or incorporated
  definitions for the selected root.

These are target-resolution requirements, not an asserted formal statement.

## Boundary and degenerate cases

The statement phase must resolve maps on the boundary of the renormalization domain, non-strict
versions of the monotonicity and domain inequalities, the critical point and endpoints, functions
outside the chosen analytic disk, failure of second-order vanishing, spectrum on the unit circle,
zero or repeated expanding eigenvalues, local-manifold nonuniqueness, empty parameter
neighborhoods, endpoint values of the parameter interval, and the source's deliberately unproved
stronger transversality claim following Theorem 4.

## Explicit exclusions

`THM-M-1437` (Feigenbaum universality) and `THM-M-1439` (Lyubich proof) are distinct targets. A
generic Banach fixed-point theorem, compact-operator spectral theorem, interval-arithmetic example,
logistic-map simulation, numerical Feigenbaum-constant approximation, finite period-doubling
experiment, or plot is not a substitute for a selected Lanford source theorem. Nor may the desired
fixed point, hyperbolicity, invariant manifolds, spectral gap, crossing, or certificate validity be
assumed as a structure field or hypothesis and then projected as proof closure.

The paper explicitly says the stronger transversal crossing discussed immediately after Theorem 4
was not proved. It cannot be promoted into the target. The later analytic proof associated with
Lyubich cannot replace Lanford's computer-assisted source boundary.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib supplies general analytic-function,
fixed-point, continuous-linear-map, compact-operator, and spectrum APIs, but the bounded intake
search found no Lanford, Feigenbaum, period-doubling-renormalization, or matching unimodal-map
theorem. The API probe is substrate discovery only, not a complete anchor audit, formalization of
the source definitions, checked transport, numerical certificate, or proof.
