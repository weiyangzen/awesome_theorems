# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10167-10172` supplies exactly the title `Runge-Kutta方法`, the
attribution Carl Runge/Martin Kutta, the year 1895, the gloss `ODE的数值积分`, importance "high,"
and status `已验证`. Git provenance places all six uncited lines in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no equation, scheme, source,
definition, binder, hypothesis, conclusion, proof, correction, or formal artifact.

`Docs/Stage0_Blueprint.md:37965-37990` repeats those fields while explicitly leaving the formal
system, logical foundation, background, exact definitions and premises, proof route, dependencies,
equivalent formulations, axioms, machine status, and artifact links open. Its generic planning
text about a known closed result is not source evidence. The rev-5.6 manifest retains `已验证` only
as `source_status_untrusted` and resets this target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| Runge-Kutta method | a family of one-step, multistage numerical schemes | exact tableau, stages, update map, and well-definedness predicate | method not selected |
| ODE | autonomous or nonautonomous initial-value problem | time/state carriers, vector field, domain, initial data, solution predicate | all open |
| numerical integration | computation of approximate states along a grid | step/grid model and exact or floating-point arithmetic semantics | all open |
| implied accuracy | consistency, order, local error, global convergence, or error bound | exact norm inequality, quantifiers, constants, horizon, and limit regime | no conclusion supplied |
| Carl Runge/Martin Kutta, 1895 | historical locator | immutable edition, exact proposition/page, definitions, translation, errata, genealogy | incomplete and internally broad |
| `已验证` | untrusted inventory status | reviewed human-source packet or kernel receipt would be required | no H or M credit |

The wording does not say whether the root is a definition, construction, accuracy theorem,
convergence theorem, order-condition characterization, or stability result. Combining these into a
single convenient proposition would broaden the source rather than clarify it.

## Historical and modern source leads

Carl Runge, *Ueber die numerische Aufloesung von Differentialgleichungen*, Mathematische Annalen
46(2), June 1895, pages 167-178, DOI `10.1007/BF01446807`, is a plausible primary historical lead.
Crossref confirms the author, title, journal, volume, issue, date, pages, and DOI. The Goettingen
Digitisation Centre issue scan was inspected under work ID `PPN235181684_0046` and issue log ID
`LOG_0018`; its metadata identifies Mathematische Annalen, Leipzig, 1895. This corroborates the
Runge/1895 catalog fields, but the scan is an entire issue, the article's mathematical text was not
transcribed and crosswalked, and the repository does not cite it or select one result from it.

Martin Kutta, *Beitrag zur naeherungsweisen Integration totaler Differentialgleichungen*,
Zeitschrift fuer Mathematik und Physik 46 (1901), pages 435-453, is a bibliographic historical
lead. J. C. Butcher, *Numerical Methods for Ordinary Differential Equations*, third edition,
Wiley, 2016, DOI `10.1002/9781119121534`, is an authoritative modern source-family lead. Neither
was inspected to an exact theorem/page in this intake. Their titles and metadata cannot select a
canonical proposition or establish `H0`.

The date field itself needs review: the catalog combines Runge and Kutta with 1895, while the
identified Kutta publication is from 1901. The discrepancy is provenance evidence that the
catalog describes a family rather than one fully identified source theorem.

## Source gate

Before the target can leave `H5`, accountable source reviewers must select one immutable
truth-valued proposition; pin its exact edition, theorem/section/page, translation, incorporated
definitions, proof boundary, and corrections; transcribe all ordered binders, assumptions,
conclusions, constant dependencies, and exceptional cases; reconcile the Runge/Kutta/date
genealogy; and explain why the selected result is `THM-M-1396` rather than the separately cataloged
Runge-Kutta stability or neighboring numerical-method targets. A second qualified reviewer must
approve the mapping. The selected proposition's H status must then be classified afresh.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks integral-curve, Picard-iteration, local-existence, Gronwall, and approximate-trajectory
interfaces. A bounded case-insensitive search over repo-local and pinned mathlib Lean sources found
no named Runge-Kutta/Kutta/RK-method or numerical-ODE-integrator declaration under the recorded
terms. This is not the required immutable external anchor audit and does not prove global absence.

The canonical module, declaration/expression, elaborated-expression hash, environment fingerprint,
checked transports, and statement mutations remain null. Adjacent APIs and a no-match name search
provide intake feasibility evidence only, not an exact statement, H0, M0, or proof credit.
