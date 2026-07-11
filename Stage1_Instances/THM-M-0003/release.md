# THM-M-0003 release decision

Item `S56-M-0003-RELEASE` has the exact verdict **blocked**. Lifecycle remains
`planned`, the accepted root vector remains `H2/M3/R3`, and both `AUDIT-Z` and
`THEOREM-Z` are false. There are no accepted receipt IDs. This is a self-tested
negative release decision, not theorem completion or master acceptance.

## Evidence reconciliation

The proof and validation receipts provide provisional kernel evidence for the
exact frozen snake-lemma target. Both the direct wrapper over pinned mathlib and
the route through the four frozen exactness segments elaborate. Lean reports
only `propext`, `Classical.choice`, and `Quot.sound`, and the scoped proof-source
hygiene check passes. This supports a provisional `M0-W` proposal only.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the prerequisite
validation receipt is warm-cache worker evidence, is not release grade, and is
not master accepted. The frozen graph and registry also retain their pre-proof
`M1` boundary. Under the weaker-status rule, no accepted lifecycle or debt
transition occurs.

`AUDIT-Z` is unavailable because the dossier lacks a reconciled complete audit,
an accepted pinpoint `H0` source crosswalk, and independently reviewed `R0`
reconstructions. The first failed release-evidence gate recorded by validation
is `trust.accepted_axiom_policy`. Transitive TCB acceptance, an immutable clean
snapshot, empty-cache network-denied cold replay, SBOM/license archives, offline
restoration, independent runners and attestations, a minimal independent
verifier, protected mutation gates, and a deterministic signed bundle are also
missing.

## Validation

The release checker binds the validation receipt by SHA-256, checks manifest,
intake, registry, graph, proof, and validation boundaries, checks the complete
release cut set, and replays the validation checker:

```text
python3 Stage1_Instances/THM-M-0003/check_release.py
  exit 0
  release-decision: ok (blocked; dependency unaccepted; H2/M3/R3 unchanged)
  validation replay: ok (exact root provisional; release gates fail closed)
  AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]
```

The narrow Lean replay was also run with `lake env lean` through
`check_proof.sh`; both exact declarations elaborated and reported the same
three axioms. No dependency update, build, clone, or fetch was performed. The
pre-existing untracked `.lake` symlink was reused only as a warm pinned cache,
so all evidence remains nonrelease worker evidence.
