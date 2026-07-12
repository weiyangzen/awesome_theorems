# THM-M-0013 rev-5.6 intake

`THM-M-0013` is the field-theory catalog item "Fundamental theorem of Galois theory." The
repository attributes it to Evariste Galois in 1832 and gives only the gloss "correspondence
between field extensions and subgroups of the Galois group," plus an untrusted `verified` label.
That identifies the classical Galois-correspondence family, but not one binder-complete theorem.

## Intake result

This dossier records a fail-closed `planned` instance. It does not silently decide whether the
extension is finite Galois or possibly infinite Galois; whether the subgroup side contains every
subgroup or only closed subgroups in the Krull topology; or whether the root includes only the
order-reversing correspondence or also the index/degree, conjugacy, normality, and quotient clauses.

J. S. Milne's *Fields and Galois Theory*, version 5.10 (2022), and the Stacks Project's immutable
source for Tag `09DW` were inspected as authoritative modern source leads. Milne's Theorem 3.17 on
pages 39-40 and Stacks Tag `09DW` give finite correspondences, while Milne's Theorem 7.13 and the
Stacks source's separately named infinite theorem require closed subgroups. The catalog selects
neither scope and supplies no historical primary-source locator. These modern sources are not
credited as `H0`.

## Formal boundary

`IntakeProbe.lean` elaborates the adjacent pinned finite and infinite correspondence APIs. Pinned
mathlib exposes an order equivalence from intermediate fields of a finite Galois extension to the
order dual of all subgroups, and a separate order equivalence for a possibly infinite Galois
extension to the order dual of closed subgroups. These are candidate-discovery observations only.
No candidate
is declared identical to the unfrozen catalog claim and no proof-body, trust, or theorem-completion
credit is assigned at intake.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M4, R4]`: the theorem family and a versioned modern source are known, but exact variant,
assumptions, historical source fidelity, complete clause mapping, and independent review remain
open; no exact usable formal target is selected; and a source-faithful proof reconstruction cannot
attach to an unfrozen root. All six downstream tasks remain open. No accepted execution state,
audit completion, theorem completion, or master acceptance is claimed.
