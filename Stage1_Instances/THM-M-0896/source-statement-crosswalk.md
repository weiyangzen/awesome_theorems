# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6558-6563` supplies exactly:

| Catalog field | Verbatim value | Intake interpretation |
|---|---|---|
| title | `有限几何` | subject label, not a proposition |
| attribution | `众多数学家` | no named theorem author or source |
| time | `20世纪` | broad catalog period |
| statement | `有限几何与图论的联系` | underspecified relationship-family gloss |
| importance | `高` | catalog metadata only |
| formalization status | `已验证` | explicitly untrusted by the rev-5.6 manifest |

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no citation, URL, theorem
number, definition, geometry or graph construction, parameters, hypotheses, conclusion, proof
locator, or formal artifact. Its exact six-line extract has SHA-256
`1b8a930087f9113a94a3f23ade1237d1e2a829af751321617d6826e7b78eb2fb`.

`Docs/Stage0_Blueprint.md:24440-24465` is a generated projection, not an independent source. It
repeats the gloss while leaving exact definitions and premises, proof history, dependencies,
equivalent statements, axiom policy, machine status, and artifact links `待补充` (to be supplied).

## Source phrase to proposition fields

| Required field | Supported by repository source? | Frozen intake value |
|---|---:|---|
| finite-geometry class | no | open |
| graph construction and graph category | no | open |
| domains and universes | no | open |
| ordered quantifiers | no | empty; no binders invented |
| parameters and hypotheses | no | empty; order, dimension, field, and incidence axioms not selected |
| exact conclusion | no | open among multiple inequivalent relationship theorems |
| direction of construction/equivalence | no | open |
| excluded degenerate cases | no | none excluded |
| canonical mathematical statement | no | `null` |
| canonical Lean target and hashes | no | `null` |
| accepted human proof source | no | none |
| accepted formal proof body | no | none |

The literal noun phrase is preserved without being promoted to a theorem. A statement worker must
obtain an approved target correction or source selection before it can populate these fields.

## Discovery reference not credited

Eric W. Weisstein, "Finite Geometry," MathWorld, was inspected at
`https://mathworld.wolfram.com/FiniteGeometry.html`. The page defines finite geometry by finiteness
of the point set and distinguishes projective plane geometries from affine plane geometries.

This mutable reference confirms that even the finite-plane reading has multiple geometry classes.
It does not state the catalog's unspecified relationship to graph theory, select a graph
construction or conclusion, supply a primary proof, or receive independent review. Its response
bytes varied across repeated retrievals during intake, so no response digest is admitted. The
repository does not cite it. It receives no H0 or statement-selection credit.

Two stable technical references were also inspected only to test whether the relationship gloss
has a unique standard reading:

- Andries E. Brouwer and Hendrik Van Maldeghem, *Strongly regular graphs*, 2021 monograph, author
  PDF `https://homepages.cwi.nl/~aeb/math/srg/rk3/srgw.pdf`, 452 pages, observed SHA-256
  `fa73d72e86bbd8dc3fbfcbca45679cb8f2671d777e91c009eeff0a563fd9289d`. Chapter 2 defines both
  a point/collinearity graph and a bipartite point-line incidence graph for a partial linear
  geometry, then gives distinct strong-regularity and parameter theorems for polar spaces and
  generalized quadrangles.
- Edwin R. van Dam, Jack H. Koolen, and Hajime Tanaka, "Distance-regular graphs," *Electronic
  Journal of Combinatorics* Dynamic Survey DS22 (2016), journal PDF
  `https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS22/pdf`, 156 pages, observed
  SHA-256 `ef07467d520aaed2f2d92d23a55974ed661a3d9e03eb08b1eca42fc944336de6`. Sections 3.1 and 4.5
  distinguish dual-polar graph families, point/collinearity graphs, and point-line incidence
  graphs, with different distance-regularity and correspondence results.

These references make non-uniqueness concrete: the same broad subject supports different geometry
carriers, graph functors, directions, hypotheses, and conclusions. Neither is cited by the catalog;
neither selects this target or receives H0, exact-statement, proof-body, or independent-review
credit.

## Neighbor record crosswalk

The catalog places this record between separate entries for distance-regular graphs, strongly
regular graphs, and design theory:

| Target | Catalog gloss | Boundary |
|---|---|---|
| `THM-M-0894` | `距离正则图的理论` | graph-theory family, not an implied finite-geometry construction |
| `THM-M-0895` | `强正则图的参数约束` | parameter theorem family, not transferable root credit |
| `THM-M-0897` | `组合设计的存在性` | design-existence family, not this geometry/graph relationship |
| `THM-M-0903` | `Euler猜想的否定` | named neighboring result, not a replacement theorem |

The adjacency makes several readings plausible but resolves none of them.

## Formal crosswalk and status boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Combinatorics.Configuration` supplies `Configuration.Nondegenerate`, `HasPoints`,
`HasLines`, `ProjectivePlane`, projective-plane order, and point/line cardinality results.
`Mathlib.Combinatorics.SimpleGraph.Basic` supplies simple graphs and graph incidence sets. The probe
checks representative declarations, but no checked map relates these generic APIs to an approved
catalog proposition. A bounded exact-name search found no incidence/Levi/collinearity/point/polarity
graph bridge for projective planes; this is intake discovery, not an external-project audit or a
global absence claim.

The root is provisionally `[H5, M4, R4]`: the supplied target is not a stable proposition, no
usable exact formal artifact is known from the bounded intake search, and no readable proof
reconstruction can attach before statement selection. No H0, M0, R0, accepted state, audit
completion, or theorem completion is claimed.
