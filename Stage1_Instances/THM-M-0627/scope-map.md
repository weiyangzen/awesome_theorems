# Scope map

## Received scope

The repository fixes only the title "path-connectedness theorem" and the phrase "properties of
path-connected spaces." Stage0 explicitly leaves the precise definitions and premises, proof
route, equivalent formulations, logical dependencies, machine status, and artifact links open.
This supports a point-set-topology topic boundary, but no ordered binders, hypotheses, or
conclusion.

## Proposition families not selected

An admitted source might select one of the following, but intake credits none as the root:

- a definition or characterization: nonemptiness plus a path between every two points;
- the continuous image of a path-connected set or space is path-connected;
- a path-connected set or space is connected;
- a surjective continuous image or quotient of a path-connected space is path-connected;
- equivalence between whole-space, universal-set, and subtype formulations;
- characterization by one path component or by the zeroth homotopy quotient;
- preservation under intersecting unions, products, group operations, or other constructions;
- existence of a path through a finite family of points.

These are not interchangeable. Some merely unfold a definition, some are implication theorems,
some require a map and continuity or surjectivity, and some introduce additional algebraic or
topological structure.

## Decisions required at statement freeze

1. Admit an immutable primary or authoritative source and one exact theorem/page/formula, including
   incorporated definitions, proof boundary, translation, corrections, and errata.
2. Confirm whether `道路连通` means path-connected rather than arc-connected, and decide whether a
   path may self-intersect.
3. Fix the path domain, endpoint convention, and continuity notion, including any transport from a
   source interval to mathlib's unit interval.
4. Choose a space-level or set-relative root and fix the ambient types, topologies, subtype
   topology, and universe levels.
5. Resolve nonemptiness explicitly. Mathlib's `PathConnectedSpace` and `IsPathConnected` exclude
   empty carriers/sets, while a bare pairwise-path formula can be vacuous on the empty case.
6. Select one result and freeze every map, set, point, quantifier, explicit and implicit hypothesis,
   and conclusion.
7. Decide singleton and empty spaces/sets, empty and universal images, constant maps, empty source
   types, non-surjective maps, and non-Hausdorff spaces as applicable to the chosen result.
8. Record checked directions for every credited alternate encoding and mutation-test removed
   hypotheses, changed domains, binder scope, and boundary cases.

## Explicit exclusions

- Do not infer the continuous-image theorem merely because neighboring `THM-M-0626` explicitly
  states the analogous result for connected sets.
- Do not select `IsPathConnected.image`, `IsPathConnected.isConnected`,
  `Function.Surjective.pathConnectedSpace`, or another convenient pinned declaration without
  source authority.
- Do not replace an implication theorem with the definition of path-connectedness, or conversely
  present a definitional characterization as the unspecified family of "properties."
- Do not strengthen path-connectedness to arc-connectedness or local path-connectedness.
- Do not encode the missing result as an opaque predicate, assumed certificate, structure field,
  or hypothesis from which the desired conclusion is projected.
- Do not treat `已验证`, an API name, a successful probe, or an unrelated build as source or theorem
  evidence.

## Lean boundary

Pinned mathlib distinguishes paths between points (`Joined`), paths constrained to a set
(`JoinedIn`), path-connected sets (`IsPathConnected`), and path-connected carriers
(`PathConnectedSpace`). It also contains separate theorems for images, surjective images,
connectedness, subtype/universal-set transports, components, and other constructions. These are
adjacent APIs only. Minimal imports for an exact root, a canonical expression, expression and
environment fingerprints, checked transports, mutation fixtures, and proof-body provenance remain
downstream.

## Retry condition

The integration lane must admit one stable proposition and an immutable source, then obtain an
independent review of its exact terminology, binders, assumptions, conclusion, proof boundary,
translation, corrections, and relationship to the catalog phrase. Only then may the statement
phase elaborate an exact target and test its identity.
