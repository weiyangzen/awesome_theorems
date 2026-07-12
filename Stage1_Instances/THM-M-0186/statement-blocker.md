# Exact-statement gate: blocked

Item: `S56-M-0186-STATEMENT`  
Theorem: `THM-M-0186`  
Base revision: `a4bbd6c3e4f1700d25c878fa90640754d2e64444`

## Decision

The intake freezes the human claim: every smooth immersion of the two-torus into Euclidean
three-space has Willmore energy at least `2*pi^2`, with scalar mean curvature normalized by
`H = (k1 + k2) / 2` and energy given by the induced-area integral of `H^2`. That claim cannot yet
be expressed exactly in the repository-pinned Lean environment.

Pinned mathlib supplies smooth-manifold immersions and basic Riemannian-manifold vocabulary, but the
scoped source inspection found no immersed-surface construction of the induced metric, second
fundamental form, principal or scalar mean curvature, induced area measure, or Willmore functional.
The absence is material, not merely a missing theorem name: these constructions tie both sides of
the inequality to the quantified immersion and fix the normalization responsible for the constant.

Declaring an arbitrary `meanCurvature`, `areaMeasure`, or `willmoreEnergy`, or accepting their
relationship to the immersion as hypotheses, would erase the defining differential geometry and
reduce the target to an assumed or unrelated real inequality. Restricting to embeddings, minimal
surfaces in `S^3`, or the weaker `4*pi` bound would substitute a different theorem. No such
surrogate, axiom, placeholder, or declaration was introduced. Machine state remains `M4`, and no
statement or theorem completion is claimed.

## Pinned boundary

`StatementInfrastructure.lean` uses only
`Mathlib.Geometry.Manifold.Immersion` and
`Mathlib.Geometry.Manifold.Riemannian.Basic`. It checks `Manifold.IsImmersion`,
`IsRiemannianManifold`, `TangentSpace`, `MeasureTheory.integral`, and `Real.pi`, then uses
`#check_failure` for representative missing curvature and Willmore identifiers. It is substrate
evidence only and receives no canonical-statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The existing `.lake` artifacts were read only; no
update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0186` | 0 | rank 673, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| pinned-mathlib `rg` search for Willmore, Clifford torus, mean/principal curvature, second fundamental form, and shape operator | 1 | no matching immersed-surface API (`rg` exit 1 means no match) |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0186/StatementInfrastructure.lean` | 0 | the five available substrate checks and four expected missing-identifier checks elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0186/statement-blocker.json` | 0 | blocker JSON is syntactically valid |
| `git diff --check -- Stage1_Instances/THM-M-0186` | 0 | no whitespace errors |

## Retry condition

Resume after dependency-legal implementation or immutable pinned integration of a concrete smooth
torus, its compact boundaryless structure, the immersion-induced metric and area, second
fundamental form and normalized scalar mean curvature, and a Willmore functional definition tied
to those objects. The exact source assumptions and conventions must then receive independent
review. A later statement run can elaborate and fingerprint that same claim, check all transports,
and execute the required removed-hypothesis, changed-domain, binder-scope, and boundary mutations.

This is the first failed gate. The assigned phase is not genuinely self-tested, so no
`.stage1-worker-selftest.json` is emitted.
