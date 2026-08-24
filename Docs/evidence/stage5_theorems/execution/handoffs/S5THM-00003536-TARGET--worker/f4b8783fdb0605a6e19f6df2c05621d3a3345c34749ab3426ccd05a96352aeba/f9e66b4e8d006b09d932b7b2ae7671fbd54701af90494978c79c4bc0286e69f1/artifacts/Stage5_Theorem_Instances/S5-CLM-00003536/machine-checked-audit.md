# Machine-checked audit

Proposed closure level: `M0-L`, trust 0. The exact target expression is bound to the frozen provider declaration type, while the provider body is not imported or referenced. `Statement.lean` contains both directions of the identity transport, `Proof.lean` contains the claim-owned replay surface, and `Audit.lean` contains exact-type and terminal application checks.

The worker gate is intentionally `--no-lean`; it verifies strict JSON, semantic-source bindings, absence of parser or declaration substitution, empty cut sets, readable reconstruction, and provisional release shape. Canonical Master must independently rebuild these files, recompute the elaborated root and transitive environment, inspect the declaration dependency/axiom closure, and replay at trust 0 before acceptance.
