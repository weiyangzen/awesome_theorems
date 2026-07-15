# THM-M-0330 proof-phase recheck at current base

Item: `S56-M-0330-PROOF`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

## Verdict

`blocked`. The exact frozen proposition is the full contraction Hille--Yosida
equivalence for every partially defined real-linear operator on every real
Banach space. No placeholder-free proof of this proposition is present in the
repository or pinned dependency closure. Neither `ForwardPackage` nor
`ConversePackage` is inhabited, so the minimal open root cut remains:

```text
M0330-B-FORWARD
M0330-B-CONVERSE
```

`root_of_direction_packages` is checked conditional composition after both
complete directions are supplied; it constructs neither. `target_iff_expanded`
is only definitional transport. The first unavailable pinned forward leaf is
`M0330-L-FWD-DENSE`; independently, the first unavailable converse construction
is `M0330-C-YOSIDA`.

The mandatory schema-1.1 dependency ledger was created before proof search. It
is bound to graph digest `73e99d22...0eca`, context digest
`068170c7...ec5c`, and this base revision. The authoritative node has no direct
hard parent, transitive ancestor, reuse hint, or shared group, so every closure,
inspection, decision, and unresolved-compatibility list is empty. This is an
audited empty context, not a claim that the theorem is mathematically
independent.

## Missing Mathematics

The forward direction still needs generator density and closedness, a
Laplace/Bochner resolvent, both inverse laws, and the `1/a` estimate. The
converse needs bounded Yosida approximants, their exponential semigroups,
uniform contraction, strong convergence to a C0 semigroup, and exact
identification of its generator with `A`.

Search over all `9676` Lean sources in the pinned package cache found no
Hille--Yosida or C0-semigroup generator theorem. Repository history, duplicate
target `THM-M-1041`, and legacy `S1_M_234.lean` contain definitions, abstract
interfaces, transports, or conditional adapters only.

The strongest audited external partial source is TauCeti at
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa`. Its generator module proves
domain density, and its resolvent module proves range/domain membership, a
right inverse, and the contraction norm bound. It is outside the pinned
closure, uses Lean `v4.32.0-rc1` and mathlib `faaff5e...`, and needs nontrivial
real-time/`NNReal` and generator transports. It still has no generator
closedness, full-domain left inverse, or converse generation theorem.
`mrdouglasny/hille-yosida` at `680e9499...d667` is likewise forward-only.
Neither source was cloned, fetched, built, integrated, or credited.

Assuming either direction package, weakening the equivalence, or replacing the
analytic predicates with abstract fields would add an unproved premise or
substitute a different theorem and was rejected.

## Scheduler Handoff

There were `32` integrated unresolved proof rechecks before this run, while the
authoritative proof item still records `attempts: 0` and `children: []`. This
exceeds the rev-5.6 five-tick split rule. The master or scheduler must reconcile
attempt accounting and split the item into dependency-legal children whose
exact contextual Lean propositions and child-to-parent composition are frozen.
Seventeen registry fingerprints and thirteen typed-graph targets remain
planned rather than exact child interfaces.

The direct prerequisite `S56-M-0330-OBLIGATION_TREE` is only `[_]`, not
master-accepted `[x]`. The worker may prepare blocker evidence, but this proof
item cannot be accepted on the current base.

## Validation

All commands ran inside this worker clone. Existing pinned artifacts were
reused read-only, temporary Lean output was removed, and no `lake update`,
`lake build`, dependency clone/fetch, checkout, or other `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 1 | Global preflight fails after the mandatory ledger is written because the fresh v2 evidence inventory includes it while the immutable checked-in inventory predates it. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | The sole fresh-build mismatch is `THM-M-0330.evidence_inventory.structured_json_files` gaining `dependency-reuse-ledger.json`; graph/context bytes are unchanged. |
| `python3 scripts/stage1_target.py check` | 0 | `1546` unique targets, ranks `1..1546`, uniform L0 rework baseline. |
| `python3 scripts/stage1_target.py show THM-M-0330` | 0 | Rank `823`; lifecycle `planned`; theorem completion false. |
| `LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-0330/check_statement.py` | 0 | Exact expression SHA-256 `56962850...bd75e`; all three mutations killed. |
| `python3 Stage1_Instances/THM-M-0330/check_anchor_audit.py` | 0 | Anchor-audit invariants pass. |
| `python3 Stage1_Instances/THM-M-0330/check_obligation_tree.py` | 0 | `19` obligations and `40` typed edges pass; root and both directions remain `M4`. |
| Direct `validate_dependency_reuse_ledger` invocation | 0 | Exact schema, graph, context, revision, and empty closure validate. |
| `python3 -m unittest scripts/test_stage1_execution_cron.py` | 0 | `62` tests pass. |
| Isolated `lake env lean --trust=0 -t0` for statement and obligation tree | 0 | Exact statement and conditional composition elaborate; the latter reports only `propext`, `Classical.choice`, and `Quot.sound`. |
| Pinned-package topical search | 1 | Expected no-match over `9676` Lean source files. |
| Scoped prohibited-token scan | 1 | Expected no-match in owned Lean sources; supporting lexical evidence only. |

The trust-level-zero replay used an explicit `LEAN_PATH` assembled from the
existing pinned package objects and wrote only a temporary `Statement.olean`
under `/tmp`. Its SHA-256 was
`e3170bec5ab039bd33781fe439cc5236e8526bcda9648931129ae32a95bf9194`.

## Retry Condition

The master or scheduler must accept or repair the prerequisite, reconcile the
repeated attempts, freeze and split exact child interfaces, and repair the v2
inventory exclusion so the required ledger does not invalidate the global
fresh-build check. Relevant placeholder-free proof bodies, or an immutable
compatible exact proof, must then enter the pinned closure.

No `.stage1-worker-selftest.json` is emitted because the assigned proof phase
is incomplete. This artifact proposes no state change and makes no theorem-
completion claim.
