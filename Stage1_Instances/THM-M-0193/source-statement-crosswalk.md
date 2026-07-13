# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1394-1399` supplies exactly the title `勾股定理`, attribution to
the Pythagorean school, approximate date 500 BCE, gloss
`直角三角形两直角边平方和等于斜边平方`, importance high, and formalization status `已验证`.
All six uncited lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:5374-5399` repeats the gloss while explicitly leaving precise definitions
and premises, proof route, dependencies, equivalent forms, axioms, machine status, and artifact
links open. The rev-5.6 target manifest retains `已验证` only as untrusted metadata and resets the
item to `L0 / rework_required`. Neither repository record provides a bibliography, edition,
theorem/page, formula, definition chain, proof boundary, translation, correction history, or
reviewer. The historical attribution and date are therefore leads only.

## Inspected source lead

John Casey, *The First Six Books of the Elements of Euclid*, third edition (Dublin: Hodges,
Figgis & Co.; London: Longmans, Green & Co., 1885), Book I, Proposition XLVII, printed pages 42-43,
states:

> In a right-angled triangle (ABC) the square on the hypotenuse (AB) is equal to the sum of the
> squares on the other two sides (AC, BC).

The public Project Gutenberg ebook `#21076` was inspected on 2026-07-13. Its PDF at
`https://www.gutenberg.org/files/21076/21076-pdf.pdf` has SHA-256
`fa77c91ea6b1e31fe09dea4d9a4310e7f8345dba5be0563603f62e7742ffce5c`; the proposition occurs
on PDF page 53. The TeX source at
`https://www.gutenberg.org/files/21076/21076-t/21076-t.tex` has SHA-256
`7cf5f99d98b81e395ccbd90f519ed653d27c5688878a5743b0293d78bc151647`; the statement starts at
line 3795 and the proof follows. The files were inspected and hashed but not added to this
repository.

This is an authoritative-edition discovery lead, not accepted `H0` evidence. It is not the
catalog's cited source, does not prove the Pythagorean-school attribution or date, and has no
recorded independent reviewer. Lawful immutable preservation, definition and assumption mapping,
translation/version review, correction/errata disposition, and proof-node crosswalk remain open.

## Clause crosswalk

| Catalog clause | Casey/Euclid I.47 | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| right triangle | triangle `ABC`, angle `ACB` right | three affine points plus `EuclideanGeometry.angle ... = Real.pi / 2` | point ordering and nondegeneracy open |
| two legs | sides `AC` and `BC` containing the right angle | `dist A C`, `dist B C` or reordered equivalents | endpoint and leg order open |
| hypotenuse | side `AB`, opposite `C` | `dist A B` | maps only after binder order is fixed |
| squares | Euclidean squares constructed on the sides | products or powers of real distances | area-to-length-square transport open |
| sum equals | square on `AB` equals squares on `AC`, `BC` | equality in `Real` | syntax and orientation open |
| theorem direction | right angle implies square equality | forward implication | pinned main candidate is a stronger iff |
| boundary convention | ordinary Euclidean triangle | mathlib candidate permits a broad affine domain and is documented for possible degeneracy | explicit case policy open |
| `已验证` | no corresponding source claim | no expression or receipt | no credit |

## Pinned formal leads

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Geometry.Euclidean.Angle.Unoriented.RightAngle` contains the direct candidate
`EuclideanGeometry.dist_sq_eq_dist_sq_add_dist_sq_iff_angle_eq_pi_div_two`. It states, for three
points in a real inner-product affine torsor, an iff between a squared-distance equality and the
angle at the middle point being `pi / 2`. The same module contains vector-angle variants, and
`Mathlib.Analysis.InnerProductSpace.Basic` contains inner-product-zero variants.

The pinned source explicitly describes its results as applying to possibly degenerate
right-angled triangles and using only theorem-specific nondegeneracy assumptions. The intake probe
elaborates the declarations and reports `propext`, `Classical.choice`, and `Quot.sound` for the two
inspected iff candidates. This authenticates adjacent pinned interfaces only. Exact
source-to-formal identity, one-way projection, equality normalization, terminal proof-body and
dependency provenance, trust acceptance, and alternate transports remain downstream work.

## First source/statement gate

An independent reviewer must approve one authoritative source proposition and its definition,
assumption, conclusion, proof-boundary, translation, and errata mapping. The statement phase must
then fix the ambient space, binders, right-angle vertex, nondegeneracy policy, squared-side syntax,
direction, and every boundary case before elaborating and mutation-testing one exact Lean target.
