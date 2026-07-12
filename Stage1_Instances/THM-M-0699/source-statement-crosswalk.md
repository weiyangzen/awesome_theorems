# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the title `Löwenheim-Skolem定理`, attributes it to
Leopold Loewenheim and Thoralf Skolem, dates it 1915, and gives only `无穷模型的基数`
("cardinality of infinite models"). Stage0 repeats that phrase and explicitly leaves exact
definitions and assumptions, proof process, equivalent statements, axioms, and artifacts open.
The rev-5.6 manifest carries `已验证` only as `source_status_untrusted`.

The same repository source has separate entries for a theorem about arbitrarily large
elementarily equivalent models, a Loewenheim-Skolem-Tarski theorem about different cardinalities,
and upward/downward forms. Those entries demonstrate that the topic has intentionally separated
records; they do not identify this record's proposition and cannot be imported as its source.

## Candidate source work

The 1915 attribution is locator metadata, not a pinpoint proof source. The source phase must inspect
an immutable edition or authoritative modern statement, record theorem/page, assumptions, proof
boundary, translation issues, and errata, and independently establish which cardinality form this
target means. Until then, the human-source mapping cannot be `H0` or `H1`.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "infinite model" | an infinite structure, or a model of a theory | `Infinite M`, `L.Structure M`, optionally `Theory.ModelType` | candidate domain only |
| "cardinality" | exact `#N = kappa`, lower bound, or arbitrary largeness | `Cardinal`, `Cardinal.lift`, explicit comparisons | relation absent |
| "Loewenheim-Skolem" | upward elementary extension | `exists_elementaryEmbedding_card_eq_of_ge` | candidate only |
| "Loewenheim-Skolem" | downward elementary substructure | `exists_elementarySubstructure_card_eq` | candidate only |
| "Loewenheim-Skolem" | combined/equivalent/model form | `exists_elementaryEmbedding_card_eq`, `exists_elementarilyEquivalent_card_eq`, or `Theory.exists_model_card_eq` | candidate only |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe
imports `Mathlib.ModelTheory.Satisfiability` and `Mathlib.ModelTheory.Skolem` and checks the six
candidate declarations above. Their differing types substantiate the scope ambiguity and show that
encoding APIs are available. The probe does not choose a declaration, assert source identity, or
credit any proof body; exhaustive anchor and provenance work belongs to the later audit phase.

