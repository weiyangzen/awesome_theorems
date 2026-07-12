# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10411-10416` supplies exactly the title `随机吸引子`, the
attribution "many mathematicians", the period "twentieth century", the gloss
`随机系统的吸引子`, importance "high", and status `已验证`. Git blame attributes all six lines to
repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no
bibliography, definition, formula, theorem statement, assumptions, or proof.

`Docs/Stage0_Blueprint.md:38753-38778` repeats the gloss while explicitly leaving the formal
system, logical foundation, background, exact definitions and premises, proof route, dependencies,
equivalent forms, axioms, machine status, and artifact links open. Its generic planning text about
a known closed result is not primary-source evidence. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

The repository record therefore identifies an object or theorem family, not a stable proposition.
It gives no immutable primary edition, theorem or definition locator, exact assumptions,
conclusion, proof boundary, translation, correction, or errata record.

## Bibliographic discovery lead

A strong uncredited candidate is Hans Crauel and Franco Flandoli, *Attractors for random dynamical
systems*, *Probability Theory and Related Fields* **100**(3) (1994), 365-393, DOI
`10.1007/BF01193705`. Crossref metadata confirm the authors, title, journal, volume, issue, year,
and pages. Inspection identifies Theorem 3.11 as an existence result for a compact invariant global
random attractor of a continuous random dynamical system on a Polish space from a compact random
set that absorbs every bounded deterministic subset; its discrete- and continuous-time cases have
different measurable-completion boundaries.

This is a discovery lead, not source authority for the target. The catalog neither cites the paper
nor selects Theorem 3.11 rather than another existence, connectedness, invariant-measure,
application, forward-attraction, weak-attraction, or singleton-attractor result. No immutable
inspected-copy hash, complete definition/assumption/errata crosswalk, or independent source review
is admitted here, so the candidate supplies no H0 statement and cannot choose the Lean target.

## Component crosswalk

| Repository element | Mathematical component to freeze | Required Lean component | Intake assessment |
|---|---|---|---|
| `随机吸引子` | one definition and one truth-valued result about it | no single `Prop` follows from the object name | object/topic label only |
| "random system" | base probability flow plus random cocycle/semiflow | probability/noise type, measurable flow, time, state, cocycle laws | every model choice is open |
| "attractor" | pullback, forward, weak, local/global, point, compact, or set-valued notion | random set, invariance, basin, attraction predicate and quantifier order | meaning and conclusion open |
| randomness | pointwise, almost-sure, in-probability, or in-law scope | measure, `∀ᵐ`, measurable sections, exceptional-set policy | convergence and null-set scope open |
| attraction | convergence of images of a selected family to a random set | filter limit plus one-sided/symmetric set distance or topology | metric and initial-family class open |
| invariance | equality or inclusion after base shift | `IsInvariant`, `MapsTo`, set image/equality with base-index transport | no invariance clause supplied |
| compactness/measurability | compact random set, measurable graph or hyperspace map | `IsCompact`, Borel/measurable-set APIs, chosen random-set encoding | conditions and encoding open |
| "many mathematicians" / twentieth century | broad historical provenance | documentation only | no source title, locator, or assumptions |
| `已验证` | untrusted inventory label | accepted human-source and kernel receipts would be required | no H or M credit |

## Variant boundary

Pullback attraction changes the base point before evolving an initial family; forward attraction
does not use the same quantifier order. Weak attraction can mean convergence in probability and
does not imply pathwise pullback attraction. A one-sided Hausdorff semidistance expresses approach
without equality of sets, whereas symmetric Hausdorff distance is stronger and needs finiteness
conditions. Strict invariance is stronger than forward invariance. Existence from an absorbing set,
uniqueness, omega-limit representation, upper semicontinuity, and singleton synchronization are
distinct roots, not interchangeable formulations.

The neighboring targets for coupling, random dynamical systems, and multivalued random dynamics
cannot select one of these variants. A standard definition or remembered existence theorem would
therefore broaden or substitute the received target.

## Source gate

Before the target can leave `H5`, an accountable reviewer must approve a corrected truth-valued
root, preserve an immutable primary or authoritative edition, identify an exact theorem and every
referenced definition, transcribe ordered binders and hypotheses, check translation, corrections,
and errata, map every conclusion clause and boundary case, and obtain independent approval. The
corrected proposition's H status must then be classified afresh; it cannot inherit the catalog's
`已验证` label.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`IntakeProbe.lean` checks generic `Flow`, `IsInvariant`, `omegaLimit`, compactness,
`Metric.hausdorffDist`, measurability, and filter convergence APIs. A bounded exact-topic search
found no random-attractor, pullback-attractor, forward-attractor, random-dynamical-system, or random
compact-set declaration. The omega-limit API concerns ordinary flows unless a random model is
separately encoded; it does not identify the missing root.

The canonical module, declaration/expression, elaborated-expression hash, checked transports, and
statement mutations remain null. The probe and search are intake feasibility evidence only, not a
complete candidate audit and not H0, M0, or readable-proof closure.
