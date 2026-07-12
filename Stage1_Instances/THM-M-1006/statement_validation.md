# Statement validation record

Node: `S56-M-1006-STATEMENT`. Base revision:
`656a1be3548d492354ef99a755ef0bbcab9bd22b`.

The canonical choice is the finite discrete-time, real-valued, zero-initial martingale form. This
resolves the intake ambiguity rather than using a continuous-time or terminal-value variant. The
single import is the mathlib martingale object-model module; the expression itself defines the
finite maximum and discrete quadratic variation.

## Exact checks

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1006/Statement.lean` | 0 | Lean elaborated all definitions and printed the three expected `#check` types |
| `python3 -m json.tool Stage1_Instances/THM-M-1006/statement.json >/dev/null` | 0 | statement receipt is valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard structure passed for 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | target manifest passed with 1546 unique targets and ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1006` | 0 | rank 286, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1006` | 0 | no whitespace errors |

## Mutation boundary

The elaborated binder order makes constant uniformity structural. Removing `0 < p`, removing the
martingale premise, moving `c C` after `f`, replacing `range (n + 1)` by `range n`, or removing
`f 0 = 0` changes the declaration type and is not an alternate encoding. At `n = 0`, both defined
quantities reduce to zero under `f 0 = 0`, so the required degenerate horizon is retained.

This is statement elaboration evidence, not proof evidence. Master acceptance is still required.
