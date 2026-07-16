# Source-statement crosswalk

| Claim component | Human source anchor | Lean target | Intake assessment |
|---|---|---|---|
| Classical multiplicity conjecture | D. Kazhdan and G. Lusztig, *Representations of Coxeter groups and Hecke algebras*, Inventiones Mathematicae 53 (1979), 165-184, Conjecture 1.5 | Not yet assigned | This is the intended root family. A scanned/publisher edition, exact page text, notation table, and errata check must be pinned before the formula is transcribed: `H2` |
| Kazhdan-Lusztig polynomials and indexing | Same paper, preceding definitions and conventions | Future Coxeter/Hecke definitions | Essential premises; evaluation at `1` is meaningless without normalization and index orientation |
| Verma/simple multiplicity side | Conjecture 1.5 and its representation-theoretic setup | Future category `O` and finite-length multiplicity definitions | Exact field, Lie-algebra, integrality, regularity, and Bruhat-order assumptions remain to be transcribed |
| Historical proof route | A. Beilinson and J. Bernstein, *Localisation de g-modules*, C. R. Acad. Sci. Paris 292 (1981), 15-18; J.-L. Brylinski and M. Kashiwara, *Kazhdan-Lusztig conjecture and holonomic systems*, Inventiones Mathematicae 64 (1981), 387-410 | No candidate audited | Proof-source candidates only; editions, theorem numbers, assumptions, corrections, and node crosswalks remain open |
| Repository wording | `Docs/researches/math_theorems.md`: "Kazhdan-Lusztig polynomials in representation theory" | None | Metadata establishes neither a unique proposition nor a Lean encoding; it cannot receive source or machine credit |

## Ambiguity boundary

"Kazhdan-Lusztig conjecture" is used for conventionally equivalent character and multiplicity
formulas and is sometimes loosely applied to positivity or geometric statements. Index reversal by
the longest Weyl-group element also depends on parametrization. This dossier selects the original
1979 Conjecture 1.5 family, but deliberately does not print an unchecked symbolic equation.

The statement phase must pin a primary-source artifact, record its digest and exact pages, transcribe
all hypotheses and conventions, and either produce an exact Lean expression plus checked transports
to any alternate character formula or report a blocker. No `H0` or machine-checked claim is made.

## Statement-phase result

The required primary-source bytes or an independently accepted exact transcription are still not
present in this clone. Consequently the source-native index and normalization choices remain open,
and `Statement.lean` is only a pinned substrate probe. The legacy candidate
`AwesomeTheorems.Stage1.S1_M_055.StatementShape` is not selected: it quantifies over freely supplied
abstract data and therefore does not encode the concrete regular-integral category-O setting or the
source conventions. No candidate equation in this crosswalk is a canonical Lean target or a checked
transport. The exact statement, its premise and boundary mapping, and all source-fidelity debt remain
visible and unresolved.

Discovery links (not immutable receipts):

- Original paper DOI: <https://doi.org/10.1007/BF01390031>
- Brylinski-Kashiwara DOI: <https://doi.org/10.1007/BF01393997>
