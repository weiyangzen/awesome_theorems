# Source-statement crosswalk

## Available repository source

`Docs/researches/math_theorems.md` gives only Gerhard Gentzen, 1936, and "transfinite induction in
proof theory". `Docs/Stage0_Blueprint.md` repeats that phrase while leaving exact definitions,
hypotheses, proof route, axioms, equivalent forms, and formal artifacts open. The manifest's
`已验证` field is explicitly untrusted under rev-5.6 and supplies neither a human proof nor kernel
evidence.

## Primary-source candidates

- Gerhard Gentzen, "Die Widerspruchsfreiheit der reinen Zahlentheorie", *Mathematische Annalen*
  112 (1936), 493-565, DOI `10.1007/BF01565428`. Its author, year, and proof-theoretic setting match
  the repository metadata, making it the leading primary-source candidate. Intake has not inspected
  and approved an exact section/page proposition, its definitions, later corrections, or a stable
  translation.
- Gentzen's later consistency-proof presentation is relevant to source genealogy, but it cannot be
  silently substituted for the repository's 1936 attribution.

These are discovery anchors only. They do not establish which induction formulation the source row
intended and do not support `H0`.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "transfinite" | an ordinal or recursive ordinal notation, likely with an explicit bound | `Ordinal` or a source-faithful syntax of notations, order, bound, and well-foundedness | domain and bound open |
| "induction" | progressiveness implies the predicate at every point in the selected domain | ordered predicate binders and a precise predecessor relation | predicate/formula class and endpoint open |
| "in proof theory" | an internal schema, a metatheoretic rule, or a premise used in ordinal analysis/consistency | syntax, derivability, theory, coding, or an explicit external bridge as selected by the source | ambient theory and conclusion open |
| Gentzen, 1936 | likely consistency-proof genealogy | no formal component or proof credit | matching article candidate only |
| `已验证` | repository metadata | none | untrusted and excluded from H/M evidence |

## Lean discovery boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains
`Mathlib.SetTheory.Ordinal.Basic`. Its `Ordinal.lt_wf` establishes well-foundedness of ordinal `<`,
and `Ordinal.induction` is the corresponding semantic induction theorem (deprecated in favor of
`WellFoundedLT.induction`). `Mathlib.SetTheory.Ordinal.Veblen` defines epsilon zero, while
`Mathlib.SetTheory.Ordinal.Notation` provides constructive notation infrastructure below epsilon
zero. These are credible implementation ingredients for some readings, not proof that they encode
the intended source proposition.

Before `H0`, an independent specialist must approve a stable primary-source proposition, exact
translation, assumptions, proof mapping, and errata disposition. Before statement credit, those
reviewed rows must map to one elaborated Lean proposition with checked transports and mutations.
Neither gate is passed at intake.
