# Scope map

## Included topic boundary

- One source-specified forcing axiom or axiom schema in an explicit base set theory.
- Its specified class of forcing notions, order orientation, and any structural predicate such as
  ccc, properness, or preservation of stationary subsets.
- Its exact bound on a family of dense subsets.
- A filter or directed subset meeting every dense set in that family.
- Alternatively, one source-named application or relative-consistency theorem, with all axiom and
  large-cardinal hypotheses explicit, if that is what the source identifies as the target.

## Ambiguities to resolve at statement freeze

The repository phrase is compatible with materially different targets:

1. Martin's Axiom for ccc partial orders, possibly parameterized by a cardinal.
2. The Proper Forcing Axiom, with properness and an `aleph_1`-sized dense family.
3. Martin's Maximum or bounded variants, with different forcing classes or conclusion scope.
4. A metatheorem about relative consistency or consistency strength.
5. A particular application proved conditionally from one forcing axiom.

Even after choosing a family, the statement must freeze the ambient set theory, internal versus
external set coding, order orientation, definition of dense and filter, universe levels, exact
cardinal bound, forcing-class predicate, and whether the claim is an asserted axiom, a conditional
implication, or a model/consistency result.

## Explicit exclusions

- Martin's Axiom, PFA, Martin's Maximum, and bounded forcing axioms as substitutes for one another.
- The forcing theorem, proper forcing, iterated forcing, or preservation results as substitutes.
- Assuming a field named for the desired axiom and projecting it as a purported proof of the axiom.
- Choosing an easy consequence merely because the source says "applications".
- A conjunction of arbitrarily selected forcing axioms or applications.
- Calling an additional axiom an unconditional theorem of ZFC.
- Treating the repository label `已验证` as human-proof or kernel evidence.

No canonical Lean target is frozen at intake because the source record does not identify one.
