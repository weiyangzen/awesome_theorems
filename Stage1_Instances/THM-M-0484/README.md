# THM-M-0484 rev-5.6 dossier

This directory is the fail-closed `planned` dossier for `卢卡斯-莱默检验` (the
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
is prime. This is real intake discovery evidence for an `M3` candidate, not a terminal-body audit
or accepted `M0-W` proof receipt. The separate statement artifacts now supply the exact fingerprint.

The statement phase now freezes the sharper intake-selected target for every natural `p` with
`3 <= p`: `LucasLehmerTest p` if and only if `mersenne p` is prime. `Statement.lean` elaborates
that exact target with the sole exact-topic import, checks its `ZMod` and integer-residue forms, and
rejects four structural mutations. It also kernel-checks why weakening the lower bound to include
`p = 2` is false. The conventional odd-prime, one-based human-source form is deliberately not
credited until its source, domain, and index transports are independently reviewed.

The provisional vector remains `[H1, M3, R4]`. `instance.json` is the structured scope authority
and `task-dag.json` leaves all six downstream phases open pending master acceptance. The statement
node proposes `[_]`; no H0, M0, R0, accepted execution state, audit completion, theorem completion,
or master acceptance is claimed.

## Obligation-tree result

Registry version 1 freezes 36 obligations and seven separate typed graphs. The proof architecture
splits the exact root into forward and reverse correctness terminals, then maps the visible pinned
source body through the order, least-factor, quadratic-extension, recurrence, closed-form, and
Legendre-symbol dependencies. `ObligationTree.lean` checks ten exact conditional composition
interfaces. Seventeen additional source-body relationships remain explicit unverified decomposition
plans rather than machine-closure certificates. The frozen denominator and accepted state are not
changed by later proof work.

## Proof result

`Proof.lean` installs `lucas_lehmer_sufficiency` and `lucas_lehmer_necessity` from manifest-pinned
mathlib at their exact frozen terminal interfaces. It consumes `root_of_directions` and
`root_of_terminal` to derive the unchanged `LucasLehmerTestTarget`. Trust-zero Lean elaboration
reports both upstream terminals and all four local declarations sorry-free, with exactly `propext`,
`Classical.choice`, and `Quot.sound` in each axiom closure.

This is provisional proof-node evidence for an `M0-W` root proposal. The receipt grants exact
declaration evidence only to the two terminal interfaces, assembly node, and root. It gives no
individual closure credit to the 17 unverified source-body decompositions and accepts no obligation
or receipt. The dossier therefore remains `[H1, M3, R4]`; validation, full provenance and TCB,
primary-source `H0`, readable `R0`, independent replay, release, and theorem completion remain open.
