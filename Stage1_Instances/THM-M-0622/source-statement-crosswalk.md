# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:4615-4620` supplies only the title `蒂策扩张定理`, attribution to
Heinrich Tietze, year 1915, the gloss `正规空间中闭集上连续函数的延拓`, high importance, and formal
status `已验证`. All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. This is repository provenance, not a source or proof
receipt. The rev-5.6 manifest retains the status only as `source_status_untrusted`.

`Docs/Stage0_Blueprint.md:17017-17042` repeats the gloss while leaving the formal system,
foundations, precise definitions and premises, proof route, dependency graph, alternate forms,
axioms, machine status, and artifact links pending.

## Primary source lead

The Göttingen IIIF volume manifest identifies Heinrich Tietze's article *Uber Funktionen, die auf
einer abgeschlossenen Menge stetig sind*, *Journal fur die reine und angewandte Mathematik* 145
(1915), printed pages 9-14, DOI `10.1515/crll.1915.145.9`. Its `LOG_0006` range covers the six
printed pages. The downloaded seven-page PDF includes a repository cover plus those page images.

The scan was visually inspected. Printed page 14 gives Satz 3: a bounded continuous function on a
closed subset of a Frechet class extends continuously to the whole class. Printed page 12 defines
the Frechet class through a distance satisfying identity, symmetry, positivity, and the triangle
inequality. Printed page 9 describes the extension question, and Satz 1-2 develop stronger
majorization and semicontinuity results used in the paper.

This is primary discovery evidence and supports `H1`, not `H0`. The scan has no embedded article
text; no independently reviewed diplomatic transcription or translation, theorem-assumption map,
proof-node crosswalk, correction/errata audit, or review of the historical-to-modern normal-space
generalization exists.

## Clause crosswalk

| Repository or source component | Mathematical choice | Prospective Lean surface | Intake disposition |
|---|---|---|---|
| `正规空间` / normal space | separation of disjoint closed sets, with or without T1 | `NormalSpace X`; possibly also `T1Space X` or `T4Space X` | unresolved convention |
| `闭集上` / on a closed set | closed `s : Set X`, with `f` defined on its subtype | `hs : IsClosed s`; `f : C(s, Real)` | likely boundary; exact binder order open |
| `连续函数` | real-valued or another codomain; bounded or arbitrary | `ContinuousMap`, `BoundedContinuousFunction`, `TietzeExtension` | codomain and boundedness omitted by catalog |
| `延拓` / extension | equality after restriction or pointwise composition | `exists_restrict_eq`, `exists_extension`, or a checked transport | exact encoding open |
| Tietze 1915 Satz 3 | bounded real-valued map on a closed subset of a metric/Frechet class | bounded same-norm candidate is stronger; generic metric-to-normal transport needed | primary lead only; no accepted identity |
| modern full theorem | arbitrary real-valued map on a closed subset of a normal space | `ContinuousMap.exists_restrict_eq` with `Y := Real` | strong exact-topic candidate, not canonical yet |
| range-preserving versions | retain an interval or order-connected target set | `exists_restrict_eq_forall_mem_of_closed` | stronger optional conclusion, not implied by gloss |
| `已验证` | claimed formal status | no declaration, proof body, pin, or receipt | explicitly no credit |

## Pinned formal discovery boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Topology.TietzeExtension` contains the generic extension class and the real-valued proof
family. `IntakeProbe.lean` authenticates the relevant types under Lean 4.29.0. The axiom reports for
`ContinuousMap.exists_restrict_eq` and `Real.instTietzeExtension` are
`[propext, Classical.choice, Quot.sound]`.

The source file itself says its proof mostly follows nLab and patches a gap for unbounded
functions. That source boundary, each terminal declaration and proof body, transitive dependencies,
license, exact source-to-target match, and the generic-class versus real-instance composition still
belong to the downstream immutable anchor audit. Intake proposes `M3`, not `M0-W`.

## Status and next gate

The catalog and primary scan identify a proved theorem family, so the proposed human state is
`H1`. Pinned mathlib provides usable exact-topic interfaces and proof candidates, but the canonical
claim and Lean expression are not frozen, so the proposed machine state is `M3`. No readable proof
reconstruction exists, hence `R4`.

Before the statement gate, an independent source reviewer must approve the exact historical or
modern proposition, normal/T1 convention, codomain, boundedness and range clauses, degenerate
cases, translation, corrections/errata status, and every checked implication needed to match the
catalog. No source, proof, or theorem-completion claim follows from this intake crosswalk.
