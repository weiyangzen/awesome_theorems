# Statement validation record

Item: `S56-M-0769-STATEMENT`  
Base revision: `3159849a5319960dea505779c7c20894ea30487c`

## Frozen target

`Stage1Instances.THM_M_0769.AxiomOfChoiceTarget` states the indexed-family formulation of choice:
for `iota : Sort u` and `A : iota -> Sort v`, fiberwise `Nonempty (A i)` implies
`Nonempty (forall i, A i)`. The explicit elaborated result places the selector in
`Sort (imax u v)`. Binder order, universe scope, the sole hypothesis, and the empty-index boundary
are frozen. `axiomOfChoiceTarget_iff_pointwise` checks the binder-grouping transport by `rfl`.

The sole direct import is `Mathlib.Logic.Basic`. The proposition itself needs only core dependent
functions and `Nonempty`; this pinned module is retained as the minimal mathlib surface that also
exposes the exact foundational APIs identified at intake. This phase does not invoke or inspect
either `Classical.choice` or `Classical.axiomOfChoice` as proof evidence.

## Commands and results

All commands ran inside this worker clone. Lean used the existing pinned `.lake` closure read-only;
no update, build, clone, fetch, or dependency mutation command was run.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0769/Statement.lean` | 0 | exact target, checked transport, and four structural mutation declarations elaborated; fully explicit target printed |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0769/check_statement.py` | 0 | expression SHA-256 `1221bb601965de34dc2ea2a4ba104f1e4c4b9476ed3d682e1f822f5cc3cee505`; all four mutations distinguished |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Stage1_Instances/THM-M-0769/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `c6099963...d3dbe`, `651c8acc...b1d2`, and `321626c8...2d81`, matching `statement.json` |

## Mutation and scope boundary

The validator serializes fully explicit elaborated expressions and rejects equality with four
mutations: removing fiber nonemptiness, narrowing `Sort` to `Type`, moving the family binder under
`Nonempty`, and excluding the empty-index boundary. These checks establish statement identity, not
the truth or falsity of every mutated proposition.

Set-family membership, surjection/right-inverse, product, well-ordering, and Zorn encodings receive
no credit here because this phase adds no checked transports for them. This is statement-only
evidence pending master acceptance; it establishes no anchor-audit, proof, H0, M0, release, or
theorem-completion claim.
