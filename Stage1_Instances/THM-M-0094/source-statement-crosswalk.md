# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:691-696` supplies exactly the title
`博雷尔-韦伊-博特定理`, attribution to Armand Borel, Andre Weil, and Raoul Bott, year 1954, gloss
`紧李群表示的几何实现` ("geometric realization of compact Lie-group representations"), importance
high, and formalization status `已验证`. All six uncited fields originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:2686-2711` repeats that gloss while explicitly leaving definitions and
premises, proof route, dependencies, equivalent forms, axioms, formal system, machine status, and
artifact links open. The rev-5.6 manifest retains `已验证` only as untrusted metadata and resets the
target to `L0 / rework_required`.

Neither record identifies a bibliography, edition, theorem/page, formula, definitions, ordered
binders, proof boundary, translation/correction history, or reviewer. The title selects the full
Borel-Weil-Bott family while the gloss omits the higher-cohomology and vanishing clauses; the
degree-zero Borel-Weil realization is only a special case. The record is evidence of the requested
family, not `H0` source evidence.

## Historical source leads

A bounded Crossref query on 2026-07-13 authenticated:

- Raoul Bott, *Homogeneous Vector Bundles*, *Annals of Mathematics* 66(2) (1957), starting at
  page 203, DOI `10.2307/1969996`.

This is a strong lead for the higher-cohomology theorem conventionally associated with Bott. The
DOI redirected to an access-controlled page here, so no article text or theorem passage was
inspected. Crossref also authenticated Armand Borel's 1953 paper *Sur La Cohomologie des Espaces
Fibres Principaux et des Espaces Homogenes de Groupes de Lie Compacts*, DOI `10.2307/1969728`, but
metadata alone does not establish that it contains the exact representation-realization statement.

The repository's 1954 date and combined Borel/Weil/Bott attribution are not reconciled by those
records. No admitted authoritative exact passage, definition chain, premise/conclusion map, Borel-Weil antecedent,
translation, corrections or errata, modern reformulation transport, or independent review was
accepted. The leads support `H1`, not `H0`.

A publicly retrievable modern proof note, Jacob Lurie's *A Proof of the Borel-Weil-Bott Theorem*
(three-page PDF, 2012 file metadata), gives a precise formulation and proof in Theorem 5. For a
complex reductive algebraic group `G`, Borel subgroup `B`, flag variety `X = G/B`, maximal torus
with character lattice `Lambda`, and the shifted line-bundle convention `L_lambda := L_{rho-lambda}`,
it states total cohomology vanishing for nonregular `lambda`; for regular `lambda`, it states a
unique nonzero cohomology group in the length of the unique Weyl element sending `lambda` to a
dominant weight, dual to the irreducible representation of highest weight `w(lambda) - rho`. The
retrieved PDF SHA-256 was
`57d1df87dc0641ec70bc2e353830897dcabd88dd973d82365ee30713f0a1f8f1`. This is a precise
candidate scope and convention map, but it is not the original historical source, is not stored as
an immutable dossier source, has not received a complete assumption/correction crosswalk or
independent review, and has not been admitted; it does not clear `H0` or select conventions by itself.

## Clause crosswalk

| Repository phrase | Material interpretations | Pinned Lean surface | Intake status |
|---|---|---|---|
| "compact Lie group" | compact connected semisimple/reductive group, complexification, or a complex semisimple algebraic group | `LieGroup`, generic group APIs | topology exists, but compactness/connectedness/complexification and the flag-space bridge are not joined |
| "representations" | finite-dimensional continuous complex group representations, holomorphic representations, or highest-weight Lie-algebra modules | `Representation`, `Representation.IsIrreducible`, `LieModule.Weight` | algebraic substrate only; continuity, equivariance, and highest-weight correspondence are absent |
| "geometric realization" | global holomorphic sections, algebraic sections, or higher sheaf cohomology of a homogeneous line bundle | `CategoryTheory.Sheaf.Γ`, `CategoryTheory.Sheaf.H` | abstract site-level APIs only; no flag variety or homogeneous line bundle is supplied |
| Borel-Weil inside Bott | degree-zero dominant case is a special case/antecedent of the full regular/singular all-degree theorem | generic `cohomologyFunctor` | title selects the full family; exact degree and vanishing conventions remain open |
| flag/root data | maximal torus/Borel, positive roots, weights, Weyl vector, dot action, Weyl length | `RootPairing`, `LieAlgebra.IsKilling.rootSystem` | adjacent root data only; no flag variety, Weyl-action cohomology statement, or bridge found |
| `已验证` | untrusted inventory label | no expression or receipt | explicitly rejected as evidence |

## Pinned formal leads

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe authenticates
global sections (`CategoryTheory.Sheaf.Γ`), abstract abelian sheaf cohomology
(`CategoryTheory.Sheaf.H` and `cohomologyFunctor`), scheme module sheaves and pushforward,
Lie weights and a semisimple Lie-algebra root system, abstract root pairings, generic
representations and irreducibility, and the manifold Lie-group typeclass.

Those APIs are only adjacent infrastructure. In particular, `Sheaf.H` is general site-level Ext
cohomology, not a theorem about a coherent homogeneous line bundle on a flag variety. A bounded
case-insensitive search of repo-local Lean and pinned mathlib found no Borel-Weil/Bott declaration,
flag-variety theorem, homogeneous-vector-bundle theorem, or complete cohomology-to-representation
bridge. The probe elaborates named interfaces and reports axioms for three adjacent theorems, but it
declares no target. This supports provisional `M4`, not proof credit and not an exhaustive later
anchor/provenance audit.

## Neighbor and non-substitution boundary

The nearby `THM-M-0090` Weyl character formula, `THM-M-0091` Weyl dimension formula, and
`THM-M-0093` highest-weight theorem do not share state or proof credit. Nor may Bott periodicity,
Bott vanishing, generic sheaf cohomology, or an abstract root-system result replace this root.

## First source/statement gate

An independent review must preserve an authoritative source and select one exact proposition,
including the theorem variant, group and geometric category, flag variety and line bundle,
weights/signs/dot action, regular and singular cases, cohomological degrees, returned
representation, all boundary cases, and the historical-to-modern transport. Only then may the
statement phase elaborate and mutation-test an exact Lean target.
