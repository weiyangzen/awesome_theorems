# THM-M-0742 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the recursion-theory catalog item
`递归定理` (recursion theorem). The repository attributes it to Stephen Kleene in 1938 and supplies
only the gloss `递归函数的自指` ("self-reference of recursive functions"). Those fields identify a
theorem family, not a binder-complete proposition.

An immutable authoritative secondary source identifies the likely family as Kleene's recursion
theorem. It gives both a total-computable transformation of natural program indices and a
parameterized partial-computable formulation. Pinned mathlib contains corresponding concrete
leads in `Mathlib.Computability.PartrecCode`: `Nat.Partrec.Code.fixed_point` and
`Nat.Partrec.Code.fixed_point₂`. The declarations differ in their binders and conclusions, and the
catalog does not choose an index model or formulation.

Target ownership is also unresolved. `THM-M-0743` separately names the fixed-point theorem, while
the outside-Stage1 record `THM-C-0006` explicitly names Kleene's second recursion theorem. Selecting
one pinned declaration here without source and ownership review could duplicate a neighbor or
silently replace the received wording.

The canonical mathematical statement and Lean expression therefore remain null. The provisional
root vector is `[H1, M4, R4]`: the established theorem family and source/formal leads are known, but
the exact source statement is not admitted; no candidate receives machine credit before statement
identity is frozen; and no reviewed reconstruction can attach to an unfrozen root. All six
downstream tasks remain open. Neither audit completion nor theorem completion is claimed.
