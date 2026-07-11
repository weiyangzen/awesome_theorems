# Scope map

## Intended theorem family

- A smooth closed Riemannian manifold `(M, g0)` and metrics remaining in the conformal class of
  `g0`.
- The normalized Yamabe evolution, conventionally written
  `partial_t g = -(R_g - r_g) g`, where `R_g` is scalar curvature and `r_g` its volume average.
- A source-verified existence and/or convergence conclusion whose limiting metric has constant
  scalar curvature, with every dimension and curvature hypothesis retained.
- The equivalent scalar parabolic PDE for the positive conformal factor only after its constants,
  Laplacian sign, normalization, and transport to the metric formulation are checked.

## Decisions deferred to statement freeze

The exact primary theorem must decide compactness, connectedness, dimension, initial regularity,
volume normalization, time interval, positivity or conformal-flatness assumptions, convergence
topology and rate, uniqueness, and treatment of zero/negative Yamabe invariant. It must also decide
whether the target is a general existence theorem, a conditional convergence theorem, or a named
special case. Universes and binder order must follow that selected claim.

## Explicit exclusions

- The elliptic Yamabe existence theorem substituted for a flow theorem.
- Merely defining the flow or proving volume preservation substituted for long-time existence or
  convergence.
- Ricci flow, mean-curvature flow, or the unnormalized equation substituted for the normalized
  flow without checked equivalence.
- A convergence theorem with compactness, curvature, local conformal flatness, dimension, or sign
  hypotheses silently removed.
- An abstract structure that assumes a solution or limiting metric as a field.

## Formalization boundary

The statement phase must locate concrete mathlib interfaces for smooth manifolds, Riemannian
metrics, scalar curvature, conformal rescaling, time-dependent tensor fields, integration and
volume averages, and the relevant PDE solution/convergence notions. Missing interfaces are to be
reported as formalization debt, not replaced by uninterpreted predicates that encode the result.
