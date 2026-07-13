# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:1689-1694` supplies exactly the title `儒歇定理`, Eugene
Rouche, 1862, the gloss `函数零点个数稳定性` ("stability of the number of zeros of functions"),
high importance, and status `已验证`. All six uncited lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no formula, bibliography,
definition, premise, proof boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:6491-6516` repeats those fields and explicitly leaves the formal system,
foundation, precise definitions and premises, proof route and dependencies, alternate forms,
axioms, machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

## Duplicate-record boundary

The same repository source has an adjacent record at lines 1675-1680 for `鲁歇定理`, Eugene
Rouche, 1862, glossed as "comparison of the numbers of zeros of holomorphic functions." It is
projected as the separate rev-5.6 target `THM-M-0232`. `鲁歇` and `儒歇` are alternate Chinese
transliterations of the same surname, and the metadata provides no mathematical discriminator.
The integration lane must decide whether the records are aliases, a duplicate to reconcile, or
distinct source variants. Until then, their scope, statements, receipts, and proof credit remain
strictly separate.

## Human-source discovery lead

The Bibliotheque nationale de France catalog identifies Eugene Rouche, *Memoire sur la serie de
Lagrange*, Paris: Imprimerie imperiale, 1866, 31 pages, catalog ARK
`ark:/12148/cb31252939w`. Its record links the digitized Gallica object
`ark:/12148/bpt6k165297c` and says the printing is an extract from volume XVIII of *Memoires
presentes par divers savants a l'Academie imperiale de France*.

This bibliographic record is a primary-work lead only. Its 1866 date does not validate the
catalog's 1862 date; the work's exact theorem passage, definition chain, relation to any earlier
presentation, translation, proof boundary, corrections, and errata were not inspected and
independently reviewed here. It therefore supports H1 discovery, not H0.

## Candidate component crosswalk

| Repository/source component | Mathematical decision to freeze | Prospective Lean component | Intake status |
|---|---|---|---|
| `儒歇定理` / Eugene Rouche | exact historical theorem and relationship to `THM-M-0232` | one source-approved canonical `Prop` and an explicit duplicate policy | family identified; identity unresolved |
| zero-count stability | perturbation form versus direct comparison form | `f`, `g`, or perturbation `h`, with ordered binders | candidate forms only |
| enclosed region | disk, Jordan interior, bounded domain, or contour/cycle | set/curve, interior, boundary, orientation, compactness data | exact domain open |
| holomorphic functions | neighborhood-of-closure versus interior plus boundary continuity | `AnalyticOnNhd` or checked equivalent complex differentiability predicates | regularity open |
| smaller on the boundary | strict norm inequality with one named dominant function | pointwise `forall z in boundary, norm (...) < norm (...)` | inequality and dominance open |
| same number of zeros | finite sum of local analytic orders in the interior | analytic order/divisor restriction plus a source-approved finite count | count representation open |
| multiplicity | local order of vanishing, including repeated zeros | `analyticOrderAt`, `analyticOrderNatAt`, or checked divisor encoding | nearby APIs probed; bridge open |
| `已验证` | untrusted catalog field | no proposition or proof object | explicitly rejected as evidence |

## Alternate-form boundary

Two familiar candidate forms are:

- `norm h < norm f` on the boundary implies that `f` and `f + h` have equal interior zero counts;
- `norm (f - g) < norm f` on the boundary implies that `f` and `g` have equal interior zero counts.

Their elementary substitution relationship still needs to be stated against one exact domain and
zero-count encoding and checked in Lean before either is credited as an alternate encoding. A
Jordan-curve formulation, disk formulation, homotopy/winding formulation, and meromorphic index
form require additional checked transports. None is selected at intake.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe
checks analytic orders, isolated-zero behavior, and meromorphic divisors. Bounded searches for the
Rouche name, argument-principle wording, and equal-zero-count conclusions found no exact target in
pinned mathlib or repo-local Lean. This is bounded intake discovery, not a global absence result or
the immutable formal-candidate audit required by `S56-M-0234-ANCHOR_AUDIT`.

Before H0, an independent reviewer must preserve a lawful immutable source edition and map its
exact theorem, definitions, every assumption, conclusion, proof boundary, date history,
corrections, and errata. Before statement credit, a formal reviewer must approve and elaborate the
same source-faithful Lean expression, its minimal imports, environment and expression fingerprints,
checked alternate transports, and required semantic mutations.
