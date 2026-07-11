# Scope map

## Included claim

- Euclidean ambient space `R^n`, with `n >= 3`, an open domain `Omega`, and `p` on its boundary.
- Regularity means that the Perron solution of the Laplace Dirichlet problem attains every
  continuous boundary datum at `p`.
- The geometric side uses Newtonian capacity of `Omega`'s complement in a fixed family of
  shrinking annuli centered at `p`.
- Regularity is equivalent to divergence of the dimensionally normalized Wiener series.

## Statement-phase decisions

The inspected source must fix boundedness of `Omega`, the boundary-data class, Perron upper/lower
solution conventions, capacity normalization, open/closed annular endpoints, geometric scale, and
whether the criterion is written as a series or an equivalent integral. It must also settle empty
annular obstacles, extended-real arithmetic, and invariance under changing the geometric scale.
Binder order and universes must follow those decisions.

## Explicit exclusions

- The planar logarithmic-capacity criterion (`n = 2`) or nonlinear `p`-capacity variants.
- A barrier criterion, cone condition, or exterior-ball condition substituted for the equivalence.
- Heat-equation, parabolic, fractional-Laplacian, or fine-topology Wiener tests.
- An abstract structure carrying capacity, regularity, or the desired equivalence as assumed data.
- The checked auxiliary lemmas in legacy `S1_M_143.lean` as closure of the source theorem.

The formal target must eventually construct or import the concrete Newtonian capacity and Perron
regularity semantics; otherwise it must record a precise API blocker.
