# Statement validation record

Item: `S56-M-0083-STATEMENT`  
Base revision: `c2687431b1d86bac7bd509c9abbfdc1e763c060c`

## Frozen target

`Stage1Instances.THM_M_0083.RepresentableFunctorTarget` is the exact
intake-selected universal-element criterion for a Type-valued presheaf. It
quantifies independently over category-object, hom, and value universes. Its
sole direct import is `Mathlib.CategoryTheory.RepresentedBy`.

`PinnedMathlibSourceShape` uses mathlib's `IsRepresentedBy` predicate, and
`representableFunctorTarget_iff_pinnedMathlibSourceShape` kernel-checks that its
`map_bijective` field is precisely the explicit intake formula. This statement
node does not credit the legacy wrapper as proof evidence.

## Commands and results

All commands ran inside this worker clone. Lean commands ran from
`Formalizations/Lean` with the existing pinned Lake environment; no dependency
update or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0083/Statement.lean` | 0 | exact target, checked transport, four structural mutations, and empty-category boundary elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0083/check_statement.py` | 0 | expression SHA-256 `1319e132e2f2c66360cf15565db7a1f4acf3623597a87f92753765c02d714a19`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0083/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `c5cba3...8580`, `651c8a...b1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0083` | 0 | rank 139, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Mutation and boundary policy

The validator compares explicit elaborated expressions and rejects weakening
bijectivity to either injectivity or surjectivity, changing the universal test
object to an existential one, and retaining only the reverse implication. The
kernel-checked empty-category theorem confirms that neither side gains a hidden
nonemptiness premise. Corepresentability and specialized representability
theorems remain excluded from this root.

This is statement-only evidence pending master acceptance. It does not prove a
new theorem or advance anchor-audit, obligation-tree, proof, validation, or
release nodes.
