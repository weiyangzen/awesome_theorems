# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names Jerzy Los, gives 1955, and summarizes the result only as
"elementary equivalence of ultraproducts". Stage0 repeats that metadata. Neither record gives formal
definitions, assumptions, a proof, a theorem/page anchor, or an errata audit; the manifest therefore
correctly treats `已验证` as untrusted source metadata.

## Candidate human sources

- Jerzy Los, "Quelques remarques, theoremes et problemes sur les classes definissables
  d'algebres", in *Mathematical Interpretation of Formal Systems* (1955), is the historical primary
  publication candidate. Its exact edition, page, original formulation, hypotheses, and corrections
  have not yet been inspected in this repository.
- C. C. Chang and H. J. Keisler, *Model Theory*, third edition, North-Holland (1990), is a standard
  modern reference candidate for the ultraproduct theorem. The exact theorem/page and its
  conventions remain to be pinned and inspected.

These are discovery anchors only. They support `H1`, not `H0`.

## Claim crosswalk

| Repository phrase | Frozen mathematical component | Candidate Lean component | Intake status |
|---|---|---|---|
| "ultraproduct" | quotient of the product modulo equality on a `U`-large set | `(U : Filter I).Product M` with `Ultraproduct.structure` | located; exact expression open |
| "elementary equivalence" | equality of sentence truth with `U`-almost-everywhere factor truth | satisfaction biconditional | clarified, source approval open |
| family of structures | one `L`-structure on each nonempty `M i` | `[forall i, L.Structure (M i)]`, `[forall i, Nonempty (M i)]` | located |
| ultrafilter | proper maximal filter selecting large index sets | `U : Ultrafilter I` | located |
| arbitrary sentence | all first-order connectives and quantifiers | `phi : L.Sentence` | located |
| fundamental theorem | iff, not merely common-theory preservation | `Ultraproduct.sentence_realize` | candidate declaration checks locally |

## Formal-source boundary

Pinned mathlib's `Mathlib.ModelTheory.Ultraproducts` documents and implements the candidate theorem
`FirstOrder.Language.Ultraproduct.sentence_realize`. Its proof is downstream of
`realize_formula_cast` and `boundedFormula_realize_cast`; the quantifier case visibly chooses
witnesses using `Classical.epsilon`. This is useful anchor evidence, but the intake probe neither
freezes the normalized type nor audits imports, axioms, terminal-body provenance, placeholders,
licenses, or checked equivalence to the reviewed human source.

Before `H0`, an independent source reviewer must verify a stable source edition and pinpoint, map
every assumption and boundary case, inspect errata, and approve the source-to-canonical-statement
rows. Before any machine closure, later phases must complete exact statement and provenance gates.
