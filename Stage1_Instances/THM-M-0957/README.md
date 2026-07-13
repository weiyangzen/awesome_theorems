# THM-M-0957 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Behrend's construction. The
repository supplies only the gloss "large sets without three-term arithmetic progressions,"
attributes it to Felix Behrend in 1946, and labels it verified. Under rev-5.6 that label is
untrusted inventory metadata, not source or proof evidence.

The original two-page paper was inspected through NLM/PMC scans. It defines `v(N)` as the maximum
cardinality of a subset of the nonnegative integers at most `N` containing no three distinct terms
`A, A', A''` with `A + A' = 2 A''`. For every positive epsilon and sufficiently large `N`, it
derives

`v(N) > N^(1 - (2 * sqrt (2 * log 2) + epsilon) / sqrt (log N))`.

This is a strong primary-source lead, but not an accepted `H0` packet: the remote scan was not
admitted as an immutable repository artifact, the formula has not received independent
transcription review, and no correction or errata audit is recorded. The paper's inclusive
`{0, ..., N}` convention also differs from mathlib's `Finset.range N` convention.

Pinned mathlib contains the proof-bearing module
`Mathlib.Combinatorics.Additive.AP.Three.Behrend`. `IntakeProbe.lean` checks its 3AP predicate,
extremal-set specification, construction lemmas, and terminal bound
`Behrend.roth_lower_bound`. The terminal declaration gives an explicit all-`N` lower bound for
`rothNumberNat N`, but intake does not claim exact statement identity, audit its terminal body or
axioms, or promote it to `M0-W`.

The provisional vector is `[H1, M3, R3]`: a matching human proof source and its exact displayed
claim are identified but not independently admitted; a highly relevant pinned formal statement and
proof-bearing module are located but not source-matched or audited; and the scope is explained but
no node-by-node readable proof reconstruction exists. `instance.json` is the structured scope
authority, while `task-dag.json` keeps all six downstream phases open. No canonical Lean target,
H0, M0, R0, accepted execution state, audit completion, theorem completion, or master acceptance is
claimed.
