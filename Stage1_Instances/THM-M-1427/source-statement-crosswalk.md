# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10425`-`:10430` supplies exactly the title `复动力系统`,
"many mathematicians," "twentieth century," the gloss `复解析映射的动力学`, importance
"high," and status `已验证`. All six lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no author-level attribution,
bibliography, definition, formula, theorem locator, proposition, or proof.

`Docs/Stage0_Blueprint.md:38807`-`:38832` repeats that gloss. It explicitly leaves the background,
exact definitions and premises, proof route, proof date, dependencies, equivalent formulations,
axioms, classical/choice dependence, existing machine status, and artifact links to be supplied.
Its generic theorem-tree and 100-step text is planning boilerplate, not source evidence. The
rev-5.6 manifest carries `已验证` only as `source_status_untrusted` and resets the target to
`L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `复动力系统` | a broad field studying iteration in one or more complex variables | no single declaration follows from a field name | not a stable proposition |
| "complex" | `Complex`, the Riemann sphere, a domain, or a complex manifold | exact type, universe, topology, charts, scalar action, and compactness data | all open |
| "analytic maps" | holomorphic, entire, meromorphic, polynomial, rational, or manifold-holomorphic maps | exact map type, domain/codomain, self-map closure, regularity predicate, degree and pole conventions | all open |
| "dynamics" | iterates, orbits, periodic points, invariant sets, normality, stability, entropy, or parameter variation | iterate convention plus one exact `Prop` with ordered binders, hypotheses, and conclusion | no truth-valued conclusion supplied |
| many mathematicians / twentieth century | broad historical boundary | source-provenance documentation only | no edition, theorem, page, assumptions, proof, or errata |
| `已验证` | untrusted inventory metadata | accepted human-source and kernel receipts would be required | no H or M credit |

## Neighbor and variant boundary

Different standard choices are not alternate spellings of one claim. A holomorphic self-map of a
plane domain differs from a rational map of the Riemann sphere; an iterate-regularity lemma differs
from a periodic-point theorem; and neither selects a Julia/Fatou normal-family result. Entire and
meromorphic dynamics must address escape and poles, while polynomial and rational dynamics introduce
degree, critical points, infinity, and parameter-space choices.

The separately cataloged Julia, Fatou, Mandelbrot, Douady-Hubbard, Yoccoz, Brjuno, and Sullivan
entries are affirmative evidence that those named roots cannot silently stand for this broad field
label. No reviewed repository source chooses another canonical root.

## Source gate

Before this target can leave `H5`, an accountable owner must approve a corrected truth-valued root,
preserve and hash an immutable primary or authoritative source, identify an exact theorem and every
incorporated definition, transcribe all ordered binders, hypotheses, conclusion, and exceptional
cases, inspect corrections and errata, and justify why that proposition represents `THM-M-1427`
rather than a neighboring target. A second qualified reviewer must approve the source-to-statement
mapping.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded source-name
search found no named Julia-set, Mandelbrot-set, complex-dynamics, complex-dynamical-system,
rational-dynamics, or holomorphic-dynamics declaration in Lean sources. Matches for "Fatou" were
measure-theoretic Fatou lemmas. A separate file-path inspection found
`Mathlib.AlgebraicGeometry.RationalMap`, which describes rational maps between schemes rather than
analytic self-map iteration. `IntakeProbe.lean` verifies representative APIs for analytic and
meromorphic maps, composition, iteration, fixed points, and periodic points. They are generic
ingredients only, not a complete formal-candidate audit and not evidence for a canonical target.

The canonical module, declaration or expression, elaborated-expression hash, environment
fingerprint, checked transports, and statement mutations remain null. No H0, M0, readable-proof
closure, audit completion, or theorem completion is claimed.
