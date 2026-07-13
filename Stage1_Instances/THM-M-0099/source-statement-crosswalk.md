# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:726-731` supplies exactly the title `吴宝珠定理`, the author
Ngô Bảo Châu, the year 2008, the gloss `基本引理的证明` ("proof of the Fundamental Lemma"),
importance "high," and the status `已验证`. Git history attributes all six uncited catalog lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, theorem locator,
formula, definitions, ordered binders, hypotheses, proof boundary, correction history, reviewer,
or formal artifact.

`Docs/Stage0_Blueprint.md:2821-2846` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and assumptions, proof route, alternate forms, axioms, machine
status, and artifact links open. The rev-5.6 manifest retains the verified label only as untrusted
metadata and resets this target to `L0 / rework_required`.

The repository contains a second catalog entry at `Docs/researches/math_theorems.md:3173-3178`,
mapped to `THM-M-0434`, with the same author, year, gloss, importance, and status. Only the Chinese
title differs by explicitly saying "Ngo Bao Chau Fundamental Lemma." No repository record explains
whether these are intentional variants or a duplicate.

## Inspected primary source lead

Ngo Bao Chau, *Le lemme fondamental pour les algebres de Lie*, arXiv `0801.0446v3` (2 May 2008),
was inspected from the versioned arXiv PDF. Its SHA-256 is
`4d48819f7ecf7e4e1d0fd036df2a62fa5b49f171f6fda56449b3dfbc0d43fb51`. The introduction's
Theorem 1 appears on PDF pages 1-2; the detailed local form is Theorem 1.11.1 on PDF pages 23-24;
the source's final proof is in section 8.6. The versioned TeX source archive is a further candidate
for verbatim review, but no independent reviewer or accepted repository preservation receipt is
recorded here.

The journal record is *Publications Mathematiques de l'IHES* 111 (2010), 1-169, DOI
`10.1007/s10240-010-0026-7`; it records receipt on 2 May 2008 and publication on 7 June 2010. This
reconciles the catalog year with a manuscript date, but not the duplicate target ownership.

The inspected source supports provisional `H1`, not `H0`: exact incorporated definitions,
assumptions, normalization equivalence, unequal-characteristic source boundary, errata or
correction review, edition-to-edition comparison, lawful preservation, and independent approval
remain open.

## Clause crosswalk

| Catalog/source component | Source lead | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Ngo Bao Chau / 2008 | arXiv v3 author and date | source metadata only | strong identity lead; duplicate-ID ownership open |
| "proof of the Fundamental Lemma" | introductory Theorem 1 and local Theorem 1.11.1 | one exact source-transcribed proposition | recognizable family, but root formulation and definition chain not accepted |
| local arithmetic domain | complete DVR `O`, finite residue field `k` with `q` elements, fraction field `F` | local-field, valuation-ring, residue-field structures | exact type and characteristic binders open |
| group/endoscopic domain | reductive `G/O`, Weyl-order restriction, pointed endoscopic datum and `H` | group schemes, root data, endoscopy | no faithful pinned Lean object model located |
| matching locus | corresponding stable regular semisimple classes in `g(F)` and `h(F)` | Lie algebras, regular-semisimple and stable-conjugacy predicates | no target declaration located |
| test functions and measures | characteristic functions of `g(O)` and `h(O)` with transported Haar data | locally constant compactly supported functions and Haar/quotient measures | only adjacent Haar infrastructure located |
| conclusion | discriminant-normalized kappa orbital integral equals stable endoscopic orbital integral; detailed form uses `q^r` | equality of defined normalized integrals | canonical normalization and transport open |
| characteristic scope | article proves equal characteristic; cites Waldspurger for unequal characteristic | separate branch and checked transport | must not be collapsed into a single unsupported source claim |
| `verified` | untrusted inventory label | source review and kernel receipt would be required | no H0 or M credit |

## Pinned Lean boundary

Pinned mathlib contains `IsNonarchimedeanLocalField`, `AlgebraicGeometry.Scheme`, and
`MeasureTheory.Measure.IsHaarMeasure`. These authenticate adjacent foundations only. The bounded
search found no exact endoscopic Fundamental Lemma declaration or the required endoscopy,
transfer-factor, stable-orbital-integral, or matching-class object model.

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_083.lean` belongs to legacy target
`THM-M-0434`. It explicitly describes itself as a statement-shape boundary and encodes key notions
with abstract predicates and arbitrary functions. Its implication wrapper assumes comparison data
rather than proving Ngo's theorem. It is not imported or credited here.

## Source gate

Before leaving `H1`, accountable reviewers must resolve the duplicate target ownership, preserve
and hash an approved edition, select one pinpoint source proposition, transcribe and map every
incorporated definition, ordered binder, hypothesis, normalization, conclusion, characteristic
branch, and boundary case, audit errata and edition differences, and independently approve fidelity
to `THM-M-0099`. Only then may the statement phase freeze minimal imports, an elaborated expression
and environment fingerprint, checked alternate encodings, and the required statement mutations.
