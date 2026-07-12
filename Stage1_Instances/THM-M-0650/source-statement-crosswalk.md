# Source-statement crosswalk

## Repository source boundary

The Stage0 record supplies only the Chinese title, the gloss "a criterion for elementary
substructures", attribution to Alfred Tarski, and the year `1957`. It gives no bibliographic item,
edition, theorem number, page, proof, assumptions, or errata. Those fields are secondary metadata
(`E5`) and do not establish historical priority, an exact source statement, or `H0`.

The familiar name is commonly rendered "Tarski-Vaught test". The repository's Chinese
transliteration does not distinguish an original historical formulation from the modern textbook
criterion. Source audit must preserve an immutable primary or critical edition, transcribe a
pinpoint result, record incorporated definitions and errata, and obtain independent review.

## Crosswalk

| Repository phrase | Provisional mathematical reading | Candidate Lean surface | Open exactness question |
|---|---|---|---|
| "substructure" | an `L`-substructure `S` of an `L`-structure `M` | `L.Substructure M` | What nonempty-structure convention and language signature does the source use? |
| "witness criterion" | existential witnesses for formulas with parameters in `S` may be chosen in `S` | premise of `Substructure.isElementary_of_exists` | Does the source use arbitrary formulas, existential formulas, or a syntactic normal form? |
| "elementary" | formula realization agrees in `S` and `M` for every finite tuple | `S.IsElementary` | Is the conclusion phrased as `S prec M`, an elementary inclusion, or a bundled object? |
| "test" | usually an iff; the witness-to-elementary direction contains the induction | `isElementary_of_exists` proves the forward implication | Must the canonical root include and prove the converse explicitly? |

## Pinned formal candidates

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.ModelTheory.ElementarySubstructures` documents and exports
`FirstOrder.Language.Substructure.isElementary_of_exists`. Module
`Mathlib.ModelTheory.ElementaryMaps` exports the analogous
`FirstOrder.Language.Embedding.isElementary_of_exists`. `IntakeProbe.lean` elaborates and prints
both declarations in the pinned environment.

These are exact formal discovery anchors (`E3`), not an accepted source crosswalk or proof credit.
The statement phase must choose the substructure root, compare it binder by binder with the
reviewed human source, elaborate a canonical declaration, hash its kernel expression, check all
credited transports, and mutation-test hypothesis, domain, binder scope, and boundary cases.
