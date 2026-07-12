# Statement validation record

Base revision: `54743c8a753017ec2ce50ffebf85facec9112b95`.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1177/Statement.lean` (from `Formalizations/Lean`) | 0 | Exact target and four mutations elaborated with pinned Lean; only unused-variable warnings occur in the intentionally reduced mutation | 
| `python3 Stage1_Instances/THM-M-1177/check_statement.py` | 0 | Expression SHA-256 `bb3ff2384920048fe79eb0bad3c47a32db31bdaf4e4595898cbd5c7dbfb6ac41`; all four mutations distinguished; mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 -m json.tool Stage1_Instances/THM-M-1177/statement.json >/dev/null` | 0 | Statement receipt is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1177` | 0 | No whitespace errors |

This is statement-phase evidence only. The declaration is a `def : Prop`, not a theorem proof.
Source audit, obligation expansion, proof, validation, release, and master acceptance remain open.
