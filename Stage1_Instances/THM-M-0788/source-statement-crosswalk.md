# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` gives the Chinese title `大基数公理`, attributes it to "many
mathematicians", dates it only to the twentieth century, and says `不可达基数、可测基数等大基数`
("inaccessible cardinals, measurable cardinals, and other large cardinals"). Stage0 repeats this
metadata. The manifest retains `已验证` only as `source_status_untrusted`.

No proposition, quantifiers, hypotheses, object theory, proof source, edition, theorem/page,
assumption list, errata, or formal artifact is supplied. In particular, an axiom is normally an
assumption rather than a theorem to prove in the same object theory. The record could instead be
intending a theorem conditional on such an axiom or a metatheoretic consistency result, but it does
not say which.

## Source work required

The statement phase must locate and independently inspect a primary or authoritative source that
states the intended result. It must record exact edition, definition/theorem and page, object and
metatheory, assumptions, proof boundary, and errata. General references on large cardinals may help
discovery, but naming one at intake would not repair the missing proposition and would not be `H0`
evidence.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "inaccessible cardinal" | uncountable regular strong-limit cardinal | `Cardinal.IsInaccessible` or an object-set-theory encoding | pinned API probed; intended foundation open |
| "measurable cardinal" | uncountable cardinal carrying a nonprincipal complete ultrafilter | exact ultrafilter/measure definition in the selected object theory | named only; definition and target open |
| "other large cardinals" | a non-canonical hierarchy of stronger/weaker notions | one explicitly selected predicate per notion | unbounded topic phrase, excluded from exact target |
| "axiom" | an additional existence assumption | explicit theory extension or theorem hypothesis | assumption/conclusion role open |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.SetTheory.Cardinal.Regular` and checks `Cardinal.IsRegular`,
`Cardinal.IsStrongLimit`, `Cardinal.IsInaccessible`, its characterization theorem, and its universe
cardinal theorem. These are encoding ingredients and a foundation-boundary witness only. They do
not select or prove the absent source proposition. Measurable-cardinal vocabulary and external
formalizations remain work for the later anchor audit after statement freeze.
