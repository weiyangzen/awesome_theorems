# THM-M-1251 release decision

Item `S56-M-1251-RELEASE` has the exact verdict **blocked**. The lifecycle remains
`planned`, the accepted root vector remains `H2/M4/R4`, and both `AUDIT-Z` and
`THEOREM-Z` are blocked. `theorem_complete` remains false and there are no accepted
receipt IDs. This is a tested negative release decision, not theorem completion or
master acceptance.

## Evidence reconciliation

The proof and validation receipts provide provisional warm-cache kernel evidence for
the exact frozen pointwise-dual target. The canonical declaration closes by unfolding
the pinned mathlib `TemperedDistribution` abbreviation, and a separately written
same-workspace reconstruction also elaborates. The observed axioms are `propext`,
`Classical.choice`, and `Quot.sound`; the scoped placeholder scan passes. These facts
support only a provisional `M0-W` proposal.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the prerequisite validation
receipt is worker-self-tested, explicitly non-release-grade, and not master accepted.
The authoritative typed graph also predates proof closure and records `root_closed=false`.
The weaker status wins, so the accepted vector and lifecycle do not change.

`AUDIT-Z` is unavailable because the source, evidence, and debt inventory is not fully
reconciled and there are no independently accepted `H0` primary-source or `R0`
readability reviews. The first missing release-specific gate is
`S56-10.6-HERMETIC-COLD-BUILD`. There is no immutable empty-cache network-denied cold
build, offline restoration, complete transitive TCB, SBOM/license archive, deterministic
bundle, two qualifying signed attestations, distinct runner, or independently implemented
minimal verifier.

## Validation

The release checker binds its reconciled inputs by SHA-256, verifies the planned instance
and stale-graph conflict, checks the release cut set, and reruns the recorded narrow
validation recipe:

```text
python3 Stage1_Instances/THM-M-1251/check_release.py
  exit 0
  release-decision: ok (blocked; dependency unaccepted; H2/M4/R4 unchanged)
  validation replay: ok (exact root provisional; authoritative graph stale)
  AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]
```

No dependency update, build, clone, or fetch is performed. The existing `.lake` symlink
is reused only for narrow Lean elaboration, making this nonrelease worker evidence. Retry
requires master acceptance and graph reconciliation followed by full audit, hermetic
supply-chain, independent-verification, deterministic-bundle, and master release gates.
