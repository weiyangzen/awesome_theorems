# Build validation prescription

Worker preflight command: `complete-target-semantic-proof-debt`, exactly as
frozen in the claim card, with `--no-lean` and network denied.

Master replay obligations after harvest:

1. Place only the declared artifacts into a clean content-addressed snapshot.
2. Compile `Statement.lean`, `Proof.lean`, and `Audit.lean` independently with
   the pinned toolchain and `--trust=0`.
3. Reject any placeholder, unexpected axiom, bodyless oracle, local source-name
   capture, active numeric provider import, or dependency outside the pinned
   foundation profile.
4. Elaborate the frozen provider type and the claim-owned target, prove both
   transports, and recompute every non-foundation constant binding.
5. Mutate imports, qualified source name, graph part sizes, edge totals,
   dimension totals, Gram coefficient `1/2`, and the orthogonality decomposition;
   each semantic mutation must fail.
6. Re-run from an empty cache with networking disabled and compare complete
   stdout, stderr, object, dependency, and axiom digests.

Only the Master’s successful trace may turn the provisional candidate into an
accepted theorem completion.
