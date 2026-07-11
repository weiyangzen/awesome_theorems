# Scope map

## Included subject

- Second-order fully nonlinear elliptic PDEs `F(x, u, Du, D2u) = 0` on a specified real
  finite-dimensional domain.
- Monge-Ampere equations as one possible concrete family, only if an exact primary theorem is
  deliberately selected.
- A genuine theorem such as comparison, existence/uniqueness, an a priori estimate, or regularity,
  with all structural assumptions and the solution notion exposed.

## Decisions required at statement freeze

Select one primary theorem and freeze its dimension and domain; scalar/vector codomain; operator;
degenerate, uniform, or strict ellipticity convention; properness/convexity/concavity and continuity
assumptions; boundary data; classical, viscosity, or Alexandrov solution notion; quantified
constants; local/global conclusion; binder order; and every boundary or degenerate case. The Lean
encoding must then freeze Euclidean spaces, derivatives/Hessians, symmetric-matrix order,
determinant or operator interface, and solution predicates.

## Explicit exclusions

- Treating the PDE class, the equation `F = 0`, or "Monge-Ampere equations, etc." as a theorem.
- Silently substituting the neighboring ABP estimate, a Caffarelli regularity theorem, or the
  standalone Monge-Ampere target.
- Proving only a linear elliptic, one-dimensional, quadratic, or smooth toy case.
- Assuming the requested existence, comparison, estimate, or regularity conclusion in a structure
  field and projecting it back out.
- Claiming that a generic determinant or matrix lemma closes the nonlinear PDE theorem.

Until a source theorem is selected, a narrower choice would be invention and a broader choice would
be unformalizable umbrella prose. This is the first downstream statement blocker.
