# Scope map

## Included theorem family

- Real-valued nonnegative (or positive, as the selected source requires) harmonic functions.
- A connected Euclidean domain, with dimension and regularity fixed by the source statement.
- Interior comparison between values, or between a supremum and infimum on a compactly contained
  subregion, with a constant independent of the particular harmonic function.
- Degenerate cases such as the zero function only if compatible with the selected positivity form.

## Decisions deferred to the statement phase

The source transcription must fix whether the root is the ball formula, a compact-subset inequality,
or a point-normalized bound; whether the domain is a ball or arbitrary connected open set; the
dimension and radius hypotheses; strict positivity versus nonnegativity; and the exact constant.
It must also freeze binder order, universes, the harmonicity predicate, topology, scalar codomain,
and treatment of empty or disconnected domains and boundary points.

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
