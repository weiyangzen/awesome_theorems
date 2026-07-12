# Source-statement crosswalk

## Repository source boundary

| Repository field | Content | Intake assessment |
|---|---|---|
| Stage0 name | `K-理论` | Names a subject, not a proposition |
| Stage0 theorem content | `拓扑K-理论` | Selects topological K-theory but gives no theorem |
| Stage0 attribution/date | Michael Atiyah / Friedrich Hirzebruch; 1959 | Discovery metadata only; no publication, theorem, page, assumptions, or errata |
| Stage0 status | `已验证` | Untrusted metadata; it supplies neither human-proof nor kernel evidence |
| rev-5.6 lane | `hard_statement_first_partial_verification` | Consistent with stopping at exact-statement selection |

## Candidate primary sources

- M. F. Atiyah and F. Hirzebruch, "Vector Bundles and Homogeneous Spaces," in *Differential
  Geometry*, Proceedings of Symposia in Pure Mathematics 3, American Mathematical Society (1961),
  pp. 7-38. This is a historical source lead for the development of topological K-theory. An exact
  theorem/page/assumption/errata audit has not been performed.
- M. F. Atiyah, *K-Theory*, W. A. Benjamin (1967). This is a primary monograph lead for definitions
  and theorem-sized formulations. Edition, theorem/page, assumptions, and errata remain unverified.

These citations are discovery anchors, not `H0` evidence and not authority to choose a root.

## Candidate statement crosswalk

| Candidate mathematical root | Required source components | Required Lean components | Intake status |
|---|---|---|---|
| `K^0(X)` Grothendieck construction | space class, bundle monoid, equivalence relation, universal property | vector bundles, isomorphism classes, commutative monoid, Grothendieck group | possible root; not selected |
| Pullback functoriality | continuous maps, pullback construction, identity/composition laws | pullback bundle and induced group homomorphism | possible root; not selected |
| Reduced/relative exactness | pointed/pair conventions and exact sequence | reduced or relative groups and exactness APIs | possible root; not selected |
| Cohomology theory | grading, suspension, exactness, wedge/additivity conventions | a generalized cohomology-theory interface | possible root; not selected |
| Representability | chosen classifying space or spectrum and naturality | homotopy classes or spectrum maps and a natural equivalence | possible root; not selected |
| Bott periodicity | periodicity map and degree shift | periodicity equivalence | excluded here; owned by `THM-M-0575` |

Repository-local text search found mathlib-facing vector-bundle files and incidental
Grothendieck-group references, but no file or declaration identified as an exact topological
K-theory root for `THM-M-0574`. This is intake discovery only; the dependent anchor audit must
repeat a precommitted search against the pinned revision and inspect terminal declarations and
proof provenance.

The statement phase can proceed only after an authoritative correction replaces the subject label
with one exact proposition and pins its source theorem/pages. Inventing a conjunction of all rows,
or selecting the easiest row, would broaden or substitute the repository target.

