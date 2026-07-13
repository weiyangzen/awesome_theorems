# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6854-6859` supplies exactly the title `Kneser定理`, attribution
to Martin Kneser, year 1953, gloss `阿贝尔群上子集和的结构`, importance "high," and status
`已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, exact theorem,
definitions, binders, hypotheses, conclusion, proof boundary, correction history, reviewer, or
formal artifact.

`Docs/Stage0_Blueprint.md:25579-25604` repeats the gloss while explicitly leaving precise
definitions and premises, proof process, dependencies, alternate forms, axioms, machine status,
and artifact links open. Its generic closed-result and leaf-budget prose is planning metadata. The
rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and resets this target to
`L0 / rework_required`.

## Literal crosswalk

| Catalog element | Needed mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| `Kneser定理`, Martin Kneser | exact named result, source edition, statement, proof, and corrections | immutable source record and node mapping | theorem family identified; exact root open |
| 1953 | date-matched primary result | source-selected target | matches the integer-density paper, not the usual finite-group citation |
| "abelian groups" | exact ambient group, finiteness/topology, and structures | `AddCommGroup G` plus possible `Finite`, topology, or measure instances | absent and in tension with the date-matched source |
| "sumset structure" | sets, sum operation, stabilizer/period, invariant, and conclusion | `A + B`, `AddAction.stabilizer`, cardinal/density/measure expression | family-level only |
| `已验证` | reviewed human proof and kernel receipts | accepted H/M evidence packets | no credit |

The gloss is recognizable but not binder-complete. In particular it does not select cardinality,
asymptotic density, or Haar measure, and it states no inequality or structural alternative.

## Date-matched 1953 primary lead

Martin Kneser, *Abschätzung der asymptotischen Dichte von Summenmengen*, *Mathematische
Zeitschrift* 58 (1953), 459-484, DOI `10.1007/BF01174162`, was inspected through the GDZ article
scan `PPN266833020_0058/LOG_0059`. The observed 27-page PDF (one GDZ cover plus 26 article pages)
was 2754308 bytes with SHA-256
`71a4fab5239b149b3e382092454a2186bc1147b81bc3a2ca9ad59d5b01642dea`.

Printed page 459 defines sumsets for sets of rational integers and lower finite/asymptotic
density. Printed page 461 states a density theorem/dichotomy involving periodic residue-class
supersets. Thus this source matches the catalog year but does not directly state the familiar
finite-subset cardinality theorem over an arbitrary abelian group.

This is a discriminatory primary-source lead, not `H0`: no complete transcription and proof-node
crosswalk, translation review, correction/errata audit, or independent reviewer acceptance exists.

## Finite-subset primary lead

Martin Kneser, *Ein Satz über abelsche Gruppen mit Anwendungen auf die Geometrie der Zahlen*,
*Mathematische Zeitschrift* 61, 429-434, DOI `10.1007/BF01181357`, was inspected through the GDZ
article scan `PPN266833020_0061/LOG_0034`. The observed seven-page PDF (GDZ cover plus six article
pages) was 891400 bytes with SHA-256
`f3fc4de5349ef471fc9d365fd182f2b9c07b8dda6dd418987e46075795b8e548`.

Printed page 429 sets an arbitrary, not necessarily finite, abelian group and describes the largest
subgroup stabilizing a sumset. Printed page 430, Satz 1, says that for any two finite subsets `A`
and `B` there exists a subgroup `H` such that `A + B + H = A + B` and
`|A + B| >= |A| + |B| - |H|`. Unlike the weaker Satz 2 below it, Satz 1 does not explicitly add a
nonempty hypothesis. This source matches the catalog's group/cardinality flavor better, but not its
1953 date. Existential `H` and canonical greatest-stabilizer encodings also require a checked map.

This is an inspected primary candidate supporting discrimination only. Edition/date reconciliation,
complete definitions, proof and errata mapping, translation review, and independent acceptance are
open, so it is not `H0` and is not the canonical target.

## Locally compact primary lead

Crossref and DOI metadata identify Martin Kneser, *Summenmengen in lokalkompakten abelschen
Gruppen*, *Mathematische Zeitschrift* 66 (1956), 88-110, DOI `10.1007/BF01186598`. Its opening
pages were inspected as a materially different Haar-measure/topological formulation. It further
shows that the catalog gloss does not uniquely determine a finite-cardinality target. No complete
source packet or H credit is claimed for this candidate.

## Statement decisions still open

| Decision | Why it changes the proposition |
|---|---|
| 1953 density, volume-61 finite cardinality, or 1956 Haar measure | changes domain, invariant, assumptions, and conclusion |
| finite ambient group or finite subsets of arbitrary abelian group | changes binders and available cardinal arguments |
| existential period subgroup or canonical stabilizer | changes witness ownership and required equivalence proof |
| weak `|A|+|B|-|H|` or coset-saturated bound | changes theorem strength |
| empty inputs allowed or nonempty required | affects stabilizer finiteness and degenerate truth values |
| sets, finsets, quotient sets, or measurable sets | changes coercions, equality, and computation semantics |
| subtraction in naturals or an integer-valued inequality | changes boundary behavior |

## Lean discovery boundary

Pinned mathlib provides `AddAction.stabilizer`, pointwise `Finset.add`, stabilizer finiteness and
coercion lemmas, `cauchy_davenport_minOrder_add`, and one-set small-doubling structure. A bounded
exact-name search found no classical Kneser declaration. The sole `Kneser` hit is a TODO/reference
in `Mathlib.Combinatorics.Additive.VerySmallDoubling`; it is not a statement or proof.

`IntakeProbe.lean` authenticates only adjacent pinned interfaces. No exact proposition, minimal
canonical imports, expression/environment fingerprint, formal-candidate provenance, proof body,
or trust closure is credited. Systematic candidate discovery remains downstream.
