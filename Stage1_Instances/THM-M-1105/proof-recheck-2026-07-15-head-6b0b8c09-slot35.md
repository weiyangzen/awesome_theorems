# THM-M-1105 proof recheck at `6b0b8c09` (slot35)

Item: `S56-M-1105-PROOF`

Intent: `prove`

Recorded: `2026-07-15T20:59:24+08:00`

Base revision: `6b0b8c091fa39fd68f1ecf8eb6b41287dacb64f2`

Base tree: `d46d5701e99946a6eca3fe666b42ebbf9f4312a8`

## Verdict

`blocked`. This run cannot dependency-legally implement or claim a proof body for the exact
canonical target `Stage1.THM_M_1105.WignerSemicircleLaw`.

The first failed gate is prerequisite acceptance and exact-interface readiness. The scheduler
projection renders `S56-M-1105-OBLIGATION_TREE` only provisional `[_]`; rev-5.6 section 10.1 says
both `[ ]` and `[_]` are unfinished. The owned `task-dag.json` is stricter: it has no accepted
states and records that prerequisite as `open`. In addition, 19 of the 20 machine-required
obligations still have planned fingerprints rather than exact Lean signatures. A new small lemma
could not be checked against an accepted frozen obligation and would be irrelevant proof padding,
so none was invented.

The independent mathematical blocker is unchanged. All 20 machine-required obligations have
`terminal_proof_body_id: null`. The only local checked theorem,
`Stage1.THM_M_1105.ObligationTree.root_of_sample_weak_convergence`, consumes
`terminal : forall-almost-everywhere omega, SampleWeakConvergence A hA_hermitian omega`. That
premise is the missing analytic conclusion, so this conditional definitional composition closes
neither `M1105-T-WEAK`, `M1105-T-COMPOSE`, nor the root. No exact body exists in the scoped
repository or pinned mathlib. Audited external candidates are partial, statement-mismatched,
placeholder-bearing, outside the pinned closure, or a combination of those failures.

No Lean source, registry entry, graph, or task state was changed. The root remains
`[H2, M3, R4]`; no obligation was closed. This artifact does not satisfy the assigned proof item or
claim audit completion, theorem completion, validation, release, receipt acceptance, or master
acceptance.

## Smallest Real Validation

The Lean commands reused the automation-provided canonical `.lake` symlink read-only. No
`lake update`, `lake build`, clone, fetch, network operation, or dependency mutation was run. The
untracked symlink makes these checks warm nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1105` | 0 | Rank 545; planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1105/check_obligation_tree.py` | 0 | 22 obligations and 108 typed edges passed; denominator `409c3f4a...26f0e`; root explicitly open at M3. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1105/Statement.lean` | 0 | Exact canonical proposition elaborated; only expected unused-hypothesis linter warnings. |
| Same trust-zero command for `ObligationTree.lean` | 0 | Conditional terminal-to-root composition elaborated; the printed type contains the explicit missing terminal premise. |
| Stdin trust-zero `#print axioms` probe of that composition | 0 | Report was exactly `propext`, `Classical.choice`, and `Quot.sound`; the stdin check wrote no source artifact. |
| Token-anchored prohibited-construct scan over owned `*.lean` | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, bodyless axiom-like declaration, unsafe/oracle path, or equivalent prohibited construct. |
| Pinned-mathlib topical source scan | 0 | Sole match was Thales' unrelated geometric semicircle comment; no random-matrix semicircle terminal exists. |
| Repository-local exact-interface scan outside this dossier | 1 | Expected no-match exit; no reusable exact-interface declaration exists. |
| Proof-input diff from original execution revision `270e3fb3` | 0 | `Statement.lean`, `ObligationTree.lean`, registry, graphs, anchor inventory, task DAG, toolchain, and lock manifest are unchanged. |

Lean is version `4.29.0` at commit `98dc76e3...740`; Lake is
`5.0.0-src+98dc76e`; pinned mathlib is `8a178386...ea95`, tree
`bdc39a31...1c2b`. Full hashes and the command ledger are in the paired JSON artifact.

## Workflow Blocker And Retry

Before this run the owned path already contained 42 paired structured unresolved proof records,
while the scheduler still reported `attempts: 0` and `children: []`. Rev-5.6 section 10.2 requires
an item split after five unresolved execution ticks. This worker may not edit the authoritative DAG
or invent unassigned children, so repeated parent redispatch is no longer a conforming execution
route.

The master should first reconcile and accept the prerequisite obligation-tree item, materialize
exact Lean signatures for dependency-legal proof nodes, and split the oversized proof item into
owned child assignments for trace expansion, walk classification, non-pairing, pairing and Catalan
enumeration, concentration, almost-sure moments, semicircle moments, tightness, polynomial and
bounded-continuous approximation, and weak convergence. An alternative retry is an immutable
exact-scope Lean 4 terminal theorem that can be pinned, exact-type transported, and provenance/trust
validated without changing the target.

This current-base artifact is a nonrelease blocker handoff, not a proof receipt. Because the proof
phase is not genuinely self-tested as complete, `.stage1-worker-selftest.json` is deliberately
absent.
