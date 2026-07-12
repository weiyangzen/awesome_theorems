# Scope map

## Included theorem family

- Critical planar percolation crossing probabilities, with the lattice and whether the model is
  site or bond percolation fixed by the selected rigorous source.
- A simply connected planar domain with four counterclockwise marked boundary prime ends/points,
  and discrete domains approximating that marked domain in the source-specified sense.
- One precisely oriented open-crossing event between two specified boundary arcs, including all
  boundary-color and endpoint conventions.
- Convergence as lattice mesh tends to zero to Cardy's exactly normalized function.
- Conformal invariance only to the extent asserted by the selected rigorous theorem.

## Decisions required at statement freeze

The statement phase must select one exact rigorous theorem and freeze: site versus bond model;
triangular/hexagonal lattice conventions; critical parameter; configuration probability space;
open and closed boundary conventions; the event's source and target arcs; discrete-domain
approximation; domain regularity or prime-end accessibility; marked-point order; convergence mode;
the conformal map normalization; and the formula itself. For the common cross-ratio presentation,
the phase must also freeze which marked points map to `0`, `x`, `1`, and infinity, the real branch
of `x^(1/3)`, and the constants in the hypergeometric expression.

These are mathematical data, not cosmetic notation. Permuting the points can replace a crossing
event by its complement or transform the cross-ratio. A finite-mesh probability is generally not
equal to its scaling limit. A derivation in a physics paper and a later rigorous convergence
theorem also have different source and assumption boundaries.

## Explicit exclusions

- The broad statement that critical percolation is conformally invariant without specifying an
  event, limit, and admissible marked domains.
- Cardy's 1992 prediction treated as a rigorous proof rather than the formula's original source.
- Smirnov's full conformal-invariance theorem, an SLE scaling-limit theorem, Kesten's `p_c = 1/2`
  theorem, or critical-exponent results substituted for this crossing-formula target.
- Bond percolation on the square lattice or a universality claim for arbitrary planar models unless
  the selected source proves that exact extension.
- A rectangle-only numerical value, Monte Carlo estimate, or floating-point evaluation.
- A theorem made tautological by defining `CardyFunction` to be the probability limit, assuming
  convergence/conformal invariance as a structure field, or taking the desired equality as a
  hypothesis.
- The repository metadata value `已验证` as human-source or kernel evidence.

No canonical Lean expression is frozen at intake. A later target must expose the probability
space, discrete event, limiting filter/sequence, conformal data, and explicit Cardy function rather
than hiding the conclusion in an assumption or definition.
