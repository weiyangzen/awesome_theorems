# THM-M-1108 rev-5.6 intake

This directory began as the fail-closed `planned` intake for the Baik-Deift-Johansson theorem.
The statement phase has now selected Theorem 1.1 of arXiv:math/9810105v2 and elaborated its exact
target in `Statement.lean`; `statement.json` records the source pin and environment fingerprint.

The intended theorem family is the Tracy-Widom limit law for the length of the longest increasing
subsequence of a uniformly random permutation as its size tends to infinity. The model, centering,
scaling, limiting distribution, and convergence convention are now frozen. Independent
source-fidelity review, proof state, audit completion, and theorem completion are not claimed.

`scope-map.md` records the proposition-shaping choices,
`source-statement-crosswalk.md` separates discovery anchors from accepted evidence, and
`task-dag.json` remains the intake-era open-task snapshot pending master reconciliation. Intake
validation is recorded in `validation.md`, and statement validation in `statement-validation.md`.
