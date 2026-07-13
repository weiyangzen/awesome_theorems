# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1520-1525` supplies exactly the title `帕斯卡定理`, Blaise
Pascal, 1640, the phrase `圆锥曲线内接六边形的共线性质`, importance `高`, and status
`已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:5860-5885`
repeats the phrase while explicitly leaving the formal system, foundation, precise definitions and
premises, proof route, alternate forms, axioms, machine status, and artifact links open.

| Repository phrase | Information plausibly indicated | Information not fixed | Intake result |
|---|---|---|---|
| `圆锥曲线` (conic) | a plane conic is the locus containing the vertices | projective model, field, quadratic or synthetic definition, smooth/reducible policy | unresolved |
| `内接六边形` (inscribed hexagon) | six cyclically ordered points on the conic | order, distinctness, repeated-point tangents, general-position hypotheses | unresolved |
| `共线性质` (collinearity property) | the three opposite-side intersection points should align | exact side pairing, intersection existence, collinearity encoding, forward versus iff | unresolved |
| Pascal / 1640 | historical-family attribution | accepted edition, passage, translation, exact historical-versus-modern scope | unresolved |
| `已验证` | inventory metadata | human proof review or kernel evidence | no credit |

## Inspected modern source leads

Alessio Caminata and Luca Schaffler, *A Pascal's Theorem for Rational Normal Curves*, arXiv
`1903.00460v2` (11 May 2021), was inspected from its versioned PDF, SHA-256
`5bb1ce3b2191fcbb9ccdb3c43d308d9e7846b152e57127655ebe9d93d4553f28`. The abstract
and Section 1, printed pages 1-2, state that six points `a,...,f` in `P^2` on a conic imply
alignment of `ab ∩ de`, `af ∩ dc`, and `ef ∩ bc`. The introduction then distinguishes a convention
under which "Pascal's Theorem" includes the Braikenridge-Maclaurin converse and possibly degenerate
conics. It gives a determinant/Grassmann-Cayley equation and cites Pascal's 1640 *Essay pour les
coniques* plus modern algebraic references. This is a strong statement and proof-family lead, not a
catalog-selected root.

Kaylee Wiese, *A Group Theory Proof of Pascal's Theorem*, arXiv `2408.00020v1` (30 July 2024),
was also inspected from its versioned PDF, SHA-256
`c80285f3c7792b4f9300586cd1458b5ded76f810cc6d0fdfabc2a9afa8619b58`. Theorem 1 on
printed page 1 states the forward result in the real projective plane, using consecutive pairs
`ab/de`, `bc/ef`, and `cd/fa`. It permits repeated vertices through tangent lines provided each
paired pair of lines is not identical, and Sections 2-3 give the advertised group-theoretic proof.
That tangent-inclusive real formulation differs from a distinct-point smooth-conic formulation.

These versioned sources support provisional `H1`, not `H0`. The repository does not cite either
source, their different domain and degeneracy conventions are not reconciled, the exact proof and
definition boundary is not accepted, corrections and errata are not audited, Pascal's historical
source is not independently checked, and no independent source reviewer has approved a row-by-row
mapping.

## Crosswalk to a future statement

| Candidate component | Source-lead role | Required Lean surface | Status |
|---|---|---|---|
| projective plane | both leads formulate a projective-plane theorem | `Projectivization K (Fin 3 -> K)` or reviewed synthetic model | representation and field open |
| ordered vertices | both use six named conic points | ordered six binders plus on-conic hypotheses | distinctness/repetition open |
| side pairing | `ab/de`, `bc/ef`, `cd/fa` up to reordered notation | lines and intersection construction | incidence hypotheses open |
| conic membership | the antecedent in the forward theorem | source-faithful conic predicate | smooth/reducible and characteristic open |
| collinearity | conclusion for three intersections | projective span/dependence/determinant predicate | exact encoding and transport open |
| converse | explicit broader convention in Caminata-Schaffler | reverse implication as a separate root or transport | excluded until selected |
| repeated points | tangent convention in Wiese | tangent-line definition and well-definedness | excluded until selected |

## Pinned Lean boundary

Pinned mathlib exposes `Projectivization`, `Projectivization.Subspace`,
`Projectivization.Subspace.span`, `Projectivization.cross`, `Projectivization.orthogonal`, and
`QuadraticForm`. `Projectivization.cross` is useful homogeneous incidence substrate, but it is total
on equal points and therefore cannot by itself encode the intended distinct line/intersection
contract. The affine predicate `Collinear` is a different model and needs a checked transport before
use. `IntakeProbe.lean` elaborates only these adjacent interfaces.

A bounded case-insensitive search of pinned mathlib and repository-local Lean for Pascal theorem,
mystic hexagon, and conic-hexagon phrases found no target declaration; the only broad `Pascal` hits
in mathlib described Pascal's triangle. This is intake discovery, not the exhaustive immutable
anchor audit required by the downstream node.

## Source gate

Before `H0`, accountable reviewers must preserve and hash an approved complete edition, select one
pinpoint theorem and all incorporated definitions, map every domain, binder, hypothesis, side pair,
intersection, conic convention, conclusion, and boundary case, audit corrections and errata, and
independently approve fidelity to `THM-M-0211`. Only then may the statement phase freeze minimal
imports, one elaborated expression and environment fingerprint, checked alternate encodings, and
the required statement mutations.
