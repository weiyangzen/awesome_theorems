# Source-statement crosswalk

## Candidate primary source

Toshio Yamada and Shinzo Watanabe, "On the uniqueness of solutions of stochastic differential
equations," *Journal of Mathematics of Kyoto University* 11 (1971), 155-167, is the historical
primary-source candidate. This bibliographic identification is an intake discovery anchor only.
The exact theorem number, page span of the relevant statement, hypotheses, definitions, and any
errata have not yet been inspected from a stable copy and therefore do not establish `H0`.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "SDE" | source-specific stochastic equation and solution notion | coefficients, stochastic integral, filtered probability space | included; model open |
| "weak existence" | a solution on some stochastic basis | existentially quantified probability space, filtration, noise, solution | included; conventions open |
| "pathwise uniqueness" | same input/noise implies indistinguishable solutions | coupled solutions and almost-sure process equality | included; quantifiers open |
| "strong solution" | solution measurable from prescribed input/noise | measurable-functional/adapted construction | included; encoding open |
| "uniqueness in law" | equality of appropriate solution or joint laws | `Measure.map`/`HasLaw` equality on path space | companion claim; source placement open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_231.lean` is useful discovery material. It contains
an explicit local equation interface and distinguishes weak existence, pathwise uniqueness, and a
strong-solution conclusion. However, its stochastic integral is an interface operation and its
model retains proposition-valued object-model and regularity hypotheses. Historical audit rows and
theorem-tree metadata in that module must be re-audited at the current pinned revisions. They are
not an exact source crosswalk or a terminal proof.

Before `H0`, an independent reviewer must verify the primary edition, exact theorem/page,
definitions, every assumption and conclusion, errata, and a row-by-row mapping to the canonical
Lean statement. A modern secondary source may clarify terminology but cannot replace this gate.
