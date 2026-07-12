# Statement validation record

Item: `S56-M-0768-STATEMENT`  
Base revision: `3159849a5319960dea505779c7c20894ea30487c`

## Frozen target

`Stage1Instances.THM_M_0768.CantorBernsteinSchroederTarget` is the exact intake-selected claim:
for arbitrary `alpha : Type u` and `beta : Type v`, injections given as raw functions in both
directions imply existence of a bijective raw function. Its sole direct import is
`Mathlib.SetTheory.Cardinal.SchroederBernstein`.

`target_iff_bundled` checks the equivalence with the embeddings/equivalence spelling. The wrapper
only converts between assumed whole statements; it does not invoke mathlib's
`Function.Embedding.schroeder_bernstein` or supply proof credit for the target.

## Commands and results

All Lean commands ran from `Formalizations/Lean` against the existing pinned Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0768/Statement.lean` | 0 | exact target, checked bundled transport, and four mutations elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0768/check_statement.py` | 0 | expression SHA-256 `6de4e6083a9f47066dfed88584ba5366362c0774b16762b5fbab6d09fc39dcc0`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0768/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `78ba1d...d136`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0768` | 0 | rank 778, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0768/{instance,statement}.json` (run once per file) | 0 | both owned JSON artifacts parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0768` | 0 | no output |

The structural mutations remove the reverse-injection premise, collapse the two carrier domains,
change binder scope so a bijection is unconditional, and add nonemptiness premises that exclude
the empty boundary. They elaborate but have distinct explicit expressions, so none can silently
substitute for the canonical target.

This is statement-only evidence pending master acceptance. It does not prove the theorem or
advance anchor-audit, obligation-tree, proof, validation, or release nodes.
