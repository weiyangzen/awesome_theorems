# Scope map

## Preserved theorem family

The intake preserves the classical point-set topology family named by the catalog: two disjoint
closed subsets of a normal space admit separation by a continuous function taking endpoint values
zero and one. This is a family boundary, not an accepted exact proposition. The repository's
literal phrase, "separation of closed sets in a normal space," does not say whether separation means
disjoint open neighborhoods or a continuous `[0, 1]`-valued separator.

## Decisions required at statement freeze

1. Admit an immutable primary or authoritative source edition, exact theorem and incorporated
   definition locators, proof boundary, translation, correction or errata record, and independent
   source review.
2. Decide whether the intended root is Urysohn's continuous-function lemma or merely the
   open-neighborhood separation property. The latter is a normality definition in pinned mathlib
   and cannot silently replace the named lemma.
3. Fix the normality convention. Mathlib's `NormalSpace` requires separation of disjoint closed
   sets but no `T1Space`; some sources call only a normal T1 space normal. Any T1, Hausdorff,
   regularity, or nonempty assumption must come from the accepted source.
4. Fix the ambient universe, type `X`, topology, ordered binders for the two subsets, closedness and
   disjointness premises, and whether subsets or closed-set subtypes are quantified.
5. Fix the separator: an ordinary continuous function, `ContinuousMap`, bounded continuous map, or
   map to a unit-interval subtype; its codomain; range constraint; and exact endpoint orientation.
6. Decide whether the conclusion is pointwise equality (`EqOn`), inverse-image containment, exact
   fibers, or another encoding. Every credited alternate form needs a checked transport.
7. Resolve empty `X`, empty `s` or `t`, both sets empty, singleton sets, and the impossible
   nonempty-overlap case. Do not silently impose nonemptiness or exclude vacuous instances.
8. Mutation-test removal of closedness, disjointness, or normality; change of normality convention
   or codomain; binder-scope changes; and the recorded boundary cases.

## Candidate pinned encoding, not selected

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the direct candidate is:

```text
exists_continuous_zero_one_of_isClosed [NormalSpace X]
  {s t : Set X} (hs : IsClosed s) (ht : IsClosed t) (hd : Disjoint s t) :
  exists f : C(X, Real),
    EqOn f 0 s and EqOn f 1 t and forall x, f x in Set.Icc 0 1
```

The interface has an arbitrary universe for `X`, an explicit `TopologicalSpace X`, no T1,
Hausdorff, regularity, or nonempty premise, and orientation zero on `s`, one on `t`. These are
candidate facts authenticated by the intake probe, not choices attributed to the uncited catalog
gloss.

## Explicit exclusions

- Do not substitute `NormalSpace.normal`, `normal_separation`, or
  `normal_exists_closure_subset` for the continuous-function lemma merely because the catalog uses
  the word "separation."
- Do not substitute the regular locally compact variants with a compact first set, the bounded-map
  wrapper, or an arbitrary-endpoint generalization without an approved relationship.
- Do not substitute `THM-M-0622` (Tietze extension) or `THM-M-0623` (Urysohn metrization), even
  though their proof routes may use Urysohn's lemma.
- Do not confuse an Urysohn separation axiom for pairs of points with this closed-set lemma.
- Do not encode the missing proposition as an axiom, opaque predicate, assumed certificate,
  structure field, or hypothesis containing the desired separator.
- Do not treat the catalog's untrusted status, a theorem name, `#check`, or a successful probe as
  source identity or proof credit.

## Intake boundary

The planned intake freezes the ambiguity, direct pinned candidate, neighbor and substitution
boundaries, ownership, and open workflow. It intentionally leaves the canonical claim, Lean
expression, minimal imports, expression and environment fingerprints, checked transports, and all
statement mutations to the statement node.
