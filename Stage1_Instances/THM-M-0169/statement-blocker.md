# Exact-statement gate: blocked

Item: `S56-M-0169-STATEMENT`  
Theorem: `THM-M-0169`
Base revision: `4db87ed5646981780f2e885e21052d997afd1be7`

## Decision

The exact Lean 4 target cannot yet be truthfully selected from the intake dependency. The repository
claim says that a complete surface of constant negative curvature cannot be isometrically immersed
in Euclidean three-space, but the intake deliberately leaves the proposition's decisive choices
open. In particular, it has not accepted Hilbert's analytic-surface formulation or a modern smooth
or `C^2` Riemannian-manifold formulation; the precise regularity of the surface and map; the bridge
from Hilbert's finite-accumulation condition to metric or geodesic completeness; connectedness and
boundary conventions; or normalization at curvature `-1` versus all negative constants.

Those choices are not cosmetic. They change the domain and hypotheses and require source theorems
for any regularity strengthening. Selecting the familiar modern formulation would invent the
source-equivalence bridge that `source_statement_crosswalk.md` explicitly marks unproved. Selecting
Hilbert's coordinate formulation instead would require freezing his analytic-surface and global
accumulation definitions, which the dossier has also not done. Therefore no canonical ordered
binders, hypotheses, conclusion, degenerate cases, expression fingerprint, checked alternate-form
transport, or meaningful section 5.1 mutations can be emitted.

## Pinned Lean boundary

`StatementInfrastructure.lean` uses the nearest two direct pinned imports:

```lean
import Mathlib.Geometry.Manifold.Immersion
import Mathlib.Geometry.Manifold.VectorBundle.Riemannian
```

The probe checks that pinned mathlib exposes `Manifold.IsImmersion`, Riemannian vector-bundle
structures, the `Fin 3 -> Real` Euclidean carrier, and the generic topological `CompleteSpace`
class. A scoped search of
the pinned `Mathlib` tree found no `GaussianCurvature`, `sectionalCurvature`,
`IsometricImmersion`, induced/pullback Riemannian metric, or Riemannian-manifold completeness API.
The Riemannian module describes smooth inner products on vector bundles; it does not construct the
Levi-Civita connection or curvature needed by the theorem. Thus the currently pinned environment
also lacks the semantic interfaces for a non-placeholder exact target.

Encoding curvature, isometry, or completeness as arbitrary predicate parameters would merely hide
the missing mathematics. It would broaden the models and assume interfaces rather than state
Hilbert's theorem, so no such proxy is introduced. The probe declares no theorem, axiom, proof, or
canonical target and receives no exact-statement credit.

## Gate result

First failed gate: exact canonical-claim identity and source-faithful regularity/completeness
selection, before Lean expression elaboration. Machine status remains `M4`; statement acceptance,
proof credit, audit completion, and theorem completion are false. Retry requires an accountable
source review that freezes one exact theorem and its assumptions, followed by an implementation or
immutable dependency providing the missing curvature and isometric-immersion interfaces.

Because the assigned statement phase is not genuinely complete, no
`.stage1-worker-selftest.json` is emitted.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). Lean reused the canonical pinned
`.lake` artifact; no update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0169` | 0 | rank 666, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0169/StatementInfrastructure.lean` | 0 | all five pinned infrastructure declarations elaborated and printed their types |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-0169/StatementInfrastructure.lean` | 0 | digests `651c8a...1d2`, `321626...d81`, and `905b68...14e` |
| `python3 -m json.tool Stage1_Instances/THM-M-0169/statement-blocker.json >/dev/null` | 0 | structured blocker is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0169` | 0 | no whitespace errors |
