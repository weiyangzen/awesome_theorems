# THM-M-0814 release reconciliation

Item: `S56-M-0814-RELEASE`. Base revision:
`118d66d1986768cd9a00e661ccf6447c26a53efb`.

## Exact verdict

The release verdict is `blocked`. The lifecycle remains `planned`, the accepted root vector remains
`[H1, M3, R4]`, and both `AUDIT-Z` and `THEOREM-Z` are false. This worker accepts no receipt or
obligation and makes no authoritative state change.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`, specifically
`dependency.S56-M-0814-VALIDATION.master_acceptance`. The validation receipt is only provisional
`[_]` worker evidence with `accepted=false` and `release_grade=false`; the target-local validation
task is also still open.

Independently of that dependency failure, the exact theorem is not kernel-closed. The conditional
root declaration still consumes `MaximalFlowAttainment` and `EqualCutForMaximalFlow`. Therefore the
provisional top-spine exact-interface cut remains `M0814-L-MAX-ATTAIN` and
`M0814-T-EQUAL-CUT`, with the attainment node first. This is not the frozen graph's unreconciled
ten-node `proof_leaf_cut_set`, which remains authoritative for its pre-proof snapshot. The exact
weak-duality body and no-chain boundary body are real local progress, but neither supplies a
premise-free max-flow/min-cut theorem.

## Reconciled boundary

| Gate | Decision |
|---|---|
| Frozen exact target | provisional replay pass; no statement change |
| Weak duality | local body passes trust-zero replay; unaccepted provisional evidence only |
| No-chain branch | local body passes replay; partial progress pending exact registry-interface reconciliation |
| Canonical root | failed: maximum-flow attainment and equal-cut construction are unproved |
| Accepted graph/task state | failed: no accepted closed obligation, evidence link, receipt, or target-local task state |
| `AUDIT-Z` | false: inventory/evidence/source/public reconciliation is not completely accepted |
| Human source/readability | failed: H1 and R4 remain; no independent H0/R0 review |
| Trust/provenance/supply chain | failed: no accepted complete transitive TCB, SBOM, license, or offline archive closure |
| Hermetic release | failed: dirty worker packet and shared warm cache; no clean empty-cache cold/offline replay |
| Independent verification | failed: no distinct signed runner pair or independently implemented minimal verifier |
| Deterministic release bundle | failed: no build-twice content-addressed bundle |
| `THEOREM-Z` / theorem completion | false |

## Self-test

`check_release.py` binds the canonical statement, obligation registry, typed graphs, task DAG,
proof and validation receipts, authority inputs, and the release recipe by SHA-256. It verifies the
unchanged fail-closed decision, scans all four Lean modules for prohibited proof constructs, and
freshly compiles `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `Validation.lean` under
`--trust=0` in a network-isolated Bubblewrap temporary directory. The replay observes exactly
`propext`, `Classical.choice`, and `Quot.sound`, with no unexpected bodyless or unsafe dependency.

The integrated `check_validation.py` is not a current release recipe: it is intentionally bound to
the validation worker's historical base revision and root packet. This release checker binds the
historical receipt and performs its own fresh narrow replay rather than manufacturing the old
worker state.

This makes only the negative reconciliation self-tested and suitable for a provisional worker
`[_]` handoff. It supplies no release-grade receipt, exact-root proof credit, `M0`, `E0`/`E1`,
`AUDIT-Z`, `THEOREM-Z`, release, theorem completion, independent verification, or master acceptance.

## Retry condition

Prove and master-accept `M0814-L-MAX-ATTAIN` and `M0814-T-EQUAL-CUT`, check premise-free root
composition, reconcile the frozen graph and task authority, and accept H0/R0 plus `AUDIT-Z`. Then
complete the immutable clean cold/offline, full provenance/TCB/SBOM/license, deterministic bundle,
distinct signed runner, independent-verifier, protected-CI, `THEOREM-Z`, and final master gates.
