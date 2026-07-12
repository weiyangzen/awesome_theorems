# Exact-statement gate: blocked

Item: `S56-M-1279-STATEMENT`  
Base revision: `ad0567008a38fc8c39deda009ab34e4ca9910f46`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the accepted intake and the source
material available to this worker. The intake identifies William Beckner, "Sharp Sobolev
Inequalities on the Sphere and the Moser--Trudinger Inequality," *Annals of Mathematics* 138
(1993), 213-242, but deliberately leaves the numbered result, formula, and normalization open.
The publisher metadata confirms the author, title, volume, issue, year, pages, and DOI
`10.2307/2946638`; it exposes no article text. The DOI/JSTOR PDF endpoint returned HTTP 403, and
OpenAlex reports no open full-text location. Thus this run did not inspect an accountable copy of
the theorem body.

The name and bibliographic metadata do not determine one proposition. In particular, they do not
decide among the sharp Sobolev family, its logarithmic/limiting form, and the higher-dimensional
exponential inequality, or freeze:

- the sphere dimension and whether it is restricted to even dimensions;
- normalized probability surface measure versus unnormalized area measure;
- the precise conformally invariant operator, its Laplacian sign, factorization, and constants;
- the smooth or completed Sobolev function domain and mean normalization;
- whether sharpness, equality cases, or extremizers are part of the root conclusion; or
- low-dimensional, constant-function, and other boundary cases.

These choices change both hypotheses and conclusion. Choosing a familiar formulation from memory,
or introducing an opaque parameter for the conformal operator or sharp constant, would substitute
or broaden the theorem. It would not satisfy the rev-5.6 exact-statement identity gate.
Consequently no canonical declaration, expression fingerprint, meaningful hypothesis/domain/
binder/boundary mutations, or minimal-import claim can be produced. Machine status remains `M4`.
No statement acceptance, proof, audit completion, or theorem completion is claimed.

## Pinned Lean boundary

`StatementInfrastructureProbe.lean` checks the closest basic pinned mathlib interfaces found for
the unit sphere as a metric subtype, the Haar-derived sphere measure, Bochner and lower integrals,
the real exponential, and Euclidean space. Its two direct imports are minimal only for this probe,
not for an unknown canonical target. The probe contains no theorem, axiom, assumed analytic
package, or replacement `Prop`, and receives no statement or proof credit.

A pinned-mathlib and repository formalization search found no occurrence of `Beckner`. Searches for
Moser-Trudinger terminology locate the distinct two-dimensional target `THM-M-1277`, not an exact
declaration for this sphere theorem. Mathlib's `Measure.toSphere` gives relevant measure
infrastructure, but no inspected API supplies the intrinsic conformal operator needed to resolve
the unknown source formula.

## Required unblock

An accountable source reviewer must provide a stable primary-source copy and select an exact
theorem/page (including all immediately referenced definitions), then freeze every domain,
normalization, operator, constant, binder, sharpness/equality clause, and degenerate case. A later
statement worker can transcribe that result, minimize its imports, elaborate and fingerprint the
canonical expression, and run structural mutations.

## Narrow validation evidence

Commands were run from this worker clone on 2026-07-12. The clone's `.lake` is the existing
canonical symlink; no update, build, clone, fetch, or dependency mutation was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1279` | exit 0; rank 450, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1279/StatementInfrastructureProbe.lean)` | exit 0; all six substrate declarations printed and elaborated; not exact-statement evidence |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'Beckner' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems --glob '*.lean'` | exit 1; no matching formal source occurrence |
| `git diff --check -- Stage1_Instances/THM-M-1279` | exit 0; no whitespace errors |

First failed gate: exact primary source-statement identity. The assigned phase is therefore not
self-tested or complete, so no `.stage1-worker-selftest.json` is emitted.
