# S56-M-0388-VALIDATION handoff

The assigned v2 node has rank 3 and phase layer 5. Its complete direct/transitive parent inspection
order is empty. The target also has no incoming hard edge, reuse hint, or shared-lemma group. The
target-owned `dependency-reuse-ledger.json` records that empty audited closure against current graph
digest `39dc7ce5f668c527de899e74c99840aef50e6be4c576aaf146abed1b6749275c` and context digest
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

The structured recipe runs the HEAD-candidate validator without shell interpolation. It checks the
proof receipt's current inputs, the frozen registry and typed-node identity, the pinned Lean and
mathlib revisions, the exact Pell source and olean bytes, and prohibited constructs. It then
re-elaborates `Proof.lean` and the independently written `Validation.lean` reconstruction in a fresh
temporary directory using only the existing pinned artifacts. Both roots report exactly `propext`,
`Classical.choice`, and `Quot.sound`; both local predicate transports report no axioms.

This is a warm-cache, same-workspace node validation. The release-only cold empty-cache replay,
complete transitive TCB/SBOM archive, distinct signed runner, H0/R0 reviews, and terminal decisions
remain explicitly unclaimed. The predecessor and all earlier phases are still `[_]`, so this handoff
does not transfer acceptance and cannot write `[x]`. That unfinished predecessor is the first
acceptance failure: `G02-TOPOLOGY.S56-M-0388-PROOF`. Its legacy provisional receipt also omits the
current contract fields required of master-accepted proof evidence, so `V01-ARTIFACTS` fails closed.

This revalidation runs from base `f545339546bf410d5110d7fe44e70bdcf5d8b48e`. The existing
HEAD-tracked validator is scheduler-selected and unchanged, but it is internally pinned to its
historical worker base `c5037228977a81948bbd6119e1728b4b65b9924e`; consequently its direct
current-base replay truthfully returns `repair_required` with semantic `blocked=false`. Independent
narrow Lean replays still pass for `Proof.lean` and `Validation.lean`. This is the additional
`V02-RECIPES/validator-current-base-binding` failure, not a replacement for the earlier topology
failure. The integration lane must first accept a contract-complete proof predecessor and must then
allocate another base-bound validation replay before phase acceptance can be considered.
Refreshing the target-owned ledger and receipt makes their checked-in theorem-DAG reusable-artifact
digests stale. The graph and standard validators passed at the immutable base before this refresh;
after integration, the scheduler must regenerate that read-only projection. The target manifest and
HEAD phase-contract checks remain green.
