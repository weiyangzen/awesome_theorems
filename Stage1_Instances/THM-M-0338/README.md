# THM-M-0338 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Kadison-Singer problem. The
repository supplies only the gloss "unique extension of pure states". The conventional problem
concerns pure states on the diagonal maximal abelian C-star subalgebra of bounded operators on a
separable infinite-dimensional Hilbert space and their extensions to the full operator algebra.

That conventional scope is recorded for source discovery, but it is not yet an exact statement.
The repository does not specify the Hilbert-space model, diagonal algebra, definition of state and
purity, whether existence is included, or the codomain and restriction maps. Selecting these details
without inspecting a source would silently strengthen the gloss. The root therefore remains
`[H1, M4, R4]`.

A pinned Lean probe confirms that mathlib provides C-star algebras, star subalgebras, positive
linear maps, and bounded operators, but the bounded name search found no state/pure-state API.
This is an encoding inventory only, not a theorem statement or proof. Exact commands and results
are recorded in `validation.md`.
