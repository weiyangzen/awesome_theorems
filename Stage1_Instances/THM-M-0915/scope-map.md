# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0915`, the title "generating functions," the gloss "the
generating-function method for combinatorial sequences," a collective eighteenth-century
attribution, high importance, and an untrusted verified label. Intake preserves only that broad
method/topic boundary. It does not infer a single theorem from customary textbook material.

## Proposition-changing decisions

An accountable source correction must select one exact truth-valued result and freeze:

- the generating-function kind: ordinary, exponential, multivariate, Dirichlet, probability,
  cycle-index, or another source-defined construction;
- the coefficient carrier and algebraic structure, including whether coefficients are natural,
  integer, rational, real, complex, or values in a semiring, ring, module, or completed algebra;
- the indexed sequence, combinatorial class, weight function, recurrence, or operation whose
  behavior is asserted;
- formal-series semantics versus evaluation as an analytic function, including topology, radius
  or domain of convergence, rearrangement conditions, and equality notion;
- the exact result: coefficient recovery, equality/extensionality, addition, Cauchy product,
  composition, differentiation, recurrence solution, a combinatorial construction rule, the
  exponential formula, coefficient extraction, or an asymptotic conclusion;
- every ordered binder, hypothesis, side condition, universe, typeclass, and conclusion clause;
  and
- all alternate encodings and the checked equality, equivalence, or implication connecting them.

These decisions yield inequivalent propositions. They are a resolution ledger, not a canonical
statement.

## Candidate families not credited

- `PowerSeries.coeff_mk`: a sequence can be packaged as a formal power series and recovered
  coefficientwise. This is definition-level infrastructure, not the unspecified method.
- `PowerSeries.coeff_mul`: multiplication of formal power series gives Cauchy convolution. A
  combinatorial interpretation additionally requires a class construction and checked counting
  bridge.
- A theorem translating a specified linear recurrence and initial conditions into a rational
  ordinary generating function, and a converse coefficient result.
- The labeled exponential formula for a fully specified combinatorial species or class.
- A partition, Catalan, Fibonacci, Bell, or Stirling generating-function identity.
- Analytic coefficient extraction or an asymptotic theorem under convergence and singularity
  hypotheses.

No candidate in this list is selected or credited at intake.

## Boundary cases

Source review must resolve the empty sequence or class, zero and singleton indices, finite versus
infinite support, zero divisors and noncommutative coefficients, missing or negative indices,
initial-condition range, empty sums and products, formal composition at nonzero constant term,
division by a nonunit, equality on coefficients versus equality on a convergence domain, boundary
points of convergence, and justified interchange of infinite sums, products, derivatives, or
limits. No case is excluded before a proposition is selected.

## Neighbor and substitution exclusions

`THM-M-0916` separately owns Euler's pentagonal-number theorem and its integer-partition
generating-function identity. `THM-M-0917` separately owns the partition function, while
`THM-M-0921`, `THM-M-0922`, `THM-M-0923`, and `THM-M-0925` own Catalan, Stirling, Bell, and
Fibonacci topics. Their statements, sources, and proof credit cannot identify this root.

Probability moment-generating functions, Hamilton-Jacobi generating functions, and functions that
generate pseudorandom or algorithmic output are outside this counting-combinatorics method label.
A structure or hypothesis storing the desired identity, a finite coefficient experiment, or the
catalog's untrusted verified label cannot replace a theorem proof.

## Formal boundary

No canonical Lean target or minimal import set is frozen. At the pinned revision,
`Mathlib.RingTheory.PowerSeries.Basic` defines `PowerSeries`, `PowerSeries.mk`,
`PowerSeries.coeff`, coefficient extensionality, recovery by `PowerSeries.coeff_mk`, and product
coefficients by `PowerSeries.coeff_mul`. Partition and Catalan modules contain specialized
generating functions owned by narrower topics. `IntakeProbe.lean` elaborates only the generic
adjacent API and provides no statement or proof credit.
