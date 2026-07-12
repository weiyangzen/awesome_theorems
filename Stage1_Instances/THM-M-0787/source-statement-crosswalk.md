# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the title `伍丁定理`, attributes it to W. Hugh Woodin,
gives the year 1985, and states only `投影决定性与大基数` ("projective determinacy and large
cardinals"). Stage0 repeats those fields and explicitly leaves exact definitions, hypotheses,
proof history, dependencies, axioms, and formal artifacts open. The rev-5.6 manifest retains
`已验证` solely as `source_status_untrusted`.

This metadata has no grammatical proposition: "and" supplies neither implication direction nor an
equivalence or consistency relation. It gives no large-cardinal strength and no ambient theory.
Consequently it cannot support an exact statement or H0 classification.

## Source work required

The source audit must locate a primary publication or authoritative edition containing the intended
theorem and record a theorem/page locator, exact assumptions, definitions, proof boundary, later
corrections or errata, and independent review. A general survey or a source discussing several
Woodin results may locate candidates but cannot select one merely because its topic matches the
gloss.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "projective" | a level of the projective hierarchy or the full projective pointclasses | coded reals/Polish space, pointclasses, projections and complements | exact convention absent |
| "determinacy" | existence of a winning strategy for each game in the selected class | infinite games, strategies, payoff membership, determinacy predicate | absent from pinned target |
| "large cardinals" | specified Woodin cardinals and possibly a measurable cardinal above | ambient set/model encoding and exact large-cardinal predicates | strength absent; no credit |
| "and" | implication, converse, inner-model consequence, or equiconsistency | an exact object-level or metatheoretic proposition | relationship absent |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded name search
found no declaration mentioning Woodin or projective determinacy. `IntakeProbe.lean` checks only
the basic `Cardinal` and `Set` types from a pinned set-theory import. Those are possible
low-level ingredients, not the missing definitions, theorem statement, or proof. The later anchor
audit must repeat a precommitted search only after the canonical source proposition is selected.
