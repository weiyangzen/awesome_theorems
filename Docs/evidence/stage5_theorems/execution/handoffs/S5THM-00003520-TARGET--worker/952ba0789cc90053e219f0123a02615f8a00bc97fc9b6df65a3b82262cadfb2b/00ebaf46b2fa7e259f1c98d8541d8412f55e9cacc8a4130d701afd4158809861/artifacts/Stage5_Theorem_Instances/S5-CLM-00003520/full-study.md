# Full study

## Mathematical object

The source paper studies the equal-signature subgroup
`Γ_(m ⊕ n)` of a product of symmetric groups.  The frozen exceptional case
`(m,n) = (3,3)` is recorded as rank three, so no pair of elements has closure
equal to the whole subgroup.

## Frozen authority

Provider: `formal-conjectures-2270d31e`, revision
`2270d31e8dd611521f979de6d86da364930b7669`.  Source path:
`FormalConjectures/Arxiv/2605.12342/Conjecture1.lean`.  The source declaration,
declaration type, and raw block digests are retained in `intake.json` and the
crosswalk.  The Stage6 resolution is current and points to
`S6-CLM-00005794` / `S6-VAR-00001491`.

## Trust and replay

The provider theorem is marked `sorryAx` in the frozen source and is therefore
not used as a proof authority.  The claim-owned Lean files contain no
placeholders or local semantic redefinitions.  Machine closure is reported at
M0-L with an empty cut set; readability is R0 with an injective node/anchor
mapping and reverse fragment coverage.  Master must independently recompute
the elaborated expression, constant census, and cold replay before acceptance.

## Negative-fixture dominance

The release certificate strictly dominates THM-M-0387 by adding exact semantic
environment binding, semantic-substitution mutation checks, and cold-from-source
replay in addition to the fixture's shape predicates.
