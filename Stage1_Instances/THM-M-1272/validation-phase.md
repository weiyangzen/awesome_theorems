# THM-M-1272 validation-phase result

Item: `S56-M-1272-VALIDATION`. Base revision:
`e6c4d56e017f77b02752e6c1325f0298dfb7f4d4`. Final validation time and
raw-output digest are recorded in `validation-receipt.json`.

## Validated scope

The node-scoped runner copied `Statement.lean`, `AnchorAudit.lean`,
`ObligationTree.lean`, `Proof.lean`, and `Validation.lean` to a temporary
directory and elaborated all five at trust level zero with the pinned Lean
executable. Every Lean invocation ran inside Bubblewrap with an unshared
network namespace, a read-only host filesystem, and only the temporary module
directory writable.

The four proof-phase compactness declarations and four separately written
validation probes each report exactly `propext`, `Classical.choice`, and
`Quot.sound`. The probe imports `ObligationTree` but not `Proof`; it rebuilds
boundedness, subsequence extraction, limit identification, and the exact
`FountainLimitPackage` under different declarations. This is
separately named same-worker evidence for the compactness branch, not a second
verifier. Both exact-root observations still take
`FountainMinimaxPackage` as an explicit premise.

Selected provenance checks bind the clean pinned mathlib revision and tree,
five supporting source blobs and compiled imports, mathlib's license, and the
invoked tool identities. This does not close the full transitive declaration,
proof-body, source-boundary, TCB, or SBOM closure.

The three leaf obligation fingerprints are still frozen `planned:v1` prose
fingerprints rather than normalized elaborated declaration fingerprints. The
parent `FountainLimitPackage` type is exact and checked, but master acceptance
of leaf `M0-*` status requires authoritative type/fingerprint reconciliation.

## Commands and results

All commands ran from repository root. No dependency update, build, clone,
fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1272` | 0 | rank 165, lifecycle planned, theorem incomplete |
| `git status --short` | 0 | only the automation-provided untracked `.lake` symlink existed before this phase; validation changes are nonrelease evidence |
| `bash Stage1_Instances/THM-M-1272/check_proof.sh` | 0 | Statement, conditional composition, and four compactness obligations replayed at trust zero; minimax stayed open |
| `python3 Stage1_Instances/THM-M-1272/check_anchor_audit.py` | 0 | 11 immutable dependency heads and four non-closing candidates passed |
| `python3 Stage1_Instances/THM-M-1272/check_obligation_tree.py` | 0 | 16 obligations, 29 typed edges, root open M3 |
| `python3 Stage1_Instances/THM-M-1272/check_lean_composition.py` | 0 | conditional exact-root composition elaborated with the recorded axiom set |
| `/usr/bin/bash Stage1_Instances/THM-M-1272/check_validation.sh` | 0 | the complete recipe ran in a cleared-environment, network-denied sandbox; five-module replay, axiom reports, source hygiene, receipt/hash binding, selected provenance, and fail-closed gate decisions passed |
| `python3 -m json.tool Stage1_Instances/THM-M-1272/validation-spec.json` | 0 | structured recipe parses |
| `python3 -m json.tool Stage1_Instances/THM-M-1272/validation-receipt.json` | 0 | provisional node receipt parses |
| stage-independent trailing-whitespace scan of all five new text artifacts | 0 | no whitespace errors; unlike `git diff --check`, this covered untracked files |

The validation runner's exact summary was:

```text
PASS THM-M-1272 narrow validation
kernel: four partial proof obligations and four separately reconstructed probes replayed at trust zero with network denied
trust: machine reports only propext, Classical.choice, Quot.sound; no sorry or prohibited local device
provenance: proof hashes, selected mathlib sources/oleans/license, clean pin, and tool identities agree
root open: symmetric normalization, minimax construction, linking, odd deformation, and lower-bound package remain unproved
blocked: proof master acceptance, accepted foundation profile, cold empty-cache release replay, complete trust/provenance, and distinct-runner verification
```

## Gate decisions

| Gate | Decision | Boundary |
|---|---|---|
| Narrow kernel replay | pass | The exact statement, anchor audit, frozen conditional composer, four compactness proof declarations, and four differential probes elaborate from copied sources with network denied. |
| Placeholder and unsafe check | pass | Machine axiom output and comment-stripped scans find no `sorry`, `admit`, local axiom/bodyless declaration, unsafe/native/oracle, external implementation, or other prohibited proof device. |
| Trust observation | partial pass | Ten checked declarations report the three observed principles, but the dossier lacks an accepted versioned foundation policy and full transitive TCB closure. |
| Selected provenance | partial pass | Local receipt hashes plus selected mathlib source/blob/olean/license and tool identities agree; root and transitive provenance remain open. |
| Exact root closure | fail closed | Symmetric normalization, minimax-class construction, linking, odd deformation, and the lower-bound package are unproved; the exact root remains conditional and M3. |
| Structured recipe freshness | fail closed | The frozen obligation-tree `validation-specs.json` predates `Proof.lean`; its structural recipes do not validate the four compactness declarations. The validation phase therefore uses a new narrowly scoped recipe and grants the old recipes no proof credit. |
| Authoritative graph freshness | fail closed | `typed-graphs.json` still lists `M1272-T-CRITICAL-LEVELS` in the pre-proof cut set; only the master may reconcile it with the provisional proof receipt. |
| Hermetic release | fail closed | Network was denied, but the run reused shared warm read-only `.lake` artifacts instead of a new checkout, empty-cache cold build, or offline archive restoration. |
| Independent verification | fail closed | The differential probe ran in this worker checkout and cache; two distinct signed runners and an independently implemented minimal release verifier are absent. |

The authoritative instance still has no accepted proof state. The debt vector
remains `[H2, M3, R4]`, `audit_complete=false`, and
`theorem_complete=false`. The worker proposes `[_]` only for the self-tested
validation harness and its truthful negative gate decisions. The hermetic,
complete trust and provenance, exact-root, and distinct-runner gates still
fail; `[_]` is unfinished and grants no `E0/E1`, release, theorem completion,
or master acceptance.
