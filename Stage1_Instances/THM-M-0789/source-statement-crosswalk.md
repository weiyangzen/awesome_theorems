# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` gives the title `可测基数定理`, attributes it to Stanislaw Ulam,
dates it to 1930, and gives only `可测基数与超滤子` ("measurable cardinals and ultrafilters").
Stage0 repeats that gloss while marking exact definitions, assumptions, proof history, axioms, and
formal artifacts as open. The rev-5.6 manifest retains `已验证` only as untrusted source metadata.

No primary-source edition, theorem/page, exact proposition, assumptions, errata, or proof is
identified. The historical fields do not distinguish Ulam's inaccessibility result from a modern
ultrafilter characterization or an existence axiom.

## Candidate source work

The anchor audit must inspect an immutable primary text or an authoritative modern set-theory
reference, record its exact definition/theorem number and page, foundation, completeness and
nonprincipality conventions, proof boundary, and errata, then obtain independent review. Intake
does not assign an exact theorem to Ulam without that evidence.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "cardinal" | an uncountable cardinal kappa and a carrier of size kappa | `Cardinal`, `Cardinal.mk` | pinned API probed; exact domain open |
| "ultrafilter" | ultrafilter on kappa (or an equipotent type) | `Ultrafilter` and its coercion to `Filter` | pinned API probed |
| "measurable" | nonprincipal/uniform kappa-complete ultrafilter | `CardinalInterFilter`, plus a source-faithful nonprincipality predicate | candidate only |
| "measurable" | nontrivial kappa-additive zero-one measure | measure encoding and a checked transport to filters | candidate only; not probed |
| "theorem" | characterization, existence, or large-cardinal consequence | one concrete proposition with ordered binders and hypotheses | absent from source record |
| `已验证` | untrusted inventory label | no Lean target or proof credit | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe imports
the ultrafilter, cardinal-intersection, and regular-cardinal APIs. These are encoding ingredients,
not an identified measurable-cardinal theorem. A bounded name search found no declaration named
for measurable cardinals; that negative search is not a substitute for the later anchor audit.
