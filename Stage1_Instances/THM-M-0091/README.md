# THM-M-0091 rev-5.6 intake dossier

This directory is the fail-closed `planned` intake for `THM-M-0091`, the catalog item
`外尔维数公式` (Weyl dimension formula). The repository supplies only the gloss:

> Dimensions of irreducible representations of compact Lie groups.

The familiar theorem expresses the dimension of a highest-weight representation by a product over
positive roots. That description is a candidate family, not yet the source-certified root. The
catalog does not fix connectedness, the representation field and continuity, the maximal torus,
positive roots, highest-weight convention, root/coroot pairing, Weyl vector, product codomain, or
the treatment of torus, central, disconnected, and empty-root cases. The exact mathematical and
Lean statements therefore remain unset rather than being reconstructed from memory.

Crossref metadata authenticates Hermann Weyl's 1925 paper
*Theorie der Darstellung kontinuierlicher halb-einfacher Gruppen durch lineare Transformationen. I*
as a historical source lead. The available link returned an access page instead of a lawful article
transcription during intake, so no theorem/formula/page, definition chain, assumption map,
translation, errata audit, or independent review is credited.

Pinned mathlib contains adjacent root-pairing, positive-root, Lie-weight, representation,
finite-dimensional representation, character-at-identity, and Lie-group interfaces. The bounded
search and `IntakeProbe.lean` found no declaration that joins those interfaces into the Weyl
dimension formula. These observations establish only interface debt, not a canonical target or
proof.

The structured scope authority is [instance.json](instance.json). Proposition-changing decisions
are listed in [scope-map.md](scope-map.md), the source and formal mapping is in
[source-statement-crosswalk.md](source-statement-crosswalk.md), and all downstream nodes remain
open in [task-dag.json](task-dag.json).

Status boundary: provisional, self-tested planned intake only, with vector `[H1, M3, R4]`. No exact
source proposition, canonical Lean target, accepted proof state, audit completion, theorem
completion, or master acceptance is claimed.
