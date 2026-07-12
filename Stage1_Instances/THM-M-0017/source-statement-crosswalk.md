# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:142-147` supplies the Chinese title `施泰尼茨定理`, author Ernst
Steinitz, year 1910, and the complete statement gloss `代数闭域的特征刻画`
(`characterization of algebraically closed fields`). It supplies no citation, definitions,
quantifiers, assumptions, conclusion, equivalence direction, proof, or formal artifact. All six
lines originate in repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; that records
repository provenance, not mathematical review.

`Docs/Stage0_Blueprint.md:582-602` repeats the gloss and expressly leaves exact definitions and
premises, proof route, dependency graph, equivalent forms, axioms, machine status, and artifact
links open. The rev-5.6 target manifest preserves `已验证` only as
`source_status_untrusted` and requires uniform `L0 / rework_required` re-intake.

## Source leads and ambiguity

Crossref metadata identifies the matching primary publication: Ernst Steinitz, *Algebraische
Theorie der Korper*, Journal fur die reine und angewandte Mathematik, issue 137 (1910), pages
167-309, DOI `10.1515/crll.1910.137.167`. A direct inspection through the versioned GDZ IIIF
manifest locates these proposition-changing candidates:

- Section 17, Satz 2, page 261: an algebraically closed extension of a field contains a smallest
  algebraically closed extension, distinguished by algebraicity over the base;
- Section 21, Satz 8, page 286: for a field and a polynomial family there is, essentially uniquely,
  an extension just sufficient to split that family; and
- Section 21, Satz 9, page 287: `Jeder Korper lasst sich, und zwar im wesentlichen nur auf eine Art,
  algebraisch zu einem algebraisch abgeschlossenen Korper erweitern.` In translation: every field
  admits an algebraic extension to an algebraically closed field, essentially in only one way.

The page-287 OCR and scan mapping were inspected, but the catalog-to-`Satz` selection, exact
transcription against the scan, incorporated definitions, proof-boundary mapping, correction and
errata audit, and independent review remain open. The primary passages therefore support `H1`, not
`H0`, and do not by themselves select the canonical root.

nLab's immutable revision 31 of `algebraically closed field` gives another precise modern candidate:
two algebraically closed fields are isomorphic iff they have the same characteristic and the same
transcendence degree, and sketches the transcendence-basis/algebraic-closure construction. It is a
secondary disambiguation source, not a reviewed primary proof packet. PlanetMath's entry titled
`Steinitz theorem` instead attributes existence of algebraic closures to the same 1910 paper. This
conflict shows why the title, year, and broad catalog gloss do not determine a proposition.

## Component crosswalk

| Catalog/source component | Candidate mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| "algebraically closed fields" | two fields `K`, `L` satisfying algebraic closedness | `[Field K] [Field L] [IsAlgClosed K] [IsAlgClosed L]` | likely domain; exact source binders unreviewed |
| "characterization" | existence and essential uniqueness of algebraic closures (primary Satz 9) | `AlgebraicClosure K`, `IsAlgClosure`, and `IsAlgClosure.equiv` | strongest directly inspected historical candidate; catalog selection absent |
| "characterization" | field isomorphism iff equality of complete invariants (modern reading) | `Nonempty (K ≃+* L) ↔ ...` or a chosen `K ≃+* L` | direction and output strength absent |
| characteristic | equality of prime characteristics, including characteristic zero | shared `p` with `[CharP K p] [CharP L p]`, or an equality of `ringChar` | encoding not selected |
| transcendence degree | cardinality of a transcendence basis over the prime field | `Algebra.trdeg R K`, `Algebra.trdeg R L`, or explicit `IsTranscendenceBasis` data | base ring, lifts, and equality form open |
| same transcendence basis cardinal | an equivalence between basis index types | `e : iota ≃ kappa` passed to `IsAlgClosed.equivOfTranscendenceBasis` | sufficient-direction candidate only |
| uncountable specialization | same characteristic and same underlying cardinality imply isomorphism | `IsAlgClosed.ringEquiv_of_equiv_of_char_eq` | materially restricted alternate, not root by default |
| 1910 Steinitz attribution | directly inspected Satz 2, Satz 8, Satz 9, or the modern classification reading | no name-based Lean identity is valid | candidate passages known; catalog-to-`Satz` selection unresolved |
| `已验证` | untrusted catalog label | no proposition, declaration, or proof body | explicitly rejected as evidence |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.FieldTheory.IsAlgClosed.AlgebraicClosure` constructs `AlgebraicClosure K` and supplies
field, algebraicity, algebraic-closure, and algebraically-closed instances.
`Mathlib.FieldTheory.IsAlgClosed.Basic` supplies `IsAlgClosure.equiv`, a base-algebra equivalence
between two algebraic closures. These are strong adjacent components for Satz 9, not an accepted
exact target before the catalog's root and formulation are selected.

`Mathlib.FieldTheory.IsAlgClosed.Classification` provides adjacent classification machinery:

- `IsAlgClosed.isAlgClosure_of_transcendence_basis`;
- `IsAlgClosed.equivOfTranscendenceBasis`;
- cardinality/transcendence-basis comparisons for uncountable fields;
- `IsAlgClosed.ringEquiv_of_equiv_of_charZero`; and
- `IsAlgClosed.ringEquiv_of_equiv_of_char_eq`.

The module documentation describes the first construction as an isomorphism from equal
characteristic and equipotent transcendence bases, and the last theorem as the uncountable
same-cardinality specialization. Neither is credited as an exact catalog match before source and
statement selection. The same pinned tree labels
`Field.exists_primitive_element_iff_finite_intermediateField` as **Steinitz theorem** in
`Mathlib.FieldTheory.PrimitiveElement`; its algebraic-extension statement is a confirmed namesake,
not this target.

`IntakeProbe.lean` elaborates these names and types only. The bounded repository/mathlib search is
an intake discovery snapshot, not an exhaustive immutable anchor audit or an absence claim about
external projects.

## Required next crosswalk

The statement phase must preserve the inspected primary snapshot, obtain an accountable selection
of the precise `Satz` and claim boundary, verify its transcription against the scans with all
incorporated definitions and assumptions, review corrections and errata, and obtain independent
approval. It must then map each ordered binder and conclusion component to one exact Lean
expression. For Satz 9 this includes the base field, extension/algebra, algebraicity, algebraic
closedness, and exact uniqueness/equivalence strength. For classification it includes
characteristic, transcendence invariant, cardinal lifts, and both directions. Only checked
transports may relate alternate forms.

Until that work is complete, the source status is `H1`, the formal status is `M4`, and no readable
root proof is claimed (`R4`).
