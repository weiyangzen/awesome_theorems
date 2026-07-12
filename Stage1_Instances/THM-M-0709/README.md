# THM-M-0709 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the undecidability of Post's
correspondence problem (PCP). The repository's `已验证` label is untrusted discovery metadata and
provides neither human-source nor machine-proof credit.

The intended mathematical root is the uniform decision problem: finite PCP instances over a fixed
finite alphabet are effectively encoded, and no total computable Boolean predicate decides whether
an arbitrary encoded instance has a nonempty matching index sequence. A PCP match uses the same
index sequence on the upper and lower word lists. This excludes the decidability of one fixed
instance and the modified PCP variant unless a checked reduction is supplied.

The intake freezes this scope while leaving the exact encoding, alphabet convention, malformed-code
policy, and Lean binder order to the statement phase. `IntakeProbe.lean` checks that a direct
finite-instance/match definition and mathlib's `ComputablePred` API elaborate in the pinned
environment. It is an encoding probe, not the canonical target and not a proof.

Lifecycle is `planned`; provisional root debt is `[H1, M4, R3]`. A credible primary source is
identified but has not received a pinpoint statement/assumption/errata review, no exact Lean target
is frozen, and no reviewed reconstruction exists. All accepted proof state is empty. Exact commands
and boundaries are recorded in `validation.md`.

