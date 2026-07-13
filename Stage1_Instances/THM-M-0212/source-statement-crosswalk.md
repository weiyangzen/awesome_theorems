# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1527-1532` supplies exactly the title `布里昂雄定理`, Charles
Julien Brianchon, 1806, the phrase `圆锥曲线外切六边形的共点性质`, importance `中`, and status
`已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:5887-5912`
repeats the phrase while explicitly leaving the formal system, foundation, precise definitions and
premises, proof route, alternate forms, axioms, machine status, and artifact links open.

| Repository phrase | Information plausibly indicated | Information not fixed | Intake result |
|---|---|---|---|
| `圆锥曲线` (conic) | a plane conic is tangent to the six sides | projective model, field, quadratic or synthetic definition, smooth/singular policy | unresolved |
| `外切六边形` (circumscribed hexagon) | six cyclic side lines tangent to the conic | order, distinctness, contact points, vertex construction, ideal intersections | unresolved |
| `共点性质` (concurrency property) | three principal diagonals should meet | exact opposite pairs, diagonal existence, concurrency encoding, uniqueness, forward versus iff | unresolved |
| Brianchon / 1806 | historical-family attribution | accepted edition, passage, translation, historical-versus-modern scope | unresolved |
| `已验证` | inventory metadata | human proof review or kernel evidence | no credit |

## Inspected modern source leads

Jean Valles, *A Poncelet Theorem for Lines*, arXiv `1202.2340v1` (10 February 2012), was inspected
from its versioned PDF, SHA-256
`45dfbe033651b8fef5ca4dcc55c90fc37e47fbae571d3c8a772353fe36e264b5`. Section 2.3,
Theorem 2.8, printed page 6, works in the complex projective plane with a smooth conic. For a
polygon `L1 union ... union L2n` tangent and circumscribed to the conic, it states a dual Mobius
implication: concurrency of the first `n - 1` lines joining opposite adjacent-side intersections
implies concurrency of the remaining such line. The following remark identifies `n = 3` as
Brianchon's theorem. The paper explicitly obtains the result by polarity from the inscribed
theorem. This is a complete versioned statement and proof lead, but its complex, smooth-conic,
duality-based scope is not selected by the catalog.

Magdalena Lampa-Baczynska and Daniel Wojcik, *Relative Conics and Their Brianchon Points*, Turkish
Journal of Mathematics 45 (2021), 1605-1618, DOI `10.3906/mat-2102-2`, was inspected through the
publisher's metadata and abstract. The abstract describes six lines tangent to a common conic, the
circumscribed hexagon, and concurrency of its three diagonals at a Brianchon point. Its primary
topic is the wider configuration of relabeled hexagons and their Brianchon points, not a
catalog-selected proof boundary. A transient metadata digest is recorded, but no publisher
artifact is preserved in the repository or admitted as accepted source evidence.

These sources support provisional `H1`, not `H0`. The repository cites neither source, their exact
definitions and boundary conventions are not accepted, the original 1806 source and correction
history have not been audited, and no independent source reviewer has approved a row-by-row map.

## Crosswalk to a future statement

| Candidate component | Source-lead role | Required Lean surface | Status |
|---|---|---|---|
| projective plane | Valles uses a complex projective plane; the second abstract does not fix a field | `Projectivization K (Fin 3 -> K)` or reviewed synthetic model | representation and field open |
| ordered side lines | Valles names an ordered tangent polygon | six ordered dual points or projective lines | distinctness and cyclic contract open |
| tangency | each side is tangent to the conic | source-faithful contact or polarity predicate | encoding and characteristic open |
| vertices | adjacent lines `Li` and `Li+1` meet | checked line-intersection construction | noncoincidence and ideal cases open |
| diagonals | Valles joins the three opposite vertex pairs at `n = 3` | checked line-through-points construction | exact totality hypotheses open |
| concurrency | conclusion for the three diagonal lines | common-point/dependence/determinant predicate | exact encoding and transport open |
| duality/converse | Valles proves a dual Mobius form by polarity | checked point-line and conic-duality transport | no transport credited |

## Pinned Lean boundary

Pinned mathlib exposes `Projectivization`, `Projectivization.Subspace`,
`Projectivization.Subspace.span`, `Projectivization.cross`, `Projectivization.orthogonal`,
`Projectivization.Dependent`, `QuadraticForm`, and `QuadraticMap.polarBilin`.
`Projectivization.cross` is useful homogeneous incidence substrate, but it is total on equal
arguments and therefore cannot by itself encode the intended vertex or diagonal contract.
`Projectivization.orthogonal` is coordinate dot-product orthogonality, not a source-selected conic
polarity. Quadratic forms and their polar maps do not by themselves define the required projective
conic, dual conic, tangent lines, or proof. `IntakeProbe.lean` elaborates only these adjacent APIs.

A bounded case-insensitive search of pinned mathlib and repository-local Lean for Brianchon,
circumscribed-hexagon, and tangent-hexagon phrases found no target declaration. This is intake
discovery, not the exhaustive immutable anchor audit required by the downstream node.

## Source gate

Before `H0`, accountable reviewers must preserve and hash an approved complete edition, select one
pinpoint theorem and all incorporated definitions, map every domain, binder, hypothesis, tangent
side, vertex, opposite pair, diagonal, concurrency convention, conclusion, and boundary case,
audit corrections and errata, and independently approve fidelity to `THM-M-0212`. Only then may
the statement phase freeze minimal imports, one elaborated expression and environment fingerprint,
checked alternate encodings, and the required statement mutations.
