# Scope map

## Received scope

The repository record fixes only these facts: the title `配边理论`, the gloss "classification of
manifolds by bordism," attribution to Rene Thom, and the year 1954. It does not supply a theorem
number, page, category, orientation convention, dimension, invariant, or formal expression.

## Candidate mathematical scope

Any eventual exact target must explicitly select and encode:

- closed smooth manifolds in a common finite dimension;
- the relevant bordism relation, including boundary identifications and orientation data;
- either unoriented bordism with Stiefel-Whitney-number invariants, or oriented bordism with the
  appropriate Stiefel-Whitney and Pontryagin-number invariants;
- equality of two bordism classes or the corresponding null-bordism criterion;
- every coefficient, partition, degree, sign, and integrality convention needed to make the
  characteristic numbers well typed.

The Pontryagin-Thom construction is a second plausible reading: a bordism group is identified with
a stable homotopy group of a Thom space or spectrum. It remains in discovery scope, but cannot be
substituted for a characteristic-number criterion without a checked source-to-statement map.

## Boundaries

The following are not silently included:

- the ring presentation or multiplicative structure of bordism groups, owned separately by
  `THM-M-0604`;
- the h-cobordism or s-cobordism theorem;
- manifolds with boundary as classified objects, noncompact manifolds, singular bordism, or
  generalized homology theories beyond what the selected theorem requires;
- oriented, complex, framed, spin, or unoriented variants exchanged for one another;
- a mere definition that two manifolds are bordant, or the easy direction that characteristic
  numbers are bordism invariants, in place of a complete classification theorem.

## Formal boundary

There is no canonical Lean expression at intake. A generic quotient, an uninterpreted `Bordant`
predicate, or a proposition asserting its own classification would broaden or assume the result.
The dependent statement phase must choose concrete pinned manifold, boundary, orientation,
cohomology, characteristic-class, and characteristic-number interfaces; elaborate the precise
root; record its normalized expression and environment; and mutation-test category, orientation,
dimension, binders, hypotheses, and boundary cases.
