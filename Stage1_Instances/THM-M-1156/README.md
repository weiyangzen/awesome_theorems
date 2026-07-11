# THM-M-1156 rev-5.6 intake

This directory is the `planned` instance for the Stage0 entry named Potential theory. The repository
supplies only the phrase `Newton位势与对数位势` (Newtonian and logarithmic potentials),
which names a subject and two constructions rather than a proposition. The intake therefore freezes
the ambiguity instead of silently choosing a more convenient theorem.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Source identity | `THM-M-1156`, Stage0 phrase above, PDE category | The untrusted `已验证` label supplies no statement or evidence |
| Mathematical objects | Newtonian and logarithmic potentials | Dimension, kernel normalization, sign, density/measure class, and integrability are absent |
| Possible claims | definitions, fundamental-solution identities, Poisson equations, harmonicity off support, representation results | These are a disambiguation menu only; none is selected or credited |
| Formal target | Lean 4 proposition after a primary-source pinpoint fixes the claim | No module, declaration, binders, hypotheses, or conclusion is frozen |
| Target separation | General potential-theory entry only | Neighboring `THM-M-1157` is a distinct Newton-potential target and is not absorbed here |
| Evidence | Repository metadata and this scope audit | No human proof, Lean closure, or source-fidelity receipt exists |

## Open task DAG

`INTAKE` records the source ambiguity. `STATEMENT` is blocked until a primary source identifies one
exact proposition and all analytic conventions. Only then may `ANCHOR_AUDIT`, `OBLIGATION_TREE`,
`PROOF`, `VALIDATION`, and `RELEASE` proceed in that order. A valid resolution must say whether the
root is one theorem relating both potentials or one explicitly quantified theorem schema; merely
formalizing their definitions does not resolve the current record.

## Intake verdict

Lifecycle remains `planned`, with provisional vector `[H4, M4, R4]`. The first failed gate is exact
source-statement identification. The dossier is a truthful intake artifact, not a theorem result.
The theorem is not complete.

## Validation

The commands and exact outcomes are recorded in `validation.md`. They check target membership,
repository-standard consistency, JSON syntax, scoped references, and whitespace only.
