# Scope map

## Preserved repository scope

The catalog fixes only the title `Solymosi定理`, author József Solymosi, year 2009, and the gloss
`和集与积集的下界改进`. This identifies a published sum-product result family, not a binder-complete
theorem. Intake preserves only this boundary: a quantitative lower-bound improvement involving
the sumset and product set of a finite set.

## Candidate source family, not credited as the target

The strongest bibliographic match is József Solymosi, *Bounding multiplicative energy by the
sumset*, *Advances in Mathematics* 222(2) (2009), 402-408, DOI
`10.1016/j.aim.2009.04.006`. The inspected immutable arXiv source is `0806.1040v3`.

That paper contains several materially different candidates:

- Theorem 2.1: an asymmetric inequality for a finite set of positive real numbers, relating
  `|AA|`, `|A + A|`, `|A|`, and a logarithmic denominator.
- Corollary 2.2: a derived lower bound for `max |A + A| |AA|` with exponent `4/3` and a logarithmic
  loss.
- the asymmetric two-set inequality following Lemma 2.3;
- Theorem 3.1: a conditional lower bound for higher-fold sumsets when the product set is small.

The title, author, year, topic, and word "improved" make Theorem 2.1 or Corollary 2.2 plausible,
but the catalog does not select either. They are not interchangeable: the asymmetric theorem is
strictly more informative than its maximum corollary, and neither is the later higher-sumset result.

## Proposition-changing decisions

An approved statement run must independently select and freeze all of the following:

- exact source edition, numbered theorem or corollary, incorporated definitions, and errata;
- positive reals versus arbitrary reals or integers, and `Finset` versus finite `Set` semantics;
- whether positivity means every element is strictly positive and whether distinctness is set-like;
- pointwise sumset and product-set conventions and the cardinality codomain;
- the exact inequality direction, coefficient `4` or `2`, exponent, powers, maximum, and coercions;
- the base and formal interpretation of `log`, the ceiling convention, and real/natural powers;
- ordered binders and quantifier scope, including whether a sufficiently-large condition is intended;
- empty, singleton, and other small-cardinality cases where the printed logarithmic denominator can
  vanish, plus zero and negative elements if the domain is changed;
- whether Theorem 2.1 and Corollary 2.2 are alternate encodings related only by checked implication.

The arXiv source uses dyadic classes but does not explicitly declare the logarithm base in the
inspected text. More importantly, the printed denominator vanishes at a singleton under the usual
logarithm conventions; after clearing that denominator, the singleton claim becomes false.
Reviewers must decide between a corrected `1 < |A|` theorem and literal-source classification as
defective. These issues must not be silently repaired in Lean.

## Explicit exclusions

- Theorem 2.1 substituted for Corollary 2.2, or the reverse, without an approved canonical root and
  a checked relationship.
- The asymmetric two-set extension or Theorem 3.1 substituted for the basic sum-product result.
- Elekes's earlier bound, Bourgain's sum-product results, or the Erdős-Szemerédi conjecture.
- A version over arbitrary reals obtained by deleting positivity without source and proof support.
- An asymptotic `|A|^(4/3-epsilon)` slogan used instead of the paper's explicit logarithmic bound.
- A weakened tautology, a finite computation, or a hypothesis assuming the desired inequality.
- Pinned mathlib energy/cardinality APIs presented as Solymosi's upper-energy estimate or root proof.
- The untrusted catalog label `已验证` presented as human, kernel, or release evidence.
