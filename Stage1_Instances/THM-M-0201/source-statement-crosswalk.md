# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1450-1455` supplies exactly the Chinese title `托勒密定理`, the
attribution Claudius Ptolemy, the date `约公元150年`, the gloss
`圆内接四边形对角线乘积等于对边乘积之和`, importance `中`, and status `已验证`. Git blame
places all six uncited lines at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, edition,
theorem or page locator, formula, definitions, hypotheses, proof boundary, correction or errata
ledger, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:5590-5615` repeats the gloss while explicitly leaving exact definitions
and premises, proof route, dependencies, equivalent statements, axioms, machine status, and artifact
links open. The rev-5.6 target manifest preserves `已验证` only as untrusted metadata and resets the
target to `L0 / rework_required`.

## Candidate mathematical crosswalk

No primary or independently approved authoritative human source was inspected and admitted during
intake. The conventional expansion below is therefore a scope map, not H0 evidence.

| Catalog phrase | Conventional component | Prospective Lean surface | Intake status |
|---|---|---|---|
| `圆内接` (inscribed in a circle) | all four vertices lie on one planar circle | `Concyclic {A, B, C, D}` or a sphere-membership predicate plus coplanarity | definition, ambient dimension, and transport open |
| `四边形` (quadrilateral) | vertices `A, B, C, D` in boundary order | ordered tuple or four points plus a cyclic-order/intersection predicate | catalog supplies no order, convexity, or distinctness policy |
| `对角线` (diagonals) | `AC` and `BD` | `dist A C` and `dist B D`, with an intersection witness in the pinned candidate | point order and intersection encoding open |
| `对边` (opposite sides) | pairs `(AB, CD)` and `(BC, DA)` | `dist A B * dist C D` and `dist B C * dist D A` | matches candidate conclusion after equality symmetry |
| `乘积等于...之和` | `AC * BD = AB * CD + BC * DA` | an equality in `Real` between products of metric distances | precise scalar and segment-length encoding open |
| Ptolemy / ca. 150 CE | historical attribution metadata | human-source provenance record | no source edition, passage, proof, genealogy, or attribution audit |
| `已验证` | untrusted inventory label | no declaration or proof credit | explicitly rejected as evidence |

Before H0, an accountable reviewer must preserve an immutable approved edition, pinpoint the exact
statement and incorporated definitions, map every assumption and conclusion, audit translation,
historical attribution, corrections, and errata, map the human proof boundary to future obligations,
and approve the crosswalk independently.

## Pinned formal candidate boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Geometry.Euclidean.Sphere.Ptolemy` states that it proves Ptolemy's theorem for the lengths
of the diagonals and sides of a cyclic quadrilateral. Its principal declaration is
`EuclideanGeometry.mul_dist_add_mul_dist_eq_mul_dist_of_cospherical`:

- it quantifies points `a b c d p` in a real inner-product affine metric space;
- it assumes `Cospherical {a, b, c, d}`;
- it assumes `angle a p c = pi` and `angle b p d = pi`, placing `p` strictly between the endpoints
  of each diagonal without separately asserting transversality or uniqueness; and
- it concludes `dist a b * dist c d + dist b c * dist d a = dist a c * dist b d`.

The file itself records that this formulation works around the absence of a cyclic-polygon concept
and distinguishes strict and weak cyclicity. Its source is pinned by SHA-256
`d13991b9cfa5aed210efd9dfa59ee78d50d7a73c6e7dcb74ea09b33b3785b547`; the Lean 4 file was
introduced at mathlib commit `8663fc73b2d17c0b51b8094a11e5e1252f2a5d31`. The current pinned
declaration reports only `propext`, `Classical.choice`, and `Quot.sound` through Lean's axiom
printer.

`EuclideanGeometry.mul_dist_le_mul_dist_add_mul_dist`, in
`Mathlib.Geometry.Euclidean.Inversion.Basic`, proves the associated inequality for arbitrary four
points and is explicitly a non-substitute. `IntakeProbe.lean` authenticates both exposed types and
axiom reports. It does not select the canonical root, prove equivalence to an admitted human source,
inspect terminal proof-body provenance, close the transitive trust boundary, or admit an M0 wrapper.
The direct equality interface therefore supports only the provisional intake classification M3.

## Source gate

The statement phase must first select the exact human proposition, resolve every boundary in
`scope-map.md`, and elaborate a canonical Lean expression with minimal imports, fixed options, an
environment fingerprint, checked alternate transports, and the four required mutation classes.
Only after that freeze may the anchor audit decide whether the pinned declaration matches or
transports to the exact root and classify its proof body, dependencies, axioms, placeholders,
unsafe/oracle boundaries, and trust profile.
