# THM-M-0650 proof validation

Item: `S56-M-0650-PROOF`. Base revision:
`a74bf62e5952864a45901ffdf9160b000ba3fd01`.

The proof uses the exact frozen statement and the proof-bearing Tarski-Vaught
declarations in mathlib revision `8a178386`. No network operation or dependency
mutation was used. `Statement.olean` was built only in a temporary directory and
deleted after elaboration.

| Command | Exit | Result |
| --- | ---: | --- |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0650` | 0 | rank 696; planned; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0650/check_proof.py` | 0 | source and frozen-input checks passed; proof SHA-256 `34966c58...52f5` |
| `tmp=$(mktemp -d); (cd Formalizations/Lean && lake env lean -R ../.. -o "$tmp/Statement.olean" ../../Stage1_Instances/THM-M-0650/Statement.lean) && (cd Formalizations/Lean && LEAN_PATH="$tmp:${LEAN_PATH:-}" lake env lean ../../Stage1_Instances/THM-M-0650/Proof.lean); rc=$?; rm -rf "$tmp"; exit $rc` | 0 | exact root and embedding terminal wrapper elaborated; each reports only `propext`, `Classical.choice`, `Quot.sound` |

Two preliminary invocations failed before the successful isolated-module recipe:
one ran root-relative Python paths from `Formalizations/Lean`, and one omitted
Lean's `-R ../..` package root while producing the temporary olean. Neither
invocation changed a dependency or produced proof credit.

This is proof-phase evidence only. The foundation/trust certificate, validation,
release, H0/R0, master acceptance, and theorem completion remain downstream.
