# Exact-statement gate: blocked

Item: `S56-M-0597-STATEMENT`

## Decision

The exact tubular-neighborhood target cannot be truthfully elaborated against
the pinned mathlib revision. The intake claim requires all of the following to
be connected in one proposition:

- a finite-dimensional smooth Riemannian ambient manifold;
- a smoothly embedded submanifold;
- the metric-orthogonal normal bundle of that submanifold, including its smooth
  total-space manifold structure and zero section;
- open neighborhoods of the zero section and embedded image; and
- a smooth diffeomorphism between those neighborhoods that agrees with the
  original embedding on the zero section.

The pinned library supplies Riemannian tangent bundles, smooth embeddings, and
generic manifold diffeomorphisms, but it does not supply a bundled embedded
submanifold or its normal bundle. A repository-wide search of the pinned
`Mathlib` tree found no tubular-neighborhood declaration and no normal-bundle
construction for an embedded submanifold. In particular, there is no canonical
normal-bundle total space with the topology and charted-manifold instances
needed to instantiate `Manifold.Diffeomorph` on an open neighborhood.

Adding an arbitrary vector bundle and a proposition saying that it is the
normal bundle would introduce extra input and leave the essential geometric
identification unchecked. Replacing smooth diffeomorphism by an equivalence,
homeomorphism, retraction, or unconstrained `Prop` field would weaken the
conclusion. Neither is the exact intake claim.

The historical
`AwesomeTheorems.Stage1.S1_M_253.StatementShape` was inspected only as
discovery input. Its `hasSmoothNormalBundleModel`,
`normalBundleSplittingData`, `smoothOnDomain`, and
`diffeomorphsDomainOntoNeighborhood` members are bare proposition-valued
stand-ins. Its result is therefore not an exact encoding and receives no
rev-5.6 statement or proof credit.

## Lean boundary checked

`StatementProbe.lean` uses only these direct imports:

```lean
import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.Geometry.Manifold.SmoothEmbedding
```

It elaborates checks for `IsRiemannianManifold`, `Bundle.RiemannianBundle`,
`IsContMDiffRiemannianBundle`, `Manifold.IsSmoothEmbedding`, `TangentSpace`,
`Bundle.TotalSpace`, and `Diffeomorph`. These are independent
substrates, not a substitute formal target. The environment is the existing
pinned Lean/mathlib installation; no dependency update, build, fetch, or clone
was performed.

Base revision: `3ec252ff03162db067bf77973c0a74a97d4bbe0a`.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0597/StatementProbe.lean` | 0 | all seven pinned substrate declarations elaborated and their types printed |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && rg -ni 'tubular\|normal bundle\|normalBundle' .lake/packages/mathlib/Mathlib` | 1 | no matches in the pinned mathlib source tree (`rg` exit 1 means no matches) |
| `sha256sum Stage1_Instances/THM-M-0597/StatementProbe.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | probe `fb79f333...19ea6`, toolchain `651c8acc...d2`, manifest `321626c8...b2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0597` | 0 | rank 253, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `rg -n '\bsorry\b\|\baxiom\b\|placeholder\|fake result' Stage1_Instances/THM-M-0597/StatementProbe.lean` | 1 | no forbidden proof-gap declarations (`rg` exit 1 means no matches) |
| `git diff --check -- Stage1_Instances/THM-M-0597 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Gate result and retry condition

First failed gate: rev-5.6 section 5 exact-statement identity. The canonical
formal target remains absent, so there is no honest elaborated-expression hash,
transport, or mutation suite. Machine status remains `M4`, and the theorem is
not complete. Retry when a pinned dependency supplies a smooth embedded-
submanifold normal-bundle construction (including the total-space manifold and
zero section), or after that infrastructure is implemented and kernel-checked
as its own prerequisite. No `.stage1-worker-selftest.json` is emitted because
the assigned statement phase is blocked rather than complete.
