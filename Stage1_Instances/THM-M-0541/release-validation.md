# THM-M-0541 release decision

Item `S56-M-0541-RELEASE` has the exact verdict **blocked**. The lifecycle remains
`planned`, the accepted root vector remains `[H2, M3, R4]`, and both `AUDIT-Z` and
`THEOREM-Z` are blocked. `theorem_complete=false`, and no receipt is accepted. This is a
self-tested negative release decision, not theorem completion or master acceptance.

## Evidence reconciliation

The prerequisite validation receipt supplies provisional worker evidence that a fresh temporary
copy of `Proof.lean` kernel-replays the exact frozen root. Its scoped placeholder scan passes, and
Lean reports only `propext`, `Classical.choice`, and `Quot.sound`. This does not change accepted
state. The first failed node gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: that receipt is explicitly
non-release-grade worker evidence and has no master acceptance. The planned instance and pre-proof
typed graph still record `[H2, M3, R4]`, no accepted closed obligations, and
`theorem_complete=false`; the weaker structured status therefore wins pending master reconciliation.

`AUDIT-Z` is unavailable because complete inventory and source-boundary reconciliation plus
independently accepted `H0` source and `R0` readability records are absent. The first
release-specific failure is `S56-10.6-HERMETIC-COLD-BUILD`: there is no immutable empty-cache,
network-denied cold build or offline archive restoration. Complete transitive provenance and TCB,
SBOM/licenses, protected CI, two qualifying signed attestations, distinct provisioned runners, an
independently implemented minimal verifier, and a deterministic release bundle also remain open.

## Validation

Commands run from base revision `760cbc73b01804753c0dfb5f84b703dff6d026de`:

```text
python3 Stage1_Instances/THM-M-0541/check_release.py
  exit 0: blocked decision and provisional exact-root replay agree; H2/M3/R4 unchanged;
  AUDIT-Z=false; THEOREM-Z=false; accepted receipts=[]

python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-0541
python3 -m json.tool Stage1_Instances/THM-M-0541/release-decision.json
git diff --check -- Stage1_Instances/THM-M-0541 .stage1-worker-selftest.json
  all exit 0
```

No dependency update, build, clone, fetch, network operation, or `.lake` mutation was performed.
The pre-existing pinned warm `.lake` artifacts were used only for the narrow Lean replay, so they
are not release evidence. Retry requires master reconciliation and acceptance, independent H0/R0
review, then hermetic supply-chain and independent-runner evidence under the complete release gate.
