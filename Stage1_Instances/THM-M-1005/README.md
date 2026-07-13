# THM-M-1005 rev-5.6 intake

This directory is the `planned` intake for Doob's maximal inequalities. It freezes the intended
theorem family as maximal estimates for a discrete-time submartingale or martingale, while leaving
the exact variant, source theorem, index convention, and formal statement to the statement phase.

The Stage0 phrase "moment estimate for a martingale maximum" and its untrusted "verified" label
are discovery input only. They neither select among the weak `L1`, `Lp`, and related variants nor
provide proof credit. The provisional root vector is `[H2, M4, R4]`; no canonical Lean target,
audit completion, or theorem completion is claimed.

The scope map, source-statement crosswalk, and open task DAG define the downstream work. Intake
validation and its exact limits are recorded in `validation.md`.

The rev-5.6 statement and bounded anchor audit now select and elaborate the strong finite-horizon
`L^p` target. The obligation-tree phase freezes its 14 canonical obligations and seven typed graphs
in `obligation-registry.json`, `typed-graphs.json`, and `obligation-tree.md`. The exact root remains
open at `M3`; the minimal open cut is the strong analytic estimate, not the checked weak mathlib
anchor.

The proof phase now vendors the complete real-valued analytic proof from immutable, unmerged
mathlib PR `#39349` at commit `4b63335c679c15aab74a00d37714d41aa99d701d`, preserving its
Apache-2.0 attribution. `Proof.lean` applies that theorem to `|f|`, transports `p.toReal` back to
the exact finite `ENNReal` exponent, and checks the result through the frozen root composer. This
is provisional worker evidence only: master acceptance, validation, release, source/readability
review, and theorem completion remain downstream.

The release phase now records a self-tested negative reconciliation in `release-decision.json` and
`release-receipt.json`. Fresh network-isolated warm-cache replay corroborates the exact root, but the
validation dependency is unaccepted and its receipt is stale after a runner-input change,
authoritative `M4/M3` state conflicts, `AUDIT-Z` is open, and the cold/offline, trust, source,
readability, independent-verifier, and deterministic-bundle gates are missing. The exact verdict is
therefore `blocked`; lifecycle remains `planned`, the accepted vector remains `[H2, M4, R4]`, and
`theorem_complete=false`.
