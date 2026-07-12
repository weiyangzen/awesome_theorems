# Source-statement crosswalk

## Available repository source

`Docs/researches/math_theorems.md` records only the Chinese title `素模型`, attribution to
"multiple mathematicians", the twentieth century, and the sentence `素模型的存在性与唯一性`.
`Docs/Stage0_Blueprint.md` repeats that sentence and explicitly leaves precise definitions,
hypotheses, proof history, axioms, dependencies, and machine artifacts to be supplied. Neither file
contains a bibliography, theorem number, page, exact wording, or errata record.

Thus the repository record does not identify one theorem. Its `已验证` value is metadata-screening
input, not a reviewed human proof or kernel receipt.

## Candidate scholarly anchors

- C. C. Chang and H. J. Keisler, *Model Theory*, third edition, North-Holland (1990), the treatment
  of prime and atomic models.
- David Marker, *Model Theory: An Introduction*, Graduate Texts in Mathematics 217, Springer
  (2002), the chapter material on atomic and prime models.

These are discovery candidates only. No exact edition passage, theorem/page, assumptions, proof,
corrections, or errata has been inspected and independently reviewed for this intake, so they do
not establish `H0` or select a canonical statement.

## Crosswalk

| Repository phrase | Mathematical data needed | Required Lean component | Intake result |
|---|---|---|---|
| "prime model" | a model of fixed `T` elementarily embeddable into every model of `T` | language, structures, theory satisfaction, elementary embeddings | family identified; definition not frozen |
| "existence" | a sufficient and necessary/source-stated condition for a prime model | explicit hypotheses and construction/existence proposition | unresolved; unconditional form excluded |
| "uniqueness" | any two prime models of the same `T` are isomorphic, under exact source conditions | two models, primeness witnesses, structure isomorphism | intended family identified; exact theorem open |
| theory/language | completeness, consistency, countability, cardinality conventions | universes, theory type, model instances | absent from source |
| atomic/isolated types | standard existence criterion or characterization in some formulations | types, realization, isolation, atomic-model predicates | candidate bridge only; source selection required |
| `已验证` | an untrusted catalog label | inspectable source or kernel evidence | no credit |

## Lean discovery boundary

A repository-wide search found no theorem-specific Lean module for `THM-M-0676`. In pinned
mathlib, `Mathlib/ModelTheory` provides substantial first-order syntax, semantics, elementary maps,
elementary substructures, types, and related infrastructure. The only name hits for `IsAtomic` in
the scoped search concern **atomic formulas** in `Mathlib/ModelTheory/Complexity.lean`; they are not
an atomic-model or prime-model existence theorem. This negative scoped search is intake discovery,
not the later immutable candidate/provenance audit.

Before `H0`, an independent reviewer must select a stable source, verify exact theorem/page,
definitions, all hypotheses, proof boundaries, corrections, and errata, and approve a row-by-row
source mapping. Before statement credit, those approved rows must map to an elaborated Lean
expression with checked transports for any alternate formulation.
