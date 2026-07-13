# THM-M-0941 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6875-6880` supplies exactly:

| Field | Literal value | Intake meaning |
|---|---|---|
| title | `Freiman定理` | identifies Freiman's theorem family |
| proposer | `Gregory Freiman` | attribution metadata only |
| time | `1964` | unsupported chronology lead |
| statement | `小加倍集的结构` | "structure of sets with small doubling"; not a proposition |
| importance | `高` | scheduling metadata only |
| formalization status | `已验证` | explicitly untrusted; no H/M credit |

All six uncited lines entered in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:25660-25685`
repeats them while explicitly leaving definitions, premises, proof route, dependencies, equivalent
forms, axioms, machine status, and artifacts open.

## Source-discrimination lead

Ben Green and Imre Z. Ruzsa, *Freiman's Theorem in an arbitrary abelian group*, arXiv
`math/0505198v2` (submitted 2005-05-10; version 2 dated 2006-02-07), was inspected on 2026-07-13.
The observed 15-page PDF has SHA-256
`52386eb9e6c3ad51f71f9872365de9ccd361f25532f070e1197112e5c4c815ff`.

- Page 1 defines `A + A` for a finite subset `A` of an abelian group and calls
  `|A + A| = K |A|` doubling `K`.
- Page 1 describes the classical integer theorem: if `A` is a finite subset of the integers and
  `|A + A| <= K |A|`, then `A` lies in a proper multidimensional arithmetic progression of
  dimension `d(K)` and size at most `f(K)|A|`.
- Pages 1-2 explain why this progression-only form fails in arbitrary abelian groups and define
  coset progressions.
- Theorem 1.1 on page 2 gives an arbitrary-abelian-group extension with a coset progression and
  explicit asymptotic bounds involving an absolute constant `C`.
- The final publication is *Journal of the London Mathematical Society* (2) 75(1) (2007),
  163-175, DOI `10.1112/jlms/jdl021`; the inspected artifact was arXiv version 2.
- Reference [6] cites G. Freiman, *Foundations of a structural theory of set addition*, AMS
  Translations of Mathematical Monographs 37 (1973). Crossref records DOI `10.1090/mmono/037` and
  a later online publication date, but this intake did not obtain and review the monograph's exact
  theorem passage or any source establishing the catalog's 1964 date.

This later paper is credible evidence that the catalog names a real theorem family, but it is not
accepted H0 evidence for one exact target. It juxtaposes at least two materially different roots,
does not supply the catalog's 1964 locator, and itself says its proof draws on other sources. A
pinpoint primary statement, incorporated definitions and assumptions, proof boundary, correction
and errata status, lawful durable source, and independent review remain open.

## Clause crosswalk

| Catalog component | Inspected source lead | Prospective Lean surface | Intake result |
|---|---|---|---|
| set | finite `A` | `Finset G` or a finite `Set G` | finiteness/nonempty/domain binders open |
| small doubling | `|A+A| <= K|A|` | cardinal inequality or `Finset.addConst` | `K` type, normalization, and edge cases open |
| structure | proper progression over integers; coset progression in arbitrary groups | new progression/coset-progression data and carrier | target container and properness open |
| bounded complexity | dimension `d(K)`, size `f(K)|A|` | existential functions or explicit bounds | quantifier order and bounds open |
| containment | all of `A` lies in the container | finset/set inclusion | full-set versus large-subset variants open |
| ambient group | integers in the classical statement; arbitrary abelian group in Theorem 1.1 | additive group typeclasses and transports | proposition-changing choice unresolved |
| `已验证` | no corresponding cited artifact | accepted source/kernel receipts required | no credit |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Combinatorics.Additive.DoublingConst` defines `Finset.addConst`, and its imported
Plunnecke-Ruzsa module proves additive growth inequalities. `Mathlib.Combinatorics.Additive.FreimanHom`
defines additive Freiman homomorphisms and isomorphisms. `VerySmallDoubling` proves special
structural results such as `Finset.doubling_lt_three_halves`, `doubling_lt_golden_ratio`, and
`doubling_lt_two`; these strict small-parameter classifications do not state the full catalog
family. The discovery-only probe elaborates these APIs and records selected axiom reports, but none
defines the required generalized progression container or states the unresolved Freiman root. This bounded search is not the later immutable
anchor audit and not a global absence theorem.

## Exit gate

Before statement freeze, independent source and formal reviewers must select and admit a pinpoint
source proposition, reconcile the 1964 attribution, and approve the ambient group, finite/nonempty
set, doubling parameter, progression kind, properness, rank and size bounds, constants, binders, and
boundary cases. The statement phase must then elaborate and mutation-test the exact target. Until
then the root remains `[H1, M4, R4]`.
