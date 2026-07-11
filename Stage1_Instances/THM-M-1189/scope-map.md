# Scope map

## Included claim family

- The linear inhomogeneous heat operator `partial_t - Delta` on a space-time cylinder or an
  explicitly selected parabolic subdomain.
- A priori control of two spatial derivatives and one time derivative of a solution by Holder data,
  with parabolic scaling `alpha` in space and `alpha / 2` in time.
- Interior, initial-boundary, and global estimates are distinct variants; exactly one must be chosen
  from a primary source before the canonical statement is frozen.
- The constant must expose its dependence on dimension, `alpha`, domain geometry, time interval,
  and separation from the parabolic boundary as applicable.

## Statement-phase decisions

Primary-source inspection must fix `0 < alpha < 1`, the spatial dimension and scalar field, the
domain regularity, classical-solution assumptions, the definition of parabolic Holder seminorms,
compatibility conditions, the parabolic boundary, and whether the right side contains an `L-infinity`
norm of `u`, boundary/initial norms, or both. It must also decide bounded versus local cylinders and
record degenerate cases such as empty time intervals or zero radius.

## Explicit exclusions

- Elliptic Schauder estimates or mere smoothness of the heat kernel as substitutes.
- Existence/uniqueness without the quantitative parabolic Holder estimate.
- An ODE, finite-dimensional, weak energy, or continuity estimate presented as the full theorem.
- A proposition that assumes the desired estimate or packages it as structure data.

The statement phase must either define the concrete parabolic Holder spaces and derivatives in Lean
or record the exact missing API boundary. Partial lemmas may receive their own later obligations but
cannot broaden or replace the root claim.
