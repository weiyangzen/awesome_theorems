# THM-M-0578 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the Milnor exotic-sphere
target. The repository source says only that there is a manifold homotopy
equivalent to the standard sphere but not diffeomorphic to it. That wording
does not specify a dimension, and it is weaker than the homeomorphism to the
7-sphere proved in Milnor's historical construction. Intake preserves this
ambiguity rather than silently replacing the source statement by the familiar
seven-dimensional theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Existence of a smooth manifold with the source-text sphere comparison and failure of diffeomorphism | Dimension and the exact topological comparison are unresolved |
| Constructed object | A candidate Milnor seven-manifold, commonly presented as an oriented `S^3`-bundle over `S^4` | No bundle parameterization or smooth-manifold encoding is selected |
| Topological comparison | Homotopy equivalence as written, or homeomorphism if primary-source audit authorizes the historical sharpening | A homeomorphism cannot be credited from the weaker generated phrase alone |
| Smooth distinction | Nonexistence of a diffeomorphism with the standard smooth sphere | Orientation conventions and the invariant used as the obstruction remain open |
| Boundary cases | Dimension, standard smooth structure, orientation reversal, and homeomorphic versus merely homotopy-equivalent inputs | These become statement mutations only after the root is fixed |
| Formal system | Lean 4 plus pinned mathlib | Exact imports, available manifold APIs, expression, and environment fingerprint remain for the statement phase |

The provisional scope nodes are construction, sphere comparison, smooth
obstruction, and boundary conventions. They are navigation labels only, not a
frozen obligation registry or machine-proof credit.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first
failed theorem gate is exact-statement identity. A primary historical proof
source has been identified, but the repository wording is insufficient to
choose between the literal dimension-unspecified claim and the stronger
seven-dimensional homeomorphic exotic-sphere theorem. The statement phase
must make that choice from source evidence and then freeze the complete Lean
type. No theorem completion is claimed.

## Validation

The commands and exact results for this intake are recorded in
`validation.md`. They validate target membership, repository structure, JSON
syntax, and dossier hygiene only. Master acceptance remains outstanding.

## Statement phase

The ambiguity is now resolved for the statement node by the second repository entry, which names
the existence of a seven-dimensional exotic sphere, and Milnor's cited homeomorphic-to-the-7-sphere
result. `Statement.lean` freezes the exact target as existence of a smooth seven-manifold
homeomorphic, but not diffeomorphic, to the standard smooth seven-sphere. The target and four
structural mutations elaborate under the pinned Lean environment. This is statement-only evidence:
the root remains unproved and master acceptance is pending.

## Anchor-audit phase

The immutable candidate ledger is recorded in `anchor-audit.json`. At pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the exact candidate
is a `proof_wanted` source marker discarded after signature elaboration, not a
retained theorem. Bounded external searches found no exact proof-bearing Lean 4
candidate; authenticated GitHub code search was unavailable and is not treated
as a negative result. The root remains `M4` with `formalization_debt`; this
phase supplies no proof or theorem-completion credit.

## Obligation-tree phase

`obligation-registry.json` freezes 13 root-relevant obligations, and
`typed-graphs.json` separates proof, refinement, provenance, evidence, trust,
documentation, and workflow edges. The route separates the Milnor bundle
construction, homeomorphism, and invariant obstruction. `ObligationTree.lean`
checks only final conditional composition; all three inputs remain open, the
root remains `M4`, and no theorem-completion credit is claimed.
