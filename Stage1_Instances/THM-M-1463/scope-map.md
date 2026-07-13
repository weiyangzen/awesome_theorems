# THM-M-1463 scope map

## Catalog scope preserved

- Target identity: `THM-M-1463`, named `Petrov-Galerkin方法`.
- Catalog attribution and date: many mathematicians, twentieth century.
- Literal gloss: `推广的Galerkin方法` (a generalized Galerkin method).
- Recognizable topic boundary: a Galerkin-style variational approximation in which trial and test
  spaces need not coincide.

This is all the repository fixes. It identifies a numerical method family, not one proposition.

## Decisions required before statement freeze

An accountable source correction must select one immutable proposition and freeze:

1. The real or complex scalar field, Banach or Hilbert trial and test spaces, universes,
   finite-dimensional subspaces, norms, completeness, and inclusion maps.
2. The bilinear or sesquilinear form, argument orientation, continuity constant, right-hand-side
   functional, and the continuous variational problem, if any.
3. The discrete Petrov-Galerkin equations, including trial space `U_h`, test space `V_h`, and the
   exact quantifier order for the trial solution and every test vector.
4. The stability contract: discrete inf-sup constant, adjoint or transpose nondegeneracy, kernel
   condition, dimension compatibility, coercivity or Fortin condition, and strict positivity.
5. The selected conclusion: existence and uniqueness, stability, quasi-optimality, a priori error,
   convergence over a mesh or approximation family, or a conjunction explicitly stated by the
   source.
6. Every norm and constant in the conclusion, whether the bound is sharp, and which approximation
   infimum or best-approximation object is used.
7. Mesh, regularity, approximation, consistency, conformity, and boundary assumptions for any
   PDE- or finite-element-specific result.
8. Ordered binders, alternate encodings, logical principles, and exact versus numerical
   computation semantics.

These choices change truth conditions and proof obligations. They are a resolution checklist, not
a canonical statement.

## Candidate theorem families not credited

- Well-posedness of a continuous or discrete variational problem from a Babuška or
  Banach-Nečas-Babuška inf-sup condition.
- Stability of the discrete Petrov-Galerkin solution in terms of the right-hand-side norm and a
  positive discrete inf-sup constant.
- A quasi-optimal error estimate comparing the discrete solution with the best trial-space
  approximation, with a source-selected continuity/stability constant.
- A Fortin-operator criterion transferring continuous stability to discrete spaces.
- A convergence or a priori estimate for a concrete finite-element, discontinuous
  Petrov-Galerkin, least-squares, or minimum-residual scheme.

None is selected, stated, or credited at intake. Merely defining the variational equations is not
a theorem about their solvability, stability, or error.

## Boundary and degenerate cases

The statement phase must resolve zero trial or test spaces, unequal finite dimensions, zero
right-hand side, zero bilinear form, zero or unattained inf-sup constants, nontrivial left or right
kernels, inconsistent discrete equations, nonunique solutions, exact inclusion of the continuous
solution in the trial space, empty approximation families, nonconforming spaces, and constants
whose denominators vanish. It must also distinguish equality of trial and test spaces from the
genuinely Petrov-Galerkin case.

## Explicit exclusions

- `THM-M-1462` ordinary Galerkin method and `THM-M-1464` discontinuous Galerkin method are separate
  catalog roots and confer no statement or proof credit here.
- Lax-Milgram or coercivity alone cannot replace a source-selected Petrov-Galerkin stability or
  error theorem.
- A generic Banach-Nečas-Babuška theorem, finite-dimensional invertibility theorem, or orthogonal
  projection fact is substrate unless an accepted source crosswalk proves exact identity.
- A PDE-specific finite-element result, discontinuous Petrov-Galerkin method, least-squares method,
  or minimum-residual theorem cannot be chosen merely because it is convenient to formalize.
- A structure or hypothesis that stores the desired solution, stability, or error estimate is not
  a proof.
- The catalog label `已验证`, a name match, or a successful API probe gives no H or M credit.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides continuous bilinear maps and
operator-norm bounds, Hilbert-space projections, and a real coercive Lax-Milgram equivalence. A
bounded exact-topic search found no Petrov-Galerkin-, Babuška-, Nečas-, or inf-sup-named terminal
declaration. These are intake discovery observations only, not the downstream exhaustive anchor
audit or a global absence claim.
