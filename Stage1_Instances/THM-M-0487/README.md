# THM-M-0487 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0487`, the weak (ternary)
Goldbach theorem. The frozen human claim is: every odd integer greater than five is a sum of three
primes, with repetition permitted. Intake does not freeze or claim an accepted Lean expression.

An immutable source lead was inspected: Harald A. Helfgott, *The ternary Goldbach conjecture is
true*, arXiv:1312.7748v2. Its unnumbered Main Theorem says exactly that every odd integer greater
than five is a sum of three primes. The proof combines an analytic result above `10^27` with a
separate finite verification. Source admission, the full dependency and computation crosswalk,
errata review, and independent review remain open, so this is `H1`, not `H0`.

The intended Lean family quantifies natural `n`, requires `5 < n` and `Odd n`, and asks for three
natural prime witnesses whose sum is `n`. The statement phase must freeze that target, check the
integer-to-natural transport, and mutation-test all boundaries. In particular, repeated summands
must remain possible: the first included input is `7 = 2 + 2 + 3`. The merely eventual theorem
owned by `THM-M-0508` is weaker and cannot substitute for this target.

`IntakeProbe.lean` authenticates pinned prime, parity, and boundary APIs only. It declares no target
and proves no part of weak Goldbach. `instance.json` is the scope authority, `scope-map.md` and
`source-statement-crosswalk.md` record the exact boundaries, and `task-dag.json` leaves all six
downstream phases open.

Status boundary: self-tested planned intake proposal pending integration-lane acceptance. The
provisional root vector is `[H1, M4, R3]`; no canonical Lean expression, H0, M0, R0, accepted proof
state, audit completion, or theorem completion is claimed.
