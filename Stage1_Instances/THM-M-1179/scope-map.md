# Scope map

## Included family

- Real Monge-Ampere equations such as `det(D^2 u) = f` on a specified finite-dimensional domain,
  with convexity/ellipticity and a classical, Alexandrov, or viscosity solution notion.
- Complex Monge-Ampere equations on a specified complex or Kahler manifold, if primary-source
  evidence establishes that this is the intended branch.
- One exact existence, uniqueness/comparison, regularity, or estimate theorem, once selected from an
  inspected primary source.

## Decisions required by the statement phase

The next phase must select one branch and freeze the primary theorem and pinpoint, ambient space and
dimension, domain and boundary data, operator normalization, right-hand side, solution notion,
quantifier order, hypotheses, exact conclusion, exceptional cases, and all constants. It must then
freeze the Lean types, universes, determinant/Hessian or complex-form encoding, imports, and target
expression. These choices cannot be inferred from the bare equation name.

## Explicit exclusions

- Treating an equation definition as though it proves existence, solvability, or regularity.
- Proving only the determinant of a constant or quadratic Hessian.
- Replacing the nonlinear PDE by a one-dimensional ODE or generic determinant identity.
- Assuming existence, uniqueness, or regularity in a package field and projecting it back out.
- Conflating the real equation, complex equation, optimal-transport applications, Caffarelli
  regularity, and the Calabi conjecture without a checked equivalence to the selected source theorem.

Until one proposition is sourced, there is no legitimate canonical statement to elaborate or
mutation-test.
