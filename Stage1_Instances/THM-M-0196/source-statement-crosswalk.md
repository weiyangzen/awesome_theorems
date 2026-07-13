# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1415-1420` supplies exactly the Chinese title `九点圆定理`, the
attribution Karl Wilhelm Feuerbach, the year 1822, the gloss `三角形九点共圆`, importance `高`, and
status `已验证`. Git blame places all six uncited lines at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, formula,
definition of the nine points, hypotheses, proof boundary, corrections, reviewer, or formal
artifact.

`Docs/Stage0_Blueprint.md:5455-5480` repeats the gloss while explicitly leaving exact definitions
and premises, proof route, dependencies, equivalent statements, axioms, machine status, and
artifact links open. The rev-5.6 target manifest preserves `已验证` only as untrusted metadata and
resets the target to `L0 / rework_required`.

## Candidate mathematical crosswalk

No primary or independently approved authoritative human source was inspected and admitted during
intake. The conventional expansion below is therefore a candidate scope map, not `H0` evidence.

| Catalog phrase | Conventional component | Prospective Lean surface | Intake status |
|---|---|---|---|
| `三角形` (triangle) | a nondegenerate Euclidean triangle | `Affine.Triangle ℝ P`, an affine-independent 2-simplex | exact source domain and dimension open |
| first three points | midpoints of the three sides | `s.faceOppositeCentroid i` for `i : Fin 3` | exact-topic candidate; source definition open |
| second three points | midpoints from orthocenter to vertices | `s.eulerPoint i`, with `Affine.Triangle.eulerPoint_eq_midpoint` | candidate transport is pinned but not source-approved |
| third three points | feet of the three altitudes | `s.altitudeFoot i` | exact-topic candidate; foot convention open |
| `共圆` (concyclic) | one circle contains all three indexed families | membership in `s.ninePointCircle : EuclideanGeometry.Sphere P` | root packaging and circle equivalence open |
| Feuerbach / 1822 | historical catalog metadata | human-source provenance record | no primary edition, passage, or attribution audit |
| `已验证` | untrusted inventory label | no Lean declaration or proof credit | explicitly rejected as evidence |

Before `H0`, an accountable reviewer must preserve an immutable approved edition, pinpoint the
statement and incorporated definitions, map every assumption and conclusion, distinguish
Feuerbach's tangency theorem and historical attribution, audit corrections and errata, map the
human proof boundary to future obligations, and approve the crosswalk independently.

## Pinned formal candidate boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Geometry.Euclidean.NinePointCircle` says it defines the nine-point circle and, for
triangles, proves that it passes through nine specific points. The relevant declarations are:

- `Affine.Simplex.ninePointCircle`, a sphere centered on the Euler line with radius one half the
  circumradius when specialized to triangles;
- `Affine.Simplex.faceOppositeCentroid_mem_ninePointCircle`, which specializes at `n = 2` to the
  three side midpoints;
- `Affine.Simplex.eulerPoint_mem_ninePointCircle`, which supplies the second indexed family;
- `Affine.Triangle.eulerPoint_eq_midpoint`, which identifies those Euler points with the three
  vertex-orthocenter midpoints; and
- `Affine.Triangle.altitudeFoot_mem_ninePointCircle`, which supplies the three altitude feet.

The same module also proves `Affine.Simplex.ninePointCircle_eq_circumsphere_medial`, a promising
bridge from the constructed sphere to the medial triangle's circumcircle. The source file is pinned
by SHA-256 `929704e099f22672cb05e3847592d3e9084c209ae266473c71b105dd3bc63bc1` and originates in
mathlib commit `704e19496d40b7c2234985dafaf4c9ac58f3008e`.

`IntakeProbe.lean` checks the exposed types and axiom reports of the three membership bodies. It
does not define the canonical conjunction or set statement, prove an equivalence to a reviewed
human source, inspect terminal proof-body provenance, close transitive trust, or admit an `M0-W`
wrapper. Those belong to the statement, anchor-audit, proof, and validation phases. The candidate
therefore receives discovery evidence only and the planned root remains `M4`.

## Source gate

The statement phase must first select the exact human proposition, decide every boundary in
`scope-map.md`, and elaborate a canonical Lean expression with minimal imports, fixed options, an
environment fingerprint, checked alternate transports, and the four required mutation classes.
Only after that freeze may the anchor audit decide whether the pinned mathlib declarations compose
to the exact root and classify proof bodies, dependencies, axioms, placeholders, unsafe/oracle
boundaries, and candidate M status.
