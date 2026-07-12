# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10432-10437` supplies exactly the title `Julia集`, Gaston Julia,
1918, the gloss `复动力学的排斥集`, importance "high," and status `已验证`. All six lines entered
the repository in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no
bibliography, stable source identifier, formula, definition, theorem statement, or proof.

`Docs/Stage0_Blueprint.md:38834-38859` repeats that gloss and explicitly leaves definitions and
premises, the proof route, dependencies, equivalent forms, axioms, machine status, and artifact
links open. Its generated wording that a closed result is known and requires a leaf audit is
planning metadata, not primary-source or machine evidence. The rev-5.6 manifest carries `已验证`
only as `source_status_untrusted` and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `Julia集` | a set associated with a selected complex dynamical system | exact map, ambient type, topology, iterate and set predicate | object label, not a proposition |
| "complex dynamics" | iteration of a polynomial, rational sphere map, or another analytic/meromorphic map | map type, domain/codomain, degree, analytic/meromorphic data, treatment of infinity and poles | all open |
| "repelling set" | repelling periodic points, their closure, non-normality, instability, or complement of a stable region | periodicity, multiplier/derivative, norm, strict inequality, closure or normal-family predicate | meaning and hypotheses open |
| "set" | definition, equality, inclusion, density, invariance, boundary, topological property, or concrete computation | one exact `Prop` with ordered binders, hypotheses, and conclusion | no truth-valued conclusion supplied |
| Gaston Julia / 1918 | historical attribution and year | pinpoint source provenance only | no edition, stable theorem ID, page, assumptions, proof, or errata |
| `已验证` | untrusted inventory metadata | inspectable human proof and kernel receipt would be required | no H or M credit |

## Bibliographic discovery boundary

A historical work matching the attribution is Gaston Julia, *Memoire sur l'iteration des fonctions
rationnelles*, *Journal de mathematiques pures et appliquees*, series 8, volume 1 (1918), pages
47-245. This citation is recorded only as a discovery candidate. No immutable edition was preserved
in this intake, and no exact theorem, incorporated definitions, page-level assumptions, proof
boundary, translation, corrections, or errata were inspected and accepted. It therefore receives
no H credit and does not select the canonical claim.

Standard modern characterizations do not repair the source omission by themselves. Non-normality
of iterates, complementarity with the Fatou set, closure of repelling periodic points, and the
boundary of the filled Julia set have different scopes and prerequisite hypotheses. Their familiar
relationship is precisely material that a source-selected statement and checked transports would
need to establish, not permission to choose one silently.

## Neighbor and variant boundary

The repository separately catalogs complex dynamical systems, Fatou sets, Mandelbrot sets,
Douady-Hubbard, Yoccoz, Sullivan no wandering domains, and McMullen. This separation is affirmative
evidence that none of those nearby objects or theorems may replace the Julia-set target merely
because it is convenient to formalize.

## Source gate

Before an approved correction can leave `H5`, an accountable reviewer must preserve and hash an
immutable primary source, select one exact theorem or definition-plus-theorem and edition/page/
section, transcribe every incorporated definition, ordered binder, hypothesis, conclusion, and
exceptional case, inspect its proof dependencies and corrections or errata, and justify why that
proposition represents `THM-M-1428` rather than a neighboring target. A second qualified reviewer
must approve the source-to-canonical-statement mapping.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded source-name
search found no occurrence of `Julia`, `Mandelbrot`, or the queried complex/rational/holomorphic
dynamics phrases in Lean sources. Pinned APIs do include `AnalyticAt`, `Function.iterate`,
`Function.IsPeriodicPt`, `Function.periodicPts`, `closure`, and `frontier`. These are discovery
facts only, not a complete formal-candidate audit and not evidence for a canonical target.

The canonical module, expression, expression hash, checked transports, and statement mutations
remain null. No H0, M0, readable-proof closure, audit completion, or theorem completion is claimed.
