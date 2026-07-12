# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9782-9787` supplies exactly the title `变分方程`
(`variational equation`), attribution to "many mathematicians," a twentieth-century date, the
gloss `解的敏感性方程` (`solution sensitivity equation`), importance "high," and status
`已验证`. Git history places this uncited record in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. It contains no equation, source, definitions,
binders, hypotheses, conclusion, proof boundary, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:36480-36505` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 target manifest retains `已验证` only as
untrusted source metadata and resets the target to `L0 / rework_required`.

The neighboring targets are material boundaries: `THM-M-1339` concerns continuous dependence, and
`THM-M-1340` concerns differentiability with respect to parameters. This intake neither absorbs
those roots nor borrows any future evidence from them.

## Inspected source lead

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, American Mathematical Society, 2012, is an authoritative modern source lead. The
author-hosted preliminary edition was inspected from the official book page. Its relevant passages
distinguish several candidate claims:

- Section 2.4, equation (2.49), page 46: the initial-state derivative of the flow satisfies the
  homogeneous first variational equation, with identity initial condition in equation (2.50).
- Theorem 2.10, pages 46-47: under `C^k`, `k >= 1`, hypotheses, the local solution map is `C^k`, and
  its derivatives satisfy corresponding variational equations.
- Theorem 2.11, pages 47-48: a parameterized vector field yields local `C^k` dependence on time,
  initial time, initial state, and parameter.
- Section 2.5, equation (2.58), page 49: for a scalar perturbation parameter and parameter-independent
  initial data, the parameter derivative satisfies an inhomogeneous first variational equation with
  zero initial condition.

The official errata dated 2026-06-23 was also inspected. Its page-45 correction concerns the proof
of the preceding continuous-dependence result; the bounded search found no listed correction to
pages 46-49, Theorems 2.10-2.11, or equations (2.49) and (2.58). Repeated PDF retrievals were not
byte-stable and some arrived incomplete, so no response digest is treated as an immutable edition.
The source lead is not accepted as `H0`: the repository does not cite it or select one candidate,
the exact edition bytes must be stably preserved at acceptance, and a complete
definition/premise/conclusion/errata crosswalk plus independent review remain open.

## Component crosswalk

| Catalog component | Source-family alternatives | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "solution" | unique local flow near initial data, or a selected individual solution | `IsIntegralCurve`, derivative predicates, or a future solution-map definition | equation, carrier, and domain open |
| "sensitivity" | derivative with respect to initial state, initial time, external parameter, or field | `HasFDerivAt`, `fderiv`, and continuous linear maps | variable and derivative mode open |
| "equation" | homogeneous state variational equation or inhomogeneous parameter sensitivity equation | a linear ODE along the base curve, with or without a forcing term | materially different candidate roots |
| coefficient | state derivative of the vector field evaluated along the base solution | Frechet derivative composed with trajectory evaluation | regularity and operator orientation open |
| initial data | identity operator, arbitrary tangent vector, zero vector, or derivative of parameterized initial data | explicit continuous-linear-map or vector condition | source-dependent and absent from catalog |
| conclusion | derivative satisfies the equation, equation solution equals the derivative, or both with uniqueness | exact derivative and ODE predicates plus checked composition | logical strength open |
| `已验证` | untrusted inventory label | no Lean proposition or proof object | no H or M credit |

## Lean and evidence boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only
probe checks integral-curve, derivative, Frechet chain-rule, continuous-linear-map composition, and
linear-map-application derivative interfaces. A bounded exact-name search over repo-local Lean and
pinned mathlib returned no ODE `variational equation`, `variation equation`, or `sensitivity
equation` declaration. The nearby Picard-Lindelof results establish existence and initial-state
Lipschitz/continuous dependence for a fixed field, not the differentiable sensitivity equation.
These observations are not the later immutable external anchor audit and do not establish global
absence.

Before leaving `H1`, accountable reviewers must select an immutable source proposition, preserve
the exact edition, transcribe every incorporated definition, ordered binder, hypothesis, equation,
initial condition, and conclusion, reconcile the `THM-M-1339`/`THM-M-1340` boundaries, inspect all
relevant errata, and independently approve the mapping. Only then may the statement phase freeze a
minimal Lean import, elaborated expression, checked transports, and the required mutations.
