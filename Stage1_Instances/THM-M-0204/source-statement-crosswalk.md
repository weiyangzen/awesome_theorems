# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:1471-1476` supplies exactly the title `斯图尔特定理`, attribution
Matthew Stewart, year 1746, gloss `三角形中线长度公式`, importance `中`, and status `已验证`.
All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, work, edition,
theorem/page, formula, definitions, ordered binders, assumptions, proof boundary, correction,
erratum, or reviewer.

`Docs/Stage0_Blueprint.md:5671-5696` projects the record as `THM-M-0204` while explicitly leaving
the formal system, precise definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifact links open. Its generated claim that a closed result is known
is not evidence. Rev-5.6 retains `已验证` only as untrusted metadata and resets the item to
`L0 / rework_required`.

## Literal crosswalk

| Repository component | Mathematical detail required | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Stewart's theorem | decide general cevian identity versus named family | one source-faithful `Prop` | unresolved name/gloss mismatch |
| triangle | ordered vertices, ambient plane/space, nondegeneracy | affine points and exact structures | absent |
| median | midpoint construction and chosen vertex/base | `midpoint ℝ b c` or checked equivalent | absent |
| length formula | exact equality, square or square root, orientation | `dist` powers/products and equality in `ℝ` | absent |
| general cevian, if intended | division point, internal/external convention, directed lengths | point plus angle/betweenness or affine parameter | not stated by the gloss |
| Matthew Stewart, 1746 | exact work, edition, proposition, genealogy, corrections | source provenance only | catalog lead, not H0 |
| `已验证` | claimed formal status | accepted exact declaration evidence | explicitly rejected |

## Human-source boundary

No theorem-level primary or authoritative source is cited or accepted. A bibliographic lead often
associated with the attribution is Matthew Stewart's 1746 work *Some General Theorems of
Considerable Use in the Higher Parts of Mathematics*, but this run could not retrieve and verify a
lawful edition, exact proposition, page, definitions, formula, or proof. The title is therefore a
search lead only, not an inspected source, `E4`, or H0 evidence.

The exact historical relation between Stewart's named general theorem, the repository's median
gloss, and the midpoint identity conventionally called Apollonius's theorem remains unaudited.
Accordingly `H1` records a well-established complete theorem family with unresolved source
reconstruction; it does not approve a statement, attribution, date, or proof-node crosswalk.

Before H0, reviewers must lawfully preserve an immutable edition, identify the precise theorem and
page, transcribe all incorporated definitions, binders, hypotheses, conclusion, division and
degeneracy conventions, map each clause to Lean, audit translation/corrections/errata and the
historical attribution, and independently approve the mapping.

## Pinned Lean discovery boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Geometry.Euclidean.Triangle` contains:

- `EuclideanGeometry.dist_sq_mul_dist_add_dist_sq_mul_dist`, documented as Stewart's theorem. For
  affine points `a b c p`, an angle-pi hypothesis at `p` gives the ordinary-distance identity
  `dist a b ^ 2 * dist c p + dist a c ^ 2 * dist b p =
  dist b c * (dist a p ^ 2 + dist b p * dist c p)`.
- `EuclideanGeometry.dist_sq_add_dist_sq_eq_two_mul_dist_midpoint_sq_add_half_dist_sq`, documented
  as Apollonius's theorem. It gives
  `dist a b ^ 2 + dist a c ^ 2 =
  2 * (dist a (midpoint ℝ b c) ^ 2 + (dist b c / 2) ^ 2)` without an explicit hypothesis.

The second proof specializes the first when `b != c` and separately handles `b = c`. Adjacent
angle and midpoint declarations expose the exact internal-division and endpoint-distance behavior.
The intake probe elaborates both candidates and prints their reported axiom sets in the pinned
environment. This establishes usable direct formal interfaces, hence provisional `M3`, but not
source-to-root identity, a canonical statement, accepted proof provenance, or M0 credit.

The general declaration's formal name and comment favor Stewart's theorem; the median declaration's
formula favors the literal catalog gloss. Neither metadata match resolves the conflict. A later
anchor audit must inspect terminal bodies, transitive dependencies, axioms and TCB only after the
statement phase freezes which proposition is actually requested.

## First blocker and retry condition

The first downstream blocker is exact source-statement identity. An approved source decision must
resolve general cevian versus median scope, all point and length conventions, ambient geometry,
nondegeneracy and boundary cases listed in the scope map. The statement phase can then encode and
elaborate only that proposition, minimize imports, serialize its fingerprints, check alternate
encodings, and mutation-test hypotheses, domains, binder scope, and boundary cases.
