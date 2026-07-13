# THM-M-0484 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `卢卡斯-莱默检验` (the
Lucas-Lehmer test). The repository supplies only the gloss `梅森素数的快速检验` ("a fast test
for Mersenne primes"), attributes it to Edouard Lucas and Derrick Lehmer in 1930, and marks it
`已验证`. Those fields identify a standard theorem family, but the verified label is untrusted
metadata and the adjective "fast" is not itself a truth-valued correctness theorem.

## Intake result

An inspected modern mathematical source lead states the conventional criterion: for an odd prime
`p`, set `M_p = 2^p - 1`, start the Lucas-Lehmer recurrence at `4`, and repeatedly square and
subtract `2`; then `M_p` is prime exactly when the term after `p - 2` updates is zero modulo
`M_p`. The source uses one-based recurrence indices, while pinned mathlib uses a zero-based
sequence and the hypothesis `3 <= p`. The two formulations appear to match after an index and
domain transport, but the catalog cites no source and no primary edition, complete proof/errata
audit, checked transport, or independent review is accepted. The candidate scope is therefore
frozen without pretending that source fidelity is closed.

Pinned mathlib contains exact-topic definitions and both correctness directions. `IntakeProbe.lean`
authenticates those interfaces and composes them into the candidate iff under `3 <= p`. It also
kernel-checks the essential low-index boundary: the test is false at `p = 2` although `2^2 - 1`
is prime. This is real intake discovery evidence for an `M3` candidate, not an exact statement
fingerprint, terminal-body audit, or accepted `M0-W` proof receipt.

The provisional vector is `[H1, M3, R4]`. `instance.json` is the structured scope authority and
`task-dag.json` leaves all six downstream phases open. No canonical Lean declaration, H0, M0, R0,
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
