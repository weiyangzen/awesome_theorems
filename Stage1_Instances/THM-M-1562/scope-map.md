# Scope map

## Included claim

The root is a conjunction with one shared, concrete limiting law:

- **GUE branch:** the soft-edge limit for the largest eigenvalue of a source-normalized complex
  Hermitian GUE matrix, after source-exact centering and `N^(2/3)` scaling.
- **KPZ branch:** the one-point long-time limit for the source-normalized narrow-wedge KPZ height at
  the spatial origin, after source-exact deterministic centering and `T^(1/3)` scaling.
- **Identification branch:** both limits use the same beta-2 Tracy-Widom distribution `F_2`, built
  from the Airy-kernel Fredholm determinant (or connected to an equivalent Painleve II formula by
  a checked bridge).

The conjunction is intentional: proving only the random-matrix branch would duplicate the scope of
`THM-M-1107` and would not account for this target's catalogue phrase "random matrices and KPZ."

## Statement-phase decisions

The primary-source audit must freeze the GUE density or entrywise law, trace convention, spectral
edge, eigenvalue ordering, and all scale constants. For KPZ it must freeze the equation's
coefficients, white-noise normalization, narrow-wedge initial condition/renormalized solution
concept, height sign convention, deterministic centering, scale constant, and convergence mode.
It must also freeze a concrete Airy function, Airy kernel, operator domain, trace-class result, and
Fredholm determinant.

The Lean target must expose the probability spaces, measurability, both directed limits, and the
common distribution. If pinned libraries lack the required SPDE or operator interfaces, the next
phase must record that exact blocker. An abstract structure with either convergence statement as a
field is not an encoding of the theorem.

## Explicit exclusions

- GOE/beta-1, GSE/beta-4, or arbitrary beta ensembles.
- Edge universality for general Wigner matrices.
- KPZ universality for arbitrary initial data, stochastic growth models, or all points in space.
- Longest-increasing-subsequence, directed last-passage-percolation, or PNG limits as substitutes
  for the stated narrow-wedge KPZ-equation branch; they may serve only as separately mapped bridges.
- Finite-dimensional simulation, numerical Fredholm determinants, or empirical histograms.
- A named but opaque probability law with no audited Airy-kernel or equivalent construction.
- The repository metadata label `已验证`, which is untrusted and grants no proof credit.

## Boundary cases

Matrix size zero and nonpositive KPZ time are excluded. Thresholds range over every real number.
Other normalizations may be credited only after a checked scaling transport. Neither finite-size
agreement nor convergence of moments alone substitutes for the source-specified distributional
limits.

