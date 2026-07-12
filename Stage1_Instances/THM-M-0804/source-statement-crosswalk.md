# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the title `核心模型`, attributes it to Ronald Jensen and
John Steel, dates it only to the 1990s, and gives `大基数的内模型` ("an inner model for large
cardinals") as its entire statement. Stage0 repeats this metadata while marking exact definitions,
assumptions, proof process, equivalences, axioms, and machine artifacts as `待补充`. The rev-5.6
manifest preserves `已验证` only as `source_status_untrusted`.

This record supplies no publication, edition, theorem number, page, hypotheses, conclusion, proof
boundary, errata, or formal artifact. Attribution and a topic gloss do not establish an `H0`
source statement.

## Candidate source work

Jensen and Steel publications and later fine-structure monographs are candidate locators, not
accepted citations. The source audit must locate an immutable passage which identifies the exact
version of the core model and one theorem, then record publication metadata, theorem/page,
large-cardinal assumptions, premouse/iterability conventions, conclusion, proof boundary, and
errata. Independent review is required before source fidelity can close.

## Crosswalk

| Repository phrase | Required mathematical decision | Required Lean component | Intake status |
|---|---|---|---|
| "inner model" | transitive set/class model and ambient theory | an explicit first-order/set-theory model encoding | absent |
| "core model" | exact fine-structural construction and version | premouse/extender/strategy definitions | absent from target and not found by bounded mathlib name search |
| "large cardinals" | exact strength and positive/negative hypotheses | formal cardinal predicates and assumption binders | unspecified |
| "model for" | existence, iterability, universality, covering, or other conclusion | one concrete `Prop` with ordered binders | absent |
| `已验证` | untrusted inventory label | no proposition and no proof credit | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.SetTheory.ZFC.Basic` and checks `ZFSet`, membership, ordinals, and powersets.
These demonstrate only a foundational encoding surface. A bounded case-insensitive search of
mathlib for `core model`, `inner model`, `premouse`, and `extender model` found no relevant
declaration. This is not the later immutable anchor audit and cannot prove absence in external Lean
projects.
