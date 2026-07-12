# Statement validation record

Item: `S56-M-0707-STATEMENT`

Base revision: `f4c286c4ebc4a8b1a5d0a746afd6fba9849e4c7c`.

The canonical target is the arbitrary-program/arbitrary-input halting predicate for the pinned
`Nat.Partrec.Code` universal evaluator. This is a concrete effectively encoded program model, not
Lean's unrestricted `Decidable` typeclass and not timeout observation. `ComputablePred` requires a
total Boolean indicator that is partial-recursive. `Part.Dom` supplies the existential finite
evaluation meaning of halting.

`Mathlib.Computability.Halting` is the minimal direct import discovered for the statement: the
target needs both the universal code evaluator from `PartrecCode` and `ComputablePred`, whose
definition is introduced by `Halting`. The validation used the existing pinned `.lake` artifacts
read-only. No update, build, clone, fetch, or dependency mutation was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0707` | exit 0; rank 748, L0/rework_required, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0707/Statement.lean)` | exit 0; exact target, definitional expanded-shape iff, four mutations, and two boundary witnesses elaborated |
| `python3 Stage1_Instances/THM-M-0707/check_statement.py` | exit 0; expression SHA-256 `9eea217b4bee04ef468074d9f414ff4af376153349db418ff39facce8c31e46b`; all four mutations distinguished |
| `sha256sum Stage1_Instances/THM-M-0707/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes `1df141...7a0f`, `651c8a...b1d2`, and `321626...d81` |
| `python3 -m json.tool Stage1_Instances/THM-M-0707/statement.json` | exit 0; valid JSON |
| forbidden-term scan over the statement Lean and validator | expected exit 1; no prohibited declarations or proof-gap tokens |
| `git diff --check -- Stage1_Instances/THM-M-0707` | exit 0; no whitespace errors |

The four mutations change the quantified domain, restrict arbitrary input to self-input, erase the
effectivity requirement, or incorrectly assert that halting is not recursively enumerable. The
Lean boundary witnesses additionally confirm a terminating program and a divergent program in the
selected semantics. These are statement tests only. Source approval, the Turing-machine transport,
anchor provenance, proof closure, hermetic validation, and independent review remain downstream.
