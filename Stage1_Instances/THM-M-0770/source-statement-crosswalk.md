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
| "partially ordered set" | carrier with reflexive, antisymmetric, transitive order | `alpha : Type u` with `PartialOrder alpha` and `Nonempty alpha` | exact Lean domain self-tested |
| omitted premise | every nonempty chain has an internal upper bound | `IsChain (fun x y => x <= y) c -> c.Nonempty -> BddAbove c` | restored and elaborated; primary-source fidelity remains open |
| "maximal element" | an element with no distinct strictly larger element | `IsMax m`, with a checked equality-form expansion under `PartialOrder` | exact Lean conclusion self-tested |
| Max Zorn / 1935 | historical discovery key | immutable bibliographic record and source hash | no primary source pinned |
| "verified" | untrusted metadata status | kernel receipt for the exact normalized statement | supplies no proof credit |

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, bounded repository
search located `Mathlib/Order/Zorn.lean`. The statement phase selects the type shape of
`zorn_le_nonempty`, specialized from its `Preorder` parameter to the intake-required
`PartialOrder`. `Statement.lean` checks a direct local copy of that type and separately expands
`IsMax` to equality maximality. This is not an anchor audit: dependency closure, proof-body
provenance, trust report, and exact primary-source H0 remain open.

## Hazards for the next phase

The canonical statement now chooses explicit carrier nonemptiness and bounds only for nonempty
chains. The all-chain form is elaborated only as a distinct mutation, not credited as an automatic
transport. `IsMax` in a preorder need not express equality maximality without antisymmetry, which is
why the target retains `PartialOrder`. A relation-based theorem assumes transitivity separately,
while a subset theorem also requires the upper bound to remain in the subset. Those variants remain
bridge obligations rather than substituted roots.

The provisional human state is `H1`: Zorn's lemma is a recognized proved theorem and the unresolved
source reconstruction is explicit, but exact edition/theorem/page, assumption and definition
crosswalks, errata review, and independent acceptance are absent. The canonical expression is now
self-tested, but machine state remains `M3`: statement elaboration is not proof or anchor closure,
and master acceptance is pending.
