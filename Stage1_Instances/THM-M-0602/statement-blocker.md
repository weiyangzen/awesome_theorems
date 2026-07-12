# Exact-statement gate: blocked

Item: `S56-M-0602-STATEMENT`

Theorem: `THM-M-0602`

Base revision: `a755bddf3ef1127293a161eabda268d04a9877b3e`

## Decision

The exact Lean 4 target cannot be truthfully selected or elaborated from the accepted intake. The
repository source says only "simply connected h-cobordisms and diffeomorphism." The intake correctly
leaves open the selected primary-source theorem and page, whether the dimension bound applies to
the cobordism or its ends, which space bears the simple-connectivity hypothesis, the boundary and
collar conventions, and whether the conclusion is a diffeomorphism of the ends or a product
trivialization relative to one end. These choices change the proposition. Choosing the familiar
modern formulation without an accepted source crosswalk would invent missing mathematics.

The pinned mathlib snapshot also lacks the required formal surface. Its bordism module explicitly
says that bordisms are future work and currently defines only closed `SingularManifold` objects.
There is no bundled smooth cobordism with two identified boundary components, no predicate saying
that both boundary inclusions are homotopy equivalences, and no relative product-trivialization
interface. Pinned mathlib does separately expose simple-connectedness, abstract homotopy
equivalences, smooth diffeomorphisms, and manifold boundaries, but combining these unrelated APIs
with locally invented opaque fields would be a proxy statement rather than the exact theorem.

Therefore this phase emits no canonical declaration, elaborated-expression hash, checked
transport, or mutation claims. In particular, it does not weaken the result to mere existence of a
diffeomorphism between two arbitrary manifolds and does not put the desired product
diffeomorphism into a hypothesis. Machine status remains `M4`; theorem completion is false.

## Pinned infrastructure probe

`StatementInfrastructure.lean` checks only the nearest independent interfaces using four direct
imports:

```lean
import Mathlib.AlgebraicTopology.FundamentalGroupoid.SimplyConnected
import Mathlib.Geometry.Manifold.Bordism
import Mathlib.Geometry.Manifold.Diffeomorph
import Mathlib.Topology.Homotopy.Equiv
```

The probe prints the types of `SimplyConnectedSpace`, `ContinuousMap.HomotopyEquiv`,
`SingularManifold`, `Diffeomorph`, and `ModelWithCorners.boundary`. It declares no theorem, axiom,
proof, local model of cobordism, or substitute target, and receives no exact-statement credit.

The reused environment is Lean `4.29.0` (commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`) with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` and `lake-manifest.json`
SHA-256 values are respectively `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`
and `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
No update, build, clone, fetch, or dependency mutation was performed.

## Validation evidence

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai). Exact results are also appended
to `validation.md`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0602` | 0 | rank 640, planned, legacy artifacts unaccepted, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| pinned mathlib source search for h-cobordism/bordism APIs | 0/1 | no h-cobordism declaration; `Geometry/Manifold/Bordism.lean` documents bordisms as future work |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0602/StatementInfrastructure.lean` | 0 | all five pinned substrate declarations elaborated and printed their types |
| `git diff --check -- Stage1_Instances/THM-M-0602` | 0 | no whitespace errors |

## Gate result

First failed gate: exact canonical-claim/source identity. Even after source identity is accepted,
the missing pinned smooth-cobordism API remains a formalization blocker. Retry requires an immutable
primary-source theorem/page with reviewed assumptions and conventions, followed by kernel-checkable
definitions for a compact smooth cobordism, its ordered boundary identifications and inclusions,
the inclusion homotopy-equivalence conditions, and a relative product diffeomorphism.

Because the assigned statement phase is not complete, no `.stage1-worker-selftest.json` is emitted.
