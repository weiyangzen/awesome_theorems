# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6693-6698`, introduced by repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`, is the entire catalog record:

- title: `生成函数` (generating functions);
- attribution: `众多数学家` (many mathematicians);
- period: `18世纪` (eighteenth century);
- statement gloss: `组合序列的生成函数方法` (the generating-function method for combinatorial
  sequences);
- importance: high; and
- status: `已验证`.

`Docs/Stage0_Blueprint.md:24958-24983` repeats the gloss while explicitly leaving definitions and
premises, proof route, dependencies, equivalent forms, foundations, machine status, and artifact
links open. The rev-5.6 manifest preserves the verified label only as `source_status_untrusted` and
resets the target to `L0 / rework_required`. These inventory records are not primary sources or
proof receipts.

## Literal crosswalk

| Repository element | Required mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| "generating functions" | one source-selected construction and result | one canonical proposition/type | subject family only |
| "combinatorial sequence" | index set, coefficient carrier, sequence or counted class | ordered binders and algebra/typeclass context | all open |
| "method" | a specific transformation plus a theorem about its input and output | exact hypotheses and conclusion | no truth-valued conclusion given |
| historical attribution | edition, theorem/page, definitions, assumptions, proof, corrections | documentation and provenance map | no citation or locator |
| `已验证` | accepted human proof and/or exact kernel evidence | accepted source and proof receipts | no H or M credit |

## Authoritative subject-family lead

Herbert S. Wilf, *generatingfunctionology*, second edition, Academic Press (1994), author-hosted
Internet Edition, was inspected as a source-family lead. The observed PDF contains 231 pages,
1,247,451 bytes, and SHA-256
`aeecec4df4fbb81b5a3824492ed816c290af44fccb0b1307f7f42f26e5b008ef`.

The second-edition preface says the book concerns generating functions and their uses in discrete
mathematics. Its contents separately list formal power series (section 2.1), formal ordinary
power-series generating functions (2.2), formal exponential generating functions (2.3), analytic
power-series theory (2.4), and formal Dirichlet series (2.6). Printed pages 30-31 define a formal
power series as a coefficient sequence, define equality coefficientwise, and give the Cauchy
product in equation (2.1.2). The discussion explicitly distinguishes formal algebraic manipulation
from analytic convergence.

This is evidence that the catalog wording spans many constructions and results, not evidence for a
particular root. The repository does not cite Wilf; the book is not an admitted source packet; and
no exact theorem/premise/proof/errata crosswalk or independent review exists. It is therefore an
`E5` discovery lead and not `H0` evidence.

## Required source admission

Before statement work can leave `H5`, an accountable reviewer must select and preserve one lawful,
immutable authoritative source proposition; transcribe its definitions, ordered binders,
hypotheses, conclusion, boundary and convergence conditions; locate its proof; audit edition
changes, corrections, and errata; justify why that proposition faithfully represents the broad
catalog method rather than a narrower neighboring target; and obtain independent approval.

Only then may a statement worker encode the same claim in Lean, minimize imports, serialize the
elaborated expression and environment, check alternate transports, and run removed-hypothesis,
changed-domain, binder-scope, and boundary mutations. Until then the canonical mathematical
statement, formal expression, expression hash, and checked transports remain null.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, generic formal
power-series substrate exists in `Mathlib.RingTheory.PowerSeries.Basic`: `PowerSeries.mk` packages
coefficient functions, `PowerSeries.coeff_mk` recovers them, `PowerSeries.ext` proves
coefficientwise extensionality, and `PowerSeries.coeff_mul` gives Cauchy convolution.
`Nat.Partition.genFun` and `PowerSeries.catalanSeries` are specialized neighboring examples. These
declarations are discovery inputs only; none is selected as `THM-M-0915`, and the later exhaustive
anchor audit remains open.
