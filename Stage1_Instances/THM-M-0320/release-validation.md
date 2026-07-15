# THM-M-0320 release reconciliation

Item: `S56-M-0320-RELEASE`

Base revision: `7505614b75de56cf10bbd196a4aaa0ca2a117064` (tree
`730e162a2133e4a077d764043b5e722c1f7feb39`).

## Exact Verdict

The release verdict is `blocked`. Lifecycle remains `planned`, the accepted
root vector remains `[H1, M4, R4]`, and both `audit_complete` and
`theorem_complete` are false. This worker accepts no receipt or obligation and
makes no `AUDIT-Z`, `THEOREM-Z`, release, or theorem-completion claim.

The first failed workflow gate is
`dependency.S56-M-0320-VALIDATION.master_acceptance`
(`S56-10.2-DEPENDENCY-ACCEPTANCE`). The direct validation dependency is only a
provisional `[_]` scheduler projection. Its receipt has `accepted=false`,
`release_grade=false`, `verdict=blocked`, and no accepted receipt or closed
obligation. Its useful kernel observation cannot promote authoritative state.

## Evidence Reconciliation

`Proof.lean` contains a placeholder-free inhabitant of the exact frozen target.
The proof and validation receipts record trust-zero fresh-output warm-cache
replays whose exact root used only `propext`, choice, and `Quot.sound`. The
current target sources and those historical receipt input hashes still agree.
This is meaningful provisional machine evidence, but it is not accepted
`E0/E1`, a cold release replay, or theorem completion.

Structured authority remains unreconciled. `instance.json` is planned at
`[H1, M4, R4]` with no accepted proof state, the local task DAG has
`accepted_states=[]`, and the typed graph retains the pre-proof open cut
`M0320-T-GRAPH` and `M0320-C-CORE`. The receipts also disagree about
`M0320-T-SUBTYPE`: the proof receipt lists it as provisionally kernel-inhabited,
while the validation receipt treats it as an unreconciled architecture node.
The weaker authoritative state controls until master reconciliation.

The historical validation recipe cannot be replayed as current receipt
evidence. It is hard-bound to revision `63a9ed9c...` and rejects current HEAD
`7505614b...` at its base-revision assertion. Its recorded validation interval
also postdates the timestamp of the commit that contains it, so freshness
requires independent review. The current pinned Lake surface now resolves, but
it remains an untracked symlink to shared warm artifacts. Two bounded root
rechecks by the primary worker were inconclusive under concurrent load: one
stopped on a transient olean write failure and one timed out after 300 seconds.
A separate read-only audit agent in this same worker clone reported a complete
exit-0 replay; no proof failure is inferred or release-grade reproduction
claimed.

`AUDIT-Z` fails independently. The exact statement lacks an accepted normalized
expression fingerprint, the primary source lacks accepted pinpoint H0 review,
and no required readable node has independently accepted R0. The task/graph,
source, provenance, trust, freshness, and public projections are not fully
reconciled.

The first release-specific failure is
`S56-RELEASE-IMMUTABLE-CLEAN-INPUT`; this worker uses the shared warm `.lake`
symlink. The next reproduction gate is
`S56-10.6-HERMETIC-COLD-EMPTY-CACHE`. There is no immutable clean empty-cache
cold build, offline archive restoration, accepted foundation and complete
TCB/SBOM/license closure, two distinct signed runner attestations,
independently implemented minimal verifier, protected adversarial CI evidence,
or deterministic content-addressed release bundle.

## Commands And Results

Commands ran from the worker clone on 2026-07-15 (`Asia/Shanghai`). No `lake
update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets and ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0320` | 0 | Rank 686 remains planned, L0/rework-required, and theorem-incomplete. |
| `python3 Stage1_Instances/THM-M-0320/check_anchor_audit.py` | 0 | Anchor boundary, seven probes, and the pinned mathlib revision passed. |
| `python3 Stage1_Instances/THM-M-0320/check_obligation_tree.py` | 0 | Ten obligations and 22 typed edges passed; the authoritative root remained open. |
| `cd Formalizations/Lean && timeout 30 lake env lean --version` | 0 | Pinned Lean 4.29.0 at commit `98dc76e3...` resolved; the shared warm `.lake` remained unmodified. |
| `timeout 30 /usr/bin/bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --unshare-net --die-with-parent --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv TZ UTC --setenv LEAN_NUM_THREADS 1 --setenv STAGE1_SKIP_RECEIPT_CHECK 1 --setenv STAGE1_OUTER_NETWORK_ISOLATED 1 /usr/bin/python3 -I -B Stage1_Instances/THM-M-0320/check_validation.py --probe` | 1 | The historical validator rejected current HEAD at its snapshot assertion, before Lean replay. |
| `timeout 300 bash Stage1_Instances/THM-M-0320/check_proof.sh` (attempts 1 and 2) | 1, then 124 | First attempt stopped on a transient olean write failure; second timed out after 300 seconds under concurrent load. Neither result is proof-failure or release evidence. |
| `python3 -I -B Stage1_Instances/THM-M-0320/check_release.py` | 0 | Current hashes, authority, receipt conflicts, and blocked terminal decisions agreed. |
| `for f in <three release JSON files> .stage1-worker-selftest.json; do python3 -m json.tool $f >/dev/null || exit; done` | 0 | All structured release artifacts parsed separately. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0320-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0320/check_release.py` | 0 | Checker compiled without repository bytecode output. |
| `git diff --check -- Stage1_Instances/THM-M-0320 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics. |

Retry requires dependency-ordered master acceptance and append-only
task/graph/obligation/expression reconciliation, followed by accepted H0/R0 and
foundation/provenance/TCB/SBOM/license evidence, immutable cold offline
reproduction, distinct signed verification, the independent minimal verifier,
protected CI, a deterministic bundle, and final separate master decisions for
`AUDIT-Z` and `THEOREM-Z`.

Status boundary: this artifact self-tests only the truthful negative release
decision. It grants no accepted `M0`, `E0/E1`, `H0`, `R0`, `AUDIT-Z`,
`THEOREM-Z`, release, theorem completion, or master acceptance.
