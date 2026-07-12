# Anchor audit

Item: `S56-M-0646-ANCHOR_AUDIT`  
Audit date: 2026-07-12  
Base revision: `83f5974d31f82ec4ad3b558c2e1c5078e070e986`

## Pinned mathlib result

The repository pins Lean 4.29.0 and mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. At that immutable revision,
`Mathlib.ModelTheory.Satisfiability` contains two usable upward candidates:

| Declaration | Exact relationship | Provenance and decision |
|---|---|---|
| `FirstOrder.Language.exists_elementarilyEquivalent_card_eq` (lines 257-262) | Same existential elementary-equivalence and exact-cardinality conclusion. It needs infinitude of `M`, infinitude of `kappa`, and the language-cardinality bound. The frozen `#M <= kappa` premise is stronger than needed and is deliberately unused. | Terminal body splits on cardinal direction through `exists_elementaryEmbedding_card_eq`; eligible exact `M0-W` candidate. |
| `FirstOrder.Language.exists_elementaryEmbedding_card_eq_of_ge` (lines 217-236) | Matches both upward cardinal bounds and returns the stronger elementary embedding `M -> N`; `ElementaryEmbedding.elementarilyEquivalent` gives the checked conclusion transport. | Terminal body uses elementary diagrams, a large model, and downward cardinal realization; eligible stronger `M0-W` candidate. |
| `FirstOrder.Language.exists_elementarySubstructure_card_eq` in `Mathlib.ModelTheory.Skolem` | Downward construction of a small elementary substructure. | Direction mismatch; retained only to disambiguate the theorem name. |

`AnchorAudit.lean` checks all three declarations, elaborates exact witnesses for the two upward
routes, and prints their axiom profiles. The output for each upward declaration and each local
witness is `[propext, Classical.choice, Quot.sound]`. The terminal source bodies contain no
`sorry` or `admit`. Mathlib's local `LICENSE` is Apache-2.0. This identifies a genuine pinned
library closure candidate, rather than an anchor-only URL.

This phase does not promote the authoritative root to accepted `M0-W`. Proof-body transitive
provenance, typed composition, trust, validation, and master acceptance belong to later nodes. The
authoritative root therefore remains its pre-acceptance `M4`; `M0-W` here is the candidate
classification and the next phase must place the chosen route in the frozen obligation graph.

## External Lean 4 result

A bounded public search found only pinned mathlib and
`FormalizedFormalLogic/Foundation@c28942b7d9d0df41ee5b736602c3f27b8643532c`. The latter was
downloaded as an immutable archive (SHA-256
`477e62680d4fe1d2629fc652c39b55bf04ee38eb76afe85c5c2341f05e935975`) outside the repository and
was not installed into `.lake`. Its Lean 4.29.0 module
`Foundation.FirstOrder.SetTheory.LoewenheimSkolem` proves elementary equivalence for a countable
Skolem hull in the fixed language of set theory. Its imported `Skolemization/Hull` module likewise
implements the downward, countable-language theorem. Neither supplies arbitrary-language upward
models of a requested cardinal, so it is not an integration candidate. The two terminal files
contain no `sorry`/`admit`; broader unrelated project placeholders receive no credit.

Sourcegraph's dated, content-hashed response contained six matches: four mathlib content hits and
two Foundation path/content hits. GitHub's quoted ASCII repository search returned a complete zero
result. GitHub code search was rate-limited with HTTP 403, so that lane is recorded as blocked and
is not represented as a negative search. These searches are bounded discovery evidence, not a
claim that no other Lean formalization exists.

## Boundary

The formal-anchor inventory is self-tested and finds no repo-local integration debt: the exact
candidate is already in the pinned dependency closure. This node establishes neither primary
human-source fidelity (`H0`) nor readable reconstruction (`R0`), and it does not claim audit or
theorem completion.
