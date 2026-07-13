# Scope map

## Received claim

The repository root is only `闭线性算子的连续性` ("continuity of closed linear operators"), attributed
to Stefan Banach in 1932. It contains no formula or citation. Intake therefore freezes the literal
gloss and its omissions rather than choosing a familiar theorem by convention.

## Candidate classical boundary

The closest standard interpretation is: an everywhere-defined linear map between Banach spaces has
a continuous underlying function if its graph is closed in the product topology. Every component
below remains a statement-phase decision, not an intake assertion of exact source identity.

| Scope dimension | Candidate standard form | Material alternatives still open |
|---|---|---|
| operator domain | total linear map on all of `E` | closed partial or densely defined operator, closed relation |
| spaces | Banach domain and codomain | F-spaces, Frechet spaces, barrelled/topological vector spaces, one-sided completeness |
| scalars | real or complex | arbitrary nontrivially normed field as in the pinned mathlib generalization |
| graph | `{(x, g x) | x in E}` closed in `E × F` | sequential closedness, net/filter closedness, partial-domain graph |
| conclusion | `Continuous g` | existence of a bound, construction of `E ->L[𝕜] F`, local continuity |
| theorem direction | closed graph implies continuity | converse, iff package, contrapositive, sequential criterion |

## Boundary cases

The later statement gate must explicitly resolve:

- zero, trivial, finite-dimensional, real, complex, and generalized scalar spaces;
- empty/trivial types where typeclass hypotheses permit them;
- zero and identity maps;
- a graph closed because the domain is total versus a graph over a proper or dense submodule;
- failure when completeness of either space is removed;
- product norm topology versus an unspecified or weaker product topology;
- continuity of the coerced function versus boundedness or a bundled continuous-linear-map output;
- whether sequential closedness is equivalent in the selected metrizable setting.

No degenerate case is excluded at intake.

## Pinned Lean boundary

The direct candidate type, rendered schematically, is:

```lean
{𝕜 : Type*} [NontriviallyNormedField 𝕜]
{E : Type*} [NormedAddCommGroup E] [NormedSpace 𝕜 E] [CompleteSpace E]
{F : Type*} [NormedAddCommGroup F] [NormedSpace 𝕜 F] [CompleteSpace F]
(g : E ->ₗ[𝕜] F)
(hg : IsClosed (g.graph : Set (E × F)))
⊢ Continuous g
```

This type is a strong exact-topic candidate, not the frozen canonical target. It makes the missing
catalogue assumptions visible. `LinearMap.graph` is the total graph; `LinearPMap.graph` ranges over
an explicit domain submodule, and `LinearPMap.IsClosed` merely asserts that partial graph is closed.

## Explicit exclusions

The following do not satisfy or replace the received root without a source-approved checked
transport:

- the Banach open mapping theorem, inverse mapping theorem, or uniform boundedness principle;
- closed range, closed kernel, closed embedding, or completeness of the graph alone;
- the converse that a continuous map into a Hausdorff space has closed graph;
- a theorem only for finite-dimensional spaces, bounded operators, symmetric operators, or one
  special scalar field;
- a closed partially defined/unbounded operator asserted to be continuous on the ambient space;
- the sequential criterion or `ContinuousLinearMap.ofIsClosedGraph` used as an unreviewed substitute;
- the untrusted `已验证` label, theorem name, API probe, or source URL used as proof credit.

The intake boundary is `[H1, M3, R4]`, planned, with no accepted state. All proof architecture,
source review, target elaboration, anchor/provenance audit, and release work remains downstream.
