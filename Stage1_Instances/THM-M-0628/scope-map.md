# Scope map

## Received scope

The repository fixes only the title "local compactness theorem" and the phrase "properties of
locally compact spaces." Stage0 explicitly leaves the precise definitions and premises, proof
route, equivalent formulations, axioms, machine status, and artifact links open. This supports a
point-set topology topic boundary, but no ordered binders, hypotheses, or conclusion.

## Proposition families not selected

An admitted source might select one of the following, but intake credits none as the root:

- a definition or characterization by compact neighborhoods of each point;
- a basis of compact or compact-closed neighborhoods;
- existence of an open neighborhood with compact closure;
- compact-neighborhood results for compact subsets inside open subsets;
- inheritance by products, finite function spaces, open, closed, or locally closed subspaces, or
  suitable quotients and embeddings;
- regularity, Baire, compact-open evaluation, or other consequences of local compactness;
- a relationship between weak local compactness and the stronger neighborhood-refinement notion;
- a compactification theorem.

These are not interchangeable. Some are definitions, some require R1 or Hausdorff separation,
some are preservation theorems, and some introduce substantial new constructions.

## Decisions required at statement freeze

1. Select an immutable primary or authoritative source and one exact theorem/page/formula, including
   all incorporated definitions, proof boundary, translation, corrections, and errata.
2. Fix the local compactness convention: existence of some compact neighborhood, refinement of
   every neighborhood by a compact neighborhood, relatively compact open neighborhoods, or an
   explicitly transported equivalent form.
3. Fix separation assumptions independently: none, T0, T1, R1, regular, Hausdorff, or locally
   Hausdorff. These assumptions change equivalences outside the Hausdorff setting.
4. Fix the ambient type, topology, universe levels, subspace or product types, and all typeclass
   assumptions.
5. Fix the exact result, ordered binders, quantifiers, explicit and implicit hypotheses, and one
   conclusion rather than the open-ended word "properties."
6. Fix whether compact sets must be closed and whether "neighborhood" means a set in `nhds x`, an
   open set containing `x`, a closed neighborhood, or a set whose closure is compact.
7. Decide empty and singleton spaces, non-Hausdorff examples, compact spaces, discrete spaces,
   empty or universal neighborhoods, empty products, finite versus infinite products, and empty
   compact subsets.
8. Record checked directions for every credited alternate encoding and mutation-test removed
   assumptions, changed domains, binder scope, and boundary cases.

## Explicit exclusions

- Do not select mathlib's `LocallyCompactSpace.local_compact_nhds`, `exists_compact_subset`, or
  `exists_compact_between` merely because a convenient pinned declaration exists.
- Do not replace the root with `WeaklyLocallyCompactSpace.locallyCompactSpace`; that declaration
  additionally relies on the enclosing R1 context.
- Do not substitute `THM-M-0629` (Alexandroff one-point compactification) or inherit any evidence
  from that separate target.
- Do not use a product, open-subspace, closed-subspace, quotient, Baire, or compact-open theorem as
  the unspecified generic "properties" root.
- Do not encode the missing result as an opaque predicate, axiom, assumed certificate, structure
  field, or hypothesis from which the desired conclusion is projected.
- Do not treat the catalog label `已验证`, an API name, a successful probe, or an unrelated build as
  source or theorem evidence.

## Lean boundary

Pinned mathlib distinguishes `WeaklyLocallyCompactSpace` (some compact neighborhood at each point)
from `LocallyCompactSpace` (compact refinement inside every neighborhood), explicitly noting that
literature conventions agree for Hausdorff spaces but not in general. Under R1 assumptions it
provides a bridge from weak to strong local compactness and compact-closed neighborhood bases.
These are adjacent APIs only. Minimal imports, a canonical expression, expression and environment
fingerprints, transports, mutation fixtures, and proof-body provenance remain downstream.

## Retry condition

The integration lane must admit one stable proposition and an immutable source, then obtain an
independent review of its exact definitions, binders, assumptions, conclusion, proof boundary,
translation, corrections, and relation to the catalog phrase. Only then may the statement phase
elaborate an exact target and test its identity.
