# THM-M-1356 rev-5.6 intake

`THM-M-1356` is the ordinary-differential-equations catalog item "Routh-Hurwitz criterion."
The catalog supplies only the gloss "conditions for the real parts of a polynomial's roots to be
negative," attributes the result to Edward Routh and Adolf Hurwitz, gives the year 1895, and labels
it `verified`. That last field is untrusted metadata, and the gloss is not a binder-complete
proposition.

## Intake result

This directory is a fail-closed `planned` dossier. It preserves the recognizable stability-
criterion family without choosing a convenient formulation. The catalog does not fix the degree
and coefficient indexing, real versus complex coefficients, leading-coefficient normalization,
strict versus closed left half-plane, multiplicity convention, Hurwitz matrix orientation,
principal-minor indexing, Routh-array alternative, degeneracies, or whether the desired result is
an equivalence or only one implication.

Hurwitz's 1895 article was inspected from the Goettingen Digitisation Centre scan. On pages
273-274 it treats a real degree-`n` equation with positive leading coefficient and states the
necessary-and-sufficient positivity of the finite Hurwitz determinants for all roots to have
negative real parts. Barkovsky's modern lecture notes give the corresponding finite-matrix form as
Theorem 40 on printed page 19. A second modern source uses ascending coefficients and an infinite-
matrix factorization, confirming that coefficient and matrix conventions cannot be inferred from
the catalog gloss alone. These are source leads, not an accepted canonical root or `H0` evidence.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned polynomial-root, complex-real-part, submatrix, and
determinant APIs. A bounded exact-topic search found no Routh-Hurwitz theorem in pinned mathlib or
repo-local Lean. Those observations are discovery inputs only, not the downstream anchor audit.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M4, R4]`: an established theorem family and primary/modern source passages are known, but
exact root selection, complete source mapping, errata review, and independent acceptance remain
open; no exact formal artifact is credited; and no source-faithful readable proof can attach to an
unfrozen root. All six downstream tasks remain open. No accepted state, audit completion, theorem
completion, or master acceptance is claimed.
