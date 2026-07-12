# Lean anchor audit

Item: `S56-M-0651-ANCHOR_AUDIT`  
Base revision: `3dfb8575e8f56f817e48b9846f7ff2fbd146b603`

## Exact comparison target

All candidates were compared with
`Stage1Instances.THM_M_0651.OmittingTypesTarget`, expression SHA-256
`789c281a89ba5947476cb2189ae3e216de0eeaa0b5d016549489d8c1553d8c43`.
The target uses pinned mathlib first-order semantics, a satisfiable theory, a Nat-indexed family of
varying finite arities, local partial-type and nonprincipality predicates, and asks for an
at-most-countable model omitting every family member. A name or broadly similar theorem was not
treated as an exact anchor.

## Pinned mathlib

The immutable mathlib input is commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`, under Lean 4.29.0. A scoped search of every Lean file
under `Mathlib/ModelTheory` found no occurrence of omitting-types terminology, model-theoretic
nonprincipality, or partial types. Thus there is no direct declaration candidate in this snapshot.

The nearest real declarations are infrastructure, not closure:

| Declaration | Usable role | Why it does not close the target |
|---|---|---|
| `Theory.isSatisfiable_iff_isFinitelySatisfiable` | compactness | does not construct a model meeting countably many omission requirements |
| `Theory.CompleteType.exists_modelType_is_realized_in` | complete-type/model bridge | realizes one complete type, the opposite direction from omission |
| `Language.exists_elementarySubstructure_card_eq` | cardinal control | can reduce an existing suitable model, but does not first produce one omitting the types |

`Types.lean` explicitly records a TODO to connect complete types to sets of formulas. The target's
local representation supplies that missing statement-level encoding, but no pinned theorem bridges
nonprincipality to simultaneous omission.

## External Lean 4 candidates

The strongest located candidate is
`FirstOrder.Language.omitting_types` in
`cameronfreer/infinitary-logic`, module
`InfinitaryLogic.Methods.Henkin.Completeness`, frozen at commit
`3f3a920f45117c7ff2e50e0af137ab779b009fa8`, tree
`6affba7d9ca14375003e1f1f0c8f103cc572649b`. The file is Git blob
`277372417de825a4798675a627d6ce86dc59cebf`, SHA-256
`c41efef1e6941c2d85757dad99b3c3556daa3421819519f5b15fa468edd38a58`.
Its terminal theorem has a proof body and its file contains none of `sorry`, `admit`, `axiom`,
`unsafe`, `implemented_by`, or `opaque`.

It is not an exact candidate. It works in a separate `Lomega1omega` implementation with
`Theoryomega` and `Formulaomega`, treats unary types only, indexes the family by a `Set`, and states
non-isolation through its own consistency-property API. No checked semantic transports to the
pinned mathlib `Theory`, finite-arity `Formula`, or local `IsNonprincipal` exist. It also requires
Lean `v4.32.0-rc1`, mathlib `360da6fa...`, and LeanArchitect, whereas this target is pinned to Lean
4.29.0 and mathlib `8a178386...`. It is therefore a proof-architecture reference, not an imported
body or `M0` anchor.

Two other credible public Lean logic repositories were inspected at immutable heads:

| Project | Commit / tree | Result |
|---|---|---|
| `FormalizedFormalLogic/Foundation` | `87d4dd68...` / `93152b3b...` | no matching omitting-types, partial-type, or nonprincipal text in Lean/Markdown sources |
| `Mathias-Stout/Many-sorted-model-theory` | `af0c20fa...` / `a3be52bf...` | no matching text in Lean/Markdown sources |

The public repository search is discovery evidence rather than a claim about all possible private
or future projects. The immutable candidates actually identified above are fully classified in
`anchor-audit.json`.

## Validation

Commands ran in the worker clone without updating, fetching, or modifying `.lake`.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0651/Statement.lean` | 0 | exact frozen target and checked omission transport still elaborate |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD^{commit} HEAD^{tree}` | 0 | `8a178386...`; `bdc39a31...` |
| scoped `rg` over pinned `Mathlib/ModelTheory` for omitting types, nonprincipality, and partial types | 1 | no matches; exit 1 is the expected no-match result |
| GitHub commit/tree API plus archive scan for the three external projects | 0 | immutable identities and candidate/no-candidate classifications reproduced |
| `python3 -m json.tool Stage1_Instances/THM-M-0651/anchor-audit.json` | 0 | structured audit is valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets accepted |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets accepted |
| `python3 scripts/stage1_target.py show THM-M-0651` | 0 | rank 697, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0651` | 0 | no whitespace errors |

## Verdict and boundary

The anchor inventory is self-tested and ready for master review. No exact mathlib or external Lean
4 closure was found; the canonical root remains `M4`. The first open bridge is the actual
countable Henkin/Baire construction proving simultaneous omission in the pinned mathlib semantics.
This audit does not prove the theorem, accept a source at `H0`, complete the overall audit, or alter
any master-owned state.
