# Source-statement crosswalk

## Repository evidence boundary

The repository metadata names Max Zorn, gives 1935, and says only "existence of a maximal element in
a partially ordered set." It supplies no publication title, stable edition, theorem number, page,
quoted statement, proof, referenced definitions, assumptions, translation policy, or errata record.
The phrase is incomplete as a theorem because it omits the chain upper-bound premise. This intake
interprets it as the standard Zorn theorem family, but H0 must wait for a pinpoint primary-source
audit and independent review.

## Crosswalk

| Repository phrase or datum | Frozen mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "partially ordered set" | carrier with reflexive, antisymmetric, transitive order | `alpha` with `PartialOrder alpha` candidate | included; universe and binder order open |
| omitted premise | every chain has an internal upper bound | `IsChain (fun x y => x <= y) c` implies `BddAbove c`, or the nonempty-chain variant | restored as indispensable; exact convention open |
| "maximal element" | an element with no distinct strictly larger element | `IsMax m` or an explicitly equivalent predicate | included; exact predicate and transport open |
| Max Zorn / 1935 | historical discovery key | immutable bibliographic record and source hash | no primary source pinned |
| "verified" | untrusted metadata status | kernel receipt for the exact normalized statement | supplies no proof credit |

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, bounded repository
search located `Mathlib/Order/Zorn.lean`. Candidate declarations include
`exists_maximal_of_chains_bounded`, `zorn_le`, and `zorn_le_nonempty`. The file describes
`exists_maximal_of_chains_bounded` as its primary statement and specializes it to orders. This is a
useful statement-phase lead, not an anchor audit: intake has not frozen an exact source statement,
normalized types, dependency closure, axiom report, proof-body provenance, or checked equivalence to
the canonical human claim.

## Hazards for the next phase

The empty-chain and nonempty-carrier presentations are mathematically interderivable only after the
relevant inhabitance reasoning is made explicit. `IsMax` in a preorder need not express equality
maximality without antisymmetry. A relation-based theorem assumes transitivity separately, while a
partial order packages more laws. A subset theorem also requires the upper bound to remain in the
subset. Each difference must be mapped rather than erased by choosing whichever declaration is most
convenient.

The provisional human state is `H1`: Zorn's lemma is a recognized proved theorem and the unresolved
source reconstruction is explicit, but exact edition/theorem/page, assumption and definition
crosswalks, errata review, and independent acceptance are absent. Machine state remains `M3` because
formal candidates exist but no canonical expression or exact-match evidence has been accepted.
