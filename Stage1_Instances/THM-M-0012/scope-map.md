# THM-M-0012 Scope Map

## Frozen human scope

The repository claim identifies the conventional fundamental-theorem-of-algebra family. The
statement phase freezes it as every univariate `f : Polynomial Complex` outside the image of
`Polynomial.C` having a root `z : Complex`. Binders are ordered as polynomial, nonconstancy
hypothesis, then existential root. This fixes the repository-scope Lean expression while leaving
pinpoint historical source fidelity and every proof gate open.

The intended conclusion is existence, not uniqueness or an algorithm for computing a root. The
root must lie in `Complex`, not merely in an unspecified extension. A later formulation may package
the result as algebraic closedness or splitting only after a checked directional crosswalk shows
that it returns the catalog claim without assuming it.

## Frozen statement decisions

1. Nonconstant means exclusion of all `Polynomial.C c`, including zero.
2. The canonical conclusion is `Polynomial.IsRoot f z`; evaluation at zero is credited through a
   checked iff.
3. The canonical target is pointwise existence. `IsAlgClosed Complex` remains an uncredited
   stronger packaging.
4. Positive `WithBot Nat` degree is credited through a checked iff.
5. The sole direct import, expression/environment fingerprints, four structural mutations, and
   zero/constant/linear boundary witnesses are recorded in the statement artifacts.

## Boundary cases

- The zero polynomial and all nonzero constant polynomials are outside the nonconstant antecedent.
- Linear and higher-degree complex polynomials are included without monicity or irreducibility.
- Repeated roots, coefficients that happen to be real, and polynomials with zero constant term are
  included without special treatment.
- A claim only about odd-degree real polynomials, a fixed degree, or roots in an algebraic extension
  is a strict substitution and cannot close this target.

## Discovery boundary

Pinned mathlib contains `Complex.exists_root` in
`Mathlib.Analysis.Complex.Polynomial.Basic` with a positive-degree hypothesis, as well as the
`Complex.isAlgClosed` instance and the generic `IsAlgClosed.exists_root` API. The statement phase
now establishes exact target identity with the positive-degree pointwise shape but does not inspect
or credit any candidate proof body, transitive trust closure, or anchor audit. Consequently the root
is provisionally `H1 / M3 / R4`, with no accepted execution state.

## Explicit exclusions

- The real odd-degree root theorem, intermediate value theorem, or Liouville theorem by itself.
- A monic, irreducible, real-coefficient, separable, or degree-bounded special case.
- An encoding that assumes `[IsAlgClosed Complex]` as an unexplained premise.
- Numerical approximations, computer algebra output, experiments, or unchecked certificates.
- The catalog's `已验证` label, a theorem name, or successful `#check` output as theorem-completion
  evidence.
