# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10348-10353` supplies exactly the title
`Bowen-Margulis测度`, the attribution Rufus Bowen / Grigory Margulis, the year 1970, the gloss
`双曲系统的测度`, importance "high," and status `已验证`. The record was introduced by repository
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; it contains no citation or theorem statement.

`Docs/Stage0_Blueprint.md:38510-38535` repeats the same fields while explicitly leaving exact
definitions and premises, proof route, dependencies, equivalent formulations, axiom use,
machine-checked status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

The repository record therefore identifies an object/theorem family, not a stable proposition. It
does not supply an edition, stable source identifier, page or theorem number, exact assumptions,
conclusion, proof, translation, corrections, or errata.

## Crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `Bowen-Margulis测度` | a convention-dependent invariant measure or measure class | one source-selected definition and one exact proposition about it | object name only; no root kind selected |
| "hyperbolic system" | geodesic flow, Anosov map/flow, Axiom A basic set, symbolic suspension, or another model | phase type, topology/geometry, time action, invariant subset, hyperbolicity and regularity hypotheses | system and scope open |
| "measure" | Borel/Radon measure, invariant probability, locally finite lift, or boundary measure class | measurable space, `Measure`, finiteness/probability structure, normalization, invariance | kind and normalization open |
| Bowen / Margulis / 1970 | a broad historical attribution spanning distinct constructions and settings | source provenance only | no title, edition, locator, assumptions, proof, or errata |
| `已验证` | untrusted inventory metadata | inspectable source proof and kernel receipt would be required | no H or M credit |

## Bibliographic discovery boundary

The names suggest historical source families concerning invariant measures for hyperbolic systems
and geodesic flows. Intake does not promote a remembered citation or modern textbook formulation
to an authoritative source. In particular, the catalog's single year and joint attribution do not
show that Bowen and Margulis stated one proposition with identical system, normalization, or
conclusion. A later source may use "Bowen-Margulis measure" for an object characterized as a
measure of maximal entropy, while a geometric source may construct it from a boundary density.
Those formulations require a reviewed equivalence, not a terminology match.

Before the source status can leave `H5`, an accountable reviewer must identify an immutable primary
or authoritative edition, select one exact theorem/definition passage, transcribe every definition,
ordered binder, hypothesis, conclusion, and exceptional case, check translation and errata, and
justify why that proposition represents `THM-M-1416` rather than a neighboring target. A second
reviewer must approve the source-to-canonical-statement mapping. The corrected proposition's H
status must then be classified afresh; it cannot inherit the catalog's `已验证` label.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks adjacent APIs for `Measure`, `IsProbabilityMeasure`, `MeasurePreserving`, `Ergodic`, `Flow`,
and `Dynamics.coverEntropy`. The cover-entropy definition implements a Bowen-Dinaburg topological
invariant; the shared surname does not make it a Bowen-Margulis measure theorem.

A bounded topic search under pinned `Mathlib/Dynamics` and `Mathlib/MeasureTheory` found no
occurrence naming a Bowen-Margulis measure, a measure of maximal entropy, Patterson-Sullivan data,
or a geodesic flow. This is intake discovery only, not the required immutable anchor audit and not
proof of global absence. The canonical module, expression, normalized expression hash, checked
transports, and statement mutations remain null. No H0, M0, or readable-proof closure is claimed.
