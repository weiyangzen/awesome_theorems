# THM-M-0865 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Kuratowski's theorem. The repository
catalog supplies Kazimierz Kuratowski, the year 1930, and only the gloss `平面图的禁用子图刻画`
("characterization of planar graphs by forbidden subgraphs"). Its `已验证` value is untrusted
metadata, not a source-fidelity, Lean, or completion receipt.

## Frozen family and boundary

The conventional theorem family says that a graph is planar exactly when it contains no
subdivision, equivalently no topological-minor model, of `K5` or `K3,3`. A modern authoritative
source lead, Diestel's *Graph Theory*, 6th edition, states this as part of Theorem 4.4.6. That theorem
also gives the ordinary-minor characterization and attributes it jointly to Kuratowski and Wagner.
Because the catalog says only "forbidden subgraphs" and the neighboring `THM-M-0866` separately
owns Wagner's forbidden-minor theorem, this intake does not silently choose the ordinary-minor
form, merge both targets, or freeze one binder-complete proposition.

The catalog does not define graph finiteness, simplicity, planarity or plane embedding, subdivision,
topological-minor containment, `K5`, `K3,3`, or boundary cases. The exact 1930 article is identified
by DOI and pages, but its mathematical text and historical vocabulary were not admitted and
independently reviewed. These proposition-changing choices remain the first statement blocker.

## Lean boundary

Pinned mathlib supplies `SimpleGraph`, graph isomorphisms, subgraph-copy containment,
`completeGraph`, and `completeBipartiteGraph`. A bounded search located no graph-planarity,
subdivision, topological-minor, ordinary-minor, or Kuratowski interface. `IntakeProbe.lean`
authenticates only the adjacent graph vocabulary and a predicate-parameterized shape; it states no
target theorem and earns no proof credit.

The provisional root vector is `[H1, M4, R3]`: an exact modern theorem source lead exists, but the
catalog-to-source selection, historical source boundary, corrections, and independent review are
open; no usable target-specific Lean artifact was located; and no source-faithful proof
reconstruction exists beyond this scope/status dossier. All six downstream phases remain open. No exact Lean statement, H0, M0,
R0, accepted state, audit completion, theorem completion, or master acceptance is claimed.
