# Statement validation

Item: `S56-M-0843-STATEMENT`  
Base revision: `5c38e670073bc890a78e61556f36d2c6b35d257d`

## Frozen target

`Stage1Instances.THM_M_0843.SzemerediRegularityTarget` formalizes the effective Lean-facing
statement displayed on page 9:10 of Dillies and Mehta's ITP 2022 article. Every finite simple graph,
positive real tolerance, and lower bound no larger than the vertex count yields a uniform
equipartition of the whole vertex set with at most the explicit graph-independent
`SzemerediRegularity.bound epsilon l` parts. There is no global edge-density premise; the
repository's "dense graph" wording names the usual setting rather than an assumption in the
inspected statement.

The paper's introductory existential-bound shape is recorded separately, and
`szemerediRegularityTarget_implies_existentialBoundTarget` checks a one-way transport by choosing
the explicit bound. This alternate uses the same formal `Finpartition.IsUniform` predicate; no
converse or transport to the prose theorem's differently presented unordered-pair convention is
credited. The statement uses only
`Regularity.Bound` and `Regularity.Uniform`; deleting either import fails, while the proof-bearing
`Regularity.Lemma` module is deliberately absent. Thus this phase neither imports nor inspects the
available proof declaration.

## Commands and results

All commands ran in this worker clone. Lean used the existing pinned Lake artifacts read-only. No
dependency update, build, clone or fetch command was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0843` | 0 | rank 1032; planned; legacy artifacts unaccepted; theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-0843/Statement.lean` from `Formalizations/Lean` | 0 | target, existential transport and four mutations elaborated; `#check_failure` verified all four equality rejections; explicit expression printed; transport axioms are `propext`, `Classical.choice`, `Quot.sound` |
| `python3 ../../Stage1_Instances/THM-M-0843/check_statement.py` from `Formalizations/Lean` | 0 | expression SHA-256 `3fe13f3562cb642e45e467687508ac44f945e9848ff53d22b9cf068d7ec11219`; all mutations distinct; deleting either direct import fails; pinned mathlib agrees |
| `python3 Stage1_Instances/THM-M-0843/check_statement_artifacts.py` | 0 | fresh elaboration agrees with statement metadata, authority hashes, provisional receipt, and worker handoff; theorem completion remains false |
| `lake env lean --version` and `lake --version` | 0 | Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake 5.0.0-src+98dc76e |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| JSON parse, Python compile, scoped prohibited-construct scan and whitespace checks | 0 overall | structured artifacts parse; checker compiles outside the repo; no forbidden Lean declaration or whitespace error |

## Mutation and evidence boundary

Lean rejects definitional equality with each changed statement, and the checker independently
compares their fully explicit serializations. The mutations remove positivity, change `Real` to
`Rat`, make the lower bound existential, and exclude `l = 0`. These are identity tests; the
phase does not claim that each mutated proposition is false.

The historical intake checker intentionally binds the earlier nine-file intake snapshot. Adding
statement artifacts and reconciling the scope/crosswalk projections makes that snapshot check
stale; it is not rewritten or presented as a statement validator. The intake receipt remains
historical evidence for its own snapshot.

This is statement-only evidence pending master acceptance. It provides no formal-anchor or proof
credit, H0/R0, obligation tree, audit completion, release validation or theorem completion.
