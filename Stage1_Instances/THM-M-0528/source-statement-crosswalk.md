# Source-statement crosswalk

## Repository source

The repository research record gives the Chinese title `单值化定理`, the gloss
`覆盖空间的提升唯一性`, attribution to multiple authors, a twentieth-century date, and the label
`已验证`. It gives no edition, theorem number, page, hypotheses, or formal declaration. Under
rev-5.6 the status label is untrusted and supplies no proof credit.

## Source candidates

Allen Hatcher, *Algebraic Topology* (2002), Section 1.3 is a primary textbook candidate for the
covering-space lifting theory. The pinned mathlib source independently identifies Hatcher's
Theorem 1.7 (p. 30) for homotopy lifting and Propositions 1.31 and 1.33 for related fundamental
group and lifting-criterion results. These are discovery anchors only: this intake did not freeze
an exact Hatcher proposition as the repository target or complete an edition/page/errata review.

The pinned mathlib checkout at commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains relevant candidate APIs in `Mathlib.Topology.Covering.Basic` and
`Mathlib.Topology.Homotopy.Lifting`, including `IsCoveringMap.eq_of_comp_eq`, path-lift uniqueness,
and `IsCoveringMap.existsUnique_continuousMap_lifts`. This is a machine-candidate discovery note,
not an anchor audit or repo-local closure claim.

## Crosswalk

| Repository datum | Human-source component | Required Lean component | Intake status |
|---|---|---|---|
| `单值化定理` | ambiguous title | no title-driven proposition | analytic interpretation explicitly excluded |
| `覆盖空间` | covering projection | `IsCoveringMap p` or checked equivalent | subject fixed; exact encoding open |
| `提升` | maps into the total space commuting with projection | continuous maps/functions plus `p ∘ g = f` | binder order and representation open |
| `唯一性` | equality from a common initial value | equality/unique-existence conclusion | path versus general-map variant open |
| implicit domain condition | connectedness used to propagate equality | `PreconnectedSpace`, `PathConnectedSpace`, or source-equivalent hypotheses | must be selected from exact source |
| `已验证` | unsupported metadata label | no accepted declaration | untrusted; zero proof credit |

The statement phase selects the general-map variant matching `IsCoveringMap.eq_of_comp_eq`, which
the pinned mathlib source labels Proposition 1.34 of Hatcher. `Statement.lean` freezes every formal
quantifier and checks the pointwise/composite-equality transport. To advance source fidelity to
`H0`, the dependent anchor audit must still inspect a stable primary edition, record its exact page
and assumptions, check errata, and independently review the source-to-Lean crosswalk.
