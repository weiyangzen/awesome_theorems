# THM-M-0129 current-base statement blocker

## Scope and authority

This is the target-scoped fail-closed result for
`S56-M-0129-STATEMENT` at worker base
`e19e77ec08fca6a8a9c45a003c9904020dae8382` (tree
`53ff0ebe013670fc0332bf326fd860b29857ddab`). It changes no Lean source,
phase receipt, dependency ledger, validator candidate, task-state authority,
theorem-DAG projection, lifecycle, debt vector, or acceptance state.

The exact claim tuple is
`(v2_execution_rank=281, phase_layer=1, phase_item_id=S56-M-0129-STATEMENT)`.
The assigned and observed theorem-DAG SHA-256 is
`53622c848d6a0d8327bba8cd22bf45463f0dd8acb7ea0af2884713983e76c91f`;
the stable dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

`Docs/Stage1_Blueprint_v2.md` records both the intake predecessor and this
statement item as `[_]` with one attempt. That is unfinished worker evidence,
not master acceptance. The existing `statement-receipt.json` is historical
negative evidence: it is `accepted=false`, has no statement fingerprint, and
binds base `dae1951609072752d49d111bf00e78e4512f2d14`, an obsolete theorem-DAG
digest, and the former `[ ]`/attempt-zero cursor. It is not refreshed or
credited as current evidence.

## Dependency and reuse audit

The supplied `parent_inspection_order` and every direct-parent,
transitive-ancestor, hard-edge, reuse-hint, and shared-group list are exactly
empty. The complete closure was traversed exactly once as `[]` before any
Lean replay. No provider state, receipt, declaration, body, import, copy,
transport, acceptance, or proof credit was consumed or inherited. No proof
work was performed. The tracked schema-1.1 ledger truthfully has empty
`inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`, but remains bound to the historical
base. A ledger-only rewrite cannot repair the immutable validator and would
invalidate the historical receipt bindings, so it was not rewritten.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_semantically_stale_for_current_worker_base`
is the first worker-unrepairable gate. The HEAD phase contract has SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`
and declares two candidate paths. Exactly one exists:
`Stage1_Instances/THM-M-0129/check_statement.py`, SHA-256
`79af4075049bdbde1ea3e1580519e5eac9df414c274074b54f563d8fe1fb6e08`,
Git blob `cc7f95c83d02599804eb6b487cb436601cba8796`. Its worktree and HEAD bytes
agree. This worker did not create, refresh, replace, rename, or delete a
validator candidate.

The mandatory command

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0129/check_statement.py
```

exited `1`, wrote no stderr, and emitted exactly one 436-byte JSON object
(plus its final newline), SHA-256
`f6fd12d153e21fcea837646b9b2b151a572c06bfb993143f10a1f5f3f209e557`:

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"S01-ARTIFACTS","item_id":"S56-M-0129-STATEMENT","message":"statement packet check failed: AssertionError: ","open_obligations":1,"phase":"statement","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0129","verdict":"repair_required"}
```

The stdout satisfies the typed result schema, but its semantics are
`failed` / `repair_required`, with both phase flags false. The immutable
validator asserts historical receipt/base/cursor and worker-diff conditions;
it therefore cannot validate current integrated HEAD. Exit zero from other
checks cannot override this semantic result, and a worker may not repair the
scheduler-owned validator. Consequently no current-base phase receipt or
`.stage1-worker-selftest.json` can be truthfully emitted.

## Positive statement gate

Independently, `S02-EXACT-TARGET` and `S03-MUTATIONS` remain open. Shimura's
1973 Main Theorem and adjacent results distribute construction, coefficient,
modularity, cuspidality, and Hecke assertions across different hypotheses and
conventions. Parameterization, normalization, target level and character,
conductor, parity, squarefree admissibility, low-weight cuspidality, bad-prime
range, and degenerate cases still require an approved exact selection or
explicit composition. Selecting one result narrows the intake; silently
conjoining them invents a different root.

`Statement.lean` therefore remains declaration-free. At trust level zero its
two adjacent imports elaborate, while `StatementInfrastructure.lean` checks
ordinary `CuspForm`, `DirichletCharacter`, and conductor interfaces and
confirms that `HalfIntegralWeightModularForm`, `ShimuraLift`, and
`ShimuraCorrespondence` are absent from the pinned closure. These are bounded
negative observations, not a canonical target, target-minimal import proof,
expression/environment fingerprint, checked transport, or mutation
certificate.

## Checks run

All commands ran in this worker clone on 2026-07-17 (Asia/Shanghai). The
automation-provided `.lake` symlink was reused without update, build, clone,
fetch, checkout, network access, or dependency mutation.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All assurance groups and projections passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 nodes, 10822 phase states, typed relationships, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phase contracts, twelve common gates, and twenty-three references passed. |
| `python3 scripts/stage1_target.py check` | 0 | The 1546-target L0/rework-required manifest passed. |
| `python3 scripts/stage1_target.py show THM-M-0129` | 0 | Rank 47, planned, legacy evidence unaccepted, theorem incomplete. |
| Candidate enumeration and Git-blob comparison | 0 | Exactly one candidate exists and its worktree/HEAD bytes agree. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0129/check_statement.py` | 1 | One typed `repair_required` result; `phase_accepted=false`. |
| From `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0129/Statement.lean` | 0 | Declaration-free boundary module elaborated; no target credit. |
| From `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0129/StatementInfrastructure.lean` | 0 | Three interfaces and three expected-missing identifiers checked. |
| `git diff --check -- Stage1_Instances/THM-M-0129 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics before this artifact was added. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No handoff exists because mandatory replay and the positive predicate failed. |

## Retry condition and status boundary

The scheduler/master lane must publish a current-authority validator at
exactly one declared path and issue a fresh claim whose immutable base
contains that blob. Positive closure separately requires master acceptance of
intake, independent approval of an exact primary result or explicit owned
composition, reconciliation of every theorem-changing convention, sufficient
pinned interfaces, a kernel-elaborated target and fingerprints, target-import
minimality, checked transports, and all four mutation classes.

This artifact is blocker evidence only. It grants no state transition, phase
receipt, self-test handoff, statement or proof credit, inherited provider
acceptance, `AUDIT-Z`, `THEOREM-Z`, theorem completion, or master acceptance.

