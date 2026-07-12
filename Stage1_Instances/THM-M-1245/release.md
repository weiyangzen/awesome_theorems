# THM-M-1245 release decision

Item `S56-M-1245-RELEASE` has the exact verdict **blocked**. The lifecycle remains
`planned`, the accepted root vector remains `H2/M4/R4`, and both `AUDIT-Z` and
`THEOREM-Z` are blocked. `theorem_complete` remains false and no receipt is accepted.
This is a tested negative release decision, not theorem completion or master acceptance.

## Evidence reconciliation

The validation receipt supplies provisional warm-cache evidence that the exact frozen Sobolev
target kernel-replays through the pinned mathlib terminal theorem. Checked composition and a
separately written same-workspace reconstruction reach the same exact root, the scoped placeholder
scan passes, and Lean reports only `propext`, `Classical.choice`, and `Quot.sound`. These results do
not change accepted state.

The first failed node gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the validation receipt is explicitly
non-release-grade worker evidence and has no master acceptance. The authoritative typed graph also
predates the proof and records `root_closed=false` and `M1`, while the planned instance remains
`H2/M4/R4`. The weaker structured state wins until master reconciliation.

`AUDIT-Z` is unavailable because complete inventory/source-boundary reconciliation and independently
accepted `H0` primary-source and `R0` readability records are absent. The first release-specific
failure is `S56-10.6-HERMETIC-COLD-BUILD`: there is no immutable empty-cache network-denied cold
build or offline restoration. Complete transitive provenance/TCB, SBOM/licenses, protected CI,
two qualifying attestations, distinct runners, an independently implemented minimal verifier, and
a deterministic release bundle also remain open.

## Validation

From base revision `5deb8c587c4f4bde14e6c99658fe76c173180019`, the release checker binds the
reconciled inputs by SHA-256, preserves the structured-state conflict fail-closed, verifies the
release cut set, and reruns the narrow validation checker:

```text
python3 Stage1_Instances/THM-M-1245/check_release.py
  exit 0
  release-decision: ok (blocked; dependency unaccepted; H2/M4/R4 unchanged)
  validation replay: ok (exact root provisional; authoritative graph stale)
  AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]

python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-1245
python3 -m json.tool Stage1_Instances/THM-M-1245/release-decision.json
git diff --check -- Stage1_Instances/THM-M-1245 .stage1-worker-selftest.json
  all exit 0
```

No dependency update, build, clone, fetch, network operation, or `.lake` mutation was performed.
The pre-existing shared pinned `.lake` artifacts were used only for narrow Lean replay, so this
remains nonrelease worker evidence.
