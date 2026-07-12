# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:526-531` supplies exactly the title `有限单群分类定理`, attribution
to many mathematicians, the year 1983, the claim `所有有限单群属于18个无穷族或26个散在群`, high
importance, and status `部分验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, stable source ID,
definition, exact list, ordered binder, hypothesis, formal conclusion, proof boundary, correction
history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:2055-2080` repeats the claim while explicitly leaving the formal system,
foundation, exact definitions and premises, proof process, dependencies, alternate forms, axioms,
machine status, and artifact links open. Its generic branch-deepening language is planning metadata,
not branch evidence. The rev-5.6 manifest preserves `部分验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Catalog element | Necessary mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| "finite simple group" | a finite nontrivial group with only trivial normal subgroups | `[Group G]`, `[Finite G]`, `IsSimpleGroup G` | adjacent pinned API elaborated; exact source convention open |
| "belongs to" | classification up to group isomorphism | existential `MulEquiv` to a constructed representative | relation and representative universe absent |
| "18 infinite families" | an exact convention-sensitive family roster with admissible parameters | typed sum of constructed cyclic, alternating, and Lie-type representatives | roster, count convention, constructions, and exceptions absent |
| "26 sporadic groups" | exact sporadic representatives with identity and nonduplication rules | finite index plus constructed groups and equivalences | no representatives or formal taxonomy located |
| collective attribution / 1983 | historical coordinates | provenance only | points to a literature family, not a pinpoint theorem |
| `部分验证` | untrusted inventory field | branch-level receipts would be required | no H or M credit |

The slogan is recognizably about CFSG, but a giant disjunction over invented names would not be the
received theorem. The number 18 depends on how families and twisted/exceptional cases are grouped;
small-parameter exclusions and exceptional isomorphisms affect representatives; and the slogan does
not specify whether classification data must be unique.

## Inspected exact-statement witness

Valdo Tatitscheff, *A short introduction to Monstrous Moonshine*, arXiv `1902.03118v4` (24 May
2021), PDF pages 2-3, Theorem 1, was inspected from the versioned arXiv PDF. It says that a finite
simple group is either an element of one of 18 infinite families or one of 26 exceptional sporadic
groups. The following paragraph counts the two familiar families of cyclic prime-order and
alternating groups, then 16 Lie-type families: nine Chevalley, four Steinberg, one Suzuki, and two
Ree families, with the Tits group appended.

Among the sources inspected in this bounded intake, this is the closest literal-statement match,
but it is an expository secondary preprint, not a primary proof source or the catalog's cited
provenance. Its preceding simple-group definition does not explicitly exclude the trivial group,
so the standard nontriviality convention is also an incorporated-definition issue. It does not
construct a formal family datatype, enumerate all admissible parameters and low-rank exclusions,
resolve every exceptional isomorphism, or supply the complete primary proof ledger. Immediately
before Theorem 1 it dates completion to 2004 and mentions a correction in 2008, so it does not
validate the catalog's bare 1983 date. The immutable PDF has SHA-256
`d7a471c813f8d21383c9ac5ff1cdffd58f1a43f1346e872d350a16e06a19eb6c`; the observed arXiv metadata
response has SHA-256 `e84ba46ff664fc3c715f361545b8990be6bcd1add4c14d94fcf06b7c162a4246`.
It is admitted only as an `E5` statement and taxonomy witness and cannot by itself establish `H0`.

## Inspected primary-book proof-boundary lead

Daniel Gorenstein, *The Classification of Finite Simple Groups*, Volume 1: *Groups of
Noncharacteristic 2 Type*, The University Series in Mathematics, originally Plenum Press, 1983;
Springer online ISBN `978-1-4613-3685-3`, DOI `10.1007/978-1-4613-3685-3`, was inspected through the
publisher's metadata, front matter, table of contents, Introduction abstract, and Conclusion
abstract.

The publisher describes classification of all finite simple groups as one theorem whose complete
proof was developed over 30 years by about 100 group theorists in roughly 500 articles and 10,000
pages. This supports `H1`: a complete published proof is represented in the literature, but this
intake has not built the pinpoint primary-source, assumption, errata, and node crosswalk required
for `H0`.

The source also establishes an important boundary. Volume 1 is not a self-contained proof of the
catalog slogan. Its contents cover low 2-rank cases, involution centralizers, the B-theorem, groups
of component type, Lie-type and sporadic cases within that route. The Conclusion says the volume
outlines the noncharacteristic-2 theorem: a minimal counterexample to CFSG is of characteristic 2
type with proper subgroups that are K-groups. That is a deep reduction, not the terminal
18-family/26-sporadic enumeration. The catalog does not cite the book, and the inspected material
does not select the exact counting convention or supply a complete source-node ledger.

Observed temporary discovery-input digests are recorded in `intake-receipt.json`. No external file
is copied into the repository, and no source is admitted as `H0` or independently reviewed.

## Lean discovery boundary

Pinned mathlib defines `IsSimpleGroup` as a nontrivial group whose normal subgroups are bottom or
top. `Mathlib.GroupTheory.SpecificGroups.Cyclic` proves that a commutative group is simple exactly
when its cardinality is prime, including finiteness. `Mathlib.GroupTheory.SpecificGroups.Alternating`
proves simplicity of `alternatingGroup (Fin 5)` but explicitly leaves general alternating-group
simplicity as a TODO.

These results authenticate definitions and two special branches only. A bounded case-insensitive
search over pinned mathlib and repo-local Lean found no terminal classification-of-finite-simple-
groups, sporadic-group, Mathieu-group, or Monster-group declaration. A documentation index mentions
the theorem title without a mapped declaration. These observations are not an exhaustive external
candidate audit and receive no root coverage credit.

Before leaving `H1`, reviewers must pin a statement and full source boundary, define and crosswalk
the family convention and all representatives, record assumptions and corrections, map the human
proof architecture, and obtain independent source approval. Only then may the statement phase
freeze a minimal-import Lean expression, checked transports, environment fingerprint, and the
required removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
