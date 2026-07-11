# Statement validation record

Item: `S56-M-1234-STATEMENT`. Base revision:
`a85ff9c25a5e8675747ebeb5917fdc10a9278662`.

The canonical declaration is `Stage1Rev56.THMM1234.Statement` in `Statement.lean`.
It selects the whole-plane, unforced, finite-energy existence formulation and does not add the
commonly associated uniqueness conclusion. The direct imports are feature modules for smooth test
functions and derivatives, Euclidean volume, `MemLp`, and Bochner integration.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1234/Statement.lean` | 0 | elaborated `Stage1Rev56.THMM1234.Statement : Prop`; printed the exact expanded binder shape; all four embedded structural mutation checks passed |
| `python3 -m json.tool Stage1_Instances/THM-M-1234/statement.json >/dev/null` | 0 | statement record is valid JSON |
| `rg -n '\\b(sorry\\|axiom\\|placeholder)\\b' Stage1_Instances/THM-M-1234/Statement.lean Stage1_Instances/THM-M-1234/statement.json` | 1 | no forbidden proof escape or substitute marker (`rg` exit 1 means no match) |
| `git diff --check -- Stage1_Instances/THM-M-1234` | 0 | no whitespace errors in owned changes |

Environment: Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, toolchain-file SHA-256
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`, and Lake-manifest
SHA-256 `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

This is statement elaboration evidence only. The theorem is unproved; primary-source fidelity,
candidate audit, proof architecture, kernel closure, and release gates remain downstream.
