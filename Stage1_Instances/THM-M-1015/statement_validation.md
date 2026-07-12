# Statement validation record

Base revision: `b2c5ff63ca2e762d1b24d1dc514782747d1a6e1b`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1015/check_statement.py` | 0 | Lean elaborated the target, checked `statement_iff_expanded`, and distinguished all four mutations; expression SHA-256 `8a9448c3ebc73ab5f6bec86b4ca9f25e4f400f2b5dba7276fddd30f641d48e97` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 -m json.tool Stage1_Instances/THM-M-1015/statement.json >/dev/null` | 0 | statement metadata is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1015` | 0 | no whitespace errors |

The checker invokes `lake env lean` narrowly against `Statement.lean` from the
pinned Lean project. The only direct import is
`Mathlib.MeasureTheory.Function.ConvergenceInDistribution`; the historical
independence import was removed. These are statement-only results. No proof or
downstream phase is claimed, and master acceptance remains pending.
