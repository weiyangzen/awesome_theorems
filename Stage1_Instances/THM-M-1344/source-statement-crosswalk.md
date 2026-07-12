# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9803-9808` supplies exactly the title `李雅普诺夫间接法`,
Aleksandr Lyapunov, 1892, the gloss `线性化稳定性`, importance "high," and status `已验证`. Git
provenance places all six uncited lines in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The entry contains no source title, theorem/page,
equation, definition, binder, hypothesis, conclusion, proof boundary, erratum, or formal artifact.

`Docs/Stage0_Blueprint.md:36561-36586` repeats those fields while explicitly leaving the formal
system, logical foundation, exact definitions and premises, proof route, dependencies, equivalent
statements, axioms, machine status, and artifact links open. Its generic planning claim that a
closed result is known is not source evidence. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `李雅普诺夫间接法` | infer nonlinear local behavior from a linearization | source-selected nonlinear system, linearization, and transfer theorem | recognizable family; root not selected |
| `线性化` | derivative/Jacobian at an equilibrium, or an infinite-dimensional generator/semigroup derivative | `HasFDerivAt`/`fderiv`, matrix or continuous-linear-map representation, exact spectrum encoding | phase space and operator model absent |
| `稳定性` | Lyapunov, asymptotic, exponential stability, or instability | exact epsilon-delta or exponential predicate and forward-time solution quantifiers | strength and direction absent |
| Aleksandr Lyapunov / 1892 | historical attribution | immutable edition/translation, theorem/page, definitions, genealogy, errata | no pinpoint source |
| `已验证` | untrusted inventory status | accepted source review and kernel receipt would be required | no H or M credit |

The gloss does not say whether the target is the negative-spectrum stability implication, the
positive-spectrum instability implication, both implications, or a weaker conclusion. It also does
not choose the treatment of critical spectrum. These cannot be silently collapsed into one Lean
target.

## Inspected discovery source

Rasha Al Jamal, Amenda Chow, and Kirsten Morris, *Linearized stability analysis of nonlinear
partial differential equations*, arXiv:`1509.05792v1` (2015), is a stable secondary discovery
source. The complete six-page arXiv PDF inspected during intake had SHA-256
`8d4a57ebaaef66c46cc5d0c7b0adc9de043c80ba01ddd48b53e439ef24a7e2c6`.

Its Theorem 3.1 states two separate finite-dimensional conclusions for `z' = F(z)` at an
equilibrium `z_e`: if every spectral value of the derivative has negative real part, the
equilibrium is exponentially stable; if some spectral value has positive real part, it is
unstable. The surrounding paper contrasts this with Banach-space semigroup versions requiring
additional differentiability and well-posedness assumptions, and its conclusion notes that mere
asymptotic stability of the linearized system need not decide the nonlinear problem.

This source is useful because it exposes the choices hidden by the catalog gloss. It is not the
catalog's cited source, a primary historical proof, or H0 evidence. Its own citations and proof
references, the 1892 source or an approved translation, exact theorem ancestry, corrections, and an
independent source review remain open.

## Candidate source-to-Lean components

| Candidate component | Prospective pinned Lean surface | Intake assessment |
|---|---|---|
| nonlinear trajectory solving `z' = F(z)` | `IsIntegralCurve` or an exact `HasDerivAt` predicate | solution model not selected |
| local existence and uniqueness | `IsPicardLindelof` and `ODE_solution_unique_univ` as adjacent APIs | hypotheses do not yet match a source target |
| equilibrium `F z_e = 0` | an explicit equation and constant integral-curve bridge | equilibrium scope and domain absent |
| derivative `DF(z_e)` | `HasFDerivAt` or `fderiv` | finite-dimensional coordinates versus Banach space open |
| spectral sign | `spectrum` and, in finite dimension, `Module.End.hasEigenvalue_iff_mem_spectrum` | real/complex scalar transport and sign predicate open |
| local exponential stability | source-defined constants and all nearby solutions for forward time | no pinned ODE stability predicate or terminal theorem located |
| instability | negation of the source's stability predicate with a positive-spectrum witness | whether this branch belongs to the root is open |

The API probe authenticates names and types only. No candidate is a canonical statement, checked
transport, proof body, or M0 result.

## Source gate

Before the target can leave `H1`, an accountable reviewer must select one immutable proposition and
edition, record exact theorem/page and every referenced definition, transcribe all ordered binders,
hypotheses and conclusions, audit translation and errata, decide whether both spectral directions
belong to the root, classify critical spectrum, and justify the boundaries against the neighboring
targets. A second qualified reviewer must approve the mapping. The selected claim's H status must
then be classified afresh; it cannot inherit `已验证`.

## Lean discovery boundary

At the pinned mathlib revision, the discovery-only `IntakeProbe.lean` elaborates ODE solution,
local-existence, uniqueness, derivative, spectrum, and finite-dimensional eigenvalue APIs. A
bounded name search over repo-local Lean and pinned mathlib found no target-specific indirect-method
or nonlinear ODE stability theorem. This is not an exhaustive anchor audit or a global absence
claim. The canonical module, expression, expression hash, environment fingerprint, checked
alternate encodings, and mutation fixtures remain null.
