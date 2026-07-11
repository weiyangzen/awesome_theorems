# Statement Validation Record

Item: `S56-M-0133-STATEMENT`  
Base revision: `e9f41b190b7bb99c8cb0895e307c26570b0a78fe`

## Frozen target

`Stage1Instances.THM_M_0133.WilesFermatLastTheoremTarget` is the exact FLT root selected by the
intake: natural exponent `n >= 3`, natural values `a`, `b`, and `c`, all nonzero, and the
disequality `a^n + b^n != c^n`. The module's sole direct import is `Init`.

`target_iff_pinnedMathlibSourceShape` checks the direct expansion of the three pinned mathlib
definitions. `target_iff_positiveNaturalSourceShape` checks the source-wording transport from
nonzero naturals and `n >= 3` to positive naturals and `n > 2`. Thus zero values and exponents at
most two are out of scope without relying on an unchecked prose equivalence.

## Commands and results

Commands ran inside this worker clone on 2026-07-12 (Asia/Shanghai). Lean commands ran from
`Formalizations/Lean` using the existing pinned Lake environment; no dependency mutation command
was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0133/Statement.lean` | 0 | exact target, two checked transports, four mutations, and two exponent-two counterexamples elaborated; explicit target printed |
| `python3 Stage1_Instances/THM-M-0133/check_statement.py` | 0 | expression SHA-256 `8e0d406e9e5ba4504c1930352fde324a02df4a30cbfd75f796b9a3d2627113c1`; all four structural mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-0133/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `01ea92...21e1`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target projection passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0133` | 0 | rank 22, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0133/statement.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0133` | 0 | no whitespace errors |

This is statement-only worker evidence pending master acceptance. The duplicate mathematical shape
with `THM-M-0387` does not transfer proof or receipt credit between theorem IDs. No anchor-audit,
proof, validation, release, audit-completion, or theorem-completion claim is made.
