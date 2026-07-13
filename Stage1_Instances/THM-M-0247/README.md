# THM-M-0247 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Kolmogorov's periodic
conjugate-function weak-type theorem. The repository says only "weak-type estimate for conjugate
functions," attributes it to Andrey Kolmogorov, and dates it to 1925. Those fields identify a
theorem family but are not source, statement, or proof evidence.

The intake inspected A. Kolmogoroff's 1925 paper and identifies Theorem I on printed page 25 as the
leading source-exact root: for a summable periodic function `f`, its almost-everywhere boundary
conjugate `g`, and a threshold `R`, the angular measure of `{theta | |g theta| > R}` times
`R` is bounded by an absolute constant times the `L^1` integral of `f`. This is the periodic weak
`(1,1)` endpoint theorem, not Marcel Riesz's strong `L^p` theorem.

The mathematical source statement is frozen only as an intake candidate pending independent source
review. The primary scan uses angular Lebesgue measure on `[-pi, pi]`; pinned mathlib's convenient
`AddCircle.haarAddCircle` is probability-normalized. The statement phase must check that scaling,
select an exact conjugate-function construction and representative policy, elaborate the target,
and decide how the source's "arbitrary number" threshold maps to the standard meaningful `R > 0`
weak-type domain before mutation-testing it. `IntakeProbe.lean` only authenticates adjacent APIs.

Root vector: `[H1, M4, R4]`. No task state, proof, `H0`, `M0`, `R0`, audit completion, theorem
completion, accepted receipt, or master acceptance is claimed.
