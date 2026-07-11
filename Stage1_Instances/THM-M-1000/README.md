# THM-M-1000 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the source label "transportation inequality."
The repository supplies only the Chinese description `最优传输的集中` (concentration of optimal
transport), with no formula, author, hypotheses, or bibliographic anchor. That wording does not
identify one theorem: at minimum it is compatible with Talagrand's Gaussian quadratic
transportation-cost inequality and with Marton's transportation/concentration results. Selecting
either would broaden or substitute the source rather than transcribe it.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Source identity | The exact theorem meant by `最优传输的集中` | Blocked until an authoritative formula or pinpoint source selects a theorem |
| Candidate family | Transportation-cost inequalities relating Wasserstein cost, entropy, and concentration | Candidate discovery only; no member is canonical |
| Mathematical objects | Probability measures, couplings, transport cost/Wasserstein distance, relative entropy | Spaces, measurability, moments, constants, and absolute continuity remain unknown |
| Lean statement | A future exact Lean 4 proposition matching the selected source | No module, declaration, expression, or transport is credited |
| Proof architecture | Definitions, coupling/duality or entropy reduction, tensorization/concentration branch | Deferred until the root statement is identified |
| Foundations | Lean 4 kernel with versioned mathlib and an accepted foundation/TCB profile | Exact toolchain and dependency closure remain open |

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H4, M4, R4]`. The first failed gate is source
statement identification. The retry condition is an authoritative source containing the exact
formula, domains, quantifiers, assumptions, conclusion, and constant normalization. Only then may
the statement phase select a candidate and elaborate it. The theorem is not complete.

Validation establishes target membership, repository-standard consistency, JSON syntax, and local
artifact hygiene only. Exact commands and results are recorded in `validation.md`.
