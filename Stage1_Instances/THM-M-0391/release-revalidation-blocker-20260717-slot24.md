# THM-M-0391 release revalidation blocker

Item: `S56-M-0391-RELEASE`

Worker base revision: `f545339546bf410d5110d7fe44e70bdcf5d8b48e`

Worker base tree: `6dc924134293b2674df7324ff98b6fdaf660159e`

## Verdict

This current-base release revalidation is **blocked** and is not a self-tested
release-phase handoff. No release receipt is refreshed, no state transition is
proposed, and no `AUDIT-Z`, `THEOREM-Z`, release, theorem-completion, or master-
acceptance claim is made.

The exact claim-order tuple is `(v2_execution_rank=5, phase_layer=6,
phase_item_id=S56-M-0391-RELEASE)`. The sole task-state authority records every
`THM-M-0391` phase as `[_]`; in particular the required
`S56-M-0391-VALIDATION` predecessor is not master accepted `[x]`. Its receipt is
provisional ancestor evidence and cannot support release acceptance.

## Dependency and reuse audit

The current authoritative theorem-DAG SHA-256 is
`39dc7ce5f668c527de899e74c99840aef50e6be4c576aaf146abed1b6749275c`,
and the stable target dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The complete required parent inspection order is exactly empty: the target has
no direct hard parents, transitive hard ancestors, hard edges, reuse hints, or
shared lemma groups. The empty sequence was traversed exactly once. No provider
declaration was imported, copied, transported, or credited, and no provider
acceptance was transferred.

The tracked schema-1.1 dependency ledger is historical evidence, not a
current-base ledger. It records theorem-DAG digest
`e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b`
and repository revision `1cc6aa61bb055a5c032297ee457905c849af7608`.
A future admissible revalidation must refresh it to the exact graph and worker
base above while preserving empty `inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`.

## First worker gate failure

The HEAD release contract declares three candidate paths and exactly one exists:
`Stage1_Instances/THM-M-0391/check_release.py`. It is a tracked regular file
with Git blob `ece5308813f987fd3607e90fd71c308c9da5d7e3` and SHA-256
`69dbaacbd705ff25f7d8b823e18735dc5603af910bb774ffafc04d5931adf581`.
The scheduler owns this candidate, and the worker left it byte-for-byte
unchanged as required.

The exact declared command was run:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0391/check_release.py
exit: 1
stdout: empty
stderr: THM-M-0391 release validator: repository HEAD differs from the claimed worker base
```

The validator is hard-bound to ancestor base
`1cc6aa61bb055a5c032297ee457905c849af7608`, tree
`dc3053b55c5724ccb2e6a247e7deffebca9dbb99`, and prior theorem-DAG digest
`e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b`.
It exits before emitting the mandatory single
`stage1-validator-semantic-result/1.0` JSON object. A nonzero exit with empty
stdout cannot become typed self-test evidence, and scheduler policy forbids the
worker from refreshing or replacing this validator. Therefore this worker must
leave no `.stage1-worker-selftest.json`.

The tracked `release-spec.json`, `release-decision.json`,
`release-receipt.json`, and `release-validation.md` are likewise ancestor-bound
historical negative evidence. They truthfully describe an open release, but
their changed invalidation inputs and the failed selected validator prevent a
current phase receipt.

## Current checks

The following read-only current-base checks passed:

```text
python3 Docs/tools/check_stage1_standard.py                           exit 0
python3 Docs/tools/check_stage1_theorem_dag_v2.py                     exit 0
python3 Docs/tools/check_stage1_phase_acceptance_contracts.py         exit 0
python3 scripts/stage1_target.py check                                exit 0
python3 scripts/stage1_target.py show THM-M-0391                      exit 0
cd Formalizations/Lean && lake env lean --trust=0 \
  ../../Stage1_Instances/THM-M-0391/Statement.lean                    exit 0
cd Formalizations/Lean && lake env lean --trust=0 \
  ../../Stage1_Instances/THM-M-0391/Proof.lean                        exit 0
cd Formalizations/Lean && lake env lean --trust=0 \
  ../../Stage1_Instances/THM-M-0391/Validation.lean                   exit 0
git diff --check -- Stage1_Instances/THM-M-0391                       exit 0
```

The Lean commands reused the automation-provided pinned `.lake` symlink
read-only; no `lake update`, `lake build`, dependency fetch/clone, or `.lake`
mutation was performed. These are shared warm nonrelease checks. They elaborate
the exact statement and only the elementary `M0391-B-EE` branch plus an
independently written same-workspace probe. The partial proof reports
`propext` and `Quot.sound`; the probe additionally reports
`Classical.choice`. There is still no declaration proving
`Stage1Instances.THMM0391.MihailescuTarget`.

Fourteen of fifteen frozen root-relevant obligations and exact root composition
remain open at `M4`. The dossier remains `H1` and `R4`, and it lacks a complete
accepted audit, root provenance/trust/TCB closure, immutable empty-cache cold and
offline replay, SBOM/license closure, deterministic evidence bundle, accepted
bundle-derived public projections, two qualifying independent attestations, and
an independently implemented minimal verifier. Consequently
`audit_complete=false` and `theorem_complete=false` remain the only truthful
terminal booleans.

## Retry condition

Install a HEAD-tracked release validator whose unchanged blob already exists at
the next worker base and whose exact declared command emits the mandatory
semantic JSON there. Refresh the empty dependency ledger and exactly one release
receipt on that same base. Release acceptance still requires dependency-ordered
master acceptance through validation and every audit/release gate; theorem
completion separately requires exact kernel closure of the unchanged
Mihailescu root and every root-critical gate.
