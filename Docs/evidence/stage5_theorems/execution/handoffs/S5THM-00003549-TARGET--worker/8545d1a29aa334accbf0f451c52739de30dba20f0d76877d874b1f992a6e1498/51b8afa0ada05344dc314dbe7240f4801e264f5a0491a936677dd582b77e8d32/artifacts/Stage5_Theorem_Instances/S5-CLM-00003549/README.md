# S5-CLM-00003549 — Erdős Problem 1, least five-element ambient value

This package independently closes the frozen `Erdos1.erdos_1.variants.least_N_5` statement.
The claim-owned root uses the explicit witness `{3, 6, 11, 12, 13}`, an exhaustive finite
exclusion through twelve, and interval monotonicity. `Statement.lean`, `Proof.lean`, and
`Audit.lean` each import the exact pinned provider module and actively reference the frozen
qualified declaration.

The previous harvested checkpoint reached Master elaboration, where final `whnf` checking of the
finite decision exceeded the default command heartbeat budget. This generation rematerializes
that proof and applies `maxHeartbeats 0` and `maxRecDepth 100000` at file scope in both proof
replays, covering declaration finalization as well as tactic construction. These are reduction
resource settings, not axioms, oracles, or changes to the target proposition.

Worker validation is the prescribed semantic-only `--no-lean` preflight. Provider-native
trust-zero compilation and final theorem acceptance remain exclusively with Master. Anchor
digests in `anchor-audit.json` address the complete UTF-8 bytes of their named files; readable
fragment digests use the byte convention stated in `proof-outline.md`.
