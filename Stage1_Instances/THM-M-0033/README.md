# THM-M-0033 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalogue entry named Serre's
conjecture. The repository supplies the gloss "projective modules over polynomial rings are free,"
attributes it to Jean-Pierre Serre in 1955, and labels it verified. Under rev-5.6 that label is
untrusted metadata, not an exact proposition, a human-source audit, or a machine-proof receipt.

The gloss identifies the classical problem solved by the Quillen-Suslin theorem, but it omits the
coefficient-ring class, the number and indexing of indeterminates, finite-generation assumptions,
module and universe conventions, the precise meaning of freeness, and boundary cases. Intake does
not silently fill those clauses from a familiar modern formulation. The adjacent catalogue target
`THM-M-0034` is also kept distinct; its label and status cannot supply evidence for this target.

Pinned mathlib has definitions and APIs for projective modules, free modules, polynomial rings, and
multivariate polynomial rings. The discovery probe confirms those interfaces. The bounded search
found no Quillen-Suslin or Serre-conjecture declaration, and `Module.Projective.of_free` proves the
reverse implication (free implies projective), not the requested result. These facts are substrate,
not a formal candidate for the root.

The provisional root vector is `[H1, M4, R4]`. A classical theorem family and credible primary and
solution publication leads are known, but no exact primary passage or assumption crosswalk is
accepted; no usable exact formal artifact was found; and no source-faithful proof reconstruction
exists.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` freeze the admissible family and non-substitution boundary.
`task-dag.json` keeps all six downstream phases open. Exact scoped checks are recorded in
`validation.md`. No H0, M0, R0, accepted execution state, audit completion, theorem completion, or
master acceptance is claimed.
