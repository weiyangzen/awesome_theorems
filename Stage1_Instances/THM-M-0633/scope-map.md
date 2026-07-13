# Scope map

## Preserved catalog scope

The received claim is exactly “a continuous function on a compact set is uniformly continuous.”
The title and wording identify the Heine-Cantor family and favor a compact-subset formulation, but
the catalog is not a binder-complete mathematical source. Intake preserves that family without
silently resolving the missing structures or selecting one of several related encodings.

The likely mathematical components, none yet credited as the canonical proposition, are:

- ambient and codomain spaces carrying uniform structures, and hence induced topologies;
- a subset `s` of the ambient space;
- compactness of `s`;
- a function continuous on `s`; and
- uniform continuity of the same function on `s`.

## Proposition-changing decisions

An approved source and independent review must settle the following before statement execution:

1. Whether the theorem ranges over metric spaces, Hausdorff uniform spaces, or another explicitly
   delimited class, including every separation assumption intended by the source.
2. Whether the compact object is a subset of an ambient space or the entire domain as a compact
   space, and whether a subset formulation uses the subtype or an ambient function restricted to
   the set.
3. Whether continuity is `ContinuousOn f s`, continuity of the subtype restriction, or global
   `Continuous f`, and whether uniform continuity is `UniformContinuousOn f s` or
   `UniformContinuous f`.
4. The ordered universes, types, typeclasses, set and function binders, implicit versus explicit
   arguments, hypotheses, and conclusion.
5. The exact relationship between the compact-subset and compact-domain forms and a checked
   transport for every alternate encoding that receives credit.
6. The selected foundation, classical-choice, trusted-computing-base, and computation policies.

These choices are not mere spelling changes. A compact subset of a noncompact ambient space and a
compact whole domain have related but different binder structures; global continuity is stronger
than continuity on the chosen subset.

## Boundary and mutation cases

Statement review must explicitly resolve the empty compact set, singleton and finite compact sets,
an empty ambient type, constant functions, noncompact subsets, global versus relative continuity,
functions continuous only on the subset, changes to the domain or codomain uniformity, and any
separation assumptions. The empty-set relative conclusion may be vacuous, but intake does not
silently exclude it. Later statement mutations must test removed compactness, changed domains,
binder scope, and relevant boundary cases as required by the rev-5.6 statement gate.

## Explicit non-substitutions

- Do not replace the compact-subset wording with the whole-domain theorem merely because the latter
  has a short pinned declaration; any relationship must be selected and checked explicitly.
- Do not replace uniform continuity with continuity, Lipschitz continuity, Holder continuity,
  equicontinuity, convergence, or a metric epsilon-delta special case without source authority.
- Do not strengthen `ContinuousOn f s` to global `Continuous f` or change the compactness hypothesis
  to closedness, boundedness, completeness, total boundedness, or local compactness.
- Do not use the stronger `IsCompact.uniformContinuousAt_of_continuousAt` result as the root; it
  controls points near the compact set and has a different conclusion.
- Do not treat a theorem name, module documentation, the catalog label `已验证`, or a successful API
  probe as source identity or theorem completion evidence.
- Do not encode the result as an axiom, opaque premise, structure field, certificate, or hypothesis
  that already contains the desired uniform-continuity conclusion.

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Topology.UniformSpace.HeineCantor` explicitly presents the Heine-Cantor theorem and exposes
both `IsCompact.uniformContinuousOn_of_continuous` and
`CompactSpace.uniformContinuous_of_continuous`. The discovery-only probe checks these declarations
and adjacent predicates. They are direct exact-topic candidates, not a frozen source transport or
an anchor-audit receipt. Minimal import confirmation, canonical expression elaboration, expression
and environment fingerprints, checked transports, mutations, proof-body provenance, and trust
closure remain downstream.
