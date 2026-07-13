# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1478-1483` supplies exactly the title `莫利定理`, Frank Morley,
the year 1899, the gloss `三角形角三等分线交点构成等边三角形`, importance `中`, and status
`已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, theorem
locator, diagram, definitions, binders, hypotheses, intersection convention, proof boundary,
correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:5698-5723` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof path, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

## Inspected proof-source lead

F. Glanville Taylor and W. L. Marr, "The six trisectors of each of the angles of a triangle,"
*Proceedings of the Edinburgh Mathematical Society* 32 (1913), pages 119-131, DOI
`10.1017/S0013091500035100`, was inspected from the Cambridge-hosted PDF observed on 2026-07-13.
Cambridge/Crossref metadata gives publication in February 1913, while the printed scan says that
the paper was received and read on 14 November 1913. That impossible chronology may reflect a
volume-dating or scan/edition peculiarity and must be reconciled at accepted source review.

Section 1 says the result was traced to Professor Morley and distinguishes the internal-trisector
particular case from Morley's broader internal/external construction. Section 2, printed page 119,
states:

> If the angles of any triangle ABC be trisected, the triangle DEF, formed by the meets of pairs
> of trisectors, each pair being adjacent to the same side of ABC, is equilateral.

Sections 2-4 then give two geometric proofs and a trigonometric proof. The observed PDF SHA-256 is
`3d8603772297831131307442eb8400e210b9d07fe82e446573e7e963575bba5d`.

This is a credible, proposition-level, complete proof lead. It is not `H0` evidence: the catalog
does not cite or select this paper; no reviewer has independently checked the scan, diagram-dependent
definitions, proof, publication history, corrections, or errata; the paper's historical account
says Morley's broader result was unpublished; and the exact transport from its construction to a
Lean proposition has not been approved.

## Clause crosswalk

| Catalog component | Taylor-Marr component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `三角形` (triangle) | "any triangle ABC" in ordinary plane geometry | three points in a two-dimensional Euclidean affine space plus noncollinearity and orientation data | exact ambient and nondegeneracy clauses are implicit/open |
| `角三等分线` (angle trisectors) | each vertex angle is trisected; Section 2 chooses pairs adjacent to a side | angle equalities using `EuclideanGeometry.angle` or oriented-angle data, with ray/betweenness predicates | internal ray, supporting-line, ordering, and existence encodings open |
| `交点` (intersections) | `D`, `E`, `F` are meets of the three adjacent pairs | existential points on selected rays/lines, or constructed line intersections | uniqueness, parallel exclusion, and binder order open |
| `构成等边三角形` | Section 2 concludes triangle `DEF` is equilateral | three pairwise distance equalities, two equalities plus nondegeneracy, or three angles equal to `pi / 3` | exact conclusion and checked equivalence open |
| internal/external scope | Section 1 calls the internal case particular; Section 5 develops a larger six-trisector family | separate directed-angle/indexed-line formulation | explicitly excluded from the root unless source selection broadens it |
| Frank Morley / 1899 | catalog attribution; paper traces origin to Prof. Morley but gives a different informal chronology | provenance only | primary discovery record and exact date unresolved |
| `已验证` | untrusted inventory label | accepted source review and kernel receipt would be required | no H0 or M credit |

## Pinned Lean boundary

Pinned mathlib contains `EuclideanGeometry.angle_add_angle_add_angle_eq_pi`, the law of sines,
the isosceles theorem and converse, oriented angle addition, `Collinear`, `Wbtw`, and triangle
congruence. These declarations are relevant substrate for defining trisector rays and recognizing
an equilateral conclusion. They do not select the adjacent ray pairs, construct their intersections,
or state Morley's theorem.

`Affine.Simplex.interior` is a possible internal-ray guard, while `Affine.Simplex.Equilateral` and
`Affine.Triangle.equilateral_iff_dist_01_eq_02_and_dist_01_eq_12` provide candidate conclusion
interfaces. The bundled `Affine.Triangle` already carries affine independence; a bare conjunction
of distance equalities permits three coincident points. A future statement must preserve the
source's phrase "triangle DEF" rather than silently losing conclusion nondegeneracy.

A bounded exact-topic search of repo-local Lean and pinned mathlib found no declaration for Morley,
angle trisection/trisectors, or the full equilateral conclusion. This is intake discovery only, not
the later immutable anchor audit and not a global absence theorem. `THM-M-0656`, Michael Morley's
model-theoretic categoricity theorem, is a distinct target and an especially important name
collision, not a formal anchor for this item.

## Source and statement gates

Before leaving `H1`, accountable reviewers must preserve an approved immutable source edition,
pinpoint and transcribe the exact proposition and incorporated definitions, map every construction,
binder, hypothesis, conclusion, diagram case, and boundary, audit publication history, corrections,
errata, and the historical attribution, and independently approve fidelity to `THM-M-0205`.

The statement phase must then freeze minimal pinned imports and one elaborated Lean expression,
record expression and environment fingerprints, compile any transport between ray/line,
oriented/unoriented, and side/angle equilateral encodings, and mutation-test noncollinearity,
internal adjacency, intersection incidence, binder scope, and degenerate cases. Until then, no
canonical obligation or proof credit exists.
