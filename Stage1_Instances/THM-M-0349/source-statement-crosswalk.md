# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the title `共轭函数定理`, attributes it to Marcel Riesz,
gives the year 1927, and supplies only `共轭函数的L^p有界性` ("the L^p boundedness of conjugate
functions"). Stage0 repeats this gloss but leaves the exact definitions, assumptions, proof route,
axioms, and formal artifacts open. The rev-5.6 manifest preserves `已验证` only as an explicitly
untrusted source label.

The same repository inventory contains a separate earlier "Riesz brothers theorem" with the same
gloss and a separate Hilbert-transform boundedness entry. This duplication makes a pinpoint source
and convention audit essential; adjacent labels cannot disambiguate or provide proof credit.

## Candidate source work

Marcel Riesz's original work on conjugate functions and a stable edition of Antoni Zygmund's
*Trigonometric Series* are candidate locators for the classical theorem. No exact edition,
article title, theorem number, page, wording, or errata was independently inspected during this
intake. These locators are therefore discovery leads, not `H0` evidence. The source audit must pin
one passage and independently verify every assumption and convention.

## Crosswalk

| Repository phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "conjugate function" | periodic Hilbert transform of `f` | a concrete operator on circle functions or `L^p` classes | intended family identified; definition open |
| `L^p` | periodic function space for exponent `p` | `MeasureTheory.Lp` over the selected Haar measure | API probed; exponent encoding and scalars open |
| "boundedness" | `||Hf||_p <= C_p ||f||_p` | a continuous linear map or explicit norm inequality | conclusion shape provisional; constant open |
| Marcel Riesz / 1927 | historical locator | no Lean term or proof credit | exact primary passage open |
| `已验证` | untrusted inventory metadata | no statement or proof evidence | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks `UnitAddCircle`, its Haar measure, the additive-circle representation, `MeasureTheory.Lp`,
and `MemLp`. A bounded name/content search found no theorem-specific circular Hilbert
transform or conjugate-function declaration. This is a bounded intake observation, not the later
immutable anchor audit and not proof of absence from all Lean projects.

Before statement credit, the selected source rows must map to one elaborated Lean proposition, and
all alternate operator encodings receiving credit must have checked witnesses. Before `H0`, an
independent reviewer must approve the pinned edition, passage, assumptions, definitions, proof
boundary, and errata record.
