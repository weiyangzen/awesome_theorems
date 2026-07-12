# THM-M-1096 rev-5.6 intake

This directory is the `planned` intake for the Khasminskii ergodicity theorem. The repository's
only statement text is "ergodicity of diffusion processes." That phrase does not determine one
proposition: positive/null recurrence, the invariant measure, observable class, convergence mode,
and initial-state quantifiers all materially change the claim.

The intake therefore freezes the intended theorem family without choosing those details. It also
identifies Khasminskii's 1960 primary article by stable bibliographic metadata. The article's exact
theorem statement has not been inspected and is not represented as if it had been. The provisional
root vector is `[H1, M4, R4]`. There is no accepted proof state, canonical Lean expression, audit
completion, or theorem completion.

`scope-map.md` records the decisions the statement phase must make;
`source-statement-crosswalk.md` prevents the short repository label from silently becoming a
broader or easier theorem; and `task-dag.json` leaves every downstream rev-5.6 phase open.
