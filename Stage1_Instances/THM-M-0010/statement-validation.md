# Statement validation record

Item: `S56-M-0010-STATEMENT`  
Base revision: `9e3fd02a2a952da7031bb1dd61387443dd4c1cc7`

## Frozen target

`Stage1Instances.THM_M_0010.ArtinReesTarget` is the exact intake-selected equality for an ideal of
a commutative Noetherian ring and a submodule of a finite module. The target preserves separate
universes for the ring and module, the existential `k` before universal `n`, the `k <= n` guard,
natural subtraction, ideal action on submodules, and equality rather than containment. Its sole
direct import is `Mathlib.RingTheory.Filtration`, the module exporting the pinned declaration.

`PinnedMathlibSourceShape` reproduces the type of `Ideal.exists_pow_inf_eq_pow_smul` at pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
`artinReesTarget_iff_pinnedMathlibSourceShape` checks the statement transport definitionally. This
statement phase does not use or credit the declaration's proof body.

## Commands and results

All commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean` against the
existing pinned `.lake` link; no dependency update, fetch, build, or cache mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0010/Statement.lean` | 0 | canonical target, definitional transport, four mutations, and four boundary expressions elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0010/check_statement.py` | 0 | expression SHA-256 `4904e2a629f74a9ee9347b8309a6103bb6ee0e64e5357fc18f709f82c2e95a0d`; all four mutations distinguished; pinned mathlib revision matched |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0010/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `a8470a...28b3`, `651c8a...1d2`, and `321626...2d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0010` | 0 | rank 103, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Mutation and boundary policy

The validator compares fully explicit elaborated expressions and distinguishes removal of ring
Noetherianity, removal of module finiteness, removal of the lower-bound guard, and weakening the
equality to eventual containment. Separate Lean expressions instantiate bottom and top ideals,
the bottom submodule, and the `n = k` boundary without excluding them. The top submodule and trivial
module remain admitted by the unqualified target binders.

This is statement-only evidence pending master acceptance. It does not prove Artin-Rees or advance
anchor-audit, obligation-tree, proof, validation, or release nodes.
