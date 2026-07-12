# THM-M-1252 release decision handoff

## Exact verdict

`S56-M-1252-RELEASE` is **blocked**. The lifecycle remains `planned`, the accepted root vector
remains `[H2, M4, R4]`, and both `audit_complete` and `theorem_complete` remain false. There are no
accepted receipt IDs. This is a self-tested negative release decision, not theorem completion or
master acceptance.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the validation prerequisite has only a
`provisional_worker_selftest` receipt and is not master-accepted. The next failed theorem gate is
structured-state freshness. `Proof.lean` and `Validation.lean` provide provisional exact-root
kernel evidence through pinned mathlib, while the frozen typed graph still records `root_closed=false`.
Only the integration lane may reconcile that authoritative state.

## Evidence boundary

The narrow validation establishes the exact statement, the specialized pinned theorem
`Distribution.dsupport_compl_eq`, checked child-to-parent composition, and a same-workspace direct
reconstruction. The checked declarations report `propext`, `Classical.choice`, and `Quot.sound`,
and the local sources contain no placeholder, new axiom, or unsafe declaration. This supports an
`M0-W` proposal only; accepted state remains unchanged.

`AUDIT-Z` fails because the root remains `H2/R4`: there is no accepted primary-source theorem,
assumption, errata, and node crosswalk or independently reviewed readable reconstruction. Release
also lacks an immutable clean input, empty-cache network-denied cold build, offline restoration,
complete transitive TCB/SBOM/license evidence, two separately provisioned signed attestations, an
independently implemented verifier, protected CI mutation evidence, and a deterministic bundle.

## Self-test

Commands were run from base revision `d9a306e1c1d941b347946d9efe1f1a8225f40978`. No dependency
update, build, fetch, clone, or `.lake` mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups; 1546 uniform-L0 targets; execution skill present

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1252
  exit 0: rank 431; lifecycle planned; theorem_complete=false

python3 Stage1_Instances/THM-M-1252/check_release.py
  exit 0: provisional exact-root validation replayed; dependency acceptance,
  structured freshness, H0/R0, hermetic, independent-verifier, and master gates remain open;
  verdict blocked

python3 -m json.tool Stage1_Instances/THM-M-1252/release-decision.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-1252
  exit 0: no whitespace errors
```

Retry requires master reconciliation and acceptance of the dependency chain, independent H0/R0
acceptance, and a separately provisioned release lane that closes hermetic reproduction,
supply-chain, independent verification, CI, deterministic-bundle, and master-acceptance gates.
