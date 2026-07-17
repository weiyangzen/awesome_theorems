# THM-M-0113 proof validator-base blocker

## Scope

This is the target-scoped fail-closed result for `S56-M-0113-PROOF` at
worker base `c09fec56b723330b06490622768353922c42475f` (tree
`0d742d5018bc3b55b0352c28cca02f5d961018fb`). It changes no theorem source,
historical phase receipt, dependency ledger, validator candidate, task-state
authority, generated DAG, lifecycle, debt vector, or acceptance state.

The sole task-state authority records the item as `[_]` with one attempt; its
obligation-tree predecessor is also `[_]` with one attempt. This is unfinished
worker evidence, not master acceptance. The exact claim tuple is
`(v2_execution_rank=262, phase_layer=4,
phase_item_id=S56-M-0113-PROOF)`. The authoritative theorem-DAG SHA-256 is
`c5d478054cf32914251001d24d128b3b21ba29414965d64947d78768329660bd`;
the dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## Dependency And Reuse Audit

The prescribed `parent_inspection_order`, direct-hard-parent list,
transitive-hard-ancestor list, hard-edge list, reuse-hint list, and
shared-lemma-group list are all empty. The complete ordered closure was
traversed exactly once as the empty sequence before proof inspection. No
provider state, receipt, declaration, reusable artifact, proof body, checkbox
credit, or acceptance was consumed, copied, transported, or inherited. The
empty admitted context is not a claim that Hodge decomposition is
mathematically independent.

The tracked target-owned `dependency-reuse-ledger.json` has schema
`stage1-dependency-reuse-ledger/1.1` and truthfully has empty `inspections`,
`reuse_decisions`, and `unresolved_compatibility_obligations`. It remains
historical evidence bound to base
`94009a6bebd743588e09c3b45bfbf18bf9b5c5e3` and theorem-DAG digest
`eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153`.
A current ledger would bind the current base and graph above while retaining
the same empty collections. It is deliberately not refreshed because the
mandatory authority replay below fails, so no truthful current receipt or
self-test packet can consume it.

## First Failed Gate

`G05-AUTHORITY-REPLAY / validator_base_binding_stale` is the first gate that
cannot be repaired within this worker assignment. The HEAD proof contract has
SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`
and declares two scheduler-owned candidates:

- `Stage1_Instances/THM-M-0113/check_proof.py`
- `Stage1_Instances/THM-M-0113/check_proof.sh`

Exactly one exists: `check_proof.py`, SHA-256
`d8699c95e10820abfe28df27ff5e73a1a08783aa76ce3b027d2dacc39429480c`,
Git blob `ba75b9dbf37eb093f982d3f8add2c788c19e439e`. Its worktree, HEAD, and
worker-base bytes agree, so selection is unambiguous and this worker has not
modified it. The exact contract-selected argv was run without shell
interpolation:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0113/check_proof.py
```

It exited `1`, wrote zero stderr bytes, and wrote exactly one JSON object on
stdout (SHA-256
`cb78a08ed2f5d769ab9bcbf3ebac9bc6544dd0bce651a613d95dd18735f792c2`):

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"P01-ARTIFACTS","item_id":"S56-M-0113-PROOF","message":"Proof evidence replay failed: repository HEAD differs from the claimed worker base","open_obligations":26,"phase":"proof","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0113","verdict":"repair_required"}
```

The immutable validator still requires obsolete base
`94009a6bebd743588e09c3b45bfbf18bf9b5c5e3`, tree
`daabee9f9b2c6e98d84b6290f78a209b950485fc`, graph digest
`eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153`,
and the historical worker packet. The worker may not create, refresh, rename,
replace, or delete a declared validator. Therefore this phase is not genuinely
self-tested at the current base. The historical `proof-receipt.json` is not
refreshed or presented as current evidence, and no
`.stage1-worker-selftest.json` is emitted.

The scheduler-owned role map required for master artifact resolution is also
absent from this clone. That is a downstream master-lane condition and does
not authorize the worker to manufacture it.

## Independent Mathematical Blocker

Even after the mechanical validator repair, the assigned positive proof
predicate cannot close for the current frozen statement. The unchanged,
placeholder-free declaration

```text
Stage1Instances.THMM0113.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0113.HodgeDecompositionTarget.{0, 0, 0, 0}
```

was freshly re-elaborated at trust level zero. `HodgeData.isKahler` is an
unconstrained proposition independent of the arbitrary `cohomology` and
`hodgePiece` fields. The countermodel takes the compact zero-dimensional
complex manifold `Fin 0 -> Complex`, sets `isKahler := True`, every
cohomology space to `Complex`, and every Hodge piece to bottom. Degree-zero
spanning would force bottom to equal top and hence `1 = 0`.

The isolated replay copied `Statement.lean` and `Proof.lean` to a fresh
directory under `/tmp`, used the existing pinned `lake env` toolchain with
`--trust=0`, and removed the scratch directory afterward. Both Lean steps
exited `0`. The statement output SHA-256 was
`483a37eb70184d0596b11301c4e15018629fd00bbd8a601fdc6ad7691dcd7e84`,
the proof output SHA-256 was
`ee6378a7e948bc9267ee992aaa0355f1d6717185bddfcf0c3ac7099bd90b2d4c`,
and `Statement.olean` SHA-256 was
`94fe8a2182ea2776a7f9972ca82cd7c88b50fb2f57091d6527a82eb178d975e0`.
Lean reported only `propext`, `Classical.choice`, and `Quot.sound`. A scoped
source scan found no `sorry`, `admit`, `sorryAx`, `native_decide`, bodyless
declaration, unsafe injection, or unverifiable oracle.

This refutes only the frozen abstract encoding, not the mathematical Hodge
decomposition theorem. It closes zero positive obligations and supplies no
positive terminal body or acceptance credit. The frozen registry still has
26 obligations and 49 typed edges with root `M0113-ROOT` at M4. The
obligation-tree predecessor is only worker-provisional `[_]`, not
master-accepted `[x]`, so topology independently blocks positive proof-phase
acceptance.

## Checks Run

All commands ran from this worker clone on 2026-07-17 (Asia/Shanghai). The
automation-provided untracked `Formalizations/Lean/.lake` symlink was used
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
command, or cache mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups, the 1546-target set, v2 DAG, phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 states, typed relationships, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phases, twelve common gates, and 23 source references passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 ordered L0/rework-required targets passed. |
| `python3 scripts/stage1_target.py show THM-M-0113` | 0 | Rank 25; planned lifecycle; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0113/check_anchor_audit.py` | 0 | Frozen target boundary, four candidate rows, twelve probes, and mathlib pin agree. |
| `python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py` | 0 | 26 obligations and 49 typed edges passed; root remains M4. |
| Candidate enumeration and Git-blob comparison | 0 | Exactly `check_proof.py` exists; worktree, HEAD, and worker-base blob are identical. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0113/check_proof.py` | 1 | Exactly one typed `failed` / `repair_required` result reported the obsolete embedded base; `phase_accepted=false`. |
| Isolated trust-zero Lean replay of `Statement.lean` and `Proof.lean` | 0 | The exact negative specialization checked with the three expected axioms. |
| Scoped prohibited-construct scan | 1 | Expected no-match result. |
| `git diff --check -- Stage1_Instances/THM-M-0113 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics in the target-scoped delta. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No false self-test handoff was emitted. |

Structural passes and the checked countermodel cannot override the mandatory
semantic validator failure. `audit_complete=false` and
`theorem_complete=false`.

## Retry Condition And Status Boundary

The scheduler/master lane must publish a refreshed `check_proof.py` (or
exactly one other declared candidate) in an authoritative commit and issue a
fresh claim whose base contains that identical validator blob. A fresh worker
may then bind a current empty dependency ledger and exactly one current phase
receipt and run the selected argv.

That mechanical repair will not make the positive target provable. Reopen
`S56-M-0113-STATEMENT`; replace the disconnected `isKahler` proposition and
arbitrary cohomology/Hodge-piece fields with faithful native constructions or
noncircular law-bearing hypotheses; accept a new statement fingerprint and
real mutation-failure evidence; then freshly freeze and master-accept the
anchor audit and obligation tree before proof execution resumes.
Alternatively, explicitly redirect the item to the checked counterexample
target.

This artifact is a target-scoped blocker only. It grants no state transition,
proof-phase acceptance, accepted receipt ID, provider acceptance transfer,
positive root closure, validation, release, AUDIT-Z, THEOREM-Z, theorem
completion, or master acceptance.
