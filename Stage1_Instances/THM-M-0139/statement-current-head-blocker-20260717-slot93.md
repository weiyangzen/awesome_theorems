# THM-M-0139 current-HEAD statement blocker

Item: `S56-M-0139-STATEMENT`

Worker base revision: `6cff7bae0e4547cf9ad8b7abaae20d1abb9fe049`

Worker base tree: `28c148dbd84fbd549c749f060c92c9a3f00b16d0`

Worker verdict: `blocked`

Proposed state: unchanged `[_]`

Phase accepted: `false`

## First failed gate

`G05-AUTHORITY-REPLAY / validator_candidate_stale_at_current_base`

The HEAD statement contract declares two scheduler-owned validator candidates. Exactly one exists:
`Stage1_Instances/THM-M-0139/check_statement.py`. It is tracked at this worker base with SHA-256
`e80831652f0e66266d0e6a1290ee91d0bc1ff7af3c0fd58e608f78790063f780` and Git blob
`0c386f309d0f86194d5357f4b52e61d5af6e939a`; this worker did not create, modify, rename, replace, or
delete it. The required argv was run exactly as selected by the contract:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0139/check_statement.py
```

It exited `1`, wrote no stdout, and wrote exactly
`THM-M-0139 statement validator: repository HEAD differs from the claimed worker base` to stderr.
The validator hard-codes the earlier base `94009a6bebd743588e09c3b45bfbf18bf9b5c5e3`, tree
`daabee9f9b2c6e98d84b6290f78a209b950485fc`, graph digest
`eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153`, and statement item state
`[ ]` with zero attempts. The current authorities instead record graph digest
`80cf05109d5b3776b7defe95fdb591b216894a57ecbb7180a59f315a67d487d5` and statement state `[_]`
with one attempt. Thus the validator produced no required
`stage1-validator-semantic-result/1.0` JSON object. The worker is forbidden to refresh a
scheduler-owned candidate, so no lawful current-base node receipt or self-test handoff can be
produced.

## Claim order and dependency audit

The exact claim tuple is `(v2_execution_rank=289, phase_layer=1,
phase_item_id=S56-M-0139-STATEMENT)`. The target dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

The supplied `parent_inspection_order` is the empty sequence. The target node declares no direct
hard parent, transitive hard ancestor, incoming hard edge, reuse hint, or shared lemma group, so the
complete closure was traversed exactly once with zero parent IDs. There were no parent phase states,
receipts, declarations, proof bodies, or reusable artifacts to consume. No exact reuse, checked
transport, provider checkbox state, acceptance, evidence credit, or proof credit is transferred. The
empty declared closure is not a claim of mathematical independence.

The checked-in `dependency-reuse-ledger.json` has schema
`stage1-dependency-reuse-ledger/1.1` and truthfully empty `inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`, but it currently belongs to the later anchor-audit attempt and
binds repository revision `1cc6aa61bb055a5c032297ee457905c849af7608` and graph digest
`e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b`. The integrated statement
receipt instead binds the earlier statement ledger bytes. Because this assignment is already `[_]`,
there is no invalidation receipt authorizing replacement, and the immutable validator cannot replay,
this recheck does not rewrite either historical packet. The current graph/context/empty closure are
bound explicitly above.

## Statement boundary

The positive statement predicate also remains false. The owned evidence still lacks immutable
primary-source bytes or an independently accepted exact transcription of Kazhdan-Lusztig (1979),
Conjecture 1.5. Consequently the Weyl-group parametrization, Bruhat orientation, dot action,
longest-element transforms, order of the Verma/simple indices, and polynomial index normalization
remain theorem-changing open choices. Selecting one from memory would broaden, narrow, or substitute
the source claim.

`Statement.lean` therefore remains only a four-import substrate probe. It elaborates the Coxeter
length, polynomial evaluation, simple-object, Artinian-object, and Noetherian-object interfaces but
declares no canonical target, expression fingerprint, alternate transport, mutation fixture, proof,
axiom, or placeholder. The legacy `S1_M_055.StatementShape` quantifies over freely supplied abstract
data and does not construct or bind the source-native category-O and Kazhdan-Lusztig objects, so it
receives no statement or proof credit. No canonical target-minimal import set or meaningful
removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation suite exists.
The intake prerequisite is also only `[_]`, not dependency-ordered master-accepted `[x]`.

## Commands and exact results

All Lean checks used the automation-provided canonical `.lake` symlink read-only. No `lake update`,
`lake build`, dependency clone/fetch, checkout, or package mutation was run.

| Command | Exit | Result boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, the 1546 uniform-L0 targets, v2 theorem DAG, seven-phase contract, and execution skill passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 blueprint states, two hard edges, five reuse hints, 311 shared groups, and acyclicity passed |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | seven phase contracts, twelve common gates, and 23 source references passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0139` | 0 | rank 55, planned, legacy artifacts unaccepted, theorem incomplete |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0139/Statement.lean` | 0 | the unchanged substrate probe elaborated; sandbox stream-fd warnings preceded the five expected `#check` types and do not establish an exact target |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0139/check_statement.py` | 1 | no stdout; the immutable validator rejected current HEAD at its earlier-base guard |
| `test ! -e .stage1-worker-selftest.json` | 0 | no handoff exists because the mandatory validator did not emit semantic JSON and the positive statement predicate remains false |
| `git diff --check -- Stage1_Instances/THM-M-0139 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics in the target-owned delta |

## Retry condition and status boundary

The scheduler/master lane must first refresh exactly one declared validator candidate at an
authoritative checkpoint and issue a fresh claim whose base contains that identical candidate and
current authority bindings. The source lane must also admit and independently approve immutable
Conjecture 1.5 bytes or an exact transcription with pinpoint locator, incorporated definitions,
notation ledger, all assumptions, corrections and errata disposition, and boundary cases. After
dependency-ordered intake acceptance, a fresh statement worker can encode only that approved claim,
provide the required pinned semantic interfaces, prove import minimality, bind the elaborated
expression and environment, compile every credited transport, and execute all four mutation classes.

This file is target-scoped blocker evidence only. It does not replace the historical statement
receipt, alter the authoritative `[_]` state, claim a current self-test, satisfy the positive phase
predicate, transfer provider acceptance, prove the theorem, decide `AUDIT-Z` or `THEOREM-Z`, or
support master acceptance. No `.stage1-worker-selftest.json` is emitted.
