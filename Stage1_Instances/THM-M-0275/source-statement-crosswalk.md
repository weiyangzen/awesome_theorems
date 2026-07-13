# Source-statement crosswalk

## Repository records

`Docs/researches/math_theorems.md:1978` through `:1983` and `:2253` through `:2258` contain
identical records: title `一致有界性原理`, attribution Stefan Banach/Hugo Steinhaus, year 1927,
gloss `算子族的一致有界性`, importance high, and status `已验证`. All twelve uncited lines
originate at repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Stage0 deduplicates
those two literal records into `THM-M-0275` while explicitly leaving definitions, assumptions,
proof route, equivalences, axioms, and formal artifacts open.

The source corpus separately records `THM-M-0312`, `共鸣定理`, with the gloss "pointwise bounded
operators are uniformly bounded", attribution Stefan Banach, and year 1929. That is likely the same
mathematical theorem family under another name, but it remains an independent manifest target.
No statement, lifecycle, obligation, proof-body, evidence, or receipt state crosses the ID boundary;
the integration lane must eventually decide the duplicate/relationship policy.

The `已验证` labels are inventory metadata only. They do not identify a truth-valued proposition,
primary proof, Lean expression, or accepted receipt.

## Inspected primary source

Stefan Banach and Hugo Steinhaus, *Sur le principe de la condensation de singularites*,
*Fundamenta Mathematicae* 9 (1927), 50-61, DOI `10.4064/fm-9-1-50-61`, was inspected from the
publisher-provided scan. The PDF has SHA-256
`1ae76c338ac45f26c4da9093435fde2b1db942cc65332569f216139a114e0548`, 567964 bytes, and six
two-page image sheets. The publisher page identifies the authors, volume, year, pages, DOI, and a
CC-BY download. These observed bytes are not vendored and are not release evidence.

Journal pages 51-52 define the source setting: a complete metric real vector space `D`, a normed
vector codomain `C`, a continuous additive functional `u(x)`, and its least norm bound. Section 2,
Lemma 3 and its proof on page 53 say, in translation:

> If `(u_n(x))` is a sequence of linear functionals and `limsup_n norm (u_n(x))` is finite on a
> set of second category, then `limsup_n norm (u_n)` is finite.

Its proof invokes Lemma 2 to obtain uniform boundedness on a ball, moves that bound to the unit ball
by linearity, and concludes one operator-norm bound. Lemmas 1-2 supply the closed-set decomposition
and Baire-category ball step. Completeness of the domain is used through the second-category
property. The article's Theorems I and II on pages 54-55 concern condensation for double sequences.

This is a primary theorem passage and proof lead, hence `H1`, but not `H0`: an independent source
review, correction/errata audit, exact convention translation, and arbitrary-family mapping are
not accepted. In particular, the printed result is sequence-indexed while the catalog says a
family. Passing between them is not silently treated as source identity.

## Source-to-candidate crosswalk

| Catalog/source element | Mathematical component | Pinned Lean candidate | Intake result |
|---|---|---|---|
| operator/functionals | continuous additive maps from complete `D` to normed `C` in the 1927 conventions | continuous semilinear maps `E ->SL[sigma12] F` | exact linear/scalar transport open |
| complete metric domain | Baire-category premise used in Section 2 | `[CompleteSpace E]` plus normed topology | strong match; exact structures open |
| pointwise bounded | source Lemma 3 uses finite pointwise limsup; conventional root uses a bound for every index at each `x` | `forall x, exists C, forall i, norm (g i x) <= C` | sequence/family and encoding transport open |
| uniformly bounded | one operator-norm bound | `exists C', forall i, norm (g i) <= C'` | candidate interface elaborates |
| arbitrary operator family | present only in the catalog gloss/conventional formulation | arbitrary `iota : Type*` | not literal in inspected Lemma 3 |
| real-linear 1927 conventions | real scalar multiplication in `D`; normed vector codomain | two fields and `RingHomIsometric sigma12` | mathlib generalization, not frozen root |
| verified | untrusted catalog label | accepted kernel/source receipts | no credit |

## Pinned formal leads

At pinned mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- `Mathlib.Analysis.Normed.Operator.BanachSteinhaus`, lines 31-40, contains
  `banach_steinhaus` with the arbitrary-family pointwise-bound implication above.
- The same file, lines 44-50, contains `banach_steinhaus_iSup_nnnorm`.
- `Mathlib.Analysis.LocallyConvex.Barrelled`, lines 159-178, contains the more general
  `WithSeminorms.banach_steinhaus` equicontinuity theorem.
- `Mathlib.Analysis.Normed.Operator.NormedSpace`, lines 286-323, relates uniform
  equicontinuity, pointwise norm estimates, common operator-norm bounds, and the `ENNReal` supremum.

`IntakeProbe.lean` checks these declarations under the pinned toolchain. This authenticates public
interfaces only. Exact root selection, normalized-expression comparison, checked transports,
terminal declaration and body provenance, transitive dependency and axiom closure, placeholders,
and receipt eligibility belong to downstream statement and anchor-audit phases.

## First downstream gate

The statement phase must admit and independently review an immutable source proposition; settle
the sequential historical result versus conventional arbitrary-family root; fix common-field
linear versus maximal semilinear scope; map every structure, binder, premise, conclusion, and
boundary case; audit corrections or errata; and then elaborate a minimal exact Lean expression with
checked alternate encodings and all four required mutation classes.

Until then, `H1` records the matching inspected primary passage with incomplete exact mapping,
`M3` records direct pinned interfaces without a frozen canonical target or proof credit, and `R4`
records the absence of an accepted source-faithful reconstruction.
