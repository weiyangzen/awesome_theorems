# Exact-statement gate: blocked

Item: `S56-M-1194-STATEMENT`  
Theorem: `THM-M-1194`  
Base revision: `31b7ab5b3902c4a80878c2007218f90566a8b85c`

## Decision

The primary source can now be identified, but its main tensor inequality cannot be elaborated as
an exact Lean 4 proposition using the pinned repository environment. No `Statement.lean` is
emitted: replacing the missing differential-geometric notions by arbitrary functions or by a
record whose fields assume the desired semantics would be a substituted theorem, not exact
statement evidence.

The source is Richard S. Hamilton, *A matrix Harnack estimate for the heat equation*,
*Communications in Analysis and Geometry* **1** (1993), no. 1, 113-126,
DOI `10.4310/cag.1993.v1.n1.a6`. The repository gloss "matrix Li-Yau inequality" identifies the
favorable-geometry clause of the paper's Main Theorem on pages 113-114: on a compact Riemannian
manifold, for a positive solution `f` of the heat equation for `t > 0`, if Ricci is parallel and
sectional curvature is weakly positive, then for every vector field `V` the symmetric two-tensor

```text
D_i D_j f + (f / (2 t)) g_ij + D_i f V_j + D_j f V_i + f V_i V_j
```

is weakly positive. The paper also states a separate general-geometry error-term estimate. That
second clause is not silently folded into the target selected by the repository's singular
"matrix Li-Yau inequality" gloss.

The checked mathlib revision has basic Riemannian-manifold and covariant-derivative
infrastructure, and a Euclidean-space Laplacian, but the scoped search found no source-level API
combination for all of the following root binders and predicates:

- a compact smooth Riemannian manifold with the paper's Levi-Civita connection conventions;
- sectional curvature and its pointwise nonnegativity;
- the Ricci tensor and its vanishing covariant derivative;
- the manifold Laplace-Beltrami operator and a time-dependent positive heat solution;
- the covariant Hessian of a scalar function and positive-semidefinite order on the resulting
  symmetric covariant two-tensor.

The Euclidean `InnerProductSpace` Hessian/Laplacian cannot substitute for the manifold theorem:
doing so removes the curvature hypotheses and changes the domain. Likewise, quantifying over
uninterpreted `laplacian`, `hessian`, `ricciParallel`, and `sectionalCurvatureNonnegative` fields
would elaborate only an arbitrary interface and would not freeze Hamilton's claim. Therefore
minimal imports, an explicit expression fingerprint, checked transports, and meaningful mutation
tests cannot yet be produced. Machine status remains `M4`; no statement, proof, audit-completion,
or theorem-completion credit is claimed.

## Pinned environment and validation

Validation date: 2026-07-12 (Asia/Shanghai). Commands ran in this worker clone. Existing `.lake`
artifacts were only read; no update, build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1194` | 0 | rank 388, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |
| pinned-mathlib `rg` search for heat equation, matrix Harnack, sectional curvature, parallel Ricci, Hessian, and Laplacian | 0 | 216 textual hits, principally Euclidean Laplacian and basic manifold infrastructure; no Hamilton-target declaration or complete statement API |
| `git diff --check -- Stage1_Instances/THM-M-1194` | 0 | no whitespace errors before this artifact was added |

There is no applicable `lake env lean <target>.lean` command because the exact target cannot be
formed in this environment. Elaborating a weakened Euclidean target or an assumed abstract
interface would be fake validation.

## Retry condition

Unblocking requires pinned Lean definitions (or a pinned compatible dependency) for the
Levi-Civita Hessian, Laplace-Beltrami heat equation, sectional and Ricci curvature predicates, and
positive-semidefinite symmetric two-tensors, with conventions crosswalked to pages 113-114 of the
paper. A later statement run must then encode the displayed inequality with the source's ordered
binders, minimize imports, print and hash the expression, check an equivalent tensor formulation,
and mutation-test compactness, positivity, heat evolution, parallel Ricci, sectional curvature,
time positivity, and tensor order.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
