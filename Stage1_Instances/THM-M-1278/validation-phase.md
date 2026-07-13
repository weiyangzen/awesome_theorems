# THM-M-1278 validation-phase result

Item: `S56-M-1278-VALIDATION`. Base revision:
`0712591ddaea6a40a0dc6482670e6129e727f5df`. Validation time:
`2026-07-13T19:30:11Z` (`2026-07-14T03:30:11+08:00`).

## Validated scope

The node-scoped runner copied `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and
`Validation.lean` to a temporary directory and elaborated all four at trust level zero with the
pinned Lean executable. Every Lean invocation ran inside Bubblewrap with an unshared network
namespace, a read-only host filesystem, and only the temporary module directory writable.

The two proof-phase declarations and two separately written validation probes each report exactly
`propext`, `Classical.choice`, and `Quot.sound`. The probe imports `ObligationTree` but not `Proof`;
it independently selects a mean-subtracted ambient representative and re-establishes its energy
invariance. This is implementation-diverse same-worker evidence for two partial obligations only,
not a second verifier or an Onofri proof.

Selected provenance checks bind the clean pinned mathlib revision/tree, the source blobs and
compiled imports supporting constant subtraction, smoothness, and gradients, and mathlib's license.
This does not close full transitive declaration/proof-body provenance or the complete TCB/SBOM.

## Commands and results

All commands ran from repository root. No `lake update`, `lake build`, dependency clone/fetch, or
`.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1278` | 0 | rank 449, lifecycle planned, theorem incomplete |
| `git status --short` | 0 | only the automation-provided untracked `.lake` symlink existed before this phase; validation changes are nonrelease evidence |
| `bash Stage1_Instances/THM-M-1278/check_proof.sh` | 0 | two partial declarations replayed at trust zero with the recorded axiom set |
| `python3 Stage1_Instances/THM-M-1278/check_proof.py` | 0 | proof receipt hashes, selected obligation fingerprints, and open-root boundary passed |
| `python3 Stage1_Instances/THM-M-1278/check_obligation_tree.py` | 0 | 15 obligations, 54 typed edges, root open M3 |
| `env LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC LEAN_NUM_THREADS=1 python3 -B Stage1_Instances/THM-M-1278/check_validation.py` | 0 | network-denied four-module replay, exact axiom reports, source hygiene, receipt/hash binding, selected provenance, and fail-closed gate decisions passed |
| `python3 -m json.tool Stage1_Instances/THM-M-1278/validation-spec.json` | 0 | structured recipe parses |
| `python3 -m json.tool Stage1_Instances/THM-M-1278/validation-receipt.json` | 0 | provisional node receipt parses |
| `git diff --check -- Stage1_Instances/THM-M-1278 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The validation runner's exact summary was:

```text
PASS THM-M-1278 narrow validation
kernel: two partial proof bodies and two separately reconstructed probes replayed at trust zero with network denied
trust: machine reports only propext, Classical.choice, Quot.sound; no sorry or prohibited local device
provenance: proof hashes, selected mathlib sources/oleans/license, clean pin, and tool identities agree
root open: sharp Onofri, area/finiteness, normalization transport, and canonical namespace bridge remain unproved
blocked: proof master acceptance, cold empty-cache release replay, complete trust/provenance, and distinct-runner verification
```

## Gate decisions

| Gate | Decision | Boundary |
|---|---|---|
| Narrow kernel replay | pass | The exact statement, frozen open-root composition harness, two partial proof bodies, and two differential probes elaborate from copied sources with network denied. |
| Placeholder/unsafe check | pass | Machine axiom output and comment-stripped local scans find no `sorry`, `admit`, local axiom/bodyless declaration, unsafe/native/oracle, external implementation, or other prohibited proof device. |
| Trust observation | partial pass | All four declarations report the expected three principles; `Classical.choice` has no accepted theorem-specific foundation policy and full transitive TCB closure is absent. |
| Selected provenance | partial pass | Local receipt hashes plus selected mathlib source/blob/olean/license and tool identities agree; root and transitive provenance remain open. |
| Exact root closure | fail closed | The sharp estimate, sphere area/finiteness, normalization and log/exp transport, and complete mean-shift interface are unproved. |
| Canonical target transport | fail closed | `ObligationTree.lean` duplicates the statement structures in a distinct namespace and has no checked transport from `Root` to `Statement.OnofriInequality`. |
| Source/readability fidelity | fail closed | Intrinsic-smooth/ambient-extension equivalence, representative independence, Hausdorff sphere-area normalization, primary-source mapping, and independent R0 review are absent. |
| Hermetic release | fail closed | Network was denied, but the run reused shared warm read-only `.lake` artifacts rather than a new checkout, empty-cache cold build, or offline archive restoration. |
| Independent verification | fail closed | The differential probe ran in this worker checkout/cache; two distinct signed runners and an independently implemented minimal release verifier are absent. |

The authoritative graph still records no accepted closed obligations; only the master may reconcile
the proof receipt's two provisional selected-witness bodies. The debt vector remains
`[H2, M3, R4]`, `audit_complete=false`, and `theorem_complete=false`. This worker receipt is
provisional `[_]` evidence for truthful narrow validation, not `E0/E1`, release, theorem
completion, or master acceptance.
