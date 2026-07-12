# THM-M-1108 rev-5.6 intake

This directory is the fail-closed `planned` intake for the Baik-Deift-Johansson theorem. The
repository record fixes only the authors, the year 1999, and the phrase "distribution of the
longest increasing subsequence". It does not state the random-permutation model, centering,
scaling, limiting distribution, or convergence convention.

The intended theorem family is the Tracy-Widom limit law for the length of the longest increasing
subsequence of a uniformly random permutation as its size tends to infinity. The exact
primary-source statement and conventions remain open for the statement phase. The provisional
root vector is `[H2, M4, R4]`; no exact Lean target, source-fidelity review, proof state, audit
completion, or theorem completion is claimed.

`scope-map.md` records the proposition-shaping choices,
`source-statement-crosswalk.md` separates discovery anchors from accepted evidence, and
`task-dag.json` keeps every downstream phase open. Intake validation is recorded in
`validation.md`.
