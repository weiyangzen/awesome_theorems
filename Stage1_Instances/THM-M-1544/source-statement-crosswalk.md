# Source-statement crosswalk

## Primary source anchor

M. F. Atiyah, N. J. Hitchin, V. G. Drinfeld, and Yu. I. Manin, "Construction of instantons",
*Physics Letters A* **65** (1978), 185-187, DOI `10.1016/0375-9601(78)90141-X`, is the original
primary-paper anchor. Its pagination and bibliographic identity are frozen here; exact displayed
formulae, hypotheses, theorem wording, and any errata have not yet received the source audit needed
for `H0`. The Stage0 attribution and year agree with this anchor, but its label `已验证` is untrusted
metadata and provides no proof credit.

## Crosswalk

| Repository/source phrase | Intended component | Required Lean component | Intake status |
|---|---|---|---|
| "ADHM construction" | algebraic construction and classification of instantons | a concrete correspondence theorem, not a packaged assumption | included; exact formulation open |
| instanton | framed ASD connection of fixed charge on `S^4`/`R^4` | bundles, connections, curvature, Hodge star, finite-action/framing conditions | included; APIs open |
| algebraic data | finite-dimensional matrices/linear maps with reality structure | typed finite-dimensional linear maps and adjoints | included; presentation open |
| ADHM equations | quadratic real/complex moment-map relations | explicit equations | included; conventions open |
| nondegeneracy | regularity/stability ensuring a bundle and nonsingular connection | explicit rank/stability predicate | required; exact predicate open |
| equivalence | gauge classes correspond to basis-change classes | quotients or setoids and a checked bijection | included; groups open |
| construction | kernel/monad data reconstruct the ASD connection | concrete reconstruction plus correctness | included; analytic obligations open |

## Fidelity boundary

The three-page original article is a primary discovery anchor, not yet a fully audited modern
statement specification. The statement phase must inspect a stable copy, determine exactly which
direction and gauge group the paper proves, cross-check definitions against a detailed standard
treatment, record edition/page anchors and errata, and obtain independent review. No repository
Lean declaration or external formalization has been credited at intake.
