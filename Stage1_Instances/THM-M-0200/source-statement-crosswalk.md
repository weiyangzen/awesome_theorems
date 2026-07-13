# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1443-1448` supplies exactly the title `塞瓦定理`, attribution to
Giovanni Ceva, year 1678, gloss `共点线的比例关系`, importance medium, and formalization status
`已验证`. All six uncited lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:5563-5588` repeats the gloss while explicitly leaving the target system,
foundation, precise definitions and premises, proof route, dependencies, equivalent forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as untrusted
metadata and resets the item to `L0 / rework_required`. Neither repository record contains a
bibliography, edition, theorem/page, formula, logical direction, definition chain, proof boundary,
translation, correction history, reviewer, or formal artifact. The attribution and date are leads
only.

## Inspected source lead

Thomas Prince, "The Birational Geometry of Ceva's Theorem," arXiv `2406.08378v1`, submitted
2024-06-12, was inspected in its immutable version-1 PDF on 2026-07-13. Theorem 1 on PDF page 1
fixes a triangle `ABC` and points `D`, `E`, and `F` on `BC`, `AC`, and `AB`. It states that the
segments `AD`, `BE`, and `CF` meet at one point if and only if

`AE / EC * CD / DB * BF / FA = 1`.

It further says that the result holds for points on produced side lines when signed length is used.
Section 2, PDF pages 2-3, proves the equivalence by homogeneous coordinates and a determinant. The
PDF SHA-256 is `e4448220b1b79f8b9f52bdd3384d5a1bb19603d1b84896d8fe8642deb06f8fae`.

This source is a precise modern theorem-and-proof discovery lead, not accepted `H0` evidence. The
catalog does not cite it; no independent reviewer has mapped it to the catalog; and its reference
edition, signed-length convention, correction/errata state, long-term lawful preservation, and
relationship to Ceva's 1678 source remain unaccepted. The historical attribution has no inspected
primary 1678 passage, edition, translation, or correction history here.

## Clause crosswalk

| Catalog element | Prince, Theorem 1 | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `共点线` | `AD`, `BE`, `CF` coincide at one point | `p' : P` with `p'` on each line through `t.points i` and `p i` | common-point witness is plausible; existence predicate and projective infinity open |
| `比例关系` | cyclic product of three side ratios equals one | product of distances, or affine weights `r i / (1 - r i)` | ratio orientation, sign, and transport open |
| triangle | noncollinear coordinate transformation is used in the proof | `t : Affine.Triangle k P` bundles affine independence | ambient field, metric, plane dimension, and source identity open |
| side points | `D`, `E`, `F` on one side each; produced lines use signed length | membership in full `line[k, ...]` | segment versus full line and external-point sign open |
| direction | necessary and sufficient condition | `Iff` or two implications | pinned declarations supply only concurrency to product |
| denominator exclusions | ratios require relevant endpoints to differ | quotient candidate assumes `p i != t.points (i + 2)` | all zero cases and reciprocal orientation open |
| Giovanni Ceva / 1678 | mentioned as theorem history, not a primary edition | provenance only | no source-fidelity credit |
| `已验证` | no corresponding claim | no expression or accepted receipt | no H or M credit |

Prince's displayed cyclic product is the reciprocal/relabeling of some other conventional displays;
the equality to one is invariant under taking the reciprocal, but the exact ordered ratio transport
must still be explicit and checked.

## Pinned formal leads

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.Normed.Affine.Ceva` contains distance forms
`Affine.Triangle.prod_dist_eq_prod_dist_of_mem_line_of_mem_line` and
`Affine.Triangle.prod_dist_div_dist_eq_one_of_mem_line_of_mem_line`. The latter assumes side-line
membership, one finite common point, and a nonzero denominator endpoint, then derives a product of
three unsigned distance ratios equal to one.

Its imported module `Mathlib.LinearAlgebra.AffineSpace.Ceva` contains the algebraic weight forms
`Affine.Triangle.prod_eq_prod_one_sub_of_mem_line_point_lineMap` and
`Affine.Triangle.prod_div_one_sub_eq_one_of_mem_line_point_lineMap`, plus generalized
affine-combination results. The Ceva modules entered mathlib at commit
`7303ce67d95f49d7fa68145c228cd915e3cc0435` on 2026-01-14. Pinned mathlib's `docs/100.yaml`
and `docs/1000.yaml` map the distance quotient declaration to Ceva's theorem.

The intake probe elaborates all six declarations. Four representative bodies report exactly
`propext`, `Classical.choice`, and `Quot.sound`. This authenticates direct pinned interfaces and
their observed foundation boundary only. All four triangle-product declarations prove only the
forward concurrency-to-product direction; the two generalized declarations are forward
affine-weight proportionality leads. None proves the converse or an iff, and no canonical wrapper,
statement fingerprint, terminal provenance audit, dependency closure, or trust acceptance is
credited at intake.

## First source/statement gate

An independent reviewer must approve an immutable exact source proposition and map every
definition, ordered binder, assumption, direction, ratio/sign convention, conclusion, proof
boundary, translation, correction, and erratum. The statement phase must then fix the Euclidean or
affine domain, dimensionality, nondegeneracy, side-line/segment convention, endpoint cases,
concurrency encoding, and direction before elaborating and mutation-testing one exact Lean target.
