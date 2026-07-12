# Scope map

## Included theorem family

- A source-specified Lipschitz curve in the complex plane, with its parametrization, orientation,
  regularity, and measure made explicit.
- The Cauchy singular-integral kernel on that curve, initially defined by the source's truncations
  or principal-value prescription.
- Uniform `L^2` control of the truncations and/or a bounded `L^2` extension, exactly as related by
  the selected theorem.
- The source's normalization constant and the dependence of the operator norm on the Lipschitz
  character of the curve.

## Decisions reserved for statement freeze

The paper title fixes an `L^2` boundedness headline but not a unique formal proposition. The
statement phase must inspect a stable copy and decide:

1. whether curves are global graphs `t + i A(t)`, general Lipschitz parametrizations, finite arcs,
   closed curves, or a theorem plus reductions among these models;
2. whether `L^2` uses parameter Lebesgue measure or arclength measure and what checked transport
   relates them;
3. whether the operator is a family of deleted-neighborhood truncations, an almost-everywhere
   principal value, a maximal truncation, or a bounded extension from a dense class;
4. the kernel orientation, factors such as `1 / (2*pi*i)`, diagonal convention, initial function
   class, and exact quantitative constant;
5. whether the theorem assumes a small Lipschitz constant, proves the arbitrary-Lipschitz case,
   or uses intermediate reductions whose hypotheses must remain visible.

## Explicit exclusions

- The classical Cauchy integral formula on circles or smooth contours as a substitute.
- Boundedness only for a smooth curve or only for `L^2` functions already assumed to have a
  bounded Cauchy transform.
- A Hilbert-transform theorem on the real line without a checked identification with the selected
  curve operator.
- Pointwise existence of a contour integral away from the curve without singular-boundary `L^2`
  boundedness.
- An endpoint `L^1`, weak-type, `L^p`, maximal-truncation, or higher-dimensional theorem silently
  substituted for the selected `L^2` claim.
- The repository label `已验证` as human-source or machine-proof evidence.

No canonical Lean target is frozen at intake. Exact binders and boundary cases depend on primary
source inspection and the formal representation of the singular integral.

