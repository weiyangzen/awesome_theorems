# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `决定性公理与描述集合论`, attributes
it only to "many mathematicians", dates it to the twentieth century, and gives the gloss `AD与投影
集合的性质` ("AD and properties of projective sets"). Stage0 repeats this metadata while marking
the exact definitions, assumptions, proof path, required axioms, and existing formal artifact as
open. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted`.

No definition, proposition, hypotheses, conclusion, source edition, theorem/page, proof reference,
or formal artifact is supplied. Neighboring records about analytic determinacy and the projective
hierarchy locate the subject area but cannot disambiguate this target.

## Candidate source work

An authoritative descriptive-set-theory monograph and the primary paper for the selected result are
candidate locators, but no edition or passage is accepted during intake. The source audit must
identify the intended theorem, record an exact edition or immutable paper revision and pinpoint,
assumptions, definitions, proof boundary, and errata, and obtain independent review. Until then,
choosing a standard consequence of AD would be speculation rather than an `H0` crosswalk.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| `AD` | every specified infinite payoff game is determined | games, strategies, payoff membership, winning and determinacy predicates | absent from pinned mathlib name search; definition open |
| "projective sets" | a lightface or boldface projective hierarchy on a coded real space | pointclass hierarchy, projection/complement operations, parameter convention | exact hierarchy not found in bounded probe; open |
| "properties" | regularity, determinacy, uniformization, scales, closure, or another consequence | one concrete proposition with all hypotheses | absent from source record |
| descriptive-set-theory infrastructure | trees, analytic sets, Polish/Borel spaces | `Descriptive.tree`, `MeasureTheory.AnalyticSet`, `PolishSpace`, `MeasurableSet` | pinned APIs probed; ingredients only |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports descriptive trees and the Polish-space analytic-set development and checks five
relevant API types. A scoped name search found descriptive trees and analytic sets but no
determinacy-game API or projective-hierarchy declaration suitable for the source gloss. This is
only an environment and feasibility observation, not the later immutable anchor audit and not
evidence that such an encoding cannot exist elsewhere.
