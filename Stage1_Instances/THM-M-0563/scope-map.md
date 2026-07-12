# Scope map

## Frozen repository scope

- Historical label: Thom cobordism theory, attributed to Rene Thom, 1954.
- Literal claim: classification of manifolds by cobordism.
- Mathematical domain: smooth compact manifolds and a cobordism equivalence relation.
- Intended result kind: a classification or complete-invariant theorem, not merely the definition
  that cobordism is an equivalence relation.

This is the most exact scope supported by the repository source. It is deliberately not promoted
to a canonical mathematical statement because several materially different Thom theorems match it.

## Candidate branches requiring source selection

1. The unoriented criterion for closed smooth manifolds in terms of Stiefel-Whitney numbers.
2. An oriented cobordism criterion involving the source-specified characteristic numbers.
3. The Pontryagin-Thom identification of cobordism classes/groups with homotopy groups of Thom
   spaces or spectra.
4. A structure theorem or computation for an unoriented or oriented cobordism ring.

These branches are alternatives, not equivalent encodings granted at intake. The statement phase
must select exactly one primary theorem or reject the metadata label as too broad.

## Decisions required at statement freeze

Freeze the manifold category (`smooth`, rather than topological or PL); closedness, compactness,
and boundary conventions; fixed dimension versus a graded family; unoriented versus oriented (or
another tangential structure); whether cobordisms and boundary identifications preserve that
structure; connectedness; empty manifolds; disjoint union and Cartesian-product conventions; the
coefficient rings and evaluation pairing for characteristic numbers; and whether the conclusion
is equality of classes, existence of a cobordism, a group/ring isomorphism, or a stable-homotopy
equivalence. Universes, binder order, quotient/setoid representation, and all degenerate dimensions
must follow the selected source.

## Explicit exclusions

- The Thom isomorphism for a vector bundle (the adjacent but distinct `THM-M-0562`).
- A theorem about characteristic classes alone, or equality of Euler characteristics.
- H-cobordism, the cobordism hypothesis, or classification up to diffeomorphism/homeomorphism.
- A one-way statement that characteristic numbers are cobordism invariants when the selected claim
  requires their completeness.
- An abstract structure that assumes the desired classifier or equivalence as a field.
- The repository label `已验证` as human-source or kernel evidence.

A later Lean target must expose concrete manifold, boundary/cobordism, orientation or tangential
structure, characteristic-class/evaluation, and quotient or stable-homotopy interfaces. Missing
library infrastructure must be recorded as a blocker rather than hidden behind assumptions.
