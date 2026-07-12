# Exact-statement gate: blocked

Item: `S56-M-1193-STATEMENT`  
Base revision: `31b7ab5b3902c4a80878c2007218f90566a8b85c`

## Decision

The intake selects the classical scalar, zero-curvature Li-Yau differential Harnack claim, but the
exact claim cannot yet be elaborated in the repository-pinned Lean environment. This is an
infrastructure blocker, not permission to replace the theorem with an abstract predicate.

The selected claim requires concrete, mutually compatible Lean definitions of all of the following:

- the Levi-Civita connection and its Ricci tensor, including the convention for `Ric >= 0`;
- the Riemannian gradient and Laplace-Beltrami operator with a fixed sign convention;
- a complete finite-dimensional Riemannian manifold and its dimension;
- spatial and temporal smoothness for `u : M -> Real -> Real`;
- the pointwise heat equation `partial_t u = Delta_g u` on `M x (0,T]`.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the Riemannian manifold
surface provides metrics, tangent bundles, and path length, and the vector-bundle surface provides
abstract covariant derivatives and torsion. The checked source inventory contains no definition of
Riemann/Ricci curvature, a Levi-Civita connection, or a manifold Laplace-Beltrami operator. The
available `Laplacian` results are for inner-product vector spaces and distributions, not functions
on a Riemannian manifold. Consequently there is no truthful minimal-import expression for the
intake root.

Introducing unconstrained parameters named `ricci`, `gradient`, or `laplacian`, or packaging the
missing mathematics into a `LiYauProblem` predicate, would merely elaborate a broadened abstract
schema. It would not encode the selected geometric PDE and is forbidden by the exact-statement
gate. Specializing to Euclidean space would remove the quantified complete Riemannian manifold and
Ricci hypothesis, so that is also a non-equivalent substitution.

## Source boundary

The repository's literal source wording is only `正解的梯度估计` ("gradient estimate for positive
solutions"). The intake conservatively selected the standard nonnegative-Ricci specialization,
but its primary-source theorem/page, premise mapping, normalization, and errata audit remain open.
This does not by itself justify changing the intake root during the statement phase. It does mean
that any future implementation of the missing differential-geometric APIs must also be checked
against the source audit before the expression can receive source-fidelity credit.

## Required unblock

Provide pinned, kernel-checkable definitions (either in mathlib or in an owned prerequisite module)
for curvature/Ricci, Levi-Civita connection, Riemannian gradient, and Laplace-Beltrami with documented
conventions. Then encode the complete-manifold, dimension, positivity, smoothness, heat-equation,
time-domain, and pointwise inequality binders without opaque stand-ins. The retry must minimize
imports, print and hash the elaborated expression, compile the logarithmic transport if it is
credited, and distinguish mutations removing positivity, completeness/Ricci, the heat equation,
and the strict `t > 0` boundary.

## Narrow validation evidence

Commands were run from this worker clone on 2026-07-12. No update, build, fetch, or mutation of
`.lake` was performed. The existing `.lake` path is an untracked link to the canonical pinned
artifacts.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique ranks, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1193` | exit 0; rank 387, planned hard anchor/wrapper lane, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |
| `rg -n -i 'ricci|curvature|laplace.beltrami|heat equation|levi.civita' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 0 only for an incidental prose mention of curvature in `MeasureTheory/Measure/Doubling.lean`; no required declaration found |
| `rg --files Formalizations/Lean/.lake/packages/mathlib/Mathlib/Geometry/Manifold` | exit 0; Riemannian `Basic`/`PathELength` and covariant-derivative `Basic`/`Torsion` exist, but no curvature or Laplace-Beltrami module |

First failed gate: exact Lean statement elaboration with minimal pinned imports. Known failures are
the declaration/expression, expression fingerprint, checked alternate transport, and meaningful
structural mutation tests. This assigned phase is therefore not self-tested or complete, and no
`.stage1-worker-selftest.json` is emitted. No proof, downstream-node, or theorem-completion credit is
claimed.
