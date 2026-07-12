# Statement validation record

Item: `S56-M-0770-STATEMENT`  
Base revision: `e3088372b5e523a6cfdb23d80c03e154fefa2f38`

## Frozen target

`Stage1Instances.THM_M_0770.ZornsLemmaTarget` quantifies over an arbitrary universe, a nonempty
type with a `PartialOrder`, and all nonempty chains in that type. If every such chain is
`BddAbove`, it concludes that some element satisfies `IsMax`. The checked theorem
`isMax_iff_no_strictly_larger` records that, under antisymmetry, this means every element above the
chosen element equals it. Thus the conclusion is maximality rather than existence of a greatest
element.

The sole direct import is `Mathlib.Order.Zorn`, the narrow pinned public module exporting the
selected `zorn_le_nonempty` interface. `PinnedMathlibSourceShape` copies that declaration's type
after specializing its `Preorder` parameter to the intake-selected `PartialOrder`, and
`zornsLemmaTarget_iff_pinnedMathlibSourceShape` checks the local identity definitionally. This is a
statement crosswalk only: the upstream proof body and transitive closure are left to anchor audit.

## Commands and results

Lean commands ran from `Formalizations/Lean` with the existing pinned Lake environment. No Lake
artifact or dependency was updated, fetched, cloned, or built.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0770/Statement.lean` | 0 | target, source-shape identity, maximality expansion, four mutations, the empty-carrier counterexample, and singleton boundary elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-0770/check_statement.py` | 0 | expression SHA-256 `e4f371f43c1ebee6f62e093d1102857b339c6e4bf70778ea18b1877fa43631fc`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Statement.lean lean-toolchain lake-manifest.json Mathlib/Order/Zorn.lean` (with the recorded paths) | 0 | hashes `2b6efe...70b6`, `651c8a...1d2`, `321626...d81`, and `706b55...e14c`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0770` | 0 | rank 579, planned, L0/rework-required, theorem incomplete |

## Mutation boundary

The validator compares fully explicit elaborated expressions and distinguishes removal of carrier
nonemptiness, weakening `PartialOrder` to `Preorder`, requiring bounds for the empty chain, and
strengthening maximality to a greatest element. The kernel additionally refutes the removed-
nonemptiness mutation using `Empty`; its nonempty-chain premise is vacuous but its conclusion would
construct an inhabitant. A singleton check exercises the included smallest carrier boundary.

This is statement-only evidence pending master acceptance. The incomplete repository metadata has
not been promoted to H0, and this node supplies no proof, anchor-audit, obligation-tree, validation,
release, audit-completion, or theorem-completion evidence.
