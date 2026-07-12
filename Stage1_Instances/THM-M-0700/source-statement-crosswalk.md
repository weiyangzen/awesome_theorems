# Source-statement crosswalk

## Repository sources

`Docs/researches/math_theorems.md` names Jacques Herbrand, gives 1930, and glosses the statement as
`量词消去与Skolem化` ("quantifier elimination and Skolemization").
`Docs/researches/cs_theorems.md` instead says `一阶逻辑的Herbrand模型` ("the Herbrand model of
first-order logic"). Stage0 repeats the first gloss but leaves definitions, hypotheses, proof,
dependencies, equivalent forms, axioms, and formal artifacts open. The rev-5.6 manifest preserves
`已验证` only as `source_status_untrusted`.

These are topic locators rather than a source-stable theorem. They do not provide original wording,
an edition or page, signature conventions, equality policy, normal form, hypotheses, conclusion,
proof boundary, translation, or errata record.

## Candidate primary source

Jacques Herbrand, *Recherches sur la theorie de la demonstration*, Travaux de la Societe des
Sciences et des Lettres de Varsovie, Classe III, no. 33 (1930), is the historically plausible
primary-source work. It is recorded only as a candidate locator at intake. The source audit must
pin an immutable scan and bibliographic edition, identify the exact theorem and pages, account for
terminology and translation, map every premise, check later corrections, and obtain independent
review. Attribution and year do not establish `H0`.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "quantifier elimination" | prenex conversion and removal of existential quantifiers by Skolem functions | syntax transformations plus preservation/equisatisfiability theorems | transformation and direction unspecified |
| "Skolemization" | expansion by fresh function symbols | language extension, formula translation, reduct/expansion semantics | mathlib `Language.skolem₁` APIs probed; not a full selected target |
| "Herbrand model" | term-generated interpretation for ground syntax | ground terms, Herbrand universe and structure, satisfaction | absent from repository record and scoped search |
| "Herbrand theorem" | finite ground-instance characterization | exact finite disjunction or unsatisfiable finite subset proposition | formulation unspecified |
| `已验证` | untrusted inventory label | no proposition and no proof receipt | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.ModelTheory.Satisfiability`. It checks first-order syntax and semantic types,
sentence realization, satisfiability, the `skolem₁` language construction, and its elementary-reduct
theorem. A scoped repository and pinned-mathlib search found these foundations but no declaration
named for Herbrand's theorem or a Herbrand-universe/model construction. This is intake discovery,
not the later immutable anchor audit and not proof that no external formalization exists.
