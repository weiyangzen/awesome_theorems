# THM-M-0082 rev-5.6 intake

This directory is the `planned` intake for the adjoint functor theorem. The included claim is
Freyd's general right adjoint functor theorem: a functor into a locally small category is a right
adjoint when its domain is complete, it preserves the relevant limits, and it satisfies the
solution-set condition. The precise universe and smallness formulation remains a statement-phase
obligation.

The legacy Lean module is discovery input only. Although it contains wrappers around mathlib's
general and special adjoint functor theorems, rev-5.6 gives them no inherited statement or proof
credit. The provisional root vector is `[H2, M4, R4]`; no exact canonical Lean target, accepted
proof state, audit completion, or theorem completion is claimed.

The scope map, source crosswalk, and open task DAG record the downstream boundary. Intake validation
and exact results are in `validation.md`.
