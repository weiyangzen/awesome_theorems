# Statement validation

Item: `S56-M-0856-STATEMENT`

Base revision: `748243faadc15828fb087059337fd05b7be9fdeb`

Base tree: `e46d642646f80980838b6f016f5d69b817bd464d`

## Frozen target

`Stage1Instances.THM_M_0856.TutteOneFactorTarget` freezes the conventional finite-simple-graph
form of Tutte's 1-factor theorem selected at intake. For every universe-polymorphic vertex carrier,
finite simple graph, and vertex subset `U`, it equates the existence of a perfect matching with the
bound saying that deleting `U` leaves at most `U.ncard` connected components of odd order.

The sole direct import is `Mathlib.Combinatorics.SimpleGraph.Matching`. It owns the perfect-matching
predicate and publicly exposes the finite connected-component, deletion, and cardinality vocabulary
needed by the target. Removing the import makes the module fail. The proof-bearing
`Mathlib.Combinatorics.SimpleGraph.Tutte` module is deliberately absent; `SimpleGraph.tutte` and its
proof body remain anchor-audit work.

Two kernel-checked `Iff` transports cover the direct inline inequality and a local no-strict-
violator spelling. The latter matches the logical condition used by the pinned candidate without
importing or crediting that candidate.

## Commands and results

All commands ran in this worker clone. Lean used the existing pinned Lake artifacts read-only. No
dependency update, build, clone, fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0856` | 0 | rank 1410; planned; legacy artifacts unaccepted; theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-0856/Statement.lean` from `Formalizations/Lean` | 0 | exact target and two transports elaborated; four expected definitional-equality rejections printed; transport axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; explicit target expression printed |
| `python3 -B ../../Stage1_Instances/THM-M-0856/check_statement.py` from `Formalizations/Lean` | 0 | expression SHA-256 `5364250d1d4e132aaf1d5ce8ad5425369546963189991202f49b2fcf65095bae`; four mutation expressions distinct; sole-import deletion failed; pinned toolchain and mathlib agree |
| `python3 -B Stage1_Instances/THM-M-0856/check_statement_artifacts.py --worker-packet .stage1-worker-selftest.json` | 0 | statement metadata, receipt, source and environment hashes, current authority identity, exact changed paths, and worker handoff agree |
| `python3 -m json.tool Stage1_Instances/THM-M-0856/statement.json` | 0 | statement JSON parses; the same command separately passed for the receipt and root packet |
| `rg -n '\b(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-0856/Statement.lean` | 1 (expected) | no prohibited construct found |
| `git diff --check -- Stage1_Instances/THM-M-0856 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics; the artifact validator also checks untracked-file formatting |

`instance.json` and the local `task-dag.json` are reconciled to the provisional statement proposal;
their task state remains open because only the integration lane can accept it. The earlier
`validation.md`, intake receipt, and `check_intake.py` remain immutable historical intake-snapshot
artifacts. After integration promoted intake to provisional `[_]`, this phase also changed
hash-bound readable inputs and expanded the artifact inventory, so the prior provisional receipt is
invalid for current replay. Running its historical checker exits 1 at the exact old-DAG assertion.
Those historical artifacts are not hidden or used as current statement evidence.

## Mutation and evidence boundary

Lean rejects reflexive definitional equality between the canonical target and each changed
proposition, while the checker compares their fully explicit serializations. The mutations remove
finiteness, restrict the graph domain to complete graphs, move the graph binder from universal to
existential scope, and exclude the empty carrier. They test statement identity; they do not claim
logical nonequivalence or that any mutated proposition is false.

The empty carrier, odd-order carriers, isolated vertices, disconnected graphs, and empty/full
deletions remain in scope. No connectedness, nonemptiness, even-cardinality, `Fintype`, or
decidability premise is inserted.

This is statement-only evidence pending dependency-ordered master acceptance. It provides no H0,
M0, R0, proof-body credit, anchor audit, obligation registry, audit completion, release evidence, or
theorem completion.
