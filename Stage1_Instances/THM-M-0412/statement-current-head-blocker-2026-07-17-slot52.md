# THM-M-0412 Statement Current-HEAD Blocker

Item `S56-M-0412-STATEMENT` was rechecked at repository base
`6cff7bae0e4547cf9ad8b7abaae20d1abb9fe049` in the exact claim-order position
`(v2 rank 259, phase layer 1, S56-M-0412-STATEMENT)`.

## Task-State And Dependency Boundary

The sole task-state authority records the item as worker-provisional `[_]` with
one attempt. Its intra-theorem predecessor `S56-M-0412-INTAKE` is also `[_]`,
not master-accepted `[x]`, and deliberately records
`unresolved_source_identity` with root vector `H5/M4/R4`.

The complete v2 parent inspection order is empty. The target has no direct hard
parent, transitive hard ancestor, hard edge, reuse hint, or shared lemma group.
The integrated schema-1.1 dependency ledger binds graph digest
`d5b27da9fcb355d5edf9d63ad5d0c4c3ec3410eba4e8e94303d5cef4895a49b9`
for its later obligation-tree attempt and the same stable context digest
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
That integrated ledger binds another phase and is a content-bound input to later
receipts, so this already-`[_]` recheck does not overwrite it without an
invalidation receipt. It contains empty `inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`, as required for this theorem's empty
context. Independently, the current graph's empty closure was
traversed exactly once in the supplied empty order. No provider artifact,
declaration body, receipt, or acceptance state was consumed.

## First Failed Gate

The positive statement gate remains blocked at
`S02-EXACT-TARGET.exact_source_statement_identity`. The authoritative local
catalog supplies only the ambiguous label "Pierce conjecture", a Trygve Nagell
attribution, the year 1948, and a topic gloss about integer points on certain
cubic curves. It supplies no immutable primary publication, theorem/page
locator, equation or curve family, domains, parameters, ordered binders,
hypotheses, conclusion, corrections, proof boundary, or boundary cases.

Repository evidence distinguishes a related 1935 Nagell theorem about
finite-order points on an integral Weierstrass cubic from Nagell's 1948 work on
another Diophantine equation. Neither is identified by the repository as a
"Pierce conjecture". Selecting Nagell-Lutz, Ramanujan-Nagell, Siegel finiteness,
an arbitrary cubic, or the legacy abstract predicate package would therefore
substitute mathematics. No such target is emitted.

Consequently `Statement.lean` remains declaration-free, `statement.json` keeps
its canonical target and fingerprints null or empty, no import-minimality claim
is possible, and all four required statement mutations remain unrun. This is a
truthful target-scoped blocker, not a broadened or weakened theorem.

## Scheduler-Owned Validator Boundary

The HEAD statement contract declares two candidate paths. Exactly one exists:
`Stage1_Instances/THM-M-0412/check_statement.py`, with Git blob
`520d20bcf5395fea157d115af349ac04b2fa6071`. It is tracked, exists unchanged at
this worker base, and was not created, edited, renamed, replaced, or deleted by
this worker. The other declared candidate is absent.

The required authority argv is:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0412/check_statement.py
```

That immutable validator is stale: it content-binds an older base revision,
older theorem-DAG digest, a prior `[ ]` task state, and the earlier
statement-attempt ledger bytes. On current HEAD it exits 1 and emits exactly one
typed `stage1-validator-semantic-result/1.0` JSON object with
`status=failed`, `verdict=repair_required`, `phase_accepted=false`, and
`first_failed_gate=VALIDATOR-INTERNAL-CONSISTENCY`. Its stderr traceback reports
the stale base-revision assertion. Stdout is 453 bytes with SHA-256
`bfdadcbfbab10bd658beaba848761b26bcc0f3cbab23ef132956372b6a197d26`;
stderr is 506 bytes with SHA-256
`4a1e9d3a658c01c35db7181410541831f960e2e73194283c696cefdbbdf5950f`.
Exit status alone is not interpreted as phase acceptance.

The worker is forbidden to refresh a scheduler-owned validator. Because the
unique HEAD candidate cannot self-test the current evidence, no new
`stage1-node-receipt/1.0` phase receipt and no root
`.stage1-worker-selftest.json` are admissible. The previously integrated
`statement-receipt.json` remains the sole phase receipt but is historical and
stale against this HEAD; it cannot support current master acceptance.

## Pinned Lean Boundary

The narrow Lean replays use the existing pinned cache only; no `lake update`,
`lake build`, clone, fetch, or dependency mutation is performed.

`Statement.lean` elaborates with empty stdout and stderr. This checks only the
declaration-free fail-closed source path. `StatementProbe.lean` elaborates six
adjacent Weierstrass APIs under Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` and mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; its stdout SHA-256 is
`52574dd9f0f5feda16279f9af5344d9218c0c6089ce238abe2bcc0c9f2628cbb`
and stderr is empty. Neither replay supplies a canonical target, expression
fingerprint, transport, mutation, proof, or acceptance credit.

The current checks produced these exact results:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, the v2 DAG, and the seven-phase contract passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorems, 10822 blueprint states, 2 hard edges, 5 reuse hints, 311 shared groups, and acyclicity passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all uniform L0 and rework-required. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phases, twelve common gates, and twenty-three source references passed. |
| direct inspection of the current DAG node and integrated schema-1.1 ledger | n/a | Current direct-parent, ancestor, edge, hint, and group closure is empty; the later-phase ledger also contains empty inspections, decisions, and unresolved obligations but is not rewritten as statement evidence. |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/Statement.lean` | 0 | Empty stdout and stderr; declaration-free negative boundary only. |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/StatementProbe.lean` | 0 | Six adjacent API checks; stdout hash as recorded above and empty stderr. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0412/check_statement.py` | 1 | One stdout semantic JSON object with `status=failed` and `phase_accepted=false`; stale-base assertion traceback on stderr. |
| `git diff --check -- Stage1_Instances/THM-M-0412` | 0 | No whitespace errors. |

All evidence is unsigned, target-scoped, nonrelease worker evidence. The
automation-provided `Formalizations/Lean/.lake` symlink is outside the owned
path and is not claimed as a worker change.

## Retry Condition

The scheduler must first publish a current-base immutable statement-validator
candidate if it wants a fresh worker self-test. Independently, positive
statement completion still requires accountable reviewers to admit and approve
an immutable source selecting one exact claim with every incorporated
definition, binder, hypothesis, conclusion, correction, proof boundary, and
boundary case. A later statement worker can then encode only that claim,
minimize imports, fingerprint the elaborated expression and environment, check
all credited transports, and run all four required mutation classes.

No statement completion, proof, phase acceptance, master acceptance, audit
completion, or theorem completion is claimed.
