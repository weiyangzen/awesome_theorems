# Lean 4 anchor audit

Item: `S56-M-0158-ANCHOR_AUDIT`  
Target: `Stage1Instances.THM_M_0158.WeingartenEquationsTarget`  
Audit date: 2026-07-12  
Worker base revision: `af0b9c3534733bf19ba3f83c1a063916aaac92fe`

## Audit boundary

This audit searched the repository, the complete checked-out source tree of pinned mathlib, and
credible public Lean differential-geometry candidates discovered through GitHub repository search.
Names were not treated as matches: in particular, `SciSolv/weingarten-lean` concerns Weingarten
calculus for random matrices, not the derivative of a surface normal. No exact theorem matching the
frozen local-coordinate target was found. This is a completed anchor inventory, not proof closure.

## Pinned mathlib

The immutable mathlib revision is
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, as recorded by
`Formalizations/Lean/lake-manifest.json` and confirmed by `git rev-parse HEAD` in the existing
package checkout. A case-insensitive source search over all `Mathlib/**/*.lean` and
`Archive/**/*.lean` found no differential-geometric declaration named or documented with
`Weingarten`, `shape operator`, `second fundamental form`, or `Gauss map`. The only
`second fundamental` hits concern the fundamental theorem of calculus.

Mathlib therefore supplies infrastructure rather than an exact anchor:

| Module / declaration family | Relevance | Exact-target status |
|---|---|---|
| `Analysis.Calculus.ContDiff.Comp` / `ContDiffWithinAt.fderivWithin_right_apply` | differentiability of coordinate partials | supporting API only |
| `Analysis.Calculus.FDeriv.Bilinear` / derivative rules for inner products | differentiate unit-normal and orthogonality identities | supporting API only |
| `LinearAlgebra.Matrix.NonsingularInverse` / `Matrix.mul_nonsing_inv`, `Matrix.nonsing_inv_mul` | solve the 2 by 2 Gram system | supporting API only |
| `Geometry.Manifold.Riemannian.Basic` and `Geometry.Manifold.Immersion` | nearby intrinsic/manifold infrastructure | no surface-normal equation |

`AnchorCandidates.lean` checks these declarations in the pinned environment and proves
`gram_inverse_probe`, showing that the frozen determinant hypothesis really reaches both matrix
inverse identities. The probe contains no `sorry`, axiom, or target proof.

## External Lean 4 candidates

All revisions below are full commit hashes returned by GitHub's commit API and were inspected from
commit-addressed source archives without adding or mutating a Lake dependency.

| Project and immutable revision | Toolchain / license | Inspection and classification |
|---|---|---|
| `qinz1yang/differential-geometry` @ `0f6734e222fd5e0b86c1ff02c2f5abde4c65e163` | Lean `v4.29.0`; Apache-2.0 | Closest candidate. `DifferentialGeometry/Geometry/Boundary/SecondFundamentalForm.lean` defines `chartCovariantDerivativeOfNormal`, `chartSecondFundamentalFormEntry`, and `secondFundamentalForm`, and proves only application and symmetry lemmas. It treats a boundary submanifold of a Riemannian manifold, accepts a chart normal extension, and does not prove the frozen Euclidean parametrized identity `dN = -(I^-1 II) dx`. Relevant module scan found no `sorry`, `admit`, `axiom`, `unsafe`, or `implemented_by`. **Related, not exact; anchor-only.** |
| `Shengrong-Wu/Differential-Geometry-Formalization` @ `e32a7aeec6061db8cfb24f8529c3ebd142ee5ad7` | Lean `v4.28.0`; Apache-2.0 | 152 Lean files; no hits for the exact theorem family (`Weingarten equation`, shape operator, second fundamental form, Gauss map). **No candidate.** |
| `jkanschik/differential-geometry-in-lean` @ `16e69eee1dc68b55aa6deff08fa6a6e1d0872161` | Lean `v4.19.0-rc3`; MIT | Two Lean files; no theorem-family hits. **No candidate.** |
| `peabrainiac/lean-catdg` @ `1ee4a2614b033dd1b4aded95759eb31eb9b0fbf4` | commit tree inspected | Categorical/diffeological geometry modules, with no surface extrinsic-geometry module in the complete commit tree. **No candidate.** |
| `SciSolv/weingarten-lean` @ `d05734050342e795eda750122a7279e1a629da4a` | Lean `v4.31.0`; Apache-2.0 | Fifteen Lean files formalizing random-matrix Weingarten functions and Gram elements. Same proper name, different theorem. **Explicitly excluded.** |

The closest external module cannot close even a transport obligation: its domain, geometric object,
definition of the second fundamental form, and conclusion differ from the frozen target, and it has
no theorem deriving a normal derivative from an inverse first-fundamental-form matrix. It is not a
pinned project dependency. Consequently there is no `repo_local_integration_debt` from a discovered
exact upstream proof; the remaining debt is `formalization_debt`.

## Exact commands and results

Commands ran from the repository root unless a `cwd` is stated.

| Command | Exit | Result |
|---|---:|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i "weingarten\|shape operator\|shapeOperator\|second fundamental\|secondFundamental\|gauss map\|gaussMap" Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/.lake/packages/mathlib/Archive --glob '*.lean'` | 0 | four unrelated fundamental-calculus prose hits; no geometry anchor |
| GitHub repository searches for `lean4 differential geometry`, `Weingarten Lean`, `shape operator Lean4`, `Gauss map Lean4`, and `differential geometry language:Lean` | 0 | candidate set above; grep.app code search returned HTTP 429 and was not credited |
| `curl .../repos/<owner>/<repo>/commits/HEAD` and `curl .../repos/<owner>/<repo>/tarball/<full-sha>` for the listed candidates | 0 | commit-addressed archives downloaded to `/tmp` for read-only inspection |
| `rg -n -i 'weingarten equation\|shape.?operator\|second.?fundamental.?form\|gauss.?map' <candidate trees> --glob '*.lean'` | 0/1 | only the qinz1yang second-fundamental-form family matched; exit 1 means no match for the other trees |
| `rg -n '\bsorry\b\|\badmit\b\|\baxiom\b\|unsafe\|implemented_by' .../SecondFundamentalForm.lean` | 1 | no placeholder or oracle boundary in the relevant external module |
| `lake env lean ../../Stage1_Instances/THM-M-0158/AnchorCandidates.lean` (cwd `Formalizations/Lean`) | 0 | API checks and determinant-to-inverse probe elaborated |
| `lake env lean ../../Stage1_Instances/THM-M-0158/Statement.lean` (cwd `Formalizations/Lean`) | 0 | canonical target still elaborates |
| `python3 ../../Stage1_Instances/THM-M-0158/check_statement.py` (cwd `Formalizations/Lean`) | 0 | canonical expression hash unchanged; four mutations remain distinguished |
| `git diff --check -- Stage1_Instances/THM-M-0158` | 0 | no whitespace errors |

## Verdict and status boundary

The node-specific anchor audit is self-tested and ready for master review. The result is negative
for exact theorem closure and positive for a usable pinned mathlib infrastructure inventory. It
does not alter the planned lifecycle, does not establish `H0`, does not prove the theorem, and does
not authorize the obligation-tree, proof, validation, release, or theorem-completion nodes.
