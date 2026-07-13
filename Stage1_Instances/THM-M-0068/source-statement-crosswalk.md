# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:505-510` supplies exactly the title `弗罗贝尼乌斯定理`, Ferdinand
Frobenius attribution, year 1895, gloss `群特征标的正交关系` ("orthogonality relations of group
characters"), importance high, and formalization status `已验证`. All six uncited fields originate
in repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:1974-1999` repeats the gloss while explicitly leaving exact definitions
and premises, proof route, dependencies, equivalent forms, axioms, machine status, and artifact
links open. The rev-5.6 manifest retains `已验证` only as untrusted metadata and resets the target
to `L0 / rework_required`.

Neither repository record gives a bibliography, edition, theorem/page, formula, definition chain,
ordered binders, proof boundary, translation or correction history, or reviewer. The Frobenius/1895
attribution is therefore a historical lead only. It is not `H0` source evidence.

A bounded zbMATH Open bibliographic query observed on 2026-07-13 locates G. Frobenius,
*Ueber Gruppencharaktere*, *Sitzungsberichte der Königlich Preussischen Akademie der
Wissenschaften* 1896, pages 985-1021, JFM `27.0092.01`, zbMATH document `2675572`. Its 1896
publication metadata conflicts with the catalog's 1895 date. The API record and review identify
the introduction of characters for arbitrary finite groups, but no preserved primary edition,
exact orthogonality passage, definition chain, or proof boundary was inspected. This is a
non-credited source lead; the date and statement identity require review.

## Clause crosswalk

| Repository phrase | Material interpretations | Pinned Lean surface | Intake status |
|---|---|---|---|
| "group" | usually a finite group in ordinary character orthogonality | `G` with `[Group G] [Fintype G]` | finiteness is absent from the catalog |
| "character" | trace of a finite-dimensional representation, irreducible character, class function, or abelian-group character | `FDRep.character`, `Representation.character` | direct representation API found; intended encoding open |
| "orthogonality" | normalized or unnormalized row relation, column relation, or an explicit package of character relations | `FDRep.char_orthonormal`, `Representation.char_orthonormal` | row relation is a strong lead, not selected root |
| second factor | inverse argument, complex conjugate, or star | `W.character g⁻¹` in the direct candidates | transport to conjugation needs source-specific field and character facts |
| delta | equality of representatives or isomorphism class | `if Nonempty (V ≅ W) then 1 else 0` or representation `Equiv` | exact identity convention open |
| normalization | divide by group order or make the raw sum equal group order times delta | cardinal inverse/invertibility APIs | convention and characteristic open |
| plural "relations" | row plus column orthogonality, or a generic family label | no single intake-selected declaration | theorem boundary unresolved |
| `已验证` | untrusted inventory label | no expression or receipt | explicitly rejected as evidence |

## Pinned formal leads

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.RepresentationTheory.Character` contains:

1. `FDRep.char_orthonormal`, for simple bundled finite-dimensional representations of a finite
   group over an algebraically closed field with invertible group cardinal.
2. `Representation.char_orthonormal`, the corresponding unbundled finite-dimensional
   representation result using `IsIrreducible` and `Nat.card`.
3. `FDRep.scalar_product_char_eq_finrank_equivariant`, which identifies the normalized character
   scalar product with the dimension of the equivariant Hom space.
4. `Representation.card_inv_mul_sum_char_mul_char_eq_finrank`, the analogous intertwining-map
   bridge.

The module source itself describes `char_orthonormal` as orthogonality of characters for
irreducible representations of a finite group. The intake probe elaborates these APIs and prints
axiom reports in the pinned environment. This is a bounded, repo-local discovery result. Exact
source identity, normalized declaration types, terminal bodies, transitive provenance, trust
acceptance, and source-to-formal transports remain downstream work.

## Neighbor and non-substitution boundary

`THM-M-0066` owns Schur's lemma and `THM-M-0067` owns Maschke's theorem. Both can occur in a proof
of character orthogonality, but neither shares status or proof credit. Mathlib's finite-abelian
Fourier characters and Dirichlet characters use the word "character" in other exact theorem
families; they cannot replace this group-representation record.

## First source/statement gate

An independent review must preserve a lawful authoritative edition and select an exact proposition
from the row, column, or explicitly packaged character-relation variants. It must map every
domain, representation, irreducibility, normalization, involution, delta, binder, conclusion, and
boundary case. Only then may the statement phase freeze and mutation-test an exact Lean target.
