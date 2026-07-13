# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:4608-4613` supplies exactly the title `乌雷松引理`, Pavel
Urysohn, 1925, the gloss `正规空间中闭集的分离` ("separation of closed sets in a normal
space"), importance "high," and status `已验证`. Git blame places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, formula,
definition chain, quantifier order, proof boundary, translation, correction history, reviewer, or
formal artifact.

`Docs/Stage0_Blueprint.md:16990-17015` repeats the gloss while explicitly leaving precise
definitions and assumptions, proof route, dependencies, equivalent forms, axioms, machine status,
and artifact links open. The rev-5.6 target manifest retains `已验证` only as
`source_status_untrusted` and resets the item to `L0 / rework_required`.

## Human-source boundary

The catalog identifies a named classical theorem family, but it does not name a publication. No
immutable primary or authoritative edition was admitted, no exact result or incorporated definition
was located, no premise-to-proof map or errata audit was performed, and no independent reviewer
approved source identity. Because rev-5.6 requires at least a named source for `H1`, the H axis
remains unclassified at intake. This does not classify the theorem as open; it refuses to derive a
human-proof status from untrusted catalog metadata or formal-library evidence. No source is accepted
as `H0`.

## Clause crosswalk

| Catalog component | Proposition-changing decision | Prospective Lean surface | Intake result |
|---|---|---|---|
| "normal space" | normal alone versus normal plus T1/Hausdorff | `[NormalSpace X]` versus stronger typeclasses | mathlib convention observed; source choice open |
| "closed sets" | two arbitrary closed subsets and their binder order | `{s t : Set X}`, `IsClosed s`, `IsClosed t` | candidate only |
| "separation" | disjoint open neighborhoods versus a continuous separator | `NormalSpace.normal` versus `exists_continuous_zero_one_of_isClosed` | named lemma suggests latter; catalog does not decide |
| eligibility for separation | explicit disjointness and its encoding | `Disjoint s t` | candidate premise; source map open |
| separator | real function, continuous map, bounded map, or unit-interval map | `f : C(X, Real)` or checked alternate | canonical encoding open |
| endpoint behavior | orientation and equality encoding | `EqOn f 0 s` and `EqOn f 1 t` | orientation not source-frozen |
| range | global `[0, 1]` bound versus codomain subtype | `forall x, f x in Set.Icc 0 1` | encoding and necessity open |
| Pavel Urysohn / 1925 | historical attribution | immutable edition and pinpoint locator | catalog lead only |
| `已验证` | untrusted inventory status | accepted source and kernel receipts required | no H or M completion credit |

## Pinned formal candidates

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Topology.UrysohnsLemma` exposes:

| Declaration | Candidate role | Intake boundary |
|---|---|---|
| `NormalSpace` / `NormalSpace.normal` | normality convention: disjoint closed sets have separated neighborhoods | definition substrate, not the named functional lemma |
| `normal_separation` | direct access to the normality field | open-neighborhood separation only |
| `normal_exists_closure_subset` | closed-set/open-set shrinking consequence | proof infrastructure only |
| `exists_continuous_zero_one_of_isClosed` | direct Urysohn continuous separator | exact-topic interface; source identity and proof credit open |

`IntakeProbe.lean` elaborates these interfaces and reports the direct axiom summary for the last
declaration as `propext`, `Classical.choice`, and `Quot.sound`. The probe does not inspect terminal
body provenance, establish a source-identical root or elaborated expression fingerprint, accept an
axiom policy, or perform the downstream anchor audit. The direct candidate therefore supports only
provisional `M3` interface classification.

`Mathlib.Topology.UrysohnsBounded.exists_bounded_zero_one_of_closed` is a bounded-continuous-map
wrapper. The compact/closed variants in `UrysohnsLemma` assume regular local compactness and a
compact first set. These are alternate or different proposition families and receive no root
credit at intake.

## Neighbor and namesake boundary

`THM-M-0622` owns Tietze extension and `THM-M-0623` owns Urysohn metrization. Their statements,
proofs, and receipts do not transfer to this target. Likewise, point-separation axioms carrying
Urysohn's name do not select the closed-set continuous-function lemma.

Before leaving intake, the statement route remains blocked on an admitted exact source proposition
and independent review. It must then freeze every definition, binder, hypothesis, conclusion,
degenerate case, minimal import, expression and environment fingerprint, checked transport, and
required statement mutation without broadening or substituting the theorem.
