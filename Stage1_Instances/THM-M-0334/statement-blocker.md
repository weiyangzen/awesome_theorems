# Exact-statement gate: blocked

Item: `S56-M-0334-STATEMENT`  
Base revision: `106084d7f6343f3046dfb9e108503edbcdc86191`

## Decision

The repository record does not identify an exact mathematical proposition, so the requested Lean
4 target cannot be truthfully selected or elaborated. Its complete wording is only
`冯·诺依曼代数的分类` ("classification of von Neumann algebras"), attributed to Francis Murray
and John von Neumann in 1936. The record supplies no theorem number, page, definitions, hypotheses,
or conclusion. The manifest's `已验证` field is explicitly untrusted metadata under rev-5.6.

As frozen by intake, the wording could denote at least:

1. the exclusive and exhaustive division of factors into types I, II, and III;
2. the refined division into `I_n`, `I_infinity`, `II_1`, `II_infinity`, and III;
3. a central decomposition theorem for an arbitrary von Neumann algebra; or
4. a historical package of definitions and several results rather than one theorem.

These choices differ in domain, quantifiers, factor and center hypotheses, projection-equivalence
and finiteness conventions, separability assumptions, boundary cases, and conclusions. Selecting
one from the title would invent or substitute mathematics. A tautological theorem that assumes a
type tag, or a theorem merely defining type predicates, would also weaken the classification claim.

The candidate source named by intake, Murray and von Neumann's *On Rings of Operators* (1936), has
not been pinned to an immutable copy and exact theorem/page with an accepted definition and errata
crosswalk. Consequently there is no canonical human claim from which to freeze ordered binders,
hypotheses, conclusion, alternate transports, or meaningful removed-hypothesis, domain, binder-
scope, and boundary mutations. Section 5's canonical-claim identity gate therefore fails before
the Lean expression and expression fingerprint gates.

## Pinned Lean boundary

The existing `IntakeProbe.lean` uses the smallest identified import:

```lean
import Mathlib.Analysis.VonNeumannAlgebra.Basic
```

It elaborates `WStarAlgebra`, `VonNeumannAlgebra`, the concrete commutant, and star-projection APIs.
The pinned module says that foundational work remains, including the relationship between its
abstract and concrete notions, and the scoped local search found no type-I/type-II/type-III
classification API. The successful probe is only an encoding-substrate check. It is not a
canonical target, theorem statement, or proof.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The canonical `.lake` artifact was reused read-only;
no dependency update, build, clone, or fetch was performed.

## Validation evidence

Commands were run from the worker clone on 2026-07-12.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0334` | exit 0; rank 827, lifecycle `planned`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean version and commit match the pinned environment above |
| `(cd Formalizations/Lean && lake --version)` | exit 0; Lake version matches the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib revision matches the value above |
| `(cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json)` | exit 0; hashes `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0334/IntakeProbe.lean)` | exit 0; all six API checks elaborated |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0334 -g '*.lean'` | exit 1, expected no-match result; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0334` | exit 0; no output |

## Gate result

First failed gate: section 5 exact canonical-claim identity. Machine status remains `M4`; no
statement credit, proof credit, audit completion, theorem completion, or accepted checklist state
is claimed. Retry requires an accountable source reviewer to pin and transcribe one exact primary
result and freeze the presentation of the algebra, factor/general-algebra scope, type definitions
and refinements, all assumptions, ordered binders, conclusion, and degenerate cases.

Because the assigned statement phase is not genuinely complete, no
`.stage1-worker-selftest.json` is emitted.
