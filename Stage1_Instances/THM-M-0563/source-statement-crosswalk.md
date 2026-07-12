# Source-statement crosswalk

## Available repository record

`Docs/researches/math_theorems.md` records Rene Thom, 1954, and only the Chinese phrase
`流形的配边分类` (classification of manifolds by cobordism). `Docs/Stage0_Blueprint.md` repeats
that phrase and adds no hypotheses or conclusion. Its `已验证` label is untrusted metadata under
rev-5.6 and gives neither `H0` nor machine-proof credit.

## Candidate primary source

Rene Thom, *Quelques proprietes globales des varietes differentiables*, Commentarii Mathematici
Helvetici 28 (1954), 17-86, is the historical primary-source candidate. This intake has not
inspected a stable scan against an exact theorem/page, definitions, later corrections, or errata.
The bibliographic locator is therefore discovery evidence only, not a claim about the wording or
scope of a numbered theorem.

## Crosswalk

| Repository/source phrase | Mathematical choice it leaves open | Required Lean component | Intake status |
|---|---|---|---|
| "manifolds" | smooth closed manifolds, dimension, orientation/tangential structure | manifold model, dimension, compactness and boundary predicates | family identified; exact domain open |
| "cobordism" | unoriented, oriented, or structured cobordism and boundary identifications | cobordism relation with structural compatibility | included; relation open |
| "classification" | complete characteristic numbers, a group/ring computation, or Pontryagin-Thom identification | both directions of a complete invariant or an explicit isomorphism | conclusion family open |
| Thom / 1954 | historical attribution and source locator | no formal proof component | primary-source candidate identified only |
| `已验证` | repository inventory status | no proof component | explicitly untrusted |

## Non-substitution boundary

The invariant direction (cobordant manifolds have equal characteristic numbers) is weaker than a
classification criterion and cannot replace it. Likewise, the Pontryagin-Thom correspondence does
not by itself supply a computation of cobordism groups, while a computation in one orientation or
coefficient convention cannot replace another. The statement phase must preserve these boundaries
in its exact source-to-Lean rows and provide checked transports for any alternate encoding.

No theorem-specific repo-local Lean artifact was found by the scoped name/ID search at intake. That
negative result is not an anchor audit. The later anchor phase must search the pinned mathlib source
and credible external Lean 4 projects at immutable revisions, recording exact declaration types,
terminal bodies, imports, and trust boundaries.

Before `H0`, an independent reviewer must inspect the selected primary edition and approve the
theorem/page, definitions, every premise, coefficient and orientation conventions, proof boundary,
and errata. Before statement credit, every selected source component must map row by row to an
elaborated canonical Lean expression.
