# Scope map

## Preserved theorem family

The received scope is the classical Kurosh subgroup theorem family. Kurosch's printed-page-651
headline says: if `G` is the free product of component subgroups `H_alpha`, every subgroup `F` of
`G` can itself be decomposed as a free product `F = * F_beta`, where every factor is either an
infinite cyclic group or conjugate to a subgroup of one component `H_alpha`. Footnote 5 says that
the product may consist of only one factor.

This source headline is existential. It does not prescribe the modern double-coset indexing,
package all infinite cyclic factors into one named free group, or assert uniqueness. Those useful
modern refinements remain candidate alternate formulations only and cannot silently enter the
root. The exact Lean proposition remains unfrozen pending definition-chain and translation review.

## Decisions required at statement freeze

1. Select and independently review an exact source theorem and its incorporated definitions,
   rather than treating the catalog gloss or a modern summary as a quotation.
2. Fix the index type, universes, group family, and ambient free-product encoding, including the
   canonical factor embeddings and any transport from another free-product construction.
3. Fix the subgroup binder and whether the theorem is unrestricted or assumes nontrivial,
   finitely generated, finite-index, normal, or other special subgroups.
4. Encode the source's factor predicate exactly: each displayed factor is either infinite cyclic
   or conjugate in the ambient group to a subgroup of one component. Fix subgroup coercions,
   isomorphism versus equality, and left-versus-right conjugation conventions.
5. Choose an existential index and factor family without strengthening the source to a canonical
   double-coset representative set. Any modern indexed refinement needs a separate checked bridge.
6. Encode "can be decomposed" as an exact isomorphism or universal-property statement showing that
   the free product of the factor family is the whole subgroup, not merely a generating map.
7. Keep existence as the source root. A packaged free group, uniqueness, rank, canonicality,
   functoriality, double-coset indexing, or normal form belongs only to sourced alternate encodings.
8. Freeze all ordered binders, hypotheses, conclusions, foundation and TCB profiles, alternate
   encodings, and checked transports before proof evidence is inspected.

## Boundary cases

Source review must address an empty index family; a singleton family; trivial factors; an empty or
infinite family of nontrivial factors; the bottom and top subgroups; a trivial ambient free product;
trivial factor intersections; repeated double-coset representatives; a trivial free factor; and
finite versus infinite generation. No case is excluded at intake.

In particular, the top subgroup should recover the original free product under the selected
conventions, while the bottom subgroup should not force a spurious nontrivial factor. These are
scope tests for a later exact statement, not proofs recorded by this dossier.

## Excluded substitutions

- Nielsen-Schreier, which says subgroups of free groups are free, is a related specialization or
  consequence route but not the general subgroup decomposition.
- The fact that a free product of free groups is free does not decompose an arbitrary subgroup of
  a free product.
- The reduced-word normal form and the universal property of `Monoid.CoprodI` define the ambient
  object but do not identify a subgroup's free-product factors.
- A theorem that the factor embeddings are injective is necessary infrastructure only.
- Binary-only, finite-family-only, finite-index-only, normal-subgroup-only, or finitely generated
  variants cannot replace an unrestricted source theorem without a checked equivalence.
- Grushko decomposition, Bass-Serre normal forms, amalgamated-product theorems, Schreier rank
  formulas, and subgroup generation statements are distinct claims unless an exact bridge is
  separately represented.
- A structure or hypothesis storing the desired decomposition supplies no existence proof.
- The theorem name, the catalog's `verified` label, the 1000-theorems title entry, and a successful
  API probe supply no human-source or machine-proof closure.

## Neighbor boundaries

`THM-M-0079` owns the Nielsen-Schreier theorem. It may eventually supply a consequence or free
factor lemma, but its proof status cannot transfer to this root. `THM-M-0078` owns the Zassenhaus
theorem family and is unrelated despite catalog proximity. Any future dependency must be frozen
under a stable obligation ID.

## Pinned formal boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Monoid.CoprodI` is the
indexed free product of groups, with canonical embeddings, a universal property, reduced words,
and injectivity of each factor embedding. The same module constructs a basis for a free product of
free groups. General subgroup, conjugation, intersection, and free-group interfaces also exist.

No declaration found in the bounded repository and pinned-mathlib search states the Kurosh
subgroup decomposition. `docs/1000.yaml` lists the title without a `decl` or URL. The available
interfaces justify `M3` infrastructure status only; they do not select or close the root. This
bounded intake inspection is not the later immutable anchor audit.
