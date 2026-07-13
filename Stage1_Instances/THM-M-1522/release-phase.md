# THM-M-1522 release decision

Item: `S56-M-1522-RELEASE`. Base revision:
`f78ecdb166de720e4af8d8859826b4a22a4c1733`; base tree:
`6d72b645f5722769d4ed5d9eea3559c9e4c69856`.

## Exact verdict

The release verdict is `blocked`. Lifecycle remains `planned`; the accepted root
vector remains `[H1, M3, R3]`; `audit_complete=false` and
`theorem_complete=false`. No receipt is accepted and this worker makes no
authoritative state transition.

The first failed release-node gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`:
`S56-M-1522-VALIDATION` is only a provisional `[_]` projection. Its receipt has
`accepted=false` and `release_grade=false`. That receipt in turn records missing
proof master acceptance. The first failed release-assurance gate is
`S56-10.6-HERMETIC-COLD-BUILD`: the successful replay uses the shared warm
`.lake` closure, not a new clean checkout with empty caches and offline-restorable
content-addressed inputs.

## Reconciliation

There is strong but provisional machine evidence. The unchanged exact root,
vendored terminal bodies, conditional composition, both root adapters, and the
Proof-free differential root elaborate at trust level zero. All checked proof
declarations are sorry-free and report exactly `propext`, `Classical.choice`, and
`Quot.sound`.

That evidence cannot be promoted as recorded. The proof receipt calls the
vendored repo-local bodies an `M0-P` candidate, but rev-5.6 reserves `M0-P` for a
proof body that is not repo-local; the evidence is at most an `M0-L` candidate
until E0 and master gates pass. More importantly, frozen obligation
`M1522-X-UPSTREAM` names `lua-vr/pointwise-birkhoff@fc06094...`, while the proof
vendors `marcmorningstar/lean4-ergodic-theory@ed3fa6...` and records no registry
or typed-graph delta. The authoritative graph therefore correctly remains
`M3`, with `M1522-L-POINTWISE` and `M1522-T-IDENTIFY` open.

`AUDIT-Z` is also false. The structured inventory and public projections are not
reconciled: the README and obligation-tree still describe the pre-proof route,
and the prose reports eleven human-source obligations while the registry has
twelve. H0 primary-source review, independently accepted R0 reconstruction,
foundation and complete trust/provenance closure, SBOM/licenses, cold offline
reproduction, two distinct signed runners, an independently implemented minimal
verifier, protected CI, and a deterministic evidence bundle remain absent.

## Commands and results

Commands ran from this worker clone on 2026-07-14 (Asia/Shanghai). The pinned
`.lake` symlink was reused without modification. No `lake update`, `lake build`,
dependency clone/fetch, checkout, or network request ran.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-1522
  exit 0: rank 190, planned L0/rework-required, theorem_complete=false

bash Stage1_Instances/THM-M-1522/check_validation.sh
  exit 0: network-isolated trust-level-zero target replay passed; requested
  declarations were sorry-free and used exactly the three observed axioms

python3 -B Stage1_Instances/THM-M-1522/check_release.py
  exit 0: hashes, authority, classification/provenance conflicts, blocked
  terminal decisions, and fresh narrow Lean replay agreed

python3 -m json.tool on release-spec.json, release-decision.json,
release-receipt.json, and .stage1-worker-selftest.json
  exit 0: all structured artifacts parsed

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1522-release-pycache python3 -m py_compile
Stage1_Instances/THM-M-1522/check_release.py
  exit 0: checker compiled outside the repository tree

git diff --check -- Stage1_Instances/THM-M-1522 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; new-file hygiene also passed
```

The predecessor `check_validation.py` is snapshot-bound to its validation-worker
base and self-test inventory, so it is not misused as a current release recipe.
The immutable receipt is hash-bound and `check_validation.sh` replays the Lean
objects directly. Retry requires dependency-ordered master acceptance and an
append-only authoritative proof/provenance reconciliation, followed by all
remaining source, readability, trust, hermetic, independence, bundle, and
master gates.
