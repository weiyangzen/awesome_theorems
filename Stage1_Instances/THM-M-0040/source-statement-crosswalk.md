# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:305-310` gives exactly the title
`阿密苏尔-列维茨基定理`, attribution Shimshon Amitsur/Alexander Levitzki, year 1950, gloss
`矩阵环满足的多项式恒等式` ("matrix rings satisfy a polynomial identity"), medium importance,
and status `已验证`. Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. It supplies no formula, matrix size, coefficient
domain, quantifiers, definition of polynomial identity, minimality clause, boundary convention,
bibliography, proof, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:1208-1233` repeats the gloss while explicitly leaving the exact
definitions and premises, formal system and foundation, proof route, dependencies, equivalent
forms, axioms, machine state, and artifact links open. The rev-5.6 manifest retains `已验证` only as
untrusted source metadata and resets the target to `L0 / rework_required`.

## Inspected primary paper

A. S. Amitsur and J. Levitzki, *Minimal identities for algebras*, *Proceedings of the American
Mathematical Society* 1(4), 449-463 (August 1950), DOI
`10.1090/S0002-9939-1950-0036751-9`, was inspected from the AMS version-of-record PDF on
2026-07-13. The observed PDF has SHA-256
`0e8233283a0d4430877fa8690c6d75ae8f3f7ccbaaeaf24aeb784038fe1c6a0b`. Crossref metadata confirms
the title, authors' initials, journal, volume, issue, pages, date, and DOI; its normalized record has
SHA-256 `fdfb49578a2f3c7055e9bbe1c344fa88b17574d3d85c7b45ee403258ba6ecbca`.

The paper gives several distinct source clauses:

- Printed page 449 defines a polynomial identity for an algebra over an underlying field and
  formula (2) defines the standard polynomial `S_(2n)` as the signed sum of all ordered products
  over permutations of `2*n` letters.
- Lemma 4 and Theorem 1 on printed page 455 prove that `S_(2n) = 0` holds for the complete algebra
  of all `n x n` matrices over that field.
- The introduction and Theorem 2 on printed pages 449 and 456 combine the identity with a prior
  lower bound to obtain minimal degree `2*n` and uniqueness among the displayed multilinear
  identities.
- Theorems 3-6 analyze broader minimal-polynomial classification and small characteristic-two
  exceptions. Theorem 7 later extends the minimal-degree statement to simple algebras over their
  centers.

This is a strong primary proof input, but it does not by itself select which source clause the
sparse catalog gloss owns. The catalog says "Alexander Levitzki," while the paper and Crossref say
`J. Levitzki`; that attribution needs accountable correction rather than silent normalization.
No independent source reviewer, correction/errata audit, lawful durable archive decision, or
accepted target-clause review is recorded. The paper therefore supports provisional `H1`, not H0.

## Component crosswalk

| Catalog/source component | Candidate mathematical meaning | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "matrix ring" | complete algebra of all `n x n` matrices over the underlying field | `Matrix (Fin n) (Fin n) F` with its ring structure | field/ring scope, positivity, and index encoding open |
| "polynomial identity" | a nonzero free noncommutative polynomial vanishing under every substitution | evaluated finite alternating sum, or a future free-algebra encoding | catalog does not identify the polynomial or representation |
| standard polynomial | signed sum over every permutation of `2*n` variables | `Equiv.Perm (Fin (2*n))`, `Equiv.Perm.sign`, `List.ofFn`, `List.prod`, finite sum | exact sign cast, product order, and expression not frozen |
| Theorem 1 | `S_(2n)` vanishes on the complete matrix algebra | universal equality to zero for every matrix tuple | strongest direct match to the gloss; still not catalog-selected |
| minimality | no lower-degree nonzero identity, with degree exactly `2*n` | a quantified free-polynomial predicate and degree comparison | additional theorem package, definitions, and source dependency |
| uniqueness | minimal multilinear identities are scalar multiples of `S_(2n)` | classification statement | not implied by the repository gloss |
| Amitsur/Levitzki, 1950 | inspected A. S. Amitsur/J. Levitzki paper | no Lean component | catalog coauthor forename mismatch remains open |
| `已验证` | untrusted inventory label | accepted source and kernel receipts would be required | no H or M credit |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.GroupTheory.Perm.Sign` supplies finite permutation signs; `Mathlib.Data.Fintype.Perm`
supplies enumeration/cardinality infrastructure; `Mathlib.Data.Matrix.Mul` supplies the square
matrix ring and ordered multiplication; and list/big-operator APIs can express ordered products and
finite sums. `IntakeProbe.lean` elaborates representative interfaces without defining a target.

A bounded case-insensitive search of repository Lean and pinned mathlib found no exact
Amitsur-Levitzki or standard-polynomial declaration. Searches for "Levitzki" encounter
`Mathlib.RingTheory.HopkinsLevitzki`, which is explicitly unrelated. This is intake discovery only,
not the downstream precommitted anchor audit or a proof of global absence. Infrastructure does not
choose the source proposition and supplies no root proof, so the machine status is `M4`.

## Source gate

Before the statement phase can close, accountable reviewers must resolve the coauthor attribution,
admit an immutable approved source edition, select the exact identity/minimality/uniqueness root,
map every definition, binder, premise, conclusion, proof-source dependency, characteristic and
boundary case, and audit corrections and errata. The selected claim must then elaborate with
minimal pinned imports, checked transports, expression/environment fingerprints, and the required
removed-hypothesis, changed-domain, binder-scope, and boundary mutations.

This crosswalk freezes source evidence, ambiguities, and non-substitution boundaries only. It does
not freeze a canonical proposition or accept H0, M0, R0, audit completion, theorem completion, or
master acceptance.
