# THM-M-0135 statement revalidation: validator-authority blocker

## Scope

This is target-scoped fail-closed evidence for `S56-M-0135-STATEMENT` at worker base
`6cff7bae0e4547cf9ad8b7abaae20d1abb9fe049` (tree
`28c148dbd84fbd549c749f060c92c9a3f00b16d0`). The authoritative claim tuple is
`(v2_execution_rank=285, phase_layer=1, phase_item_id=S56-M-0135-STATEMENT)`.
`Docs/Stage1_Blueprint_v2.md`, the sole task-state authority, records the item as `[_]` with one
attempt. This run is therefore a current-HEAD revalidation of an unfinished historical handoff; it
does not propose another state transition and cannot confer master acceptance.

The theorem-DAG SHA-256 is
`80cf05109d5b3776b7defe95fdb591b216894a57ecbb7180a59f315a67d487d5`; the stable dependency-context
SHA-256 is `068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## First Failed Gate

`G05-AUTHORITY-REPLAY.validator_candidate_not_executable_at_current_base` is the first gate that
cannot be repaired by this worker. The mandatory HEAD phase contract declares two scheduler-owned
statement-validator paths:

- `Stage1_Instances/THM-M-0135/check_statement.py`
- `Stage1_Instances/THM-M-0135/check_statement_artifacts.py`

Exactly one exists. `check_statement.py` is tracked at this worker base with SHA-256
`0ffeb38cbfdf219212796be25c0ecc41fe391d0e1302a1c8d3d4dee03ea61e41` and Git blob
`ad064f2de6cceb2da5343a004146388b022697bc`, so selection is unambiguous and its HEAD/base blob
identity passes. However, the immutable candidate binds the earlier implementation base
`307c34d30fc3763c82a944a142ae922b48ff18aa`. Running the contract-selected argv exactly,

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0135/check_statement.py
```

exited `1`, wrote

```text
THM-M-0135 statement validator: repository HEAD differs from the claimed worker base
```

to stderr, and emitted empty stdout. Thus there is no single stdout JSON object with schema
`stage1-validator-semantic-result/1.0`. The historical receipt's successful command record cannot
substitute for a replay at this base. The worker is forbidden to refresh, replace, rename, create,
or delete a validator candidate, so editing that base guard or its bound bytes would invalidate the
only eligible candidate rather than repair it.

Because the phase is not genuinely self-tested at this base, this run writes no replacement
`stage1-node-receipt/1.0` and no `.stage1-worker-selftest.json`. The tracked historical receipt is
observation-only evidence: it binds the earlier base and graph and cannot support this revalidation.

## Dependency And Reuse Audit

The exact `parent_inspection_order` is empty. Direct hard parents, transitive hard ancestors, hard
edges, reuse hints, and shared groups are all empty. The complete empty closure was traversed once
before any possible proof work. There are no parent phase states, receipts, declarations, terminal
proof bodies, or reusable artifacts to inspect or consume. No provider acceptance, proof body, or
evidence credit is transferred. The empty graph context is not a mathematical-independence claim.

The tracked `dependency-reuse-ledger.json` has schema `stage1-dependency-reuse-ledger/1.1` and
truthfully records empty `inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`, but it binds the earlier graph
`8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47` and repository
`307c34d30fc3763c82a944a142ae922b48ff18aa`. It is not refreshed in this validator-blocked run:
ledger-only changes cannot produce the mandatory authority-selected semantic replay or a lawful
self-test handoff. The current graph, context, and empty closure are bound above.

## Statement Boundary

No current source or mathematical-interface evidence repairs the positive statement predicate.
The repository catalog still identifies only the family of Macdonald identities on affine root
systems. It does not select an immutable source edition, exact page and numbered identity, affine
type, positive-root and multiplicity conventions, Weyl shift and sign, normalization, coefficient
domain, completion, ordered binders, hypotheses, conclusion, boundary cases, or errata disposition.
Selecting one member would still substitute proposition-changing mathematics.

The target-owned `Statement.lean` remains a declaration-free interface probe. Trust-zero
elaboration checks `AddMonoidAlgebra`, `HahnSeries`, Coxeter length parity, and finite
`RootPairing.weylGroup`; it supplies no canonical target or mutation evidence. The legacy
`S1_M_051.lean` shape equates arbitrary finite-support fields and does not construct the completed
denominator product or alternating Weyl expression. Accordingly the exact target, target-import
minimality, expression/environment fingerprint, credited transports, and all four required
statement mutation classes remain open. The intake predecessor is also only `[_]`, not `[x]`, so
dependency-ordered master closure is independently unavailable.

## Checks Run

All commands ran in this worker clone on 2026-07-17 (Asia/Shanghai). The automation-provided pinned
`.lake` symlink was used read-only; no update, build, clone, fetch, checkout, or dependency mutation
was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All rev-5.6 structural groups, 1546-target coverage, v2 theorem DAG, phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | All 1546 theorem nodes, 10822 phase states, typed edges, context digests, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phase contracts, twelve common gates, and validator-ownership rules passed. |
| `python3 scripts/stage1_target.py check` | 0 | The ordered 1546-target `L0/rework_required` manifest passed. |
| `python3 scripts/stage1_target.py show THM-M-0135` | 0 | Rank 51, planned lifecycle, legacy artifacts unaccepted, theorem incomplete. |
| statement candidate enumeration and HEAD/base blob comparison | 0 | Exactly one declared candidate exists, and its HEAD/base bytes are identical. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0135/check_statement.py` | 1 | The immutable validator rejected current HEAD at its earlier-base guard; stderr contained one diagnostic and stdout was empty. |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0135/Statement.lean` | 0 | Four adjacent interface types elaborated; no canonical target declaration exists. |
| `git diff --check -- Stage1_Instances/THM-M-0135 .stage1-worker-selftest.json` | 0 | No whitespace errors in this target-scoped delta. |

## Retry Condition And Status Boundary

The scheduler/master lane must publish a refreshed validator at exactly one declared statement
validator path, then issue a fresh revalidation claim whose worker base contains that identical
blob and whose validator binds the current authority inputs. Only a successful exact replay that
emits one valid semantic JSON object may support a new receipt and handoff. Positive phase closure
additionally requires intake master acceptance and an approved immutable primary-source formula
fixing every material convention, followed by exact Lean elaboration, import minimality,
fingerprinting, checked transports, and all four statement mutations.

This artifact is a target-scoped scheduler-ownership and exact-statement blocker only. It grants no
state transition, phase acceptance, exact-statement credit, proof credit, provider acceptance,
audit completion, theorem completion, or master acceptance.
