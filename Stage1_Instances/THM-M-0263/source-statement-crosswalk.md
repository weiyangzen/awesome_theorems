# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1894-1899` records exactly the Chinese title
`实数完备性定理`, attribution `Richard Dedekind/Karl Weierstrass`, year `1872`, gloss
`实数集的完备性`, importance `高`, and status `已验证`. All six uncited fields originate at repository
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:7279-7304` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, equivalent forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`. These records establish
catalog identity, not an exact proposition or proof.

## Inspected human-source lead

Richard Dedekind, *Essays on the Theory of Numbers*, authorized translation by Wooster Woodruff
Beman, Open Court, 1901, contains *Continuity and Irrational Numbers*. Section V, "Continuity of
the Domain of Real Numbers," theorem IV on book pages 19-20 states that if all real numbers are
separated into two classes and every member of the first is less than every member of the second,
then exactly one real produces that separation; the following paragraph gives a proof using the
corresponding rational cut and rational density.

The Project Gutenberg 21016 TeX transcription inspected on 2026-07-13 had SHA-256
`f837b8376cbbfca11690cea3bc0fac14fffecb88ae669e4f15158f096c915f44`. It is an accessible
authorized translation of a Dedekind source, not a catalog-cited immutable dependency or an
independently accepted source packet. The repository's joint Weierstrass attribution is still
unmapped, translation and correction status have not been independently reviewed, and no checked
bridge identifies Dedekind's cut theorem with a modern least-upper-bound or Cauchy proposition.
Consequently this is `E4`-class source discovery supporting provisional `H1`, not accepted `H0`.

## Clause crosswalk

| Repository/source phrase | Required mathematical component | Pinned Lean lead | Intake status |
|---|---|---|---|
| "real-number set" | the ordered field `Real`, not `Rat`, extended reals, or an arbitrary complete order | `Real` | domain family identified; construction/encoding policy open |
| "completeness" | least-upper-bound, cut, Cauchy, or another explicitly selected property | `Real.exists_isLUB`; `Real.instCompleteSpace` | catalog does not select between direct candidates |
| Dedekind / 1872 | cut construction and continuity of the real domain | `IsLUB` family is a prospective modern order encoding | inspected translation is a source lead; exact transport open |
| Weierstrass | sequence/limit or another source-specific account | `CompleteSpace Real`; `cauchySeq_tendsto_of_complete` | no work or passage supplied or admitted |
| `已验证` | independently accepted source or exact kernel evidence | no expression or receipt | explicitly rejected as credit |

## Pinned formal candidates

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

1. `Mathlib/Data/Real/Archimedean.lean` proves
   `Real.exists_isLUB (hne : s.Nonempty) (hbdd : BddAbove s) : exists x, IsLUB s x`, proves the
   lower-bound dual, constructs `sSup`, and installs `Real.instConditionallyCompleteLinearOrder`.
2. `Mathlib/Topology/UniformSpace/Real.lean` installs `Real.instCompleteSpace : CompleteSpace Real`;
   the generic theorem `cauchySeq_tendsto_of_complete` then yields convergence of a Cauchy sequence.
3. `Mathlib/Order/ConditionallyCompleteLattice/Basic.lean` supplies the generic `isLUB_csSup`,
   `le_csSup`, and `csSup_le` interfaces once a conditionally complete order is available.

`IntakeProbe.lean` checks these declarations and instances and records representative axiom reports.
This bounded probe does not select a canonical statement, normalize candidate types, audit terminal
bodies or transitive trust closure, or confer proof credit. Those are statement and anchor-audit
obligations.

## First failed gate

The catalog does not identify whether the root is Dedekind/cut or least-upper-bound completeness,
metric/Cauchy completeness, or another equivalent form. Before statement elaboration, accountable
reviewers must select and admit one exact source proposition, map every definition, assumption,
conclusion, proof boundary, correction, and attribution, and approve any required equivalence to the
chosen Lean encoding. Until then the canonical mathematical and Lean targets remain null.
