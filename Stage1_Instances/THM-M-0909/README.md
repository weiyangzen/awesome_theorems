# THM-M-0909 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0909`, the repository label
`Voigt定理` (Voigt theorem). The catalog supplies Margit Voigt, the year 1993, and only the gloss
`非4-可选的平面图`, literally "a planar graph that is not 4-choosable." Its `已验证`
status is untrusted inventory metadata, not a source audit or machine-proof receipt.

The primary bibliographic lead is Margit Voigt, *List colourings of planar graphs*, *Discrete
Mathematics* 120 (1993), 215-219. A zbMATH review identifies the result more precisely: Voigt
presents a planar graph on 238 vertices that is not 4-choosable. The review defines `k`-choosability
using proper colorings for every assignment of lists with at least `k` available colors at each
vertex. This fixes the theorem family, but the primary article text, construction, exact statement
locator, definition chain, proof boundary, corrections, errata, and independent admission review
were not inspected. The 2006 publication with the same title is recorded by zbMATH as a reprint and
is not silently substituted for the 1993 source.

The canonical statement remains null at intake. A source decision must still freeze finite simple
graph conventions, graph planarity or embedding data, list representation and palette, exact versus
lower-bound list cardinality, the meaning of proper list coloring, whether the 238-vertex witness is
part of the target, and the exact existential and negated-universal binder order.

`IntakeProbe.lean` checks only pinned ordinary graph-coloring interfaces. Pinned mathlib has no
located list-coloring, choosability, or graph-planarity API; its coloring module explicitly lists
planar graphs as future work. The probe is therefore substrate evidence only, not a statement,
anchor audit, construction, or proof.

The provisional root vector is `[H1, M4, R4]`: a published result and a precise secondary review are
known, but source fidelity and the primary proof boundary are not accepted; no usable source-identical formal artifact is credited;
and no source-faithful proof reconstruction exists. All six downstream tasks remain open. No H0,
M0, R0, accepted execution state, audit completion, theorem completion, or master acceptance is
claimed.
