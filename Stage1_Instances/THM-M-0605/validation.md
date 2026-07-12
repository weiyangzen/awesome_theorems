# Statement validation record

Base revision: `162f31e26f99fc08e308d576b8fb1b6f18a338c6`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0605` | 0 | rank 643; planned; L0/rework-required; source status untrusted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0605/Statement.lean >/tmp/THM-M-0605.print` | 0 | exact target elaborated; `#print` produced 15,602 bytes with explicit arguments and universes; SHA-256 `b45c5a871dc9b5862356b1fd2540c8d770d8b4488230005303cc6b41f7b33469` |
| `cd Formalizations/Lean && lake env lean /tmp/NoDiffeomorph.lean` after removing the initially separate `Diffeomorph` import | 0 | import was redundant and was removed from the committed statement |
| `cd Formalizations/Lean && lake env lean /tmp/NoSphere.lean` after removing the remaining import | 1 | fails with unknown `EuclideanSpace`; the single declared import is necessary under this deletion check |
| `for f in Stage1_Instances/THM-M-0605/mutations/*.lean; do (cd Formalizations/Lean && lake env lean ../../$f); done` | 1 each | all four expected-negative identity checks fail at `rfl`: removed homeomorphism, changed sphere dimension, existential-to-universal scope, and zero-dimensional boundary model |
| `python3 -m json.tool Stage1_Instances/THM-M-0605/intake.json >/dev/null` | 0 | updated intake record is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0605/statement-receipt.json >/dev/null` | 0 | statement receipt is valid JSON |
| `rg -n --glob '!validation.md' 'sorry\|admit\|sorryAx\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-0605` | 1 | no forbidden proof escape; exit 1 is ripgrep's no-match result |
| `git diff --check -- Stage1_Instances/THM-M-0605 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The elaboration command checks only the exact proposition definition. It does
not inhabit that proposition and is not theorem-proof evidence. The root
therefore stays `[H1, M4, R3]`; source audit, proof, all acceptance receipts,
and release gates remain open. The pre-existing untracked
`Formalizations/Lean/.lake` is reused pinned infrastructure and was not
modified or included in `changed_paths`.
