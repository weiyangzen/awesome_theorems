# THM-M-0971 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry `Shearer bound`.
The repository supplies only the gloss `optimal condition for the Lovasz Local Lemma`, attributes
it to James Shearer in 1985, and labels it verified. Under rev-5.6 that label is untrusted inventory
metadata, not a source audit, an exact Lean proposition, or proof evidence.

The matching primary-source lead is J. B. Shearer's 1985 paper *On a problem of spencer*. Its
publisher abstract studies events with a dependency graph, proves the sharp symmetric
maximum-degree threshold, and says that it also gives a sharp lower bound for the probability that
no event occurs. Later literature uses "Shearer's condition" for related independent-set-polynomial
criteria and optimality statements. The catalog does not select the symmetric threshold, the
general probability bound, a positivity criterion, or its converse/tightness direction.

That choice is proposition-changing. So are the dependency convention, graph and index model,
event measurability and probability codomain, polynomial normalization and signs, strict versus
nonstrict inequalities, treatment of zero coordinates, and boundary cases. Intake records these
choices instead of silently supplying them from memory or a later generalization.

Pinned mathlib provides measurable-event independence, finite intersections, finite simple graphs,
independent sets, neighbor finsets, and maximum degree. `IntakeProbe.lean` authenticates those
interfaces. A bounded exact-topic search found no Shearer/LLL/independence-polynomial target in
pinned mathlib or repository-local Lean. These are discovery facts and substrate checks only.

The provisional vector is `[H1, M4, R4]`: a matching primary-source lead is known, but the exact
source root, definitions, assumptions, proof boundary, corrections, and independent review remain
open; no usable exact formal artifact is credited; and no source-faithful proof reconstruction can
attach to an unfrozen root. All six downstream phases remain open. No H0, M0, R0, accepted state,
audit completion, theorem completion, or master acceptance is claimed.
