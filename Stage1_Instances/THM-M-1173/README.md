# THM-M-1173 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the De Giorgi-Nash interior regularity
theorem. The metadata label `已验证` is untrusted discovery input and supplies no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root family | Interior local Holder continuity of weak solutions of a uniformly elliptic, divergence-form, second-order scalar equation with bounded measurable coefficients | The source metadata does not choose dimension, domain, homogeneous/inhomogeneous equation, or quantitative estimate; the statement phase must choose them from a primary theorem rather than invent them |
| Domain | An open subset of Euclidean space, with estimates on balls compactly contained in it | Boundary regularity and non-Euclidean domains are excluded |
| Operator | Scalar divergence form, schematically `div (A(x) grad u) = 0`, with bounded measurable uniformly elliptic coefficients | Systems, non-divergence form, degenerate ellipticity, and lower-order terms are excluded |
| Solution notion | Sobolev weak solution | Classical-solution and viscosity-solution substitutions are excluded |
| Conclusion | A locally Holder-continuous representative, normally accompanied by an oscillation or Holder-seminorm estimate | Harnack inequalities, local boundedness, and Moser iteration are supporting results or neighboring targets, not substitutes for the root |
| Lean surface | A future exact expression using pinned mathlib measure/Sobolev/PDE APIs | No repo-local declaration or elaboration is credited at intake |
| Foundations | Lean 4 kernel plus a versioned classical/choice/quotient policy | Exact toolchain, imports, axioms, and dependency closure remain open |

The name denotes a theorem family rather than one uniquely quantified proposition. The statement
phase therefore has a hard requirement to select and pinpoint one primary-source theorem, freeze
all constants and binders, and demonstrate that it is the intended scalar homogeneous interior
claim. Broadening to systems or weakening the conclusion to mere local boundedness is forbidden.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed gate is exact
statement identification: the repository metadata is too terse to determine a unique canonical
formal target. This intake records that ambiguity instead of silently choosing a convenient
theorem. No theorem, source-fidelity, or machine-closure claim is made.

## Validation

The exact intake-only checks and results are recorded in `validation.md`. They establish target
membership, repository-standard consistency, JSON syntax, and dossier-local structure only.

