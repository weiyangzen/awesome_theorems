# Statement validation record

Item: `S56-M-0992-STATEMENT`  
Base revision: `0b8b65976c8cabfaf26316eaee8539caba8f60d0`

## Frozen target

`Stage1Instances.THM_M_0992.ChebyshevTarget` is the exact intake-selected probability-space claim:
`X` is real valued, `MemLp X 2 P` supplies the finite second moment, the threshold is a strictly
positive real, and the conclusion bounds the measure of the closed two-sided deviation event by
the real variance divided by the squared threshold (embedded in `ENNReal`). Its sole direct import
is `Mathlib.Probability.Moments.Variance`.

`PinnedIntakeShape` explicitly spells expectation as the Bochner integral. The theorem
`chebyshevTarget_iff_pinnedIntakeShape` checks the notation transport definitionally. The broader
historical extended-variance formulation and the standard-deviation-multiplier formulation are not
silently substituted for this root.

## Commands and results

All commands ran in this worker clone. Lean commands ran from `Formalizations/Lean` with the existing
pinned toolchain and Lake environment; no dependency operation was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0992/Statement.lean` | 0 | canonical target, definitional notation transport, four mutations, and two boundary lemmas elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0992/check_statement.py` | 0 | expression SHA-256 `b162195bc3a51eba84565f1c454e9005c8fec36f2e4f9e502a4ac6e8742cb8e2`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0992/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `2bd4c5...9aa`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0992` | 0 | rank 272, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0992/statement.json >/dev/null` | 0 | statement receipt is valid JSON |
| `git diff --check` | 0 | no whitespace errors |

## Mutation and boundary policy

The validator compares explicit elaborated expressions and distinguishes replacing the probability
space by an arbitrary finite measure, specializing the sample domain to `Real`, relocating the
`MemLp` premise, and allowing a zero threshold. Kernel-checked lemmas confirm that positivity rules
out division by zero and that the selected event is precisely the closed absolute-deviation event.

This is statement-only evidence pending master acceptance. It does not prove Chebyshev's inequality
or advance anchor-audit, obligation-tree, proof, validation, or release nodes.
