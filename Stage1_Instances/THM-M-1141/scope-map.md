# Scope map

## Included theorem family

- Real-valued nonnegative (or positive, as the selected source requires) harmonic functions.
- A connected Euclidean domain, with dimension and regularity fixed by the source statement.
- Interior comparison between values, or between a supremum and infimum on a compactly contained
  subregion, with a constant independent of the particular harmonic function.
- Degenerate cases such as the zero function only if compatible with the selected positivity form.

## Statement decisions frozen

The root is the compact-subset inequality of Axler--Bourdon--Ramey Theorem 3.6, not the preceding
explicit ball formula. The ambient space is `EuclideanSpace Real (Fin n)` for arbitrary `n`; the
domain is open and connected; the function is real-valued, strictly positive, and mathlib-harmonic
on the domain; and `K` is compact and contained in the domain. The existential constant `C > 1`
precedes the binders for the function and points, encoding its independence from all three.

Empty `K` and zero-dimensional ambient space are retained because the selected theorem does not
exclude them and the statement remains well formed (vacuously in the empty-set case). Strict
positivity makes every displayed denominator positive. Boundary points are excluded by `K ⊆ Ω`.

## Explicit exclusions

- Parabolic Harnack (`THM-M-1134`), divergence-form Harnack (`THM-M-1175`), and the
  Krylov-Safonov nondivergence theorem (`THM-M-1176`).
- Harnack's convergence theorem (`THM-M-1142`), Harnack measure inequalities, and graph or
  probabilistic analogues.
- The mean-value property, maximum principle, or a two-point inequality offered only as a weaker
  substitute for the selected exact source theorem.
- Any structure or hypothesis containing the desired comparison conclusion.

No existing Lean declaration has been accepted. Repo and pinned-mathlib anchor search belongs to
the later anchor-audit node and cannot supply statement or proof credit at intake.
