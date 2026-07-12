# Statement validation record

Item: `S56-M-1553-STATEMENT`  
Base revision: `b47b40ff4929fab3be62b6ae17bcd97a4f3e4f66`

## Frozen target

`Stage1Instances.THM_M_1553.HirotaKdVTarget` is the exact first claim selected by the accepted
intake: the forward KdV bridge over real space-time, with `C^5` regularity, strict positivity,
the concrete binomial definition of the Hirota operators, the transform
`u = 2 partial_x^2(log tau)`, and the fixed KdV plus-sign convention. The direct expanded form is
definitionally equivalent by `hirotaKdVTarget_iff_expanded`.

The three direct imports are the minimal tested set for `ContDiff`, `deriv`, and `Real.log`. The
historical `S1_M_212.lean` abstract derivative/certificate package is not imported and receives no
statement or proof credit.

## Commands and results

All commands ran in this worker clone. Lean commands ran from `Formalizations/Lean` against its
existing pinned `.lake`; no dependency state was updated.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1553/Statement.lean` | 0 | target, expanded transport, and three mutations elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-1553/check_statement.py` | 0 | expression SHA-256 `ef5d4bb909f3eba6d2a347e8bad055e3a4a08402beb725499259bb9bf1a9c3bc`; all mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1553/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `d5e883...0c32`, `651c8a...1d2`, and `321626...5b2d`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1553` | 0 | rank 212, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1553/statement.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1553` | 0 | no output |

## Status boundary

This is statement-only evidence pending master acceptance. Exact primary-source page/equation and
errata review remains open human-source debt. The statement node does not establish the
bilinear-to-KdV proof, anchor audit, obligation tree, hermetic replay, or theorem completion.
