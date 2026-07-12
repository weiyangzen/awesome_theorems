# THM-M-0029 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:228-233` names `中山引理`, attributes it to Tadashi Nakayama,
dates it 1951, and supplies only `关于模的生成元的引理` ("a lemma about generators of
modules"). `Docs/Stage0_Blueprint.md:911-936` repeats the gloss and explicitly leaves definitions,
premises, proof route, dependencies, equivalent formulations, axioms, and machine artifacts open.
All six catalog fields originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted`.

The catalog wording is not binder-complete. In particular, "generators" does not decide whether
the result is about vanishing of a finitely generated module, an annihilating scalar, or lifting a
generating set from a quotient. Assigning any one of these as the root without a source would
substitute missing mathematics.

## Human-source leads

The publisher-hosted PDF of Tadasi Nakayama, *A Remark on Finitely Generated Modules*, Nagoya
Mathematical Journal 3 (1951), pages 139-140, DOI `10.1017/S0027763000012265`, was inspected from
temporary storage on 2026-07-13; its observed SHA-256 is
`1a2eeb7d75a2b8373ea8eddfef547714029550b296bda80d65714134cbd36515`.
The paper contains assertions I-V. Assertion II says, under the paper's general ring convention,
that if `N` is the radical of `R` and a finitely generated right `R`-module `m` satisfies
`m = mN`, then `m = 0`. That is a precise primary candidate for the radical-vanishing form, but it
does not settle whether the catalog's generator gloss intends assertion II, assertion I, or a
modern quotient-generator formulation.

Pinned mathlib comments also cite Atiyah-Macdonald section 2.5, Eisenbud section 4.7, Matsumura
section 2.2, and the Stacks Project tag `00DV`. These are useful locators, not admitted `H0`
evidence. The publisher PDF has not been admitted to an immutable repository archive, and this
intake has not fixed the exact root, checked translations or corrections/errata, mapped all
definitions, assumptions, conclusion clauses, and proof nodes, or obtained independent review.

## Component mapping

| Catalog component | Candidate meaning | Pinned Lean surface | Intake status |
|---|---|---|---|
| module | an `R`-module or a submodule `N` of an ambient module | `[Module R M]`, `Submodule R M` | exact carrier and handedness open |
| finite-generation premise | the ambient module or submodule has a finite generating set | `Submodule.FG N` | candidate premise only; not itself the lifting conclusion |
| specified quotient generators | images of a selected family or set span modulo `I * N` and representatives span before quotienting | quotient map, `Submodule.span`, image and injectivity | candidate hypothesis/conclusion surface only |
| ideal multiple | `N <= I * N` or equality | `N <= I • N`, `N = I • N` | direction and role open |
| Jacobson condition | `I` lies in a selected Jacobson radical | `I <= Ideal.jacobson bot` or a generalized radical | absent from catalog |
| vanishing | the finitely generated submodule is bottom | `N = bot` | one candidate conclusion |
| quotient generators | lift a spanning set modulo `I * N` | quotient map, `Submodule.span`, image and injectivity | one candidate conclusion |
| Tadashi Nakayama / 1951 | catalog attribution | no formal component | not independently verified |
| `已验证` | untrusted inventory label | no formal component | no H/M credit |

## Pinned formal candidates

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- `Mathlib.RingTheory.Finiteness.Nakayama` declares
  `Submodule.exists_sub_one_mem_and_smul_eq_zero_of_fg_of_le_smul`, the determinant-trick form for
  a finitely generated submodule over a commutative ring.
- `Mathlib.RingTheory.Nakayama` declares
  `Submodule.eq_bot_of_le_smul_of_le_jacobson_bot`, the Stacks `00DV` statement (2) vanishing form.
- The same module declares `Submodule.smul_le_of_le_smul_of_le_jacobson_bot`, the Stacks `00DV`
  statement (4) relative generation consequence.
- The same module declares
  `Submodule.exists_injOn_mkQ_image_span_eq_of_span_eq_map_mkQ_of_le_jacobson_bot`, the Stacks
  `00DV` statement (8) generator-lifting form.

`IntakeProbe.lean` checks these interfaces under the pinned toolchain. Their presence supports an
`M3` interface classification only. Intake does not choose one as the canonical target, inspect
terminal body identity or transitive closure, or credit a proof.

## Required exact crosswalk

Before statement acceptance, an independent reviewer must map every source domain, ordered binder,
hypothesis, conclusion, degenerate case, definition, and alternate form to one elaborated Lean
expression. Any implication or equivalence between a source form and a pinned candidate must have
a checked witness in the required direction. Until that work exists, `canonical_statement`, the
formal module/declaration, and statement fingerprints remain null.
