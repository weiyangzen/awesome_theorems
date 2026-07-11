# THM-M-0470 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Ullmo's theorem, understood as Ullmo's
proof of the Bogomolov conjecture for curves. The Stage0 phrase "proof of the Bogomolov
conjecture" is too broad by itself: this intake deliberately does not substitute the later
general theorem for subvarieties of abelian varieties.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Finiteness of sufficiently small canonical-height points on a genus-at-least-two curve embedded in its Jacobian | Exact source notation and Lean encoding remain open |
| Arithmetic base | A number field, its algebraic closure, and algebraic points | No general finitely generated field variant is credited |
| Geometry | Smooth projective geometrically connected curve, Jacobian, degree-one embedding, symmetric theta polarization | Construction choices and invariance transports require checking |
| Height | Neron-Tate canonical height on the Jacobian | Normalization and the comparison with source notation require audit |
| Equivalent forms | Positive essential minimum; non-Zariski-density of small points | Candidate equivalences only, with no checked transport |
| Proof architecture | Arakelov intersection theory, admissible metrics, and positivity/equidistribution ingredients suggested by the primary paper | No obligation registry or proof leaf is frozen in intake |
| Formal foundations | Lean 4 plus pinned mathlib | Necessary arithmetic-geometry APIs and exact TCB are unknown |

The structured claim, binders, hypotheses, exclusions, and provisional assurance vector are in
`intake.json`. Source genealogy and statement correspondence are in
`source_statement_crosswalk.md`.

## Open task DAG

The dependent rev-5.6 nodes remain, in order: `STATEMENT`, `ANCHOR_AUDIT`,
`OBLIGATION_TREE`, `PROOF`, `VALIDATION`, and `RELEASE`. The immediate next node must choose an
exact Lean representation without weakening the arithmetic-geometric claim, elaborate it, and
mutation-test its domains, genus bound, height threshold, and finiteness conclusion.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate
is the exact Lean statement gate: there is no declaration, elaborated expression hash,
environment fingerprint, or checked transport. This theorem is not complete.

## Validation

`validation.md` records the exact structural and dossier-local checks run against the base
revision. These checks establish a self-tested intake artifact, not mathematical or kernel proof
closure.
