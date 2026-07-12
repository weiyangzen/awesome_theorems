# Statement-phase blocker

Item: `S56-M-1253-STATEMENT`  
Base revision: `a80ab2514294b0e85527fd5a7d419748401215b2`  
Verdict: `blocked`

## First failed gate

The exact-statement identity gate fails. The only repository source wording is
`分布的卷积运算` ("the convolution operation for distributions") in
`Docs/researches/math_theorems.md`. It does not specify a proposition, domain, scalar field,
quantifiers, support hypothesis, definition, conclusion, or source theorem/page. The accepted
intake consequently records
`topic_frozen_exact_source_statement_open` and makes exact primary-source selection the first
blocker. Choosing existence, well-definedness, commutativity, associativity, a support estimate,
or differentiation compatibility would invent information not present in the source record.

The pinned mathlib revision provides `TestFunction`, `Distribution`, and `Distribution.mapCLM` in
`Mathlib.Analysis.Distribution.Distribution`, but that module explicitly says that it contains very
few mathematical statements and that the theory will be expanded. A scoped search found no
convolution operation for `Distribution`; the convolution declarations found elsewhere concern
functions, measures, or Schwartz maps and cannot be substituted for this target.

Therefore no canonical Lean proposition, declaration, normalized expression hash, checked
transport, or statement-completion receipt can be produced truthfully in this phase. In
particular, introducing an assumed convolution operator or a predicate whose fields contain the
desired laws would broaden or encode the result as a premise, which rev-5.6 forbids.

## Retry condition

An immutable primary source must be supplied or selected and independently inspected down to the
exact edition, theorem/definition and page. It must determine the ambient finite-dimensional real
space, value field, ordered binders, precise support condition, definition of the convolution, and
the exact conclusion(s). Statement execution can then encode that claim against the pinned
distribution API, or record a concrete missing-API obligation without substituting another kind of
convolution.

## Scoped evidence

`StatementApiProbe.lean` is only a positive substrate probe. It does not claim to elaborate the
target.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; standard and 1546-target projection valid |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1253` | exit 0; rank 432, planned, L0/rework_required |
| `rg -n -i 'distribution\\|test.?function\\|schwartz.*convol\\|convol.*schwartz' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 0; distribution substrate and unrelated convolution APIs only |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` (matches `lakefile.lean`) |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1253/StatementApiProbe.lean` | exit 0; `TestFunction`, `Distribution`, `Distribution.mapCLM`, `𝓓(Ω, ℝ)`, and `𝓓'(Ω, ℝ)` elaborate |

Known failure: the exact Lean target is not identifiable from the repository source and hence was
not self-tested. No `.stage1-worker-selftest.json` is emitted.
