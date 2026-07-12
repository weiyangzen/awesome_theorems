# Source-statement crosswalk

## Repository source and primary candidate

`Docs/researches/math_theorems.md` and Stage0 provide only the Chinese title, Kurt Godel, 1938,
and `ZF+GCH相对于ZF一致` ("ZF+GCH is consistent relative to ZF"). Their `已验证` field is untrusted
metadata under rev-5.6 and supplies neither definitions nor proof credit.

A primary-source candidate is Kurt Godel, *The Consistency of the Axiom of Choice and of the
Generalized Continuum-Hypothesis with the Axioms of Set Theory*, Annals of Mathematics Studies 3,
Princeton University Press (1940), based on the 1938 announcements. This is a discovery anchor
only: an exact theorem/page, edition wording, assumptions, corrections, and errata have not been
independently inspected, so the intake does not claim `H0`.

## Crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| `ZF` | first-order Zermelo-Fraenkel axiom theory without Choice | language, sentences/schemas, theory, model semantics | exact encoding open |
| `GCH` | power-set cardinal at every infinite cardinal is the next aleph | internal cardinal/power-set sentence or schema | exact quantification open |
| "relative to" | `Con(ZF) -> Con(ZF+GCH)` | satisfiability implication or syntactic consistency plus transfers | semantic choice open |
| constructibility | inner universe `L` built by definability hierarchy | model-relative hierarchy and inner-model interpretation | missing concrete API |
| ZF in `L` | all selected ZF axioms hold internally | axiom-by-axiom satisfaction proofs | later obligations |
| GCH in `L` | constructible subsets admit the required cardinal bounds | internal well-order/cardinality theorem | later obligation |
| 1938 / Godel | historical locator | no Lean proposition or proof credit | candidate monograph identified |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe checks `FirstOrder.Language.Theory`, `Theory.IsSatisfiable`, `Theory.ModelType`, `ZFSet`,
`ZFSet.card`, and `Cardinal.aleph`. These are ingredients, not the target. In particular,
`Mathlib.SetTheory.ZFC.Basic` documents `ZFSet` as a model of ZFC built using Lean's axiom of
choice; it cannot by itself witness a relative-consistency implication whose premise is only ZF.
The bounded local search found no repository theorem for this target and no pinned mathlib
constructible-universe/GCH relative-consistency declaration. A later anchor audit must repeat and
extend discovery at immutable revisions and inspect terminal proof bodies.

Before `H0`, an independent source reviewer must approve the exact theorem, definitions, every
assumption, metatheory, proof boundary, and errata. Before statement credit, that crosswalk must map
row by row to one elaborated Lean expression.
