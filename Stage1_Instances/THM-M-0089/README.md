# THM-M-0089 rev-5.6 intake

`THM-M-0089` is the representation-theory catalog item named the Peter-Weyl theorem. The
repository attributes it to Fritz Peter and Hermann Weyl in 1927, but supplies only the gloss
"completeness of compact-group representations" and an untrusted `verified` label.

## Intake result

This dossier records a fail-closed `planned` instance. The gloss identifies the Peter-Weyl theorem
family, but does not select a proposition. Standard formulations concern density of matrix
coefficients in continuous functions, Hilbert-space completeness in `L2`, decomposition of a
regular representation, or consequences such as separation of points. Those formulations require
different definitions and transports and cannot be merged from memory.

The original paper has a stable bibliographic lead: F. Peter and H. Weyl, *Die Vollstandigkeit der
primitiven Darstellungen einer geschlossenen kontinuierlichen Gruppe*, *Mathematische Annalen* 97
(1927), 737-755, DOI `10.1007/BF01447892`. Crossref metadata and a GDZ scan were inspected. The scan
locates a Parseval-type `Fundamentalsatz` on page 752, a uniform `Approximationssatz` on page 753,
and class-function and separation consequences on page 754. No one of those clauses is selected by
the catalog, and no complete definition/assumption/proof-node map, correction audit, translation,
or independent review was admitted. The source therefore supports `H1`, not `H0`.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned representation, finite-dimensional-representation,
Haar-measure, continuous-to-`Lp` density, and Hilbert-basis APIs. A bounded exact-topic search found
no Peter-Weyl or matrix-coefficient declaration in repo-local Lean or pinned mathlib. These are
discovery observations only, not the downstream exhaustive anchor audit and not proof evidence.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M4, R4]`: an original source lead is known, but exact source-to-root mapping remains open; no
usable exact formal artifact is credited; and no source-faithful reconstruction can attach to an
unfrozen root. All six downstream tasks remain open. No accepted execution state, audit completion,
theorem completion, or master acceptance is claimed.
