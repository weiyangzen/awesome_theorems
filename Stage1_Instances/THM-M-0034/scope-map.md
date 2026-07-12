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

## Candidate mathematical shape

A common modern formulation is: for a field `k`, a finite set of indeterminates, and a finitely
generated projective module `P` over the resulting polynomial ring, `P` is free. This is a
candidate family description only. The statement phase must select an immutable source and decide
all of the following before it may create a canonical proposition:

| Decision | Alternatives that change scope |
|---|---|
| coefficient object | field, division ring, PID, regular ring, or another base class |
| polynomial ring | `k[X]`, finitely many named variables, `MvPolynomial (Fin n) k`, or an arbitrary finite variable type |
| module convention | left or right module; commutative specialization; bundled module versus typeclasses |
| size premise | finitely generated module, finite module typeclass, constant finite rank, or unrestricted projective module |
| conclusion | existence of some basis, finite basis of a specified rank, stable freeness, or an explicit matrix completion |
| quantifier order | fixed `n`/variable type and module versus uniform quantification over them |
| universe/finiteness encoding | `Finite`, `Fintype`, explicit finite set, or a natural number of variables |
| foundation | use of choice to select a basis and any classical ideal/module principles |

## Boundary cases held open

- zero variables, where the polynomial ring reduces to the coefficient ring;
- empty or trivial coefficient ring if the selected algebraic structures permit it;
- the zero module, rank-zero modules, and nontriviality assumptions;
- infinitely many variables;
- projective modules that are not finitely generated;
- finite generation as a module versus finite presentation or constant finite rank;
- stable freeness versus actual freeness and whether a finite basis is required;
- univariate-to-multivariate induction versus a direct finite-variable statement.

No case is excluded at intake. Every exclusion must be justified by the selected source rather than
chosen to match a convenient Lean encoding.

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
| projective module | `Module.Projective R P` | definition checked; no root theorem |
| free module | `Module.Free R P` | definition checked; conclusion candidate only |
| finite generation | `Module.Finite R P` | vocabulary checked; source premise unresolved |
| polynomial ring | `Polynomial R` | carrier checked; variable convention unresolved |
| multivariable polynomial ring | `MvPolynomial sigma R` | carrier checked; finiteness convention unresolved |
| easy reverse implication | `Module.Projective.of_free` | checked neighboring theorem; explicitly not the target |

No canonical module, declaration, elaborated-expression fingerprint, alternate transport,
obligation registry, or discovery protocol is frozen. Those are downstream gates.
