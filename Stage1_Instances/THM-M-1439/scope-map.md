# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1439`, the proof label `Lyubich证明`, attribution to Mikhail
Lyubich, the year 1999, and the gloss `Feigenbaum猜想的解析证明` ("an analytic proof of the Feigenbaum
conjecture"). Importance "high" and status `已验证` are catalog metadata, not source or kernel
evidence. Intake preserves the 1999 real/complex-dynamical renormalization subject boundary without
turning a proof description into a theorem.

## Proposition-changing decisions

An approved source correction must select one truth-valued root and freeze:

- whether the root is the paper's Hyperbolicity Theorem, its Universality Theorem, the original
  stationary period-doubling case, all real bounded combinatorics, or a conjunction of results;
- the space of quadratic-like germs, its rescaling equivalence, topology and complex analytic
  structure, the connectedness locus, hybrid classes, and real subspace;
- the finite family of disjoint real Mandelbrot copies, renormalization strips and piecewise
  renormalization operator, including what "bounded type" means;
- the compact invariant horseshoe, its conjugacy to a bi-infinite shift, and the exact definition
  and constants for uniform hyperbolicity;
- stable and unstable leaves, their connected-component convention, hybrid-class equality,
  codimension, analyticity, transversality, and exclusion of the cusp class;
- for a scaling-law root, the real analytic one-parameter family, transverse intersection,
  sufficiently-large index, uniqueness, asymptotic relation, constants, and universal parameter;
- whether supporting assumptions such as complex a priori bounds are hypotheses or discharged
  dependencies, and which combinatorial cases they cover; and
- all universes, ordered binders, quantifier dependencies, normalizations, local/global clauses,
  and degenerate cases.

These choices produce inequivalent propositions. They are a resolution ledger, not a target.

## Candidate families not credited

- Lyubich's introduction-level Hyperbolicity Theorem for the real bounded-type renormalization
  horseshoe, with its shift, stable-leaf, and unstable-leaf clauses.
- The stationary period-doubling hyperbolicity/fixed-point result closest to the original
  Feigenbaum observation and Lanford's computer-assisted setting.
- The stationary Universality Theorem giving asymptotic parameter scaling in a transverse real
  analytic family.
- The bounded-combinatorics scaling theorem in Section 9, with two-sided exponential estimates and
  transverse-family comparison.
- The conjunction of hyperbolicity, hairiness, self-similarity, universality, Hausdorff-dimension,
  and quasiconformal conclusions presented by the 1999 paper.

No family in this list is selected, asserted, or credited at intake.

## Explicit exclusions

`THM-M-1437` (Feigenbaum universality) and `THM-M-1438` (Lanford proof) are distinct roots and do not
supply inherited scope or proof credit. A result about existence of one fixed point, one unstable
eigenvalue, exponential convergence within a hybrid class, or a single period-doubling constant is
not automatically the full bounded-type Hyperbolicity Theorem. Conversely, the scaling
Universality Theorem is not interchangeable with hyperbolicity of the renormalization horseshoe.

Also excluded are structures that assume the horseshoe, hyperbolic splitting, stable/unstable
manifolds, hybrid foliation, transversality, or universal scaling as fields; a theorem merely
projecting such a field; finite-dimensional toy operators; numerical approximations to the
Feigenbaum constant; orbit plots; floating-point convergence; and unchecked computer algebra. The
catalog word `已验证` supplies neither human-source nor Lean credit.

## Boundary cases

The corrected source target must decide empty or singleton families of Mandelbrot copies, the
number of symbols, disjointness and realness, the cusp `c = 1/4`, stationary versus nonstationary
combinatorics, period doubling versus general bounded type, maps on strip boundaries, nonescaping
and infinitely renormalizable conditions, choice of connected stable/unstable components,
normalization up to rescaling, sufficiently-large indices, zero asymptotic coefficients, and
families tangent rather than transverse to a hybrid class.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib supplies generic complex analysis,
iteration, semiconjugacy, compactness, and continuous-linear-map APIs, but the bounded intake search
found no Feigenbaum-Coullet-Tresser, quadratic-like-germ, hybrid-class, Mandelbrot-copy
renormalization, or Lyubich hyperbolicity declaration. These adjacent APIs and the name search are
discovery inputs only, not an exhaustive anchor audit, statement elaboration, or proof evidence.
