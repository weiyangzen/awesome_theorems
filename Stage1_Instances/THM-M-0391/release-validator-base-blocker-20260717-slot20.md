# THM-M-0391 release validator-base blocker

## Scope and verdict

This is the target-scoped fail-closed result for `S56-M-0391-RELEASE` at
worker base `a808e6ec7a16a99e6ab3471085952287d4e24728` (tree
`9a77a1024e5129433c6dc9db23455b64c811abe1`). The verdict is `blocked`.
This report changes no theorem source, prior phase receipt, lifecycle, debt
vector, task-state authority, DAG projection, validator candidate, or
acceptance state.

The exact claim tuple is `(v2_execution_rank=5, phase_layer=6,
phase_item_id=S56-M-0391-RELEASE)`. The sole task-state authority records the
item as `[_]` with three attempts and dependency `S56-M-0391-VALIDATION`.
That predecessor is also only `[_]`, not master accepted `[x]`.

## Dependency and reuse audit

The current theorem-DAG SHA-256 is
`de71a3ca00b2ac64f96f4a0b7363cf56d09acb943716310332e693d9c9503c6a`.
The target dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The complete supplied `parent_inspection_order` is empty. The authoritative
node has no direct hard parents, transitive hard ancestors, hard edges, reuse
hints, or shared lemma groups. The empty closure was traversed exactly once;
no provider body, receipt, proof credit, or acceptance was copied, imported,
transported, consumed, or inherited.

The tracked `dependency-reuse-ledger.json` has schema
`stage1-dependency-reuse-ledger/1.1` and the required empty `inspections`,
`reuse_decisions`, and `unresolved_compatibility_obligations`. It is stale for
this claim because it binds graph digest
`e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b`
and revision `1cc6aa61bb055a5c032297ee457905c849af7608`. Refreshing the ledger alone
cannot make the assigned phase self-tested when the mandatory scheduler-owned
validator cannot run at the current base, so the prior ledger and release
packet were not partially rewritten.

## First failed worker gate

The HEAD release contract declares three candidate paths. Exactly one exists:
`Stage1_Instances/THM-M-0391/check_release.py`, a tracked regular file with Git
blob `ece5308813f987fd3607e90fd71c308c9da5d7e3` and SHA-256
`69dbaacbd705ff25f7d8b823e18735dc5603af910bb774ffafc04d5931adf581`.
Its HEAD blob equals its worker-base blob. The worker did not create, refresh,
rename, replace, or delete any validator candidate.

The exact authority-selected command produced:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0391/check_release.py
exit: 1
stdout: empty
stderr: THM-M-0391 release validator: repository HEAD differs from the claimed worker base
```

`G05-AUTHORITY-REPLAY / validator_base_stale` is therefore the first worker
gate failure. The validator hard-codes base
`1cc6aa61bb055a5c032297ee457905c849af7608`, tree
`dc3053b55c5724ccb2e6a247e7deffebca9dbb99`, and obsolete authority and target
hashes. It exits before emitting the mandatory single
`stage1-validator-semantic-result/1.0` JSON object. The worker is forbidden to
repair this scheduler-owned file. Consequently the assigned phase is not
genuinely self-tested: no release receipt was refreshed and no
`.stage1-worker-selftest.json` was written.

## Release boundary

Release independently fails `G02-TOPOLOGY`: the validation phase and all its
predecessors are `[_]`, not dependency-ordered master accepted `[x]`. The
validation receipt is provisional ancestor evidence, binds revision
`66630bedafa43a769b94226b7431188dea47edf1`, and lacks current normalized
acceptance and self-test fields.

The exact statement and statement transport elaborate with `--trust=0`.
`Proof.lean` and `Validation.lean` likewise elaborate the elementary
`M0391-B-EE` branch and its same-workspace independent reconstruction. No
declaration proves `Stage1Instances.THMM0391.MihailescuTarget`; fourteen of
fifteen frozen root-relevant obligations and exact root composition remain
open. The root stays `H1/M4/R4`. The dossier also lacks a complete accepted
audit, H0/R0 review, root provenance/trust/TCB closure, immutable empty-cache
cold/offline replay, SBOM/license closure, deterministic evidence bundle,
bundle-derived accepted public projections, two qualifying independent
attestations, and an independently implemented minimal verifier. Thus
`audit_complete=false` and `theorem_complete=false`, with no release or master
acceptance.

## Checks run

All commands ran inside this worker clone. The automation-provided pinned
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network operation, or `.lake` mutation was performed.
The structural checks below ran before this blocker file was added; final
owned-path verification then ran `git diff --check` and strict JSON parsing.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6, manifest, v2 DAG, phase contract, and skill structure passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 states, typed edges, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phase contracts and twelve common gates passed. |
| `python3 scripts/stage1_target.py check` | 0 | The 1546-target uniform-L0 manifest passed. |
| `python3 scripts/stage1_target.py show THM-M-0391` | 0 | Rank 5, planned, rework required, theorem incomplete. |
| candidate enumeration and HEAD/base blob comparison | 0 | Exactly one candidate exists and its blob is unchanged. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0391/check_release.py` | 1 | Empty stdout; stale base rejected before semantic JSON. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0391/Statement.lean` | 0 | Exact target and transport elaborated. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0391/Proof.lean` | 0 | `M0391-B-EE` elaborated; axioms: `propext`, `Quot.sound`. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0391/Validation.lean` | 0 | Same-workspace reconstruction elaborated; axioms also include `Classical.choice`. |
| `git diff --check -- Stage1_Instances/THM-M-0391 .stage1-worker-selftest.json` | 0 | The target-owned handoff has no whitespace errors. |
| strict `python3 -m json.tool` pass over every target-owned JSON file | 0 | All existing structured JSON remains syntactically valid. |

## Retry condition

The scheduler/master lane must publish a refreshed HEAD-tracked release
validator whose unchanged blob is present at the next worker base and whose
exact declared command emits one valid semantic JSON object against that base.
It must publish the authority-owned release role map before review. A later
release acceptance still requires dependency-ordered master acceptance through
validation, complete `AUDIT-Z`, and every immutable replay, supply-chain,
bundle, public, and independent-verification gate. `THEOREM-Z` separately
requires exact kernel closure and composition of the unchanged root.
