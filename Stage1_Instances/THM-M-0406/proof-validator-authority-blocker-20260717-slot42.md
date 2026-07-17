# THM-M-0406 proof validator-authority blocker

## Scope

This is the target-scoped continuation result for `S56-M-0406-PROOF` at
worker base `e19e77ec08fca6a8a9c45a003c9904020dae8382` (tree
`53ff0ebe013670fc0332bf326fd860b29857ddab`). The exact claim tuple is
`(v2_execution_rank=258, phase_layer=4,
phase_item_id=S56-M-0406-PROOF)`.

The sole task-state authority records the proof item as `[_]` with one
attempt, and its obligation-tree predecessor as `[_]`. This continuation
therefore proposes no second state transition and emits no second phase
receipt. Outcome: `blocked`; worker verdict: `no_state_change`.

## Dependency audit

The current theorem-DAG SHA-256 is
`53622c848d6a0d8327bba8cd22bf45463f0dd8acb7ea0af2884713983e76c91f`,
and the stable dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
Direct hard parents, transitive hard ancestors, hard edges, reuse hints, and
shared groups are all exactly empty. The supplied empty
`parent_inspection_order` was traversed exactly once before proof inspection.
No provider state, receipt, declaration, reusable body, proof credit,
checkbox state, or acceptance was consumed or inherited.

The integrated `dependency-reuse-ledger.json` has schema 1.1 and truthfully
records the same empty closure. It is historical, however: it binds graph
`eaee68bd...7153` and repository revision `94009a6b...`. Refreshing only that
file would make it disagree with the immutable validator and stale receipt
and could not create a lawful current-base self-test. This blocker records the
current empty context without presenting the historical ledger as fresh.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_base_binding_stale` is the first
worker-unrepairable gate. The HEAD proof contract declares two scheduler-owned
candidates. Exactly one exists and is unchanged at this worker base:

```text
Stage1_Instances/THM-M-0406/check_proof.py
SHA-256 adfb398aa59f62d42d4fb5d66169bbf088b36ebc690ee92a9f49367520a5872a
Git blob 31d2c567797e9e59a858022e43db102721a55ca0
```

The worker did not create, refresh, rename, replace, or delete either
candidate. The exact authority-selected argv was run:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0406/check_proof.py
```

It exited `1`, wrote no stderr, and emitted exactly one JSON object with
schema `stage1-validator-semantic-result/1.0`, `status=failed`,
`verdict=repair_required`, `phase_accepted=false`, fourteen open obligations,
and message `Proof blocker replay failed: worker base revision or tree
drifted`.

That result is truthful. The immutable candidate binds base `94009a6b...`,
tree `daabee9f...`, graph `eaee68bd...`, and proof cursor `[ ]`/attempt zero.
The current claim is based at `e19e77ec...`, tree `53ff0ebe...`, graph
`53622c84...`, with cursor `[_]`/attempt one. It also pins the historical
ledger, receipt, and old changed-path set. Exit zero is not inferred and the
typed negative result is not converted into a passing result.

The scheduler-owned role map
`.cron/stage1-v2-app-server/role-maps/S56-M-0406-PROOF.json` is absent. The
sole `proof-receipt.json` remains the historical blocked receipt from base
`94009a6b...`, with `accepted=false` and
`phase_predicate_proven=false`. It was left unchanged. Because this phase is
not genuinely self-tested at the current base, `.stage1-worker-selftest.json`
is deliberately absent.

## Kernel boundary

An independent trust-zero replay against the pinned Lean closure confirms the
deeper statement blocker. Fresh `/tmp` copies of `Statement.lean` and
`Proof.lean` elaborate, and Lean checks:

```text
Stage1Instances.THMM0406.not_corvajaZannierTheoremOne :
  Not (CorvajaZannierTheoremOne.{0,0} (k := Rat))
```

The model uses four boundary components, unit weights and intersections, one
point, true frozen geometric premises, and `curve = Empty`. Every premise
holds, while the conclusion would produce an inhabitant of `Empty`. The
declaration reports only `propext`, `Classical.choice`, and `Quot.sound`.

This refutes the frozen abstract encoding, not the mathematical
Corvaja--Zannier theorem. The primary source also requires the intersection
equation for all divisor pairs, including diagonal cases used in its proof;
the Lean target guards it by distinctness and otherwise leaves its geometric,
rationality, integrality, curve, and incidence fields unconstrained. No
positive proof credit follows. All fourteen frozen positive obligations remain
open, including the root cut `M0406-S-DEFINITIONS` and `M0406-ROOT`.

## Checks

Before adding this blocker pair, the Stage1 standard, theorem DAG, ordered
target manifest, obligation-tree validator, anchor-audit validator, and eleven
focused phase-contract tests passed. The trust-zero statement/countermodel
replay passed against Lean 4.29.0 commit `98dc76e...`, clean pinned mathlib
revision `8a178386...`, and clean pinned `flt-regular` revision `56161b6e...`.
No prohibited proof construct was introduced.

The automation-provided untracked `.lake` symlink was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, network operation, or
intentional cache mutation ran. `git diff --check` passed for the target-owned
delta. Adding the blocker pair changes the deterministic target evidence
inventory, so the post-write theorem-DAG and aggregate standard checks report
that the checked-in projection differs from fresh generation. The worker is
forbidden to regenerate that authority; this expected integration boundary is
not proof evidence and cannot substitute for the failed semantic replay.

## Retry condition

The scheduler must publish a refreshed immutable `check_proof.py` and the
required per-item role map at an authoritative base that binds the current
graph, `[_]`/attempt-one cursor, current ledger, sole receipt, and exact replay
recipe, then issue a fresh claim.

That mechanical repair cannot make the positive target consistent. Positive
proof work also requires reopening `S56-M-0406-STATEMENT`, replacing the
refuted abstract encoding with source-faithful intrinsic structures and every
source-required pair/place case, accepting a new statement fingerprint, and
rerunning statement, anchor-audit, and obligation-tree phases in DAG order.

This artifact grants no phase transition, proof or provider acceptance,
positive root proof, validation, release, `AUDIT-Z`, `THEOREM-Z`, theorem
completion, or master acceptance.
