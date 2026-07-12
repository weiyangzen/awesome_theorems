# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `解析集定理`, attributes it to Mikhail
Suslin, dates it to 1917, and gives only `解析集的补集性质` ("the complement property of analytic
sets"). Stage0 repeats this metadata and marks exact definitions, assumptions, proof path, axioms,
and formal artifacts as open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted`.

No primary source, edition, theorem number, page, verbatim proposition, hypotheses, proof reference,
or errata record is supplied. The historical cues make the classical Suslin theorem the leading
candidate, but they do not license selecting its modern formulation or foundation silently.

## Candidate source work

The source audit must locate an authoritative edition or immutable primary/critical source for the
intended Suslin theorem and record a pinpoint statement, definitions, assumptions, proof boundary,
translation issues, and errata, followed by independent review. A modern descriptive-set-theory
reference may clarify the Polish/standard-Borel formulation but cannot be treated as the 1917
source without an explicit historical crosswalk.

## Crosswalk

| Repository phrase | Candidate mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "analytic set" | continuous image of Baire space or a Polish space | `MeasureTheory.AnalyticSet` | pinned definition/API probed; source equivalence open |
| "complement property" | both `s` and `sᶜ` are analytic | `AnalyticSet s` and `AnalyticSet sᶜ` | leading hypothesis candidate only |
| theorem conclusion | Borel/measurable status of `s` | `MeasurableSet s` with compatible topology and measurable space | candidate only |
| Suslin theorem | analytic plus coanalytic implies measurable/Borel | `AnalyticSet.measurableSet_of_compl` | pinned candidate elaborates; exact identity and provenance unaudited |
| converse/biconditional | Borel sets and complements are analytic | `MeasurableSet.analyticSet` and complement closure | possible broader formulation; not selected |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.MeasureTheory.Constructions.Polish.Basic`. It checks the analytic-set
definition, its Polish-space range characterization, measurable-to-analytic conversion, Lusin
separation, and `AnalyticSet.measurableSet_of_compl`, whose source comment calls it Suslin's
theorem. These checks establish available encoding ingredients and a credible candidate only. They
do not replace the exact-source statement gate, terminal-body/provenance audit, or acceptance.
