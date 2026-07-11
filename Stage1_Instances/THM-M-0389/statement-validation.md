# Statement validation record

Item: `S56-M-0389-STATEMENT`  
Base revision: `0c244bf31d168018cc6a106b13aeee2251e46c42`

## Frozen target

`Stage1Instances.THM_M_0389.IntegerMarkovClassification` formalizes the standard
complete-classification reading of the repository phrase `x²+y²+z²=3xyz的整数解`.
It quantifies over `Int` and says that every solution is either `(0,0,0)` or an
even-sign variant of a triple in the closure of `(1,1,1)` under coordinate
permutations and Vieta mutations. Its only direct import is `Init`.

The intake correctly found that the short repository wording does not itself
provide a primary-source theorem/page or spell out sign, zero, and permutation
conventions. This statement phase resolves those conventions using the standard
classification and the repository's historical `S1_M_020.StatementShape`, but
does not upgrade human-source debt. Primary-source fidelity remains open for the
source/anchor audit.

## Commands and results

All commands ran inside this worker clone. Lean ran from `Formalizations/Lean`
with the existing pinned toolchain and reused canonical `.lake` artifacts.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0389/Statement.lean` | 0 | canonical target, generated-triple relation, sign relation, definitional transport, and four mutations elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-0389/check_statement.py` | 0 | expression SHA-256 `d7574d...1622`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0389/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `b1c476...04ac`, `651c8a...1d2`, and `321626...2d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0389` | 0 | rank 20, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0389/statement.json >/dev/null` | 0 | structured statement artifact is valid JSON |
| scoped forbidden-term scan of `Statement.lean` and `check_statement.py` | 1 | no proof-gap declarations found; 1 is ripgrep's no-match exit |
| `git diff --check -- Stage1_Instances/THM-M-0389 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Mutation boundary

The validator compares explicit elaborated expressions and distinguishes the
canonical classification from four changes: reducing the target to mere
existence, restricting it to positive inputs, deleting the zero case, and
allowing a one-coordinate sign change. These tests prevent the most plausible
weakenings or broadenings from silently becoming the root target.

This is statement-only evidence pending master acceptance. It does not prove
the classification or advance anchor-audit, obligation-tree, proof, validation,
or release state.
