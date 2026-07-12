# Exact-statement gate: blocked

Item: `S56-M-0596-STATEMENT`  
Theorem: `THM-M-0596`  
Base revision: `90108cd5d69f8d0a4b4ef314eb9ed5993526138d`

## Decision

The exact Lean 4 target cannot be truthfully selected or elaborated from the authoritative
repository material. The complete source wording is only `横截映射的通有性` ("genericity of
transverse maps"), attributed to Rene Thom in 1954. The accepted intake deliberately leaves the
formal statement open because this wording names a theorem family rather than one proposition.

In particular, the record does not select ordinary, parametric, jet, multijet, or relative
transversality. It does not fix the differentiability order, dimensions, compactness, boundary or
properness hypotheses; the embedded-submanifold conventions; the mapping-space topology; or
whether "generic" means residual, dense, open dense, or arbitrarily close approximation. These
choices change the domains, ordered binders, hypotheses, and conclusion. Selecting a familiar
modern formulation would invent missing mathematics, while taking transversality or genericity as
an opaque parameter would assume away the theorem.

The intake records Thom's 1954 paper and Hirsch's *Differential Topology* only as discovery
anchors. Neither has an accepted immutable edition, pinpoint theorem/page, exact transcription,
assumption and errata crosswalk, or independent source review. Consequently section 5 identity
fails before an exact human claim, canonical Lean expression, expression hash, minimal target
imports, checked alternate-form transport, or meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutations can be frozen.

## Pinned Lean boundary

`StatementInfrastructure.lean` uses two direct imports to check only independent substrate:

```lean
import Mathlib.Geometry.Manifold.Bordism
import Mathlib.Topology.Baire.Lemmas
```

It elaborates `ContMDiff`, `mfderiv`, the `residual` filter and `mem_residual`, and
`SingularManifold`. A scoped search of pinned mathlib's manifold sources found no transversality
predicate, transverse-map mapping-space locus, or genericity theorem. The only theorem-specific
hit is prose in `Mathlib.Geometry.Manifold.Bordism`: it says a transversality theorem would provide
an arbitrarily small transverse perturbation, but supplies no declaration. The probe therefore
declares no theorem, axiom, proxy predicate, or proof and receives no exact-statement credit.

The reused environment is Lean `4.29.0` (commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`), Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` and `lake-manifest.json`
SHA-256 values are respectively `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`
and `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. The canonical pinned
`.lake` artifact was reused read-only; no update, build, clone, or fetch was performed.

## Validation evidence

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0596` | 0 | rank 635, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version && lake --version && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the pinned versions and hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| pinned-mathlib `rg` search for transversality declarations and mapping-space topology | 0 | found two prose occurrences but no target predicate or theorem declaration |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0596/StatementInfrastructure.lean` | 0 | all five infrastructure declarations elaborated and printed their types |
| `git diff --check -- Stage1_Instances/THM-M-0596` | 0 | no whitespace errors |

## Gate result

First failed gate: exact canonical-claim/source identity, before Lean target elaboration. Machine
status remains `M4`; no statement acceptance, proof credit, audit completion, or theorem completion
is claimed. Retry requires an accountable reviewer to pin and inspect one exact source theorem,
freeze all variants and conventions listed above, and approve a binder-by-binder source crosswalk.
Only then can a statement run encode the missing transversality and mapping-space surfaces, minimize
imports, fingerprint the exact expression, and perform structural mutation tests.

Because the assigned statement phase is not complete, no `.stage1-worker-selftest.json` is emitted.
