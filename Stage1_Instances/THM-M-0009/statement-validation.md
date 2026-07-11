# Statement validation record

Item: `S56-M-0009-STATEMENT`  
Base revision: `9e3fd02a2a952da7031bb1dd61387443dd4c1cc7`

## Frozen target

`Stage1Instances.THM_M_0009.LongExactExtSequenceTarget` states both standard variance directions
of the Ext long exact sequence in an arbitrary abelian category with `HasExt`. For every short exact
short complex, every fixed object in the other argument, and every successive pair of natural
degrees, it requires exactness of mathlib's six-arrow covariant or contravariant window. Universal
degree quantification makes these repeating windows the continuing sequences, rather than a single
selected truncation.

The sole direct import is
`Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences`, the pinned narrow module defining the
two named sequence interfaces. The checked transport separates the two variance branches without
changing the target. This phase does not inspect or credit either upstream exactness theorem.

## Commands and results

Commands ran inside this worker clone on 2026-07-12. Lean commands ran from
`Formalizations/Lean` against the existing pinned Lake environment. No fetch, update, build, or
other `.lake` mutation command was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0009/Statement.lean` | 0 | canonical target, checked variance transport, and four mutations elaborated; fully explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-0009/check_statement.py` | 0 | expression SHA-256 `a5f8f018376a768901a6580f7a4fbfe593d73cfb89d71420b79f268b15d083be`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Stage1_Instances/THM-M-0009/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `1210c6...1e63`, `651c8a...b1d2`, and `321626...2d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0009` | 0 | rank 102, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0009/{instance,statement}.json` | 0 | both structured artifacts parsed as valid JSON |
| scoped forbidden-declaration scan of `Statement.lean` and `check_statement.py` | 1 | no `sorry`, `axiom`, or `admit` declaration matched; 1 is ripgrep's no-match exit |
| `git diff --check -- Stage1_Instances/THM-M-0009 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Mutation boundary

The validator compares fully explicit elaborated expressions. It distinguishes either single
variance branch, removal of the short-exactness/exactness structure, and replacement of universal
successive-degree coverage by only the degree-zero covariant window. These checks establish target
identity differences; they do not assert that each mutated proposition is false.

This is statement-only evidence pending master acceptance. Primary-source pinpointing still must
justify the selected scope before H0. No proof closure, M0, audit completion, independent release
validation, or theorem completion is claimed.
