# THM-M-1356 rev-5.6 dossier

`THM-M-1356` is the ordinary-differential-equations catalog item "Routh-Hurwitz criterion."
The catalog supplies only the gloss "conditions for the real parts of a polynomial's roots to be
negative," attributes the result to Edward Routh and Adolf Hurwitz, gives the year 1895, and labels
it `verified`. That last field is untrusted metadata, and the gloss is not a binder-complete
proposition.

## Intake result

This directory remains a `planned` dossier. Intake preserved the recognizable stability-
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

## Statement result

The statement phase selects Barkovsky's finite-matrix Theorem 40 form, with its stability
definition on printed page 6, matrix on printed page 18, and criterion on printed page 19.
`Statement.lean` encodes real descending coefficients, their checked transport to Lean's ascending
polynomial coefficients, strict complex-root stability, the finite Hurwitz matrix, and all leading
principal minors. `check_statement.py`, `statement.json`, `statement-validation.md`, and
`statement-receipt.json` bind the pinned elaboration, minimal imports, checked expansion, and four
required structural mutations.

The provisional vector after statement elaboration is `[H1, M3, R4]`: an exact source-selected
interface now exists, but no Routh-Hurwitz proof body is supplied. Complete proof translation,
correction or errata review, independent `H0` acceptance, obligation freeze, readable
reconstruction, release validation, and master acceptance remain open. The formal anchor audit is
reported provisionally below. No accepted proof state, audit completion, or theorem completion is
claimed.

## Anchor-audit result

`anchor-audit.json`, `anchor-audit.md`, and `AnchorAudit.lean` freeze and check the bounded formal
candidate inventory. At clean pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
the relevant polynomial/root and matrix/determinant declarations are support APIs only. A complete
exact-topic scan found no Routh-Hurwitz declaration; `docs/1000.yaml` contains a catalog title but
no formal declaration. Bounded public Lean searches likewise discovered no external terminal
candidate, while unavailable code-search lanes are recorded as access failures rather than absence
evidence.

The vector therefore remains `[H1, M3, R4]`. This provisional result completes only the assigned
candidate inventory pending master acceptance. It adds no proof credit and does not claim
exhaustive discovery, obligation-tree closure, audit completion, or theorem completion.
