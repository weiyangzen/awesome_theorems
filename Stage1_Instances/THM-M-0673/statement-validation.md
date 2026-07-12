# Statement validation record

Item: `S56-M-0673-STATEMENT`  
Base revision: `c62c7e6f4b9f2eace4ef9d3f7e3e90240c96391f`.

## Frozen target

`Stage1Instances.THM_M_0673.LosSentenceTarget` fixes the sentence form of Los's theorem over an
arbitrary first-order language, index type, family of nonempty structures, and ultrafilter. Its
conclusion is the biconditional between sentence satisfaction in `Filter.Product` and satisfaction
in almost every factor. Its sole direct import is `Mathlib.ModelTheory.Ultraproducts`.

`losSentenceTarget_iff_pinnedMathlibSentenceShape` checks the direct spelling of the polymorphic
type family exposed by pinned mathlib's `FirstOrder.Language.Ultraproduct.sentence_realize`.
This statement node does not credit that declaration's proof body; provenance, axioms, and proof
acceptance belong to later nodes.

## Commands and results

All commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean` with the
existing pinned toolchain and Lake environment. No update, fetch, build, or `.lake` mutation was
performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0673/Statement.lean` | 0 | exact target, definitional transport, four structural mutations, and principal-ultrafilter boundary elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0673/check_statement.py` | 0 | expression SHA-256 `3b541698da0e2b40d0cef5ea0f03ebd62538d330293e4e393ce053e000906cba`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0673/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `131cab45...a424`, `651c8acc...b1d2`, and `321626c8...2d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0673` | 0 | rank 717, planned, L0/rework-required, theorem incomplete |

The mutations remove factor nonemptiness, specialize the index domain to `Nat`, change universal
sentence scope to existential scope, or restrict the ultrafilter to a principal one. The validator
separately elaborates and compares their explicit kernel renderings against the root. The checked
principal instance also exercises the boundary without excluding nonprincipal ultrafilters.

This is statement-only evidence pending master acceptance. Human-source pinpoint review, anchor
audit, proof provenance and trust, obligation construction, proof acceptance, hermetic validation,
and release remain open.
