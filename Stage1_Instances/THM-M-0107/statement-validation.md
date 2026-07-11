# Statement validation record

Item: `S56-M-0107-STATEMENT`  
Base revision: `d202f3aedade691a692ec4162fc08e5f1d2694f9`

## Frozen target

`Stage1Instances.THM_M_0107.ZariskiMainFactorizationTarget` is the exact factorization root selected
at intake. It quantifies schemes `X` and `Y` in one explicit universe and a morphism `f : X ⟶ Y`.
The pinned mathlib conventions require separate typeclass hypotheses `LocallyQuasiFinite f`,
`LocallyOfFiniteType f`, `IsSeparated f`, and `QuasiCompact f`. Its conclusion existentially
quantifies the intermediate scheme and two factors, with the open immersion first, finite morphism
second, and categorical composition exactly `j ≫ g = f`.

The sole direct import is `Mathlib.AlgebraicGeometry.ZariskisMainTheorem`; the legacy
`Mathlib.AlgebraicGeometry.RationalMap` import is unrelated to this root and is omitted. The checked
lemma `relativeNormalization_implies_factorization` verifies that the canonical normalization
encoding, when supplied, witnesses the selected existential statement. It deliberately does not
prove that encoding or credit the upstream ZMT declaration; those belong to later nodes.

## Commands and results

All commands ran inside this worker clone on 2026-07-12 (Asia/Shanghai). Lean commands ran from
`Formalizations/Lean` through the existing pinned Lake environment. No update, fetch, clone, or
broad build command was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0107` | 0 | rank 31, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-0107/Statement.lean` | 0 | canonical and normalization targets, checked transport, and four structural mutations elaborated; explicit canonical expression printed |
| `python3 ../../Stage1_Instances/THM-M-0107/check_statement.py` | 0 | expression SHA-256 `1432cea76d1fbb8b70f03874753d551bc28ee05c4b86c738e4085cd6f8923f27`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0107/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `0124e9...c737`, `651c8a...1d2`, and `321626...2d81`, matching `statement.json` |
| `python3 -m json.tool Stage1_Instances/THM-M-0107/statement.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0107 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is statement-only worker evidence pending master acceptance. The statement elaborates, but no
proof of Zariski's Main Theorem is claimed. Anchor audit, obligation tree, proof, validation,
release, audit completion, and theorem completion remain open.
