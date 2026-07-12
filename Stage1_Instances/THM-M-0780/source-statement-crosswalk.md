# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `科恩力迫法`, Paul Cohen, 1963, and
the gloss `证明CH独立于ZFC的方法` ("a method for proving CH independent of ZFC"). Stage0 repeats
the gloss but leaves exact definitions, assumptions, proof route, axioms, and formal artifacts
open. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted`.

The nearby entries separately name Goedel's consistency result and `THM-M-0781` ("Cohen theorem").
Their adjacency does not establish which formal statement this method-labelled target denotes.

## Candidate primary-source work

Paul J. Cohen's 1963 papers titled *The Independence of the Continuum Hypothesis* in the
*Proceedings of the National Academy of Sciences* are primary-source candidates. They have not
been inspected here at a stable edition/page boundary, and this intake assigns them no `H0`
credit. Source audit must record the exact part, theorem or stated result, pages, assumptions,
notation, proof boundary, and errata, and obtain independent review. A modern precise source may
be needed to make implicit metatheoretic hypotheses explicit, but it cannot silently replace the
historical claim.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "forcing method" | poset, names, forcing relation, generic filter, extension | explicit structures and satisfaction/valuation operations | absent; source selection required |
| "CH" | no cardinal strictly between countable and continuum, or an equivalent form | chosen set-theory encoding and a checked CH definition | absent |
| "independent" | two relative-consistency or non-provability directions | encoded theory, proof relation or semantic consequence, consistency assumptions | ambiguous |
| "from ZFC" | exact object theory and axiom scheme encoding | first-order language, theory, models, satisfaction | generic APIs probed; ZFC encoding absent |
| `已验证` | untrusted inventory label | no proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, model-theory modules
explicitly cite earlier Flypitch forcing/CH work and expose generic first-order theories, models,
sentences, satisfaction, and semantic consequence. The bounded `IntakeProbe.lean` checks only
those encoding ingredients. The repository-local pinned mathlib name search found bibliography but
no forcing or CH-independence declaration; this bounded observation is not the later immutable
formal-candidate audit and does not establish that no external Lean artifact exists.
