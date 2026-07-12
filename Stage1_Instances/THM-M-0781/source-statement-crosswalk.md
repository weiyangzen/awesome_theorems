# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `科恩定理`, Paul Cohen, 1963, and the
sentence `CH和AC独立于ZF`. `Docs/Stage0_Blueprint.md` repeats it. The rev-5.6 manifest deliberately
stores `已验证` as `source_status_untrusted`. None of these records gives a bibliography, edition,
theorem/page, definitions, hypotheses, proof boundary, errata, or formal artifact.

## Source selection still required

Cohen's 1963 continuum-hypothesis papers and a source for the choice result are obvious candidate
locators, but intake has not independently inspected and pinned exact editions/passages. A source
audit must also identify the positive halves of each independence claim rather than attributing an
entire bundled result to one forcing argument. It must record exact statements, assumptions,
metatheory, errata, and which source node supports each formal node. Until that review, `H0` is
forbidden.

## Crosswalk

| Repository phrase | Required mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| `ZF` | exact recursively presented first-order axiom theory | language, sentences, theory encoding, proof/model semantics | absent |
| `CH` | exact sentence asserting continuum cardinality | object-theory formula, not merely Lean `Cardinal.continuum` | absent |
| `AC` | exact choice axiom or source-selected equivalent | object-theory sentence, not Lean's ambient choice | absent |
| "CH independent" | positive and negative relative-consistency/model directions | two checked targets plus their base-theory hypotheses | unresolved |
| "AC independent" | positive and negative relative-consistency/model directions | two checked targets plus their base-theory hypotheses | unresolved |
| `已验证` | untrusted inventory label | no proposition and no proof credit | rejected as evidence |

## Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded probe checks
`FirstOrder.Language.Theory`, `Theory.IsSatisfiable`, `Theory.ModelType`, cardinal continuum/aleph
objects, `ZFSet`, and `ZFSet.choice`. These demonstrate useful encoding surfaces only. In
particular, `ZFSet.choice` is documented as deriving choice from Lean's axiom of choice, so it
cannot witness independence of AC from ZF. No formal independence declaration is credited by this
intake search; exhaustive immutable candidate and proof-body audit belongs to the anchor-audit node.
