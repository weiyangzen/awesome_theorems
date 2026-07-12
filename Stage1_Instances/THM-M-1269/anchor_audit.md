# Lean anchor audit

The preferred candidate is mathlib's `exists_seq_tendsto_sInf`, pinned at
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` in
`Mathlib.Topology.Order.IsLUB`. Its source declaration is stronger than the
target: for every nonempty bounded-below set in a conditionally complete
linear order with the stated topology, it produces an antitone sequence in
the set converging to the set's infimum.

For `S = Set.range F`, `Set.range_nonempty F` supplies nonemptiness once the
domain is nonempty. Each value selected by the anchor has an `F`-preimage;
choosing those preimages gives the required sequence in `X`. The pointwise
preimage equalities transport the convergence result. `AnchorAudit.lean`
checks this wrapper against the exact statement-phase proposition. Lean's
axiom report for the anchor is `[propext, Classical.choice, Quot.sound]`.
The choice dependency agrees with the intake foundation profile; no unsafe or
oracle boundary was observed.

## Candidate inventory

| Candidate | Immutable revision | Result |
|---|---|---|
| mathlib `exists_seq_tendsto_sInf` | `8a178386ffc0f5fef0b77738bb5449d50efeea95` | Selected; stronger anchor and wrapper elaborates |
| Repo-local Lean declarations | base `4197281122e0165098f43f0b967905d0378ee2db` | No exact theorem; one descriptive workflow-text hit only |
| Pinned external packages | revisions in `lake-manifest.json`, including flt-regular `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` | No independent exact closure |
| Public external Lean code search | query run 2026-07-12 | Inconclusive: grep.app HTTP 429; GitHub API HTTP 403 |

The external search failures are recorded rather than repaired by fetching a
moving dependency. They do not block this node because the exhaustive local
and already-pinned search found a directly usable immutable mathlib anchor.
They also receive no proof credit.

## Classification boundary

The audit supports `M1`: a pinned closure candidate and exact-shape checked
wrapper exist, but the proof phase has not installed a canonical theorem, and
the obligation-tree, validation, release, and master-acceptance gates remain
open. Human status remains `H2` because no primary mathematical source has
been pinned. Readability remains `R3`. The theorem is not complete.

Exact commands and results are appended to `validation.md`; structured
candidate provenance is in `anchor_audit.json`.
