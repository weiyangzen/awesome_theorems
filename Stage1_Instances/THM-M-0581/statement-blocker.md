# Exact-statement gate: blocked

Item: `S56-M-0581-STATEMENT`  
Theorem: `THM-M-0581`  
Base revision: `7f7539be2690c4075e12d47f531aae8b181f4944`

## Decision

The exact Lean 4 target cannot yet be truthfully selected and elaborated. The intake freezes the
broad classical geometrization claim, but explicitly leaves unresolved which precise primary-source
formulation controls the root. In particular, it does not fix whether the conclusion is stated for
interiors of compact pieces, for irreducible prime components, or after a combined sphere-and-torus
cut; nor does it fix finite-volume and boundary behavior, canonicity up to isotopy, or the treatment
of exceptional Seifert pieces.

Those are proposition-changing choices, not notation. They determine the domains, ordered binders,
hypotheses, conclusion, and boundary cases. The candidate Thurston paper has not been accepted with
an immutable edition, exact theorem/page, wording, assumptions, corrections, and independent
source review. Selecting one conventional textbook formulation would therefore invent the missing
source identity. The intake's provisional state `M4` is still accurate.

The formal object model is independently unresolved. The pinned mathlib snapshot has general
manifold and Poincare-statement infrastructure, but the scoped search found no concrete APIs for
prime decomposition of 3-manifolds, JSJ cutting along incompressible tori, the eight Thurston model
geometries, or geometric structures on the resulting pieces. Defining abstract predicates or a
package whose fields assert these conclusions would assume rather than encode the theorem. The
legacy `S1_M_128.lean` does exactly that with `GeometrizationPackage`, so it receives no statement
credit and is not reused.

Consequently there is no canonical Lean expression, expression hash, minimal import set for that
expression, checked alternate-form transport, or meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutation suite. No weakened Poincare or hyperbolization special case,
abstract assumed interface, axiom, placeholder, or broadened theorem was introduced.

## Pinned Lean boundary

`StatementProbe.lean` imports the nearest pinned three-manifold statement module:

```lean
import Mathlib.Geometry.Manifold.PoincareConjecture
```

It elaborates only checks for the charted-manifold, compactness, connectedness, and adjacent
three-dimensional Poincare surfaces. This proves that the pinned toolchain and that substrate are
usable. It is not an encoding of geometrization and supplies no root proof credit.

The environment uses `leanprover/lean4:v4.29.0`, Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The worker reused the canonical pinned `.lake`
artifact read-only. No update, build, clone, fetch, or dependency mutation was performed.

## Validation evidence

Commands ran in this worker clone on 2026-07-12.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0581` | 0 | Rank 623, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository and pinned-mathlib `rg` searches for geometrization, Thurston, JSJ, prime decomposition, incompressible tori, and locally homogeneous geometry | 0 | Found only legacy abstract bookkeeping and prose; no concrete geometrization target API |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0581/StatementProbe.lean` | 0 | The adjacent pinned manifold/Poincare substrate elaborated |
| `git diff --check -- Stage1_Instances/THM-M-0581` | 0 | No whitespace errors |

The top-level `lake --version` probe failed because that directory has no default toolchain; this is
not a Lean blocker because the required project-scoped `cd Formalizations/Lean && lake env ...`
commands use the pinned `lean-toolchain` and pass.

## Retry condition

An accountable source review must first select and inspect an immutable primary-source formulation,
including pinpoint wording, assumptions, corrections, and the decomposition, boundary, volume,
canonicity, and exceptional-piece conventions. A later statement run must then implement concrete
Lean interfaces for every semantic component (or identify pinned interfaces that already do so),
elaborate and fingerprint the exact expression with minimized imports, compile all credited
transports, and run the four required structural mutations.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
