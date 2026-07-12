# Statement validation record

Base revision: `25f9c9fc7ebc5af027982533c083f67f86dddb1f`.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1277/Statement.lean` (from `Formalizations/Lean`) | 0 | Lean printed `Stage1Rev56.THMM1277.Statement : Prop`; the selected target and all supporting definitions elaborated |
| `lake env lean --version` (from `Formalizations/Lean`) | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 -m json.tool Stage1_Instances/THM-M-1277/statement.json >/dev/null` | 0 | structured statement receipt is valid JSON |
| `rg -n 'sorry\\b|\\baxiom\\b|placeholder|fake result' Statement.lean statement.json` (from the owned directory) | 1 | no forbidden-content matches; `rg` exit 1 means no match |
| `git diff --check -- Stage1_Instances/THM-M-1277 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is elaboration evidence, not proof evidence. The theorem remains unproved,
and every downstream rev-5.6 gate remains open pending master acceptance.
