# THM-M-1091 release decision

Item `S56-M-1091-RELEASE` has the exact verdict **blocked**. Lifecycle remains `planned`, the
accepted root vector remains `H1/M3/R3`, and both `AUDIT-Z` and `THEOREM-Z` are blocked.
`theorem_complete` remains false and there are no accepted receipt IDs. This is a tested negative
release decision, not theorem completion or master acceptance.

## Evidence reconciliation

The proof and validation artifacts provide provisional warm-cache kernel evidence for the exact
frozen homogeneous discrete-time target. The local root and integral transport, plus a separately
written same-workspace reconstruction, elaborate using pinned `ProbabilityTheory.Kernel.pow_add`.
They report only `propext`, `Classical.choice`, and `Quot.sound`, and the scoped placeholder and
unsafe scan passes. These facts support only a provisional `M0-P` proposal.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the prerequisite validation receipt is
worker-self-tested, explicitly non-release-grade, and not master accepted. The frozen typed graph
also predates proof closure and retains `M1091-L-POWADD` as the root cut. Under the weaker-status
rule, no accepted vector or lifecycle transition occurs.

`AUDIT-Z` is unavailable because complete inventory reconciliation and independently accepted H0
primary-source and R0 readability reviews are absent. The first release-specific failure is
`S56-10.6-HERMETIC-COLD-BUILD`: there is no immutable empty-cache network-denied cold build,
offline restoration, complete transitive TCB, SBOM/license archive, deterministic evidence bundle,
two qualifying signed attestations, distinct runner, or independently implemented minimal verifier.

## Validation

The release checker binds the validation receipt by SHA-256, checks the planned manifest boundary,
preserves the stale-graph conflict fail-closed, checks the release cut set, and reruns the recorded
narrow validation recipe:

```text
python3 Stage1_Instances/THM-M-1091/check_release.py
  exit 0
  release-decision: ok (blocked; dependency unaccepted; H1/M3/R3 unchanged)
  validation replay: ok (exact root provisional; authoritative graph stale)
  AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]
```

No dependency update, build, clone, or fetch is performed. The existing pinned `.lake` artifacts
are reused only for narrow Lean elaboration, so this remains nonrelease worker evidence. Retry
requires master dependency acceptance and graph reconciliation, followed by source/readability,
trust, hermetic supply-chain, independent-verification, deterministic-bundle, and master gates.
