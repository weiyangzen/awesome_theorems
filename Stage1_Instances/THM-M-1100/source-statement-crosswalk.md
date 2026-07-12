# Source-statement crosswalk

## Repository source boundary

`Docs/researches/math_theorems.md` records Nicholas Metropolis, 1953, and only "MCMC methods".
`Docs/Stage0_Blueprint.md` repeats those fields while leaving definitions, hypotheses, proof route,
axioms, and machine artifacts open. The `已验证` field is untrusted intake metadata under rev-5.6.
These records identify a method family and historical anchor, not an exact theorem.

## Candidate primary source

- Nicholas Metropolis, Arianna W. Rosenbluth, Marshall N. Rosenbluth, Augusta H. Teller, and Edward
  Teller, "Equation of State Calculations by Fast Computing Machines", *The Journal of Chemical
  Physics* 21(6), 1087-1092 (1953), DOI `10.1063/1.1699114`.

This is the primary paper candidate matching the repository year and attribution. It presents a
specialized sampling procedure and physical calculations rather than a numbered, general theorem
named "Markov chain Monte Carlo". The exact pages/equations, assumptions, correction history, and
any mathematical correctness argument have not been independently inspected in this intake, so the
citation is discovery evidence only and does not establish `H0`.

The later Hastings generalization is deliberately not adopted here: the repository assigns
Metropolis-Hastings its own target, `THM-M-1101`.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "MCMC methods" | one named sampler and theorem | concrete kernel plus exact `Prop` | ambiguous family; open |
| Markov chain | transition rule on a state space | `ProbabilityTheory.Kernel` and `IsMarkovKernel` or an exact alternative | substrate checked; target open |
| Monte Carlo sampling | samples or empirical averages | path law, iterates, estimator, and measurability | conclusion open |
| target distribution | canonical-ensemble law in the 1953 setting | probability measure or normalized density | conventions open |
| Metropolis acceptance | symmetric-proposal acceptance/rejection rule | measurable proposal and accepted/rejected kernel | formula and edge cases open |
| correctness | invariance, detailed balance, convergence, or estimator theorem | one source-matched proposition | not selected |
| `已验证` | screening label | accepted source review or kernel receipt | no credit |

## Required source and formal audit

Before `H0`, an independent reviewer must inspect an immutable copy or stable edition, identify the
exact result being claimed, map every equation and assumption, check errata/corrections, and approve
a row-by-row source-to-Lean crosswalk. If the 1953 source has no theorem matching a viable canonical
claim, the target must remain `H5` until an authorized correction chooses a stable proposition; a
worker must not invent one.

No repo-local or external Lean theorem is accepted at intake. The later anchor audit must search the
pinned mathlib revision and credible immutable Lean 4 projects and record exact declaration types,
proof bodies, axioms, placeholders, dependency feasibility, and statement transports. The local API
probe is environment evidence only, not a formal-candidate audit.
