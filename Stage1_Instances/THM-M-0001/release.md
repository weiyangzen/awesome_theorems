# THM-M-0001 release decision

Item `S56-M-0001-RELEASE` has the exact verdict **blocked**. The lifecycle
remains `planned`, the accepted root vector remains `H1/M3/R3`, and both
`AUDIT-Z` and `THEOREM-Z` are blocked. `theorem_complete` remains false and
there are no accepted receipt IDs. This is a tested negative release decision,
not theorem completion or master acceptance.

## Evidence reconciliation

The proof and validation receipts provide provisional warm-cache kernel
evidence for the exact frozen target. The canonical wrapper and a separately
written same-workspace reconstruction elaborate using pinned mathlib, and the
reported axiom set is `propext`, `Classical.choice`, and `Quot.sound`. The
scoped placeholder scan passes. These facts support only a provisional
`M0-W` proposal.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the prerequisite
validation receipt is worker-self-tested, explicitly non-release-grade, and
not master accepted. Moreover, the authoritative typed graph predates proof
closure and still reports the root and three exactness leaves open. The weaker
status therefore wins, and no accepted vector or lifecycle transition occurs.

`AUDIT-Z` is also unavailable. The dossier has neither an accepted complete
inventory reconciliation nor independent `H0` primary-source and `R0`
readability reviews. The first missing release-specific gate is
`S56-10.6-HERMETIC-COLD-BUILD`: no immutable empty-cache network-denied cold
build, offline restoration, complete transitive TCB, SBOM/license archive,
deterministic evidence bundle, two qualifying signed attestations, distinct
runner, or independently implemented minimal verifier exists.

## Validation

The release checker binds the validation receipt by SHA-256, checks the
manifest and planned instance boundary, verifies the stale-graph conflict is
preserved fail-closed, checks the complete release cut set, and reruns the
recorded narrow validation recipe:

```text
python3 Stage1_Instances/THM-M-0001/check_release.py
  exit 0
  release-decision: ok (blocked; dependency unaccepted; H1/M3/R3 unchanged)
  validation replay: ok (exact root provisional; authoritative graph stale)
  AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]
```

No dependency update, build, clone, or fetch is performed. The pre-existing
untracked `.lake` symlink is reused only for narrow Lean elaboration, making
this nonrelease worker evidence. Retry requires master acceptance and graph
reconciliation followed by full audit, hermetic supply-chain, independent
verification, deterministic-bundle, and master release gates.
