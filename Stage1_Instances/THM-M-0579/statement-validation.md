# Statement validation record

Item: `S56-M-0579-STATEMENT`  
Base revision: `9c8fbcb508ef94b14b4cc94df3d576550867591d`

The canonical target is
`Stage1Instances.THMM0579.Statement` in `Statement.lean`. The sole import is
`Mathlib.Geometry.Manifold.PoincareConjecture`, which is the narrow pinned mathlib
module exposing all structures used by the target. The definition is a proposition,
not a proof. `namedStatement_iff_statement` kernel-checks transport to a named
hypothesis encoding.

## Exact commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0579` | 0 | rank 114; planned; L0/rework-required; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, matching `lakefile.lean` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0579/Statement.lean)` | 0 | elaborated `Statement.{u} : Prop` and `namedStatement_iff_statement.{u} : NamedStatement ↔ Statement` |
| `python3 -m json.tool Stage1_Instances/THM-M-0579/statement.json >/dev/null` | 0 | statement record is valid JSON |
| expression hash recipe recorded in `statement.json` | 0 | `fc8cd4b59b0831ab45f0faaaa2ccf22f088cb6296c2d041577a5e4ac1f34edbe` |
| imported-module hash recipe recorded in `statement.json` | 0 | `4b9c454dac5fb68da0ff0bac0efe9e5d4ce17c87b9892ff63343c42e761bb8cf` |
| environment fingerprint recipe recorded in `statement.json` | 0 | `895f8a8c6da250b3c0516eeb6cfb86c8fe1deb178a80fcc5ae1c21d1e4de54bb` |
| `rg -n '\b(sorry\|axiom|admit)\b' Stage1_Instances/THM-M-0579/Statement.lean` | 1 | no forbidden proof construct (exit 1 means no match) |
| `git diff --check` | 0 | no whitespace errors |

## Boundary

This evidence self-tests exact statement elaboration only. No Poincare proof is
claimed. Anchor audit, obligation-tree, proof, theorem validation, release, and
master acceptance remain outstanding.
