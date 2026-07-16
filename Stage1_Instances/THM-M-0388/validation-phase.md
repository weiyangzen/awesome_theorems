# S56-M-0388-VALIDATION handoff

The assigned v2 node has rank 3 and phase layer 5. Its complete direct/transitive parent inspection
order is empty. The target also has no incoming hard edge, reuse hint, or shared-lemma group. The
target-owned `dependency-reuse-ledger.json` records that empty audited closure against current graph
digest `6ce46e0d9e79e1a40c423ae1074db34e889702b9a5b5989034cd462615fed604` and context digest
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
does not transfer acceptance and cannot write `[x]`.

This revalidation runs from base `738c0e35f61cf22c1ab5e31a5cd0ad6432f12f01`. The existing
HEAD-tracked validator is scheduler-selected and unchanged, but it is internally pinned to its
historical worker base `c5037228977a81948bbd6119e1728b4b65b9924e`; consequently its direct
current-base replay truthfully returns `repair_required`. Independent narrow Lean replays still pass
for `Proof.lean` and `Validation.lean`. The first failed current acceptance gate is therefore
`V02-RECIPES/validator-current-base-binding`. The integration lane must land this refreshed receipt
and ledger, then allocate another base-bound revalidation before phase acceptance can be considered.
Refreshing the target-owned receipt also makes the checked-in theorem-DAG reusable-artifact digest
stale. Its structural validator therefore fails for that precise expected reason until the scheduler
regenerates the read-only projection during integration; the target manifest and HEAD phase-contract
checks remain green.
