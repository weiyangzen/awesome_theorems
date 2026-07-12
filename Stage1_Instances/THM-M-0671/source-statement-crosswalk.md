# Source-statement crosswalk

## Available record and candidate source

The repository inventory gives the Chinese title "model completeness", the gloss "conditions for
a theory to be model complete", an attribution to Abraham Robinson, and the year 1956. Its
`已验证` status is explicitly untrusted under rev-5.6. These fields identify a topic, not a unique
quantified proposition.

A primary-source candidate is Abraham Robinson, *A Result on Consistency and its Application to the
Theory of Definition*, Proceedings of the Royal Netherlands Academy of Arts and Sciences / Indagationes
Mathematicae (1956). This bibliographic lead has not been independently inspected here. Its exact
edition, theorem number/page, wording, definitions, assumptions, and errata remain open, so it is a
discovery anchor only and provides no `H0` evidence.

## Crosswalk

| Repository/source phrase | Candidate mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "theory" | a set or deductively closed collection of first-order sentences | language, sentences, theory, satisfaction | included; conventions open |
| "model complete" | every embedding between models of `T` is elementary | structures, model predicate, embedding, elementary embedding | definitional family identified |
| "conditions" | a necessary-and-sufficient semantic or syntactic test | explicit iff and both directions | exact criterion not selected |
| Robinson / 1956 | historical and bibliographic locator | no formal proposition and no proof credit | candidate source only |
| existential criterion | formulas equivalent modulo `T` to existential formulas, under source conventions | syntax, realization, theory consequence, formula translation | plausible candidate; unconfirmed |

## Ambiguity and evidence boundary

At least three inequivalent formal targets fit the short record: the definition of model
completeness; a general Robinson test characterizing it; and a theorem proving model completeness
of some specified theory. They differ in domains, hypotheses, quantifiers, and conclusion. Choosing
one without primary-source inspection would substitute mathematics.

No theorem-specific Lean artifact was found by the scoped repository name search at intake. That is
not a complete mathlib or external-project anchor audit. The later anchor phase must search pinned
mathlib and credible Lean 4 projects at immutable revisions, record exact declaration types and
terminal proof provenance, and distinguish adjacent APIs for completeness and quantifier
elimination.

Before `H0`, an independent reviewer must approve an exact source edition, theorem/page, definitions,
all hypotheses, proof boundary, and errata. Before statement credit, each approved component must map
row by row to a kernel-elaborated Lean expression with meaningful mutation tests.
