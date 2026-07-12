# Scope map

## Included topic boundary

- A source-selected Selberg trace formula, not the generic idea of a trace formula.
- The exact group, discrete subgroup or lattice, quotient, and automorphic-function space.
- The source's admissible test functions and transform conventions.
- The trace-class or regularized operator and its spectral expansion.
- Every geometric contribution and its measure, orbital, and conjugacy-class normalization.
- Convergence, compactness, torsion, cusp, and smoothness hypotheses used by that formula.

## Ambiguities to resolve at statement freeze

The repository record does not decide among materially different formulations:

1. A compact quotient formula with a discrete spectral sum and identity plus nontrivial conjugacy
   classes.
2. A cofinite noncompact quotient formula containing continuous spectrum, scattering data, cusp
   terms, and regularization.
3. A classical upper-half-plane formula for a specific Fuchsian group versus a representation-
   theoretic formula for a locally compact group.
4. Weight zero, nonzero weight, or a formula restricted to a particular space of automorphic or
   cusp forms.

Even after choosing a family, Haar and quotient measures, Fourier transform, Laplacian sign,
spectral parameter, primitive conjugacy classes, orbital integrals, and multiplicities must be
fixed. These choices alter the displayed equality and cannot be inferred from the title.

## Explicit exclusions

- The Selberg sieve, Selberg integral, Selberg zeta function, or Arthur trace formula as substitutes.
- The elementary identity `LinearMap.trace = Matrix.trace`; it is only a finite-dimensional trace API.
- A theorem about one modular or cusp form that omits the spectral/geometric identity.
- A generic equality between author-supplied functions named "spectral side" and "geometric side".
- A compact-quotient formula silently substituted for the source's noncompact formula, or conversely.
- The repository labels `已验证` and "trace formula for automorphic forms" as proof or statement evidence.

No canonical Lean target is frozen at intake because the source record does not identify an exact
formula.
