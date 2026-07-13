# Source-statement crosswalk

## Repository source and provenance

`Docs/researches/math_theorems.md:1436-1441` is the complete repository source record. It gives the
Chinese title, attribution to Menelaus of Alexandria, approximate date 100 CE, gloss
`共线点的比例关系`, medium importance, and formalization status `已验证`. Git provenance attributes
all six uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Their exact UTF-8
excerpt has SHA-256 `49510ff1eb237d359de74c03be822b340b4e0b7f061ae1f12185b242d9910f5d`.
The record contains no bibliography, edition, theorem/page, formula, definitions, assumptions,
proof, corrections, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:5536-5561` repeats the gloss while explicitly leaving exact definitions
and premises, proof route, dependencies, equivalent forms, axioms, machine status, and artifact
links open. The rev-5.6 target manifest preserves `已验证` only as `source_status_untrusted` and
resets the target to `L0 / rework_required`. Neither generated projection supplies source or proof
credit.

## Inspected modern statement lead

B. D. S. "Blue" McConnell, *A Six-Point Ceva-Menelaus Theorem*, arXiv record `1403.0478`
(`math.MG`; the API labels its sole submission `v1`, submitted 2014-03-03), printed pages 1-2,
describes the conventional triangle-side setting and states Theorem 2 (Menelaus): for `D`, `E`, and
`F` on the extended side lines opposite `A`, `B`, and `C`, respectively, the points are collinear if
and only if `d e f = -1`, where
`d = |BD|/|DC|`, `e = |CE|/|EA|`, and `f = |AF|/|FB|`. Footnote 1 fixes signed segment directions
on `AB`, `BC`, and `CA` and also discusses zero, infinite, and point-at-infinity ratios. The
inspected PDF has SHA-256
`ba8ff135a0bb270547f94e3344b59b35de8c107265638f95537812c0e36a3b77`. It was retrieved on
2026-07-13 from `https://arxiv.org/pdf/1403.0478v1`; the server named it `1403.0478v1.pdf`, but its
PDF metadata and printed date say 2018-10-30. This dossier therefore binds the inspected content by
hash and does not claim that its bytes are the originally deposited 2014 artifact.

This is a secondary modern statement and proof-route lead, not accepted `H0`. It is not cited by
the catalog, it is not an edition of Menelaus's historical text, and it has no independent source
review in this dossier. Lawful durable preservation, historical genealogy, definition and premise
mapping, zero/infinite-ratio semantics, proof-node crosswalk, corrections/errata review, and an
approved relationship to the repository gloss remain open.

## Clause crosswalk

| Repository or candidate clause | Source-lead content | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `共线点` | `D`, `E`, `F` collinear | `Collinear k {D, E, F}` or an affine-span equivalent | exact predicate and point order open |
| triangle | distinct `A`, `B`, `C` with oriented edge lines | `t : Affine.Triangle k P` or explicit points plus affine independence | source-domain transport open |
| points on side lines | `D` on `BC`, `E` on `CA`, `F` on `AB` | line membership or witnesses via `AffineMap.lineMap` | binders and correspondence open |
| `比例关系` | product of three signed ratios | affine parameters or directed segment ratios in `k` | encoding and nonzero denominators open |
| displayed value | `d * e * f = -1` under the source lead's orientations | field product equality | sign and reciprocal convention not catalog-selected |
| theorem direction | collinearity iff product identity | `Iff` or separately checked implications | catalog direction open |
| infinity convention | footnote includes infinite ratios and ideal points | affine finite-point theorem or projective extension | cannot be silently dropped or added |
| Menelaus / approximately 100 CE | catalog genealogy | immutable historical-source ledger | no primary passage or genealogy audit |
| `已验证` | untrusted inventory label only | accepted human and kernel evidence would be required | no H or M credit |

## Pinned Lean substrate crosswalk

Pinned mathlib supplies `Affine.Triangle`, affine-independent triangle points, `AffineMap.lineMap`,
the line-membership/line-parameter equivalence, and `Collinear`. These are suitable vocabulary for
a future finite affine formulation. The pinned declaration
`Affine.Triangle.prod_eq_prod_one_sub_of_mem_line_point_lineMap` is Ceva's theorem: it derives a
product identity from three concurrent vertex lines. Its mathematical role, quantification, and
conclusion differ from Menelaus, so it is recorded only to prevent false reuse.

Bounded case-insensitive searches of repository-local Lean, pinned mathlib source, and pinned
mathlib history found no Menelaus-named declaration. Absence from a bounded intake search is not a
global absence proof and does not replace the later immutable anchor audit. `IntakeProbe.lean`
checks only the adjacent interfaces listed above; it declares no target and covers no proof
obligation.

An external Lean 4 candidate was located at `rjwalters/lean-genius` merge commit
`84b23f1bcdf237ee0ee4b0d16a960a04e7a9c299`, path
`proofs/Proofs/MenelausTheorem.lean`, source SHA-256
`605e0c2508eb2843a2320b52fe31e5f4a6d1b68cfe1876aa824a75728253a64f`. Its declaration
`MenelausTheorem.menelaus` is an affine-coordinate iff with nonzero denominator and noncollinear
base-triangle conditions. The unmodified 139-line source plus an axiom print elaborated under this
repository's pinned Lean/mathlib environment and reported `propext`, `Classical.choice`, and
`Quot.sound`; a scoped source scan found no prohibited proof construct. Upstream declares Lean
4.26.0 and mathlib revision `2df2f0150c275ad53cb3c90f7c98ec15a56a1a67`.

This remains intake discovery, not proof credit. The candidate is not a dependency of this
repository, has no repo-local wrapper, and is not yet mapped to an accepted human proposition.
Exhaustive terminal-body provenance, transitive dependency/trust/license audit, expression identity,
scope transport, composition, freshness receipts, and master acceptance belong to later phases. It
therefore receives no `M0`, `M1`, canonical-statement, or accepted-proof status here.

## First source and statement gate

The statement phase must select and independently approve one immutable source proposition, decide
every boundary in `scope-map.md`, and elaborate a minimal-import Lean expression with fixed
universes, namespaces, options, foundation profile, expression and environment fingerprints,
checked transports, and the four mandated mutation classes. Until then the canonical statement and
formal target remain absent, and all source, proof, audit, and completion claims remain open.
