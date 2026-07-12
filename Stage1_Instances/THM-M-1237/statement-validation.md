# Statement validation record

Base revision: `9258763ef5d98df2b13458756f43399dd7e63278`.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1237/Statement.lean` (from `Formalizations/Lean`) | 0 | Lean elaborated `Stage1Rev56.THMM1237.Statement : Prop`, its exact expanded transport, and all three negative mutation checks |
| `lake env lean --version` (from `Formalizations/Lean`) | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 -m json.tool Stage1_Instances/THM-M-1237/statement.json >/dev/null` | 0 | structured statement receipt is valid JSON |
| `rg -n 'sorry\\b|\\baxiom\\b|placeholder|fake result' Statement.lean statement.json` (from the owned directory) | 1 | no forbidden-content matches (`rg` exit 1 means no match) |
| `git diff --check -- Stage1_Instances/THM-M-1237 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The Lean check is statement elaboration evidence, not proof evidence. The root remains unproved and
all downstream rev-5.6 gates remain open pending master acceptance of this node.
