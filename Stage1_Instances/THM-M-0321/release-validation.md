# THM-M-0321 release reconciliation

Item `S56-M-0321-RELEASE` has the exact verdict `blocked`. The lifecycle remains `planned`, the
authoritative root vector remains `[H2, M3, R4]`, and both `audit_complete` and
`theorem_complete` remain false. No receipt or obligation is accepted by this worker.

## Evidence reconciliation

The direct prerequisite is not dependency-legal for release: `S56-M-0321-VALIDATION` is only
scheduler-provisional `[_]`; its receipt is `accepted=false`, `release_grade=false`, and has no
master acceptance. This is the first failed release-node gate,
`dependency.S56-M-0321-VALIDATION.master_acceptance` (`S56-10.2-DEPENDENCY-ACCEPTANCE`).

The historical validation receipt contains useful nonrelease evidence. It records a network-isolated
trust-zero elaboration of the exact target and a same-worker recomposition, observing only
`Classical.choice`, `Quot.sound`, and `propext`. Its inspected closure contained 14,374 declarations
from 553 modules with no unexpected bodyless nonaxiom or unsafe declaration. That run shared the
warm canonical cache and proof helpers, so it is neither a cold build nor independent verification.

The frozen `ObligationTree.CompactnessUpgrade` interface is false because it omits continuity or
closedness of the fixed loci. The exact proof bypasses it with `continuousCompactnessUpgrade`, but
the accepted frozen composition route is not closed; `M0321-T-UPGRADE` remains the post-proof cut.
The authoritative typed graph is also unreconciled and still projects its older pre-proof cut.

`AUDIT-Z` fails because source-boundary, proof-era graph, readable, evidence, and public-state
records are not fully reconciled and independently accepted. `THEOREM-Z` therefore fails before
considering the additional missing foundation/TCB/SBOM closure, immutable cold offline replay, two
distinct signed attestations, independently implemented verifier, protected CI, deterministic
bundle, and master acceptance.

## Current replay blocker

The smallest current Lean replay was attempted without dependency mutation:

```text
bash Stage1_Instances/THM-M-0321/check_proof.sh
  exit 1 before Lean elaboration: lake env could not resolve HEAD in
  Formalizations/Lean/.lake/packages/flt-regular
```

The automation-provided checkout has `.git/HEAD` equal to `refs/heads/.invalid`, while
`lake-manifest.json` pins `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. Per worker policy, no
`lake update`, build, clone, fetch, checkout, or `.lake` mutation was performed. This missing pinned
artifact is a blocker, not permission to fetch a moving dependency.

## Commands and results

Commands ran from base revision `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets at ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0321
  exit 0: rank 687; planned, L0/rework-required, theorem_complete=false

bash Stage1_Instances/THM-M-0321/check_proof.sh
  exit 1: missing/incomplete pinned flt-regular artifact; no Lean elaboration result

python3 -I -B Stage1_Instances/THM-M-0321/check_release.py
  exit 0: current hashes, authority, dependency, cut set, missing artifact, and negative terminal
  decisions agreed

python3 -m json.tool on release-decision.json, release-receipt.json, release-spec.json, and
.stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-m0321-release-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0321/check_release.py
  exit 0: checker compiled without repository cache output

git diff --check -- Stage1_Instances/THM-M-0321 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

The release handoff is self-tested only as a truthful negative reconciliation and proposes worker
state `[_]`. The integration lane must independently review it; it does not promote the theorem.
