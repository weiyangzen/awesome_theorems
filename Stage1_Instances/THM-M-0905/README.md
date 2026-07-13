# THM-M-0905 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named Galvin's
theorem. The repository supplies Fred Galvin, the year 1995, and only the gloss `Dinitz猜想的证明`
("proof of the Dinitz conjecture"). Under rev-5.6 the adjacent `已验证` label is untrusted inventory
metadata, not a source audit, an exact proposition, a Lean declaration, or proof evidence.

The metadata identifies the standard result family associated with Fred Galvin's 1995 paper *The
List Chromatic Index of a Bipartite Multigraph*. Crossref confirms that title and bibliographic
record. A familiar candidate theorem says that every `k`-edge-colorable bipartite multigraph is
`k`-edge-choosable, which is stronger than the complete-bipartite special case used to solve the
Dinitz array problem. The primary article text was not accessible for statement-level inspection,
however, and the catalog does not say whether this target owns the stronger graph theorem, the
Dinitz corollary, the proof method, or a conjunction. Intake therefore does not promote the
familiar slogan into a canonical root.

Material choices remain open: the multigraph and parallel-edge model; whether loops are excluded;
finiteness hypotheses; the meaning of `k`-edge-colorable; exact versus lower-bound list size;
finite-set, multiset, or duplicate-bearing list semantics; proper edge coloring; the palette and
color carrier; `k = 0`; empty and edgeless graphs; and the checked transport to `K_(n,n)` arrays.
These choices must come from an admitted immutable source and independent review.

`IntakeProbe.lean` authenticates only adjacent pinned mathlib interfaces for ordinary simple-graph
coloring, bipartiteness, edge labelings, and line graphs. A bounded search found no Dinitz, Galvin,
list-coloring, edge-choosability, or list-chromatic declaration. Simple graphs also erase parallel-
edge identity, so this substrate cannot silently encode the candidate multigraph theorem. The probe
and search are intake feasibility observations, not an anchor audit or proof.

The provisional vector is `[H1, M4, R4]`: an exact published-paper bibliographic lead and standard
result family are known, but the primary statement, incorporated definitions, assumptions, proof
boundary, errata, catalog-to-source mapping, and independent review remain open; no usable exact
formal artifact is located; and no source-faithful proof reconstruction exists. All six downstream
phases remain open. No H0, M0, R0, accepted state, audit completion, theorem completion, or master
acceptance is claimed.
