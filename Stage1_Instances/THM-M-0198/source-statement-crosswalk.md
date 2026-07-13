# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:1429-1434` supplies exactly the title `西姆松线定理`, attribution
Robert Simson, year 1756, gloss `三角形外接圆上一点在三边的投影共线`, importance `中`, and status
`已验证`. Git blame places all six uncited lines at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, edition,
theorem/page, formula, definitions, ordered binders, hypotheses, proof boundary, correction history,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:5509-5534` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, equivalent forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

## Literal clause crosswalk

| Repository phrase | Mathematical detail required | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `三角形` (triangle) | three distinct noncollinear vertices in a chosen Euclidean plane/space | `Affine.Triangle Real P` or a checked coordinate equivalent | nondegeneracy, dimension, and ordering absent |
| `外接圆` (circumcircle) | the circle through the three vertices in their plane | `Affine.Simplex.circumsphere` plus an ambient-plane boundary, or an existential sphere/circle | representation and dimension open |
| `上一点` (a point on it) | a quantified point satisfying circle membership | `p : P` and `p ∈ t.circumsphere` | vertex cases and coplanarity open |
| `三边` (three sides) | conventionally the three supporting side lines | affine spans of `(t.faceOpposite i).points` | lines versus closed segments unresolved |
| `投影` (projections) | perpendicular feet from the circle point to those sides | `(t.faceOpposite i).orthogonalProjectionSpan p` | candidate API only; coercion and indexing open |
| `共线` (collinear) | the three projected points lie on one affine line | `Collinear Real` on a range or three-point set | exact packaging and transports open |
| Robert Simson / 1756 | historical catalog metadata | source provenance record | no primary passage or attribution audit |
| `已验证` | untrusted inventory status | accepted source and kernel receipts would be required | no H or M credit |

The syntax above is prospective vocabulary only. It is deliberately not assembled into a
canonical proposition during intake.

## Human-source boundary

No primary or independently approved authoritative human source was inspected and admitted during
this intake. The catalog attribution is therefore retained as metadata only. In particular, this
run does not decide the historical attribution often discussed under the Wallace-Simson name, the
date of first proof, or whether a source states only the forward direction or the converse as well.

The provisional `H1` classification records a classical theorem believed to have a complete human
proof while the exact source reconstruction remains open. Before H0, accountable reviewers must
lawfully preserve an immutable approved edition, pinpoint the exact theorem and incorporated
definitions, map every binder, assumption, conclusion, projection and collinearity convention,
audit translations, corrections, errata and attribution, map the human proof boundary to future
obligations, and approve the crosswalk independently.

## Pinned Lean discovery boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- `Affine.Triangle` is an affine-independent 2-simplex, hence a candidate nondegenerate triangle;
- `Affine.Simplex.circumsphere` and `Affine.Simplex.mem_circumsphere` supply a canonical sphere
  through a simplex's vertices;
- `Affine.Simplex.faceOpposite` selects the side opposite each triangle vertex;
- `Affine.Simplex.orthogonalProjectionSpan` projects a point onto the affine span of a simplex;
- `EuclideanGeometry.orthogonalProjection_mem` records incidence in that affine subspace; and
- `Collinear` records that a set's affine vector span has rank at most one.

`IntakeProbe.lean` checks these interfaces in the pinned environment. A bounded search for Simson,
Wallace-Simson, pedal-line, and projection-foot collinearity declarations found no exact theorem in
pinned mathlib or repository-local Lean. Generic infrastructure is therefore classified as
provisional `M3`, not as a statement or proof of the root.

## First downstream gate

The statement phase must preserve and independently approve one exact human proposition, decide
every boundary in `scope-map.md`, then elaborate only that claim with minimal pinned imports, a
serialized expression and environment fingerprint, checked alternate encodings, and all four
required statement mutation classes. Only afterward may the anchor audit classify exact-body
provenance, trust, placeholders, unsafe/oracle boundaries, and formal candidate status.
