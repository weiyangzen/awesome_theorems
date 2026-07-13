# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1457-1462` supplies exactly the title `婆罗摩笈多公式`, attribution
to Brahmagupta, year 628, gloss `圆内接四边形面积公式` ("area formula for a cyclic quadrilateral"),
medium importance, and formalization status `已验证`. Git history places all six uncited lines in
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:5617-5642` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, equivalent forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as untrusted
metadata and resets the item to `L0 / rework_required`.

Neither record contains a bibliography, edition, chapter/verse/page locator, formula, definition of
area or cyclic quadrilateral, ordered binders, hypotheses, conclusion, proof boundary, translation,
correction history, errata, or reviewer. They establish catalog identity only.

## Human-source boundary

The title and attribution make Brahmagupta's *Brahmasphutasiddhanta* a historical primary-source
family lead, and the year 628 is consistent with the catalog identity. This intake did not inspect
or admit a Sanskrit manuscript, critical edition, exact chapter/verse/page, translation, proof,
archival identifier, correction history, or errata. It also did not establish whether the original
passage states the formula only, states or assumes cyclicity, or how later commentary supplies its
proof and modern boundary conditions.

Consequently the provisional human classification is `H1`, not `H0`: a classical proved theorem
family is known, while its exact source-to-catalog statement and assumptions remain unaudited.
Before H0 can be proposed, an accountable reviewer must preserve a lawful immutable edition,
identify the exact passage and proof boundary, transcribe every incorporated definition and
assumption, audit translation and attribution, reconcile commentary and later proof sources,
dispose of corrections and errata, list dependent source IDs, and independently approve the
crosswalk.

## Inspected secondary leads

Eric W. Weisstein, "Brahmagupta's Formula," Wolfram MathWorld,
`https://mathworld.wolfram.com/BrahmaguptasFormula.html`, was retrieved on 2026-07-13. Its metadata
and body state

```text
K = sqrt ((s-a)(s-b)(s-c)(s-d)),  s = 1/2 (a+b+c+d),
```

as the cyclic-quadrilateral specialization of a general quadrilateral formula, with the relevant
opposite angles summing to pi. The retrieved HTML had 59,682 bytes and SHA-256
`fdc7bed68dab186140b589bdc5ed73766cb182b988d8ebf9987efaf1ebc3a270`.

J. J. O'Connor and E. F. Robertson, "Brahmagupta," MacTutor History of Mathematics Archive,
`https://mathshistory.st-andrews.ac.uk/Biographies/Brahmagupta/`, was retrieved on 2026-07-13. It
states that the *Brahmasphutasiddhanta* was written in 628 and attributes cyclic-quadrilateral area
and diagonal formulas to it. It also records a proposition-changing historical dispute: the work
does not explicitly say the formulas apply only to cyclic quadrilaterals, so historians disagree
over whether that restriction was intended. The retrieved HTML had 70,173 bytes and SHA-256
`a0dd298afce7f195d672625306635f21d66844ed96806ae6a535606ee856d17e`.

Neither mutable web page is a primary proof source, accepted immutable edition, exact historical
passage, or independent review. They receive E5 discovery status only. In particular, MacTutor's
warning prevents the modern cyclic premise from being attributed to the historical source without
a critical-edition and commentary audit. The hashes record the responses observed by this intake;
mutable server output can vary, so neither hash is an offline replay input or freshness guarantee.

## Clause crosswalk

| Repository component | Conventional family component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `四边形` / quadrilateral | four vertices in cyclic boundary order | ordered points, polygon/list, or four points plus an order predicate | representation, order, convexity, simplicity, and distinctness open |
| `圆内接` / cyclic | vertices lie on one circle | `Concyclic` or `Cospherical` plus planarity/order data | exact predicate and positive-radius policy open |
| `面积` / area | nonnegative area `K` | absolute orientation form, triangulated area, convex-hull measure, or polygon area | no definition selected |
| four sides | consecutive lengths `a`, `b`, `c`, `d` | `dist A B`, `dist B C`, `dist C D`, `dist D A` | absent from repository; binder/order transport open |
| semiperimeter | `s = (a+b+c+d)/2` | local `let` or explicit real binder | not mentioned by repository |
| formula | conventional `K = sqrt((s-a)(s-b)(s-c)(s-d))` | exact real equality with `Real.sqrt` | formula absent; candidate family only |
| assumptions | ordinary cyclic quadrilateral | planar, ordered, convex/simple, distinct, nondegenerate hypotheses | entirely absent |
| equality form | square-root or squared identity | `K = Real.sqrt R` or `K ^ 2 = R` | source selection and checked transport open |
| `已验证` | untrusted inventory label | exact target and accepted receipt would be required | no H or M credit |

## Pinned Lean boundary

A bounded exact-topic search of repo-local Lean and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` found no occurrence of `Brahmagupta` tied to a geometry
declaration, no `Bretschneider` occurrence, and no cyclic-quadrilateral area or semiperimeter
declaration. The only exact-name mathlib hits were unrelated algebraic identities and a title-only
entry in `docs/1000.yaml` with no declaration mapping.

The pinned library does contain adjacent interfaces:

- `EuclideanGeometry.Cospherical` and `EuclideanGeometry.Concyclic` in
  `Mathlib.Geometry.Euclidean.Sphere.Basic`;
- `EuclideanGeometry.Cospherical.two_zsmul_oangle_eq` in
  `Mathlib.Geometry.Euclidean.Angle.Sphere`, relating angles determined by four cospherical points;
- Euclidean triangle identities in `Mathlib.Geometry.Euclidean.Triangle`; and
- exact real square-root operations and lemmas.

`IntakeProbe.lean` elaborates a small selection of these pinned APIs. Its output is evidence that
generic interfaces are available, not that a quadrilateral area object, Brahmagupta statement,
target-specific reduction, or proof exists. It declares no theorem and installs no proof credit.
This supports provisional `M4`, not `M3`: no usable target-specific formal artifact was located.
Comprehensive repo-local and external discovery remains the downstream anchor-audit task after an
exact source-selected statement is frozen.

## First source and statement gate

An independent source reviewer must admit one immutable exact human proposition and approve every
definition, premise, conclusion, proof boundary, translation, attribution, correction, and erratum.
The statement phase must then fix the area encoding, ambient dimension, ordered quadrilateral,
circle and cyclic-order predicates, side correspondence, convexity/simplicity/distinctness,
semiperimeter and square-root conventions, equality form, and every boundary case; compile checked
transports for each credited alternate; serialize the elaborated expression and environment; and
pass removed-hypothesis, changed-domain, binder-scope, and boundary-case mutations.
