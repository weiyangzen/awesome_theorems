# Source-statement crosswalk

## Repository metadata

`Docs/Stage0_Blueprint.md` is a secondary intake source. Its literal mathematical gloss is
"扩散过程的遍历性" (ergodicity of diffusion processes). It gives 1960 and Rafail Khasminskii but
leaves exact definitions and assumptions open. The rev-5.6 manifest repeats the theorem name and
marks the inherited source status as explicitly untrusted.

## Identified primary-source candidate

R. Z. Khas'minskii, "Ergodic Properties of Recurrent Diffusion Processes and Stabilization of the
Solution to the Cauchy Problem for Parabolic Equations," *Theory of Probability & Its Applications*
5(2) (1960), 179-196, DOI `10.1137/1105016`.

The title, author, journal, volume, issue, year, pages, and DOI were checked against the Crossref
publisher deposit during intake. The paper text, numbered theorem, definitions, original-language
version, and errata were not inspected. Consequently this citation is an `H1` discovery anchor,
not the edition/theorem/page/assumption crosswalk required for `H0`.

## Crosswalk

| Repository phrase | Candidate-source component | Required Lean component | Intake status |
|---|---|---|---|
| Khasminskii | R. Z. Khas'minskii | provenance only | author and DOI metadata identified |
| 1960 | volume 5, issue 2 (1960) | immutable source revision | bibliographic year identified; edition open |
| diffusion process | "recurrent diffusion processes" in article title | concrete continuous-time diffusion/Markov model | included family; definitions open |
| ergodicity | "ergodic properties" in article title | exact invariant-measure/time-limit proposition | conclusion and convergence mode open |
| no stated hypotheses | theorem text not yet inspected | ordered binders and all hypotheses | hard statement blocker |
| no stated boundary cases | recurrence/measure cases not yet inspected | explicit finite/null recurrence and degeneracies | hard statement blocker |

## Formal-source boundary

A scoped search of the pinned mathlib source found general invariant-measure and ergodic-theory
infrastructure, including `ProbabilityTheory.Kernel.Invariant`, but no occurrence of Khasminskii's
name or an identified recurrent-diffusion terminal theorem. This is search evidence only: it neither
proves absence under the later precommitted anchor-audit protocol nor credits a generic ergodic
theorem as the source result.

Before `H0`, an independent reviewer must inspect a stable primary-source edition, record the exact
theorem and page, definitions and every premise, translation differences and errata, and approve a
row-by-row mapping to the elaborated Lean target. Before any `M0` claim, the exact Lean expression
and terminal body must separately pass the rev-5.6 kernel, provenance, trust, and composition gates.
