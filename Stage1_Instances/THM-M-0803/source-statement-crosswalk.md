# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `内模型理论`, attribution "Ronald
Jensen", period "1970s", and statement `可构成宇宙的内模型` (literally, "an inner model of the
constructible universe"). Stage0 repeats this metadata. The rev-5.6 manifest retains `已验证` only
as `source_status_untrusted`. None supplies a definition, theorem number, hypotheses, conclusion,
proof source, edition, page, errata, or formal artifact.

The neighboring entries `可构成性公理` (`V=L`) and `核心模型` (inner models for large cardinals)
locate a topic but do not disambiguate this entry. Adjacency and attribution are not source evidence.

## Candidate source work

An authoritative Jensen publication or a standard set-theory edition may locate the intended
theorem, but no work has been accepted as the primary source during intake. The source audit must
record exact edition/publication, theorem or definition and page, assumptions, proof boundary, and
errata, and obtain independent review. In particular, it must determine whether the intended result
is about constructibility/fine structure, a covering lemma, or another inner model theorem. Until
then, a precise theorem title or date would be speculation rather than an `H0` crosswalk.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "constructible universe" | the hierarchy `L_alpha` and class `L` | definitions of definability and transfinite hierarchy | absent in bounded mathlib name search; exact representation open |
| "inner model" | transitive class, all ordinals, satisfaction of a chosen set theory | class/model predicate plus object-language satisfaction | definition absent from source; exact API open |
| Jensen / 1970s | fine structure or covering result | one exact proposition with assumptions | bibliographic locator only |
| "an inner model of" | model relation, existence, or property | ordered binders and concrete conclusion | grammatically and mathematically ambiguous |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.SetTheory.ZFC.Class` and `Mathlib.SetTheory.ZFC.Ordinal`. It checks the types
of `ZFSet`, `Class`, class membership/set realization, transitivity, ZFC ordinals, and rank. These
are encoding ingredients only. Mathlib's `ZFSet` is a type-level model of ZFC built using Lean's
underlying type theory; it is not by itself the constructible universe or an object-language proof
that a chosen class is an inner model. No constructible-universe or inner-model declaration was
identified by the bounded repository/mathlib name search. That search is not the later immutable
anchor audit.
