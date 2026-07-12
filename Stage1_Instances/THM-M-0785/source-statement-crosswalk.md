# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` gives the Chinese title `决定性公理`, the attribution Jan
Mycielski/Stanislaw Swierczkowski, the year 1964, and the gloss `实数集上某些博弈的决定性`
("determinacy of certain games on sets of reals"). Stage0 repeats those fields. The rev-5.6
manifest retains `已验证` only as `source_status_untrusted`.

The record gives no bibliographic work, edition, page, formal statement, payoff class, assumptions,
proof boundary, or errata. The title suggests AD, while "certain games" suggests a restriction;
these do not determine one proposition. The nearby separate entries for Martin's theorem, analytic
determinacy, and determinacy with descriptive set theory cannot be borrowed to fill this gap.

## Candidate source work

The attribution and date are discovery keys, not accepted source evidence. The source audit must
locate the cited 1964 primary publication or another authoritative statement, preserve its exact
game and pointclass conventions, record theorem/definition and page, assumptions and errata, and
obtain independent review. It must also verify whether the repository attribution concerns the
axiom itself or a theorem derived from a determinacy hypothesis.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "games" | alternating perfect-information games of length omega | plays, finite-history strategies, compatibility predicates | one candidate encoding probed |
| "sets of reals" | payoff subsets of Baire/Cantor space or real moves | explicit coding and transport to the source domain | ambiguous |
| "certain" | Borel, analytic, projective, definable, or another pointclass | a precise predicate on payoff sets | absent |
| "determinacy" | one player has a winning strategy | disjunction of first/second winning-strategy propositions | candidate schema probed |
| "axiom" | universal principle adopted over an ambient foundation | exact quantification and foundation profile | absent |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded name search
found no game-determinacy API or theorem. `IntakeProbe.lean` therefore defines only a transparent
candidate encoding with plays `Nat -> Nat`, finite-history strategies, and a full-payoff
determinacy schema. It elaborates under the pinned kernel, demonstrating expressibility only. Full
AD is not selected, and the absence of a name-search hit is not the later immutable anchor audit.
