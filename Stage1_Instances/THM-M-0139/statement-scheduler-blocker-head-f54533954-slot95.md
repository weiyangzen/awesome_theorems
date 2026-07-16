# THM-M-0139 statement scheduler blocker

Item: `S56-M-0139-STATEMENT`  
Worker base: `f545339546bf410d5110d7fe44e70bdcf5d8b48e`  
Claim order: `(289, 1, S56-M-0139-STATEMENT)`  
Verdict: `blocked`; no new self-test handoff

## First failed gate

`G05-AUTHORITY-REPLAY.validator_candidate_semantically_stale_for_current_worker_base`

The HEAD statement contract declares two scheduler-owned candidates. Exactly one exists:
`Stage1_Instances/THM-M-0139/check_statement.py`, SHA-256
`e80831652f0e66266d0e6a1290ee91d0bc1ff7af3c0fd58e608f78790063f780`, Git blob
`0c386f309d0f86194d5357f4b52e61d5af6e939a`. It is present with that same blob at the immutable
worker base, so candidate selection is unambiguous.

The mandatory argv still cannot produce valid current evidence. The unchanged validator hard-codes
base `94009a6bebd743588e09c3b45bfbf18bf9b5c5e3` and tree
`daabee9f9b2c6e98d84b6290f78a209b950485fc`. At the current base it exits `1`, writes no stdout,
and reports `repository HEAD differs from the claimed worker base` on stderr. Therefore its stdout
is not the required single `stage1-validator-semantic-result/1.0` JSON object. The worker is
forbidden to refresh, replace, rename, create, or delete a declared candidate. Exit zero from other
checks, an undeclared adapter, or the historical base-bound receipt cannot repair this
scheduler-ownership gate.

No new phase receipt or `.stage1-worker-selftest.json` is emitted. The existing
`statement-receipt.json` remains historical provisional evidence bound to its own earlier base; it
is not represented as a current replay or master acceptance.

## Dependency and reuse audit

The authoritative theorem-DAG SHA-256 is
`39dc7ce5f668c527de899e74c99840aef50e6be4c576aaf146abed1b6749275c`; the target context digest is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`. Direct hard parents,
transitive hard ancestors, hard edges, reuse hints, shared groups, and `parent_inspection_order` are
all exactly empty. The required traversal was therefore the empty traversal. No provider source,
declaration body, receipt, import, copy, transport, checkbox state, acceptance, or proof credit was
consumed or transferred. This empty graph context is not a mathematical-independence claim.

The current `dependency-reuse-ledger.json` has schema
`stage1-dependency-reuse-ledger/1.1` and still records an empty closure, but it is bound to the later
anchor-audit claim, graph digest
`e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b`, and repository revision
`1cc6aa61bb055a5c032297ee457905c849af7608`. This failed replay does not rewrite it: a ledger-only
delta cannot produce a lawful statement self-test and would invalidate the already-tracked
anchor-audit evidence that binds those bytes. A fresh validator-eligible statement run must refresh
the canonical ledger for its own base and claim order.

## Exact statement boundary

The positive statement predicate independently remains false. The owned evidence contains no
immutable primary-source bytes or independently accepted exact transcription of Kazhdan and
Lusztig (1979), Conjecture 1.5. Its Weyl parametrization, Bruhat orientation, dot-action and
longest-element convention, Verma/simple index order, polynomial-index normalization, complete
hypotheses, and boundary cases are not frozen. Choosing a remembered formula would risk
substituting a conventionally related proposition.

`Statement.lean` elaborates with the pinned Lean 4.29.0/mathlib environment, but deliberately checks
only five adjacent interfaces and declares no canonical target, transport, mutation fixture, or
proof body. The legacy `S1_M_055.StatementShape` quantifies over freely supplied abstract data; it
does not construct or bind the concrete regular-integral category-O objects and source conventions.
Neither file supplies an exact proposition, expression fingerprint, import-minimality result,
checked transport, mutation result, or proof credit.

The assigned item and its intake predecessor are both authoritatively `[_]`, not master-accepted
`[x]`. No statement acceptance, proof credit, `AUDIT-Z`, `THEOREM-Z`, or theorem completion is
claimed.

## Validation record

| Command | Exit | Result boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 1, expected after owned edit | passed before the blocker was added; afterward the target inventory differs from the read-only theorem-DAG projection until master regeneration |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1, expected after owned edit | passed before the blocker was added; afterward reports the same deterministic target-inventory drift; the worker did not edit the generated DAG |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | seven phases, twelve common gates, twenty-three source references |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets |
| `python3 scripts/stage1_target.py show THM-M-0139` | 0 | rank 55, planned, legacy artifacts unaccepted, theorem incomplete |
| from `Formalizations/Lean`: `lake env lean --trust=0 ../../Stage1_Instances/THM-M-0139/Statement.lean` | 0 | pinned adjacent-interface probe elaborated; no target/proof credit |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0139/check_statement.py` | 1 | empty stdout; obsolete-base diagnostic on stderr; no typed semantic result |

The automation-provided canonical `.lake` symlink was reused read-only. No update, build, clone,
fetch, or dependency mutation was performed.

## Retry condition

The scheduler must refresh one declared statement validator, commit it, and issue a fresh claim
whose worker base contains that identical blob. Separately, phase acceptance still requires an
immutable or independently accepted exact source transcription, a refreshed empty schema-1.1
ledger, the exact kernel-elaborated proposition with minimal pinned imports and expression/environment
fingerprints, all credited transports, and all four required mutations. This target-scoped artifact
changes no task state and intentionally leaves no worker self-test handoff.
