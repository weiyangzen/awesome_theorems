# THM-M-0450 validation-phase result

Item: `S56-M-0450-VALIDATION`. Base revision:
`309f58b7a54d36653b3483a543c6378eea53882c`. Validation time:
`2026-07-13T17:37:14Z` (`2026-07-14T01:37:14+08:00`).

## Validated scope

The node-scoped runner copied `Statement.lean`, `ObligationTree.lean`,
`Proof.lean`, and `Validation.lean` to a temporary directory and elaborated all
four with the pinned Lean executable. Every Lean invocation ran inside
Bubblewrap with an unshared network namespace, a read-only host filesystem,
and only the temporary module directory writable.

The ten proof-phase declarations and the separately written validation probe
each report exactly `propext`, `Classical.choice`, and `Quot.sound`. The probe
imports neither `Proof` nor `ObligationTree`; it reconstructs the conditional
composition into the canonical `ExactTarget`. It is implementation-diverse
same-worker evidence, not a second verifier or an unconditional proof.

Selected provenance checks bind the clean pinned mathlib revision/tree, the
source blobs and compiled imports for `AddCommGroup.fg_of_descent'` and
`WeierstrassCurve.Jacobian.Point.toAffineAddEquiv`, and mathlib's license. This
does not constitute full transitive declaration/proof-body provenance or a
complete TCB/SBOM inventory.

## Commands and results

All commands ran from the repository root. No `lake update`, `lake build`,
dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0450` | 0 | rank 92, lifecycle planned, theorem incomplete |
| `git status --short` | 0 | only pre-existing untracked canonical `.lake` before this phase; worker changes are nonrelease evidence |
| `bash Stage1_Instances/THM-M-0450/check_proof.sh` | 0 | ten declarations replayed; exact recorded axiom set and source hygiene passed |
| `python3 Stage1_Instances/THM-M-0450/check_obligation_tree.py` | 0 | 14 obligations, 31 typed edges, root open M3 |
| `env LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC LEAN_NUM_THREADS=1 python3 -B Stage1_Instances/THM-M-0450/check_validation.py` | 0 | network-denied four-module replay, axiom/placeholder checks, hash bindings, selected provenance, and fail-closed gate decisions passed |
| `python3 -m json.tool Stage1_Instances/THM-M-0450/validation-spec.json` | 0 | structured recipe parses |
| `python3 -m json.tool Stage1_Instances/THM-M-0450/validation-receipt.json` | 0 | provisional node receipt parses |
| `git diff --check -- Stage1_Instances/THM-M-0450 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The validation runner's exact summary was:

```text
PASS THM-M-0450 narrow validation
kernel: 10 proof declarations and a separately reconstructed conditional probe replayed with network denied
trust: machine reports only propext, Classical.choice, Quot.sound; no sorry or prohibited local device
provenance: proof hashes, selected mathlib sources/oleans/license, and clean pin agree
root open: weak Mordell-Weil and elliptic height packages remain unproved; no whole frozen obligation closed
blocked: proof master acceptance, cold empty-cache release replay, complete TCB closure, and distinct-runner verification
```

## Gate decisions

| Gate | Decision | Boundary |
|---|---|---|
| Narrow kernel replay | pass | The exact statement, frozen composition, partial proof bodies, and differential conditional probe elaborate from copied sources with network denied. |
| Placeholder/unsafe check | pass | `assert_no_sorry`, machine axiom output, and comment-stripped local source scans find no prohibited proof device. |
| Trust observation | partial pass | All eleven declarations report the expected three principles; no accepted foundation profile or full transitive TCB closure exists. |
| Selected provenance | partial pass | Local receipt hashes plus selected mathlib source/blob/olean/license identities agree; root and transitive provenance remain open. |
| Exact root closure | fail closed | Weak Mordell-Weil and the elliptic height package are unproved, so both compositions are conditional and no complete frozen obligation is newly closed. |
| Hermetic release | fail closed | Network was denied, but the run reused shared warm read-only `.lake` artifacts rather than an immutable new checkout, empty-cache cold build, or offline archive restoration. |
| Independent verification | fail closed | The differential probe ran in this worker checkout/cache; two distinct signed runners and an independently implemented minimal release verifier are absent. |

The debt vector remains `[H1, M3, R3]`, `audit_complete=false`, and
`theorem_complete=false`. This worker receipt is provisional `[_]` evidence for
the validation runner itself. It is not `E0/E1`, release, theorem completion,
or master acceptance.
