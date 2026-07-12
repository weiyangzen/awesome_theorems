# THM-M-1070 rev-5.6 statement

This directory is the `planned` intake for the Lévy-process target. The repository's source phrase,
"stationary independent-increment process," is too short to determine an exact proposition. This
intake therefore freezes the intended standard definition package while keeping its convention
choices open: zero initial value, joint independence of increments, stationary increment laws,
stochastic continuity, and the precise role of cadlag paths.

The statement phase selects the exact formal deliverable as the standard predicate for a
real-valued process indexed by nonnegative real time. `Statement.lean` requires measurable random
variables, a probability measure, almost-sure zero initial value, mathlib's joint finite-family
`HasIndepIncrements`, stationary increment laws via `IdentDistrib`, and stochastic continuity via
`TendstoInMeasure`. Cadlag regularity is deliberately not assumed; it belongs to a later
regularization theorem and proof obligation.

The manifest's historical `已验证` label is untrusted metadata and supplies no proof credit. No
proof credit. The exact predicate and its direct expansion elaborate against the pinned toolchain,
but no proof of a regularization or characterization theorem is claimed. The provisional root
vector is `[H1, M3, R4]`; audit and theorem completion are false. The remaining files delimit the
source, scope, downstream task, and validation boundaries.
