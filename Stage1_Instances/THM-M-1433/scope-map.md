# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1433`, the label `Brjuno条件` (`Brjuno condition`),
Alexander Brjuno, the year 1971, and the gloss `Siegel盘的线性化条件` (`a linearization condition
for Siegel disks`). Importance "high" and status `已验证` are catalog metadata, not theorem or
proof evidence. Intake preserves the arithmetic/complex-dynamical subject boundary but does not
turn the label into a theorem from memory.

## Proposition-changing decisions

An approved target correction must select an exact source proposition and freeze:

- whether the root is the arithmetic definition of a Brjuno number, a sufficient linearization
  theorem, a necessity theorem, an equivalence, or a quantitative linearization-radius estimate;
- the arithmetic parameter and its domain, especially `omega : Real`, reduction modulo integers,
  irrationality, the continued-fraction algorithm, indices and initial denominators, logarithm
  convention, and the exact convergent series or equivalent Brjuno function;
- the dynamical object: a local holomorphic germ at zero, a germ univalent on a specified disk, a
  quadratic polynomial, a vector field or differential equation, or a higher-dimensional system;
- the multiplier convention, such as `lambda = exp (2 * pi * I * omega)`, its nonzero/unit-circle
  conditions, and exclusion of roots of unity or resonances;
- the regularity and domain of the map and conjugacy, fixed-point and derivative hypotheses,
  injectivity/univalence, normalization of the conjugacy, and local versus disk-wide equality;
- whether the quantifiers say every germ with the multiplier is linearizable, one selected germ is
  linearizable, or a particular quadratic polynomial has a Siegel disk;
- whether "Siegel disk" means analytic local linearizability, a maximal Fatou component, existence
  of a positive convergence radius, or a global statement about its boundary; and
- rational angles, roots of unity, zero or infinite Brjuno sums, zero-radius conjugacies, linear
  maps, already-linear germs, and all other degenerate cases.

These choices yield inequivalent propositions. They are a resolution ledger, not a statement.

## Candidate families not credited

- The arithmetic definition `sum_n log(q_(n+1)) / q_n < infinity` for denominators of convergents
  of an irrational rotation number, with an exact indexing convention.
- Brjuno's sufficient result that a source-specified holomorphic germ with Brjuno multiplier is
  analytically linearizable near an irrationally indifferent fixed point.
- Yoccoz's universal-germ necessity and sufficiency statement, or its quantitative radius bound.
- The quadratic-polynomial statement that the fixed point of `z |-> z^2 + exp(2*pi*i*omega) z`
  is linearizable exactly for Brjuno `omega`.
- Higher-dimensional, resonant, vector-field, Hamiltonian, or ultradifferentiable Brjuno theorems.

No family in this list is selected or credited at intake.

## Explicit exclusions

`THM-M-1432` (Yoccoz theorem), generic Siegel linearization, the existence of a Siegel disk, and a
continued-fraction convergence lemma are not substitutes. A sufficient implication cannot be
silently strengthened to an equivalence, nor may a theorem about all normalized univalent germs be
replaced by a quadratic-polynomial result. A definition of the arithmetic condition alone cannot
supply the catalog's linearization conclusion.

Also excluded are structures that assume linearizability as a field, tautologies that assume the
desired conjugacy, the identity or a single already-linear map, finite continued-fraction
approximations, numerical orbit plots, truncated Brjuno sums, and unchecked symbolic power series.
The catalog label `已验证` supplies neither human-source nor Lean kernel credit.

## Boundary cases

The selected source must decide rational angles and roots of unity, integer shifts and sign changes
of the rotation number, continued-fraction termination, zero denominators, index-zero terms, the
meaning of divergence to infinity, maps with zero radius or no specified domain, normalization and
uniqueness of the conjugacy, and whether the linear map itself is admitted. Silently resolving any
of these can materially change the proposition.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides generalized and real continued
fractions, analytic-function composition, fixed points, and semiconjugacy APIs. The bounded intake
search found no target-specific Brjuno/Bryuno, Siegel-disk, or analytic-linearization declaration.
These APIs and the name search are discovery inputs only, not an exhaustive anchor audit,
statement elaboration, or proof evidence.
