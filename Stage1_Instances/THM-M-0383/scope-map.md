# Scope map

## Included topic boundary

- A source-specified Fourier restriction or adjoint extension estimate in a fixed dimension.
- The exact hypersurface, parametrization, surface measure, Fourier-transform normalization, and
  scalar field used by that source.
- The stated input and output spaces, exponent range, constants, scale dependence, and any epsilon
  loss or support assumptions.
- The precise 1991 Bourgain result intended by the repository metadata, once identified from an
  immutable passage rather than inferred from the label.

## Ambiguities to resolve at statement freeze

The repository record does not decide among these materially different targets:

1. **Sphere restriction:** bounded restriction of the Euclidean Fourier transform to a sphere, or
   the dual extension estimate, with dimension-dependent exponent conditions.
2. **Paraboloid/cone restriction:** an extension estimate for a different curved hypersurface,
   potentially connected to dispersive estimates.
3. **Local restriction:** a norm bound on a ball of radius `R`, possibly with an `R^epsilon` loss,
   rather than a global estimate.
4. **Discrete restriction:** an exponential-sum or lattice-point estimate with counting measure,
   not a continuous hypersurface theorem.
5. **An exponent improvement or partial range:** a historically specific Bourgain theorem rather
   than the full restriction conjecture.

The statement phase must inspect an immutable primary or authoritative source and freeze ordered
binders, dimension, surface and measure, transform convention, exponent inequalities, input class,
norms, constant dependencies, localization, and endpoint policy. It must determine whether the
named result is a complete theorem in a specified range or an advance toward a broader conjecture.

## Explicit exclusions

- The unrestricted Plancherel theorem, Fourier inversion, or Riemann-Lebesgue lemma as substitutes.
- A generic measure restriction operation with no Fourier estimate.
- A Tomas-Stein estimate or a modern decoupling theorem unless a checked source transport proves it
  is exactly the selected claim.
- A local estimate silently promoted to a global one, or a restricted exponent range promoted to
  the full restriction conjecture.
- A discrete exponential-sum theorem substituted for a continuous restriction theorem, or vice
  versa.
- The repository label `已验证` as evidence of a human proof, formal statement, or machine proof.

No canonical Lean target is frozen at intake because the source record does not identify one.
