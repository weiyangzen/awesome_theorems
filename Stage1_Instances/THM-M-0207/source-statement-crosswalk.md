# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1492-1497` supplies exactly the title `拿破仑定理`, attribution to
Napoleon Bonaparte, the year 1825, the gloss `三角形外正三角形中心构成正三角形` ("the centers of
equilateral triangles constructed externally on a triangle form an equilateral triangle"), medium
importance, and status `已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:5752-5777` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate formulations,
axioms, machine status, and artifact links open. The rev-5.6 target manifest retains `已验证` only
as `source_status_untrusted` and resets the target to `L0 / rework_required`.

No primary mathematical source was admitted during intake. The catalog contains no bibliography,
edition, theorem/page, quotation, formula, definition chain, proof boundary, correction history,
reviewer, or formal declaration. Its attribution and date are historical leads only. This supports
`H1`, not H0.

## Clause crosswalk

| Catalog clause | Candidate mathematical reading | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "triangle" | an ordered nondegenerate Euclidean triangle | `Affine.Triangle Real P` or three points with explicit hypotheses | domain, order, and degeneracy policy open |
| "on each side" (implicit) | one new equilateral triangle sharing each original side | three constructions indexed by the sides | correspondence and endpoint order absent from the source |
| "external" | choose the third vertex in the half-plane opposite the remaining original vertex | orientation or signed-side predicate | no orientation or half-plane convention supplied |
| "equilateral triangles" | all three side lengths of each constructed triangle agree | `Affine.Simplex.Equilateral` or distance equalities | adjacent predicate exists; construction and source transport do not |
| "centers" | usually the centroids of the three attached equilateral triangles | `Affine.Simplex.centroid` | center kind is not named; equivalence of classical centers would need proof |
| "form an equilateral triangle" | the three centers are noncollinear and pairwise equidistant | output `Affine.Triangle` plus `Equilateral`, or raw distance equalities | nondegeneracy and conclusion encoding open |
| external Napoleon variant | outward construction | source-selected external proposition | internal and mixed variants are not discussed |
| `已验证` | untrusted inventory label | no expression, build, or receipt | no H or M credit |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Geometry.Euclidean.Simplex` exposes an equilateral predicate and distance/angle lemmas;
the imported affine-simplex centroid module exposes the centroid construction. The intake probe
elaborates these interfaces and prints axioms for three adjacent support lemmas. It declares no
Napoleon target and locates no terminal proof body for one.

The formal surfaces also expose an important modeling choice: `Affine.Triangle` contains affine
independence, while a raw triple can represent degenerate inputs. Selecting the convenient bundled
type would silently add nondegeneracy unless an accepted source crosswalk justifies it.

## First source/statement gate

Accountable reviewers must preserve and approve an immutable exact source proposition, map every
definition, domain, binder, construction, orientation condition, center choice, hypothesis,
conclusion, proof boundary, translation, correction, erratum, and degenerate case, and reconcile
the internal/external variants. Only then may the statement phase choose minimal imports, freeze an
elaborated Lean expression and environment fingerprint, compile checked alternate encodings, and
run removed-hypothesis, changed-domain, binder-scope, and boundary-case mutations.
