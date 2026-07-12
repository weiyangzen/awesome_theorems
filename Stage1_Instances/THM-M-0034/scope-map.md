# Scope map

## Received identity

| Field | Frozen intake value | Boundary |
|---|---|---|
| theorem ID | `THM-M-0034` | the only target owned by this dossier |
| title | Quillen-Suslin theorem | identifies a theorem family, not an exact proposition |
| attribution/date | Daniel Quillen and Andrei Suslin, 1976 | historical discovery lead only |
| catalog gloss | proof of Serre's conjecture | refers to the neighboring conjecture record rather than spelling out this target |
| adjacent gloss | projective modules over a polynomial ring are free | narrows the family but omits material binders and hypotheses |
| catalog status | verified | explicitly untrusted under rev-5.6 |

## Selected statement shape

The proposal selects a field `k`, a positive natural number `n`, the ring
`MvPolynomial (Fin n) k`, and a type `P` with additive-group, module, finite-generation, and
projectivity instances. Its conclusion is `Module.Free (MvPolynomial (Fin n) k) P`. The coefficient
and module universes are independent.

| Decision | Alternatives that change scope |
|---|---|
| coefficient object | `Field k`; the stronger PID clause is not selected as the root |
| polynomial ring | `MvPolynomial (Fin n) k` with explicit `0 < n` |
| module convention | unital left module, harmless over the selected commutative ring |
| size premise | `Module.Finite` and `Module.Projective` |
| conclusion | `Module.Free`, existence of a basis without specified rank |
| quantifier order | `k`, field instance, `n`, positivity, `P`, additive/module/finite/projective instances |
| universe/finiteness encoding | `k : Type u`, `P : Type v`, `n : Nat` |
| foundation | proposition only here; proof-specific classical principles remain downstream |

## Frozen boundary cases

- Zero variables are excluded by `0 < n`; the inspected source does not expressly state that
  extension.
- The zero module and rank zero are included; no `Nontrivial P` premise is present.
- Infinitely many variables and projectives without finite generation are excluded.
- Actual freeness is required; stable freeness, matrix completion, and vector-bundle forms receive
  no identity credit without checked transports.
- A field is nontrivial in the selected Lean structure, so a trivial coefficient ring is excluded.

## Excluded substitutions

- `THM-M-0033`, the separately cataloged Serre-conjecture item;
- the theorem that free modules are projective, which is the easy reverse implication;
- a result only for principal ideal domains, Euclidean domains, local rings, or one variable;
- stable freeness without a checked bridge to actual freeness;
- a unimodular-row or matrix-completion result without checked equivalence to the selected module statement;
- a theorem about projective schemes, Quillen model categories, or descriptive-set-theoretic Suslin theorems;
- a structure, basis field, instance, axiom, experiment, or certificate that assumes the conclusion;
- the title, author/year, catalog status, or intake API checks used as proof evidence.

## Lean scope boundary

The pinned environment contains the prospective vocabulary:

| Mathematical component | Pinned Lean surface | Intake result |
|---|---|---|
| projective module | `Module.Projective R P` | definition selected as a target premise; no root theorem |
| free module | `Module.Free R P` | definition selected as the target conclusion |
| finite generation | `Module.Finite R P` | source-mapped premise frozen pending independent review |
| polynomial ring | `Polynomial R` | unselected alternate carrier |
| multivariable polynomial ring | `MvPolynomial (Fin n) k` | selected with `0 < n` pending master acceptance |
| easy reverse implication | `Module.Projective.of_free` | checked neighboring theorem; explicitly not the target |

The canonical declaration is `Stage1Instances.THM_M_0034.QuillenSuslinTarget`, with expression
SHA-256 `d80cc9860ed5a53c81a0851b4dc8e702aa5a23d448f373ae6d68ed0c9b5604b1`. No alternate
transport, obligation registry, discovery protocol, or proof body is credited.
