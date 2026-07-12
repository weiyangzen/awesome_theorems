# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` gives the title `解析集确定性`, attributes it only to "many
mathematicians", dates it to the twentieth century, and supplies the gloss `解析博弈的决定性`
("determinacy of analytic games"). Stage0 repeats the label without definitions, hypotheses, a
source, or a proof artifact. The rev-5.6 manifest preserves `已验证` only in the explicitly untrusted
field `source_status_untrusted`.

Thus the repository identifies a recognized topic but does not identify an exact theorem. In
particular it omits the foundation assumptions, which are part of the mathematical content rather
than implementation detail.

## Primary-source work still required

The statement phase must select and inspect an immutable primary source for the intended analytic
determinacy result. It must record edition or paper revision, exact theorem and pages, referenced
definitions, ambient theory, every large-cardinal/determinacy/choice assumption, proof boundary,
later corrections and errata, and an independent review. No remembered attribution or bibliographic
guess is accepted as `H0` at intake.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| analytic game | Gale-Stewart game whose payoff is analytic in Baire space | plays, histories, turn convention, payoff predicate | provisional; source definition open |
| analytic payoff | boldface or lightface `Sigma^1_1`, often represented by projection/tree | topology, analytic-set predicate, coding and parameter convention | pinned vocabulary probed only |
| determinacy | Player I or Player II has a winning strategy | exact strategy, compatible-play, winning predicates, and disjunction | absent; canonical encoding open |
| all analytic games | quantification over the entire source pointclass | ordered payoff and analyticity binders | candidate scope only |
| foundation | ambient set theory and any consistency-strength hypothesis | explicit assumptions/profile rather than silent Lean choice | absent and root-critical |
| `已验证` | untrusted inventory label | no proposition or proof credit | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
imports descriptive-tree and Polish analytic-set modules and checks five relevant API types. These
are encoding ingredients only. The probe does not define games, express analytic determinacy, settle
the foundation mismatch, locate a proof body, or establish absence from mathlib. Formal-candidate
discovery belongs to the later anchor-audit phase.
