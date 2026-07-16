# THM-M-0395 release revalidation blocker

Item: `S56-M-0395-RELEASE`

Worker base revision: `738c0e35f61cf22c1ab5e31a5cd0ad6432f12f01`

Worker base tree: `90fca08279c74cf64ace6ae4fa9fbe4fa31896dc`

## Verdict

This release revalidation is **blocked** and is not a self-tested release-phase
handoff. No release receipt is refreshed, no state transition is proposed, and
no `AUDIT-Z`, `THEOREM-Z`, theorem-completion, release-acceptance, or
master-acceptance claim is made.

The exact claim-order tuple is `(v2_execution_rank=8, phase_layer=6,
phase_item_id=S56-M-0395-RELEASE)`. The sole task-state authority records all
seven `THM-M-0395` phases as `[_]`; in particular the required
`S56-M-0395-VALIDATION` predecessor is not master accepted `[x]`.

## Dependency and reuse audit

The current authoritative theorem-DAG SHA-256 is
`6ce46e0d9e79e1a40c423ae1074db34e889702b9a5b5989034cd462615fed604`,
and the stable target dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The complete required parent inspection order is exactly empty: the target has
no direct hard parents, transitive hard ancestors, hard edges, reuse hints, or
shared lemma groups. Therefore no provider declaration was imported, copied,
transported, or credited, and no provider acceptance was transferred.

The tracked `dependency-reuse-ledger.json` is historical evidence, not a
current-base ledger: it records theorem-DAG digest
`e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b`
and repository revision `1cc6aa61bb055a5c032297ee457905c849af7608`.
It cannot support a fresh release receipt on this base. A current ledger would
still have exactly empty `inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`; refreshing it without a self-testable
phase receipt would not make the release handoff admissible.

## First worker gate failure

The HEAD release contract selects exactly one validator candidate,
`Stage1_Instances/THM-M-0395/check_release.py`, and requires its stdout to be
exactly one `stage1-validator-semantic-result/1.0` JSON object. The exact
declared command was run:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0395/check_release.py
exit: 1
stdout: empty
stderr: release-decision: FAIL: observed theorem-DAG digest drifted
```

The tracked validator has Git blob
`cb176d3f2c714b9bc94c282876c86545e6a56c57` and hard-codes the obsolete graph
digest above. The current graph has the task-provided digest `6ce46e0d...`.
The validator exits before emitting semantic JSON, so command failure cannot
be converted into `phase_accepted=false` evidence and exit zero cannot be
inferred. Scheduler policy also makes validator-candidate paths
scheduler-owned and rejects a worker change to this file. This worker therefore
leaves the selected validator untouched and fails closed.

The existing `release-spec.json`, `release-decision.json`, and
`release-receipt.json` are likewise bound to ancestor revision
`1cc6aa61bb055a5c032297ee457905c849af7608` and tree
`dc3053b55c5724ccb2e6a247e7deffebca9dbb99`. They are historical negative
evidence only and are not current receipts for this claim.

## Checks that remain valid

The following current-base checks passed without modifying `.lake`:

```text
python3 Docs/tools/check_stage1_standard.py                              exit 0
python3 Docs/tools/check_stage1_theorem_dag_v2.py                        exit 0
python3 Docs/tools/check_stage1_phase_acceptance_contracts.py            exit 0
python3 scripts/stage1_target.py check                                   exit 0
python3 scripts/stage1_target.py show THM-M-0395                         exit 0
python3 Stage1_Instances/THM-M-0395/check_anchor_audit.py                exit 0
python3 Stage1_Instances/THM-M-0395/check_obligation_tree.py              exit 0
python3 Stage1_Instances/THM-M-0395/check_validation.py                   exit 0
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 /usr/bin/bash \
  ../../Stage1_Instances/THM-M-0395/check_proof.sh                        exit 0
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 /usr/bin/bash \
  ../../Stage1_Instances/THM-M-0395/check_validation_lean.sh              exit 0
```

The Lean commands used the pre-existing pinned cache read-only, disposable
output directories, and `--trust=0`. They elaborated the frozen statement,
three local elementary finiteness transports, and three independently written
same-workspace probes. The reported axioms were only `propext`,
`Classical.choice`, and `Quot.sound`. The stream-fd warnings emitted by Lean in
the restricted worker sandbox did not change either exit result.

These are warm, nonrelease checks. They prove neither the Faltings root nor an
accepted frozen proof obligation. The exact root remains `H1/M4/R3`; the
receipts close zero frozen obligations, the architecture marks only statement
transport `M0395-S3` checked, and exact child-to-parent root composition remains
open.
The current validation receipt is provisional ancestor evidence, and the
release dossier still lacks accepted H0/R0 review, complete root
provenance/trust/TCB closure, immutable empty-cache cold and offline replay,
SBOM/license closure, a deterministic evidence bundle, accepted public
projections, two qualifying independent attestations, and an independently
implemented minimal verifier.

## Retry condition

Install a HEAD-tracked release validator whose blob is already present at the
next worker base and whose exact declared command emits the mandatory semantic
JSON against the then-current theorem DAG. Refresh the empty dependency ledger
and release artifacts on that same base. Release acceptance additionally
requires dependency-ordered master acceptance through validation and every
`AUDIT-Z`/release-contract gate; theorem completion separately requires exact
kernel closure of the unchanged Faltings root and every root-critical gate.

Because the mandatory selected validator did not produce a semantic result,
this worker intentionally leaves no `.stage1-worker-selftest.json`.
