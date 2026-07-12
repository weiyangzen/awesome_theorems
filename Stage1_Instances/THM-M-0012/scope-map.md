# THM-M-0012 Scope Map

## Frozen human scope

The repository claim identifies the conventional fundamental-theorem-of-algebra family. Reading it
as every nonconstant univariate polynomial with complex coefficients having a root in the complex
numbers matches standard usage and the pinned Lean candidate, but the catalog does not itself state
the arity or separately spell out coefficient and root domains. The dossier records this as the
provisional human scope that the source and statement phase must ratify, with binders ordered as
polynomial, nonconstancy hypothesis, then existential root. It does not yet freeze a Lean expression
or credit any proof.

The intended conclusion is existence, not uniqueness or an algorithm for computing a root. The
root must lie in `Complex`, not merely in an unspecified extension. A later formulation may package
the result as algebraic closedness or splitting only after a checked directional crosswalk shows
that it returns the catalog claim without assuming it.

## Decisions for the statement phase

The next phase must independently select and review a pinpoint mathematical source, then freeze:

1. The precise meaning of nonconstant: positive `WithBot Nat` degree, positive natural degree, or
   exclusion of all constant polynomials.
2. Root encoding: `Polynomial.IsRoot f z`, `Polynomial.eval z f = 0`, or an explicitly checked
   equivalent expression.
3. Whether the canonical root is the pointwise existence proposition or `IsAlgClosed Complex`, and
   the exact direction of every credited transport.
4. The minimal pinned import, namespaces, binders, universe/typeclass context, normalized expression
   hash, environment fingerprint, and proof-foundation profile.
5. Removed-hypothesis, changed-domain, binder-scope, zero/constant, and linear-polynomial mutations
   before inspecting proof closure.

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
`Complex.isAlgClosed` instance and the generic `IsAlgClosed.exists_root` API. The intake probe only
authenticated that these declarations elaborate at the recorded pin. It did not establish exact
statement identity, inspect their proof bodies or transitive trust closure, or perform the later
precommitted anchor audit. Because no exact target or statement mapping is frozen, the candidate is
not yet a usable formal artifact for this root. Consequently it remains `H1 / M4 / R4` with no accepted
execution state.

## Explicit exclusions

- The real odd-degree root theorem, intermediate value theorem, or Liouville theorem by itself.
- A monic, irreducible, real-coefficient, separable, or degree-bounded special case.
- An encoding that assumes `[IsAlgClosed Complex]` as an unexplained premise.
- Numerical approximations, computer algebra output, experiments, or unchecked certificates.
- The catalog's `已验证` label, a theorem name, or successful `#check` output as theorem-completion
  evidence.
