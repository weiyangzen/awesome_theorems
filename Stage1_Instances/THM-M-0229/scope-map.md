# Scope map

## Preserved theorem family

The intake preserves the local Great Picard family named by the catalog: a complex-valued
holomorphic function with an isolated essential singularity assumes all finite complex values with
at most one possible exception in arbitrarily small punctured neighborhoods. This is a scope
description, not a frozen proposition. In particular, it does not yet decide whether the usual
"infinitely often" conclusion belongs to the root or is a derived corollary.

## Decisions required at statement freeze

1. Preserve an immutable primary or authoritative source edition, exact proposition and
   incorporated definitions, proof boundary, correction history, and independent review.
2. Fix the function model: an ambient `Complex -> Complex` function, a function on a punctured
   domain, or another source-faithful partial-function encoding.
3. Bind the singular point and an open domain or explicit radius, and state exactly where the
   function is analytic or differentiable.
4. Define "isolated essential singularity" rather than identifying it merely as "not removable"
   or "not a pole." The definition must exclude regular, removable, and pole cases and must make
   the punctured-domain condition explicit.
5. Decide whether the conclusion quantifies over every neighborhood, every positive radius inside
   a fixed domain, or a filter basis at `Filter.nhdsWithin a {a}^c`.
6. Decide whether values range over finite `Complex` or the Riemann sphere. The finite-value
   analytic theorem allows at most one exception; the meromorphic sphere-valued variant has a
   different exception bound and is not interchangeable.
7. Freeze the exceptional-value quantifiers. One global exceptional value must not be weakened to
   a different exception for each neighborhood unless an accepted source and checked equivalence
   justify that formulation.
8. Decide whether every nonexceptional value is merely attained in every punctured neighborhood or
   is asserted to be attained infinitely often, with exact multiplicity and sequence/filter
   conventions.
9. Resolve all ordered binders, hypotheses, conclusion clauses, universes, foundation and TCB
   profiles, and every alternate encoding through checked transports.

## Boundary cases

Source review must address the value assigned to the ambient function at the singular point; empty
or trivial punctured domains; regular and removable points; poles; constant functions on the
punctured component; a function with one omitted value such as an exponential-type example; zeros
or preimages accumulating only at the singular point; counting distinct preimages versus
multiplicity; and whether the singularity is finite or at infinity.

## Excluded substitutions

- Picard's Little Theorem (`THM-M-0228`) is a related global entire-function theorem, not this local
  essential-singularity root. Neighbor status or proof credit does not transfer.
- Casorati-Weierstrass density near an essential singularity is weaker than omission of at most one
  value and cannot replace Great Picard.
- The removable-singularity theorem, classification of poles by meromorphic order, open mapping,
  maximum modulus, Liouville, and first main theorem of value distribution are substrate or
  possible dependencies, not the target.
- A theorem only for `exp (1 / (z - a))`, another example, a fixed punctured disk, or a finite set
  of queried values is not the universal theorem.
- A definition or structure field that assumes the desired value-distribution conclusion supplies
  no proof.
- Numerical sampling, a theorem name, an API `#check`, or the untrusted catalog label supplies no
  H or M credit.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery probe checks punctured-neighborhood,
analytic, removable-singularity, meromorphic-order, and cluster-point interfaces. A bounded local
name search found no Great Picard or essential-singularity declaration in pinned mathlib or the
repo-local Lean sources. This is intake discovery only, not an exhaustive anchor audit or a proof
of global absence.
