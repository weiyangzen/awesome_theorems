# THM-M-0115 validation blocker at HEAD 629a7ce2

## Scope

This is the target-scoped fail-closed result for
`S56-M-0115-VALIDATION` at immutable worker base
`629a7ce266289b9ad49a37c0cc4d89b7b148cf36` (tree
`97daff5e375fca5b6781ccf0dede0d1c25648e19`). The exact claim tuple is
`(v2_execution_rank=260, phase_layer=5,
phase_item_id=S56-M-0115-VALIDATION)`.

The complete `parent_inspection_order` is empty. It was traversed exactly
once as the complete direct and transitive hard-parent closure. The target
also has no reuse hint or shared group. No provider declaration, receipt,
artifact, checkbox state, proof credit, or acceptance was consumed or
transferred. The authoritative theorem-DAG SHA-256 is
`de71a3ca00b2ac64f96f4a0b7363cf56d09acb943716310332e693d9c9503c6a`;
the stable dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_candidate_missing` is the first
worker-unrepairable gate. The HEAD validation contract declares exactly these
scheduler-owned candidate paths:

- `Stage1_Instances/THM-M-0115/check_validation.py`
- `Stage1_Instances/THM-M-0115/check_validation.sh`

Neither path exists in the immutable base, current filesystem, or Git tree.
The worker is forbidden to create, refresh, rename, replace, or delete either
candidate. Therefore no authority-selected argv exists and no validator can
emit the mandatory single `stage1-validator-semantic-result/1.0` JSON object.
Structural exit-zero checks and bounded Lean replay cannot substitute for that
semantic result.

The scheduler-owned role map
`.cron/stage1-v2-app-server/role-maps/S56-M-0115-VALIDATION.json` is absent.
All three contract candidates for the required validation specification are
also absent. This attempt deliberately emits no `validation-spec.json`, no
`validation-receipt.json`, and no `.stage1-worker-selftest.json`.

The integrated `dependency-reuse-ledger.json` is a proof-phase ledger bound to
an older graph and repository revision. It truthfully records the same empty
closure, but it is not current validation evidence. Replacing integrated proof
evidence cannot cure the absent scheduler validator, role map, or validation
receipt, so the companion JSON blocker records the current closure audit
without overwriting the ledger.

## Positive validation boundary

Positive validation independently fails closed:

- `S56-M-0115-PROOF` is authoritative `[_]`, not master accepted `[x]`.
- `proof-receipt.json` has `accepted=false`, `verdict=blocked`, and closes none
  of the 32 positive obligations.
- Its integrated validator is stale at this HEAD and returned one typed
  `G09-FRESHNESS` result with `phase_accepted=false`.
- Trust-zero replay checks
  `Stage1Instances.THMM0115.Proof.not_grothendieckRiemannRochTarget`, whose
  type is `Not (GrothendieckRiemannRochTarget.{0,0})`.
- Both negative declarations are sorry-free and depend only on `propext`,
  `Classical.choice`, and `Quot.sound`.
- The frozen graph has `root_closed=false`, machine debt `M3`, and remaining
  machine cut set `M0115-T-RELATIVE` and `M0115-T-TODD_ACTION`.

The countermodel refutes only the current unconstrained abstract Lean
encoding, not mathematical Grothendieck-Riemann-Roch. It provides no positive
proof or validation credit. Thus `audit_complete=false` and
`theorem_complete=false`; no phase acceptance, M0, AUDIT-Z, THEOREM-Z, release,
or theorem-completion claim is supported.

## Bounded checks

Before adding this blocker pair, these checks passed:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Fifteen assurance groups, 1546 targets, the v2 graph, phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 task states, typed edges, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phases, twelve common gates, and 23 source references passed. |
| `python3 scripts/stage1_target.py check` | 0 | The ordered 1546-target L0/rework-required manifest passed. |
| `python3 scripts/stage1_target.py show THM-M-0115` | 0 | Rank 23 remains planned and theorem-incomplete. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0115/check_proof.py` | 1 | Exactly one typed stale result: `G09-FRESHNESS`, `phase_accepted=false`. |
| Contract-derived validator enumeration | 0 | Exactly zero declared validation candidates exist at immutable HEAD. |
| Trust-zero temporary replay of `Statement.lean`, then `Proof.lean` | 0 | Statement and countermodel elaborated; both declarations were sorry-free with the expected three-axiom profile. |
| Scoped prohibited-construct scan | 0 | No `sorry`, `axiom`, `admit`, `unsafe`, or `native_decide` construct occurred. |

The proof replay stdout SHA-256 was
`30974c6b4d80b58b371b8c0b2495c695bb0a35abc81818f75eb10b7572fe202b`.
Only the existing pinned `.lake` symlink was used, read-only. Compiled output
was created under `/tmp` and removed. No `lake update`, `lake build`, dependency
clone/fetch, network access, or dependency-cache mutation occurred.

The blocker JSON parsed, its identity/content-binding assertions passed,
`git diff --check` was clean, and self-test absence was confirmed. As expected,
rerunning the theorem-DAG and standard checks after adding this evidence pair
reported deterministic evidence-inventory drift. Only integration may
regenerate the read-only theorem-DAG projection; the worker did not edit it.

## Retry condition

The scheduler/master lane must publish exactly one declared validation
validator, the item role map, and an authority-bound validation specification,
then issue a fresh immutable claim containing those exact bytes. Positive
validation additionally requires reopening the unconstrained statement,
binding its formula operations to source-faithful structures and laws, and
accepting repaired statement, anchor-audit, obligation-tree, and positive proof
phases in exact DAG order before validation replay.

This blocker grants no worker state transition, validation acceptance,
provider acceptance transfer, proof credit, audit completion, theorem
completion, release, or master acceptance.
