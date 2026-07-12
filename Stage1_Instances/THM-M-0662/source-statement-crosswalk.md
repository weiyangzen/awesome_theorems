# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` attributes the entry to Saharon Shelah, dates it to 1980, and
states only "classification of simple theories". Stage0 repeats this phrase while leaving the
definitions, hypotheses, proof process, equivalent formulations, axiom profile, and formal
artifact unspecified. The rev-5.6 manifest deliberately preserves `已验证` as untrusted metadata.
No repository record identifies an edition, theorem number, page, exact proposition, or proof.

## Candidate primary source

Saharon Shelah, "Simple unstable theories", *Annals of Mathematical Logic* **19** (1980),
177-203, is the historical primary-source candidate matching the repository's author, date, and
subject. This intake has not inspected and preserved an immutable copy, selected a theorem/page,
expanded incorporated definitions, audited corrections, or obtained independent review. The
citation is therefore a discovery anchor only and does not establish `H0`.

Later texts and papers recast simplicity using modern forking/dividing and independence language.
They may help interpret the historical paper, but no later characterization may replace the
repository target without a reviewed source decision and, where meanings differ, a checked
mathematical transport.

## Metadata-to-statement crosswalk

| Repository component | Possible source meaning | Required formal content | Intake disposition |
|---|---|---|---|
| simple theories | complete first-order theories without the relevant tree property | language, complete theory, formula/parameter arrays, consistency pattern, exact tree-property predicate | subject identified; definition not frozen |
| classification | structural study, characterization, independence calculus, or a restricted counting result | one pinpoint proposition with all hypotheses and conclusion | ambiguous; no root selected |
| Shelah / 1980 | likely points to "Simple unstable theories" | immutable edition, exact page/theorem and incorporated definitions | candidate identified; unreviewed |
| `已验证` | Stage0 screening metadata | source proof and Lean evidence would need separate receipts | rejected as evidence |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.ModelTheory.Types` and its imports provide first-order theories, models, formulas, complete
and satisfiable theory predicates, types, and isolated types. `IntakeProbe.lean` checks these names
with the pinned Lean executable. A scoped search of `Mathlib/ModelTheory` found no simple-theory,
tree-property, model-theoretic dividing/forking, or independence-theorem declaration.

These generic components do not encode the intended root. The absence found by a scoped search is
not a complete external anchor audit, and no candidate receives statement or proof credit at
intake. The statement phase first needs a reviewed proposition; the later anchor-audit phase must
then search repo-local, pinned mathlib, and immutable external Lean 4 sources against that exact
type.
