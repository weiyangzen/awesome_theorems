# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1731-1736` supplies exactly the title
`阿贝尔-雅可比定理`, Niels Abel/Carl Jacobi, 1834, the gloss `代数曲线的雅可比簇`, importance
`high`, and status `已验证`. Git history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:6653-6678` repeats the metadata but explicitly leaves the precise
definitions and premises, proof route, dependencies, equivalent forms, axiom policy,
machine-checked state, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

The catalog contains no bibliography, equation, field or curve convention, base point, binder,
hypothesis, conclusion, incorporated definition, proof boundary, correction history, or reviewer.
The gloss is a noun phrase and therefore does not identify a stable proposition.

## Literal crosswalk

| Repository element | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `阿贝尔-雅可比定理` | a theorem attributed jointly to Abel and Jacobi, or a later synthesis of their results | one source-selected declaration and checked transports | title alone does not determine a theorem |
| `代数曲线` | complete nonsingular curve, smooth projective geometrically connected curve, or a broader scheme | `AlgebraicGeometry.Scheme` plus source-fixed predicates | base field and curve hypotheses absent |
| `雅可比簇` | representing abelian variety, `Pic^0`, analytic complex torus, or rational/geometric points thereof | unavailable general curve-Jacobian interface plus future constructions | object, equivalence, and functor-of-points conventions absent |
| Abel / Jacobi / 1834 | historical theorem family | immutable edition, theorem/page, definitions, proof and errata map | catalog supplies no citation or mapping |
| `已验证` | untrusted inventory label | reviewed human source and kernel receipt would be required | no H or M credit |

The title/gloss combination is proposition-changing. Merely defining a Jacobian is not a theorem;
representability, `Pic^0` identification, the kernel of the Abel map, Jacobi inversion, and a
universal property are distinct claims. Selecting one from mathematical familiarity would invent
or substitute the target.

## Inspected source-family lead

J. S. Milne, *Jacobian Varieties*, originally Chapter VII of *Arithmetic Geometry* (Springer,
1986), corrected author edition dated 2021-06-12, was inspected from
`https://www.jmilne.org/math/xnotes/JVs.pdf` (SHA-256
`36c3f09c7462dbbd4ae1f8b81a02bd9ff84f03c5a346351d7d5d78fc3f173486`). The numbering is
stated to be unchanged from the published chapter.

- Theorem 1.1 starts with a complete nonsingular curve over a field and asserts existence of an
  abelian variety `J` with a morphism from a degree-zero Picard functor, an isomorphism on `T`
  when `C(T)` is nonempty. Its surrounding text discusses descent and uniqueness.
- Theorem 1.2, assuming a rational point, states a divisorial-correspondence universal property.
- Theorem 2.5 over `Complex` identifies the analytic and algebraic Jacobians; its proof explicitly
  invokes Abel's theorem and the Jacobi inversion theorem.

These materially different exact theorems all fit parts of the catalog phrase. The catalog does not
cite Milne, and intake does not select one, map every assumption and incorporated definition,
audit corrections/errata, or supply an independent reviewer. This is a named source and explicit
unresolved mapping list, but because the received target itself is not a stable proposition the
root remains `H5`, not `H0` or `H1`.

Serge Lang's *Introduction to Algebraic and Abelian Functions*, Chapter IV, is a title-matching
source lead (`The Theorem of Abel-Jacobi`, GTM 89, Springer, 1972, DOI
`10.1007/978-1-4612-5740-0_4`). Its theorem text was not admitted or inspected in this intake, so
it is only a lead for the statement/source audit.

## Candidate component crosswalk

| Candidate component | Prospective pinned Lean surface | Missing source decision |
|---|---|---|
| base field and curve | `AlgebraicGeometry.Scheme`, `AlgebraicGeometry.Smooth`, `AlgebraicGeometry.IsProper` | exact curve carrier, structural hypotheses, genus, and geometric assumptions |
| degree-zero Picard object | general invertible sheaves and a relative Picard functor | the pinned ring-level `CommRing.Pic` is insufficient; quotient and sheaf conventions absent |
| Jacobian variety | an abelian variety representing the selected Picard functor | object and representability API absent from the pinned search |
| Abel-Jacobi map | divisor or point map normalized at a base point | domain, codomain, sign, degree, and base-point conventions |
| Abel kernel theorem | principal divisor iff zero image | separately cataloged `THM-M-0238` boundary and exact equivalence assumptions |
| Jacobi inversion | surjectivity from a source-fixed symmetric power | separately cataloged `THM-M-0239` boundary, genus, degree, and field |
| analytic comparison | quotient of holomorphic-differential dual by integral homology | complex-only analytic structures and comparison maps |
| universal property | morphisms or divisorial correspondences through `J` | pointedness, uniqueness, functor variance, and rational-point assumptions |

The API probe authenticates generic names and types only. No row is a canonical statement,
checked transport, proof body, or `M0` result.

## Neighbor target crosswalk

`Docs/researches/math_theorems.md:1717-1722` separately records `THM-M-0238` as Abel's theorem
with the gloss `椭圆积分的反演`. Lines 1724-1729 separately record `THM-M-0239` as Jacobi
inversion with the gloss `阿贝尔积分的反演`. Adjacency is evidence for keeping those roots separate;
it is not a checked implication, source map, or shared proof credit.

## Formal discovery boundary

The bounded pinned-mathlib search found no exact-topic declaration matching general Abel-Jacobi,
Jacobian variety, Picard scheme/functor, or degree-zero Picard phrasing. Pinned
`Mathlib.AlgebraicGeometry.EllipticCurve.Jacobian` files concern Jacobian coordinates on a
Weierstrass curve; `WeierstrassCurve.Jacobian` is an abbreviation for `WeierstrassCurve`.
`Mathlib.RingTheory.PicardGroup` defines invertible modules over a commutative ring and lists the
connection to invertible sheaves as a TODO. Repository-local Lean files independently record a
curve-to-Jacobian bridge and the Jacobian/Picard target for Manin-Drinfeld as formalization debt.
These are discovery boundaries, not an exhaustive formal anchor audit or proof of global absence.

## Source and statement gate

Before ordinary theorem-proof execution, accountable reviewers must select or correct one stable
truth-valued proposition, preserve an immutable primary source, transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, construction and uniqueness convention, proof
boundary, and correction state, reconcile the neighbor scopes, and independently approve the
mapping. The statement phase must then freeze minimal imports, the elaborated expression and
environment fingerprint, checked alternate transports, and removed-hypothesis, changed-domain,
binder-scope, and boundary mutations.

Until then, `H5` records that the received catalog wording is not a stable proposition. It does not
refute standard results about Jacobians or Abel-Jacobi maps. The canonical mathematical and Lean
targets remain null, and the downstream anchor audit remains open.
