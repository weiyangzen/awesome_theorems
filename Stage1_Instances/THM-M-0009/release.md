# THM-M-0009 release decision

Item `S56-M-0009-RELEASE` has the exact verdict **blocked**. The lifecycle
remains `planned`, the accepted root vector remains `H2/M3/R4`, and both
`AUDIT-Z` and `THEOREM-Z` are blocked. `theorem_complete` remains false and
there are no accepted receipt IDs. This is a tested negative release decision,
not theorem completion or master acceptance.

## Evidence reconciliation

The proof and validation receipts provide provisional warm-cache kernel
evidence for the exact frozen two-variance Ext target. The canonical wrapper
and a separately written same-workspace reconstruction elaborate using pinned
mathlib, and Lean reports `propext`, `Classical.choice`, and `Quot.sound`. The
scoped placeholder scan passes. These facts support only a provisional
`M0-W` proposal.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the prerequisite
validation receipt is worker-self-tested, explicitly non-release-grade, and
not master accepted. The authoritative typed graph also predates proof closure
and still reports the root and both exactness leaves open. The weaker status
therefore wins, and no accepted vector or lifecycle transition occurs.

`AUDIT-Z` is unavailable because the dossier has neither a reconciled complete
inventory nor independent `H0` primary-source and `R0` readability reviews.
In particular, the selected covariant-plus-contravariant scope still lacks an
accepted theorem/page/assumption/errata crosswalk. The first missing
release-specific gate is `S56-10.6-HERMETIC-COLD-BUILD`: there is no immutable
empty-cache network-denied cold build, offline restoration, complete
transitive TCB, SBOM/license archive, deterministic evidence bundle, two
qualifying signed attestations, distinct runner, or independently implemented
minimal verifier.

## Validation

The release checker binds the validation receipt by SHA-256, checks the
manifest and planned instance boundary, preserves the stale-graph conflict
fail-closed, checks the release cut set, and reruns the recorded narrow
validation recipe:

```text
python3 Stage1_Instances/THM-M-0009/check_release.py
  exit 0
  release-decision: ok (blocked; dependency unaccepted; H2/M3/R4 unchanged)
  validation replay: ok (exact root provisional; authoritative graph stale)
  AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]
```

No dependency update, build, clone, or fetch is performed. The pre-existing
untracked `.lake` symlink is reused only for narrow Lean elaboration, so this
remains nonrelease worker evidence. Retry requires master acceptance and graph
reconciliation followed by full audit, hermetic supply-chain, independent
verification, deterministic-bundle, and master release gates.
