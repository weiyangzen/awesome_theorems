# Statement phase validation

Item: `S56-M-0588-STATEMENT`

## Verdict

The exact Lean statement gate is **blocked**. No `Statement.lean` has been emitted because the
available evidence does not support an exact encoding of the frozen human claim. In particular,
using two uninterpreted propositions for "zero Whitehead torsion" and "relative product" would
elaborate syntactically but would substitute a generic equivalence for the s-cobordism theorem.
That is not valid statement evidence under rev-5.6.

## Failed gate

The first failure is exact source and object-model identification:

- The repository metadata does not locate an exact source theorem and leaves its attribution,
  smooth category, dimension convention, torsion convention, and relative-boundary conclusion
  unresolved.
- The pinned mathlib revision has manifold foundations, but its Lean sources contain no relevant
  cobordism/h-cobordism, simple-homotopy, Whitehead-group, or Whitehead-torsion interface.
- Therefore there is no identified pinned type in which both sides of the intended equivalence can
  be stated without inventing target-specific semantic primitives.

`statement-blocker.json` records the missing artifacts and the substitutions explicitly rejected.
This is a statement-phase blocker only; it is not an anchor audit and does not claim that no
external Lean project could provide the missing infrastructure.

## Commands and results

Commands were run from the repository root unless the command includes `cd`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; standard and 1546-target coverage valid |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique uniform-L0 targets |
| `python3 scripts/stage1_target.py show THM-M-0588` | exit 0; rank 628, planned, theorem completion false |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `rg -l -i 'cobord|whitehead torsion|simple homotopy' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 0; eight unrelated files matched mathlib's topological `coborder` identifier; no relevant declaration |
| `rg -n 'Whitehead|simple homotopy|torsion' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 0; torsion matches are unrelated algebra/number theory; no Whitehead/simple-homotopy API |

The project manifest pins mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. No dependency update, fetch, build, or `.lake`
mutation was performed.

Because the exact target was not elaborated, this phase is not self-tested and no
`.stage1-worker-selftest.json` is written.
