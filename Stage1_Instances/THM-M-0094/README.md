# THM-M-0094 rev-5.6 intake dossier

This directory is the fail-closed `planned` intake for `THM-M-0094`, the catalog item
`博雷尔-韦伊-博特定理` (Borel-Weil-Bott theorem). The repository supplies only the gloss:

> Geometric realization of representations of compact Lie groups.

The title selects the full higher-cohomology Borel-Weil-Bott family; the degree-zero Borel-Weil
realization is only a special case, not an admissible substitute. The gloss still does not fix the
group or flag variety, the homogeneous line bundle and weight convention, regular/singular cases,
Weyl dot action, unique cohomological degree, or the precise representation returned. The exact
mathematical and Lean statements therefore remain unset instead of being reconstructed from memory.

Crossref metadata authenticates Raoul Bott's 1957 paper *Homogeneous Vector Bundles* as a strong
historical source lead. The DOI resolves to an access-controlled page in this environment, so no
exact theorem passage, assumption map, correction audit, or independent review is credited. The
catalog's Borel/Weil attribution and 1954 date require separate source reconciliation.

Pinned mathlib contains adjacent global-section, abstract sheaf-cohomology, scheme-module,
Lie-weight, root-system, irreducible-representation, and Lie-group interfaces. A bounded search and
`IntakeProbe.lean` found no Borel-Weil-Bott declaration, flag-variety construction, homogeneous
line-bundle bridge, or theorem connecting such cohomology to an irreducible representation. These
are generic ingredients only, so the machine axis remains `M4`.

The structured scope authority is `instance.json`; proposition-changing decisions are in
`scope-map.md`; the source and formal mapping is in `source-statement-crosswalk.md`; and all six
downstream items remain open in `task-dag.json`.

Status boundary: provisional, self-tested planned intake only, with vector `[H1, M4, R4]`. No exact
source proposition, canonical Lean target, accepted proof state, audit completion, theorem
completion, or master acceptance is claimed.
