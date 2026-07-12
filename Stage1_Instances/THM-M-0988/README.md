# THM-M-0988 rev-5.6 intake

This directory is the `planned` intake for the one-dimensional Lindeberg-Levy central limit
theorem. It freezes the human claim as convergence in distribution of centered, square-root
normalized partial sums of iid real random variables with finite variance to the corresponding
centered Gaussian law.

The legacy Lean module is discovery input only. Although it contains a wrapper around a pinned
mathlib theorem, rev-5.6 requires the later statement, anchor-audit, obligation, proof, validation,
and release nodes to re-establish every claim. The provisional root vector is `[H2, M3, R4]`; this
intake claims neither kernel closure nor theorem completion.

The statement phase now freezes and freshly elaborates
`Stage1Instances.THM_M_0988.StatementShape` in `Statement.lean`, with the pinned
`Mathlib.Probability.CentralLimitTheorem` module as its sole direct import. The target includes the
zero-variance case and retains mathlib's `n = 0` convention. Four separately elaborated mutations
guard the second-moment premise, iid scope, zero-variance boundary, and square-root normalization.

The scope map, source crosswalk, and open task DAG record the exact downstream decisions. Intake
validation remains in `validation.md`; the statement fingerprint, commands, and strict status
boundary are recorded in `statement.json` and `statement-validation.md`. This remains statement-only
evidence and claims neither proof closure nor theorem completion.

The obligation-tree phase now freezes registry version 1 with 18 canonical obligations and seven
separate typed graphs. `ObligationTree.lean` checks only the conditional composition from the exact
pinned bridge to the root; the registry deliberately records no closed obligations. The remaining
root cut set is `M0988-X-PINNED`, reserved for the proof phase. Architecture validation and the
denominator hash are recorded in `obligation-tree-validation.md`; no proof or theorem-completion
credit is claimed here.
