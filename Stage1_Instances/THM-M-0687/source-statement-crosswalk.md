# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `序数分析`, attributes it to Gerhard
Gentzen, gives 1936, and states `证明强度的序数度量` ("ordinal measure of proof strength"). Stage0
repeats those fields while leaving the exact definition, assumptions, proof process, dependencies,
equivalent forms, axioms, and formal artifacts as `待补充`. The rev-5.6 manifest preserves
`已验证` only in the explicitly untrusted `source_status_untrusted` field.

This is a topic description, not a source-stable theorem statement. No work title, edition,
theorem/section/page, original wording, hypotheses, conclusion, proof boundary, errata record, or
formal artifact is supplied.

## Candidate source work

Gentzen's 1936 consistency work and later proof-theory literature are candidate locators, not
accepted sources for this intake. A source audit must determine whether the intended target is
Gentzen's PA consistency result, an exact epsilon-zero calibration of PA, or another theorem. It
must record an immutable edition or archival version, exact passage, assumptions, translation,
proof boundary, corrections, and independent review. Attribution and year alone do not establish
an `H0` crosswalk.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "proof strength" | derivability, consistency, reflection, or provably total functions of a named theory | encoded language, axioms, proof predicate, and metatheory | absent; theory unspecified |
| "ordinal" | an actual ordinal or a recursive ordinal notation with a well-founded relation | `Ordinal` or a source-matched notation datatype and order | pinned APIs probed; representation open |
| "measure" | upper bound, lower bound, equality, supremum, or reduction ordering | an exact calibration predicate and direction | absent from source record |
| "Gentzen, 1936" | possible PA/epsilon-zero historical boundary | source passage plus checked formal encoding | locator clue only |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.SetTheory.Ordinal.Veblen` and `Mathlib.SetTheory.Ordinal.Notation`. It checks
the ordinal type, its well-founded order, epsilon zero and two characterizations, and the notation
type below epsilon zero. These are ingredients for some possible readings only. The bounded scoped
search found ordinal infrastructure but no repository-local encoding of the unspecified theory or
calibration claim; this is not the later immutable anchor audit.
