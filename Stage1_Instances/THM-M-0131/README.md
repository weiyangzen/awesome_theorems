# THM-M-0131 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the repository item named "Shimura
correspondence" (`志村对应`). Historical labels and the source field `已验证` provide no proof
credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Repository claim | "a correspondence between elliptic curves and modular forms" | Preserved verbatim in meaning; it lacks the data needed for an exact proposition |
| Name interpretation | classical Shimura correspondence | The standard name commonly concerns half-integral and integral weight modular forms, not the repository gloss |
| Gloss interpretation | modularity of elliptic curves over a specified field | Field, level, weight, normalization, direction, and equivalence relation are absent |
| Lean statement | explicit universes, objects, hypotheses, and conclusion | Intentionally not invented; dependent statement phase is blocked on disambiguation |
| Machine evidence | Lean 4 plus pinned mathlib | No declaration, import, proof, or anchor is credited |
| Human evidence | a primary edition and exact theorem/page crosswalk | Not located or accepted in this intake phase |

The later statement phase must first choose one theorem family from an authoritative source and
record the field, curve hypotheses, modular-form data, correspondence relation, quantifiers, and
degenerate cases. Only then may it elaborate and fingerprint a Lean expression. Treating the broad
gloss as a proposition would silently broaden or substitute the theorem.

## Open task DAG

`source disambiguation -> exact human statement -> Lean object-model selection -> elaboration and
mutation tests -> anchor audit -> frozen obligation graphs -> proof -> validation -> release`

Every arrow is open. In particular, the similarly named Taniyama-Shimura/modularity target
`THM-M-0132` must not donate scope or proof credit to this target.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H4, M4, R3]`. The first failed gate is exact
source-statement identification. This is a truthful intake boundary, not theorem completion.

## Validation

The exact commands and results used to check membership, repository consistency, JSON syntax, and
owned-path integrity are recorded in `validation.md`.
