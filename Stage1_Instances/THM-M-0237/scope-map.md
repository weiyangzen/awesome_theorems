# Scope map

## Preserved theorem family

- The analytic Riemann-Roch theorem for divisors on a compact Riemann surface.
- A finite integral divisor `D`, its degree, the dimension `ell(D)` of the corresponding
  meromorphic-function or global-section space, genus `g`, and a canonical divisor `K`.
- The classical candidate formula `ell(D) - ell(K - D) = deg(D) + 1 - g`.

These bullets delimit the recognizable theorem family. They are not an accepted canonical
statement, source crosswalk, Lean expression, or proof.

## Decisions required at statement freeze

1. Select an immutable primary or authoritative edition with exact theorem and incorporated
   definition locators, proof boundary, corrections, errata, and independent review.
2. Fix whether a Riemann surface is nonempty and connected by definition, or whether those are
   explicit hypotheses. Decide whether disconnected compact complex one-manifolds are excluded.
3. Freeze the analytic object model: a Hausdorff second-countable complex one-manifold, another
   source-defined surface, or a checked equivalent formulation.
4. Define divisors, finite support, addition/subtraction, degree, effectivity, principal divisors,
   and the order convention for meromorphic functions.
5. Define `L(D)` and `ell(D)`: meromorphic functions `f` with `(f) + D >= 0`, including the zero
   function, or global sections of the divisor line bundle. Prove any encoding transport.
6. Define genus and canonical divisor. Fix whether `K` is chosen from a nonzero meromorphic
   differential, represented by the canonical line bundle, or used only through its divisor class,
   and prove independence of the choice.
7. Freeze the target form: the divisor-dimension formula, `ell(D) - ell(K-D)` form, line-bundle
   Euler characteristic, or an index form. No title-level equivalence is enough.
8. Resolve integer versus natural-valued dimensions and degrees, binder order, universe and
   typeclass assumptions, and every coercion in the equality.
9. Resolve genus zero and one, negative-degree divisors, `D = 0`, `D = K`, empty support, constant
   functions, a zero differential, the empty surface, and disconnected surfaces.

## Explicit exclusions

- `THM-M-0105` and `THM-M-0175`, the separately cataloged algebraic-curve Riemann-Roch targets.
- Hirzebruch-, Grothendieck-, arithmetic-, equivariant-, orbifold-, tropical-, graph-, or
  higher-dimensional Riemann-Roch theorems.
- A genus-zero, projective-line, effective-divisor, high-degree, or algebraically closed special
  case in place of the source-selected compact-surface root.
- An algebraic smooth-projective-curve statement without a checked analytification or GAGA bridge.
- A structure that stores arbitrary `degree`, `genus`, `ell`, `K`, or the desired equality as data.
- The legacy abstract packages in `S1_M_027.lean` or `S1_M_124.lean`; they are not concrete compact
  Riemann surfaces and their existential packages can make a weaker substitute proposition.
- A theorem about meromorphic orders on the complex plane, maximum modulus, or constant
  holomorphic functions on compact manifolds without the divisor/global-section formula.
- The untrusted `已验证` label, a theorem name, adjacent API elaboration, or another target's
  acceptance state as source or kernel evidence.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib contains general complex-manifold and
compact-space interfaces and plane-domain meromorphic-function APIs, but its own complex-manifold
module lists holomorphic vector/line bundles and finite-dimensional section spaces as future work.
A bounded local search found no terminal compact-Riemann-surface Riemann-Roch declaration. The
repo-local Riemann-Roch files belong to different theorem IDs and use abstract algebraic-curve data.
These observations are intake discovery only, not an exhaustive anchor audit or a proof of global
absence.
