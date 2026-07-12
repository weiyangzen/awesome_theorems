# Statement validation record

Base revision: `eb5f7c9057a60dace86040954ad22ca44a040954`.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1007/Statement.lean` | 0 | The pinned Lean kernel elaborated the target, checked alias transport, four mutation declarations, and two cutoff boundary proofs; `#print` emitted the explicit target. |
| `python3 Stage1_Instances/THM-M-1007/check_statement.py` | 0 | Expression hash `3b1a82b3fc0ce70be489e8a49279e3f29cfe244f7a50c28f5c4e5de26894cf38`; all four structural mutations differed; toolchain `leanprover/lean4:v4.29.0`; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `python3 -m json.tool Stage1_Instances/THM-M-1007/statement.json >/dev/null` | 0 | Statement receipt syntax valid. |
| `rg -n '\bsorry\b|\badmit\b|\baxiom\b' Stage1_Instances/THM-M-1007/Statement.lean` | 1 | No forbidden proof shortcuts (`rg` exit 1 means no matches). |
| `git diff --check -- Stage1_Instances/THM-M-1007` | 0 | No whitespace errors. |

This validates statement elaboration only. It does not prove Kolmogorov's three-series theorem or
clear source, proof, trust, reproducibility, or independent-review gates.
