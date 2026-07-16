# THM-M-0412 obligation-tree revalidation blocker

Item: `S56-M-0412-OBLIGATION_TREE`

Worker base: `f545339546bf410d5110d7fe44e70bdcf5d8b48e`

Base tree: `6dc924134293b2674df7324ff98b6fdaf660159e`

Claim order: `(v2_execution_rank=259, phase_layer=3,
S56-M-0412-OBLIGATION_TREE)`

Verdict: `blocked`. The target-owned architecture passes narrow independent
checks, but the mandatory unchanged scheduler-owned validator cannot prove the
phase predicate at this base. The authoritative phase remains `[_]`; this
handoff neither promotes it nor claims master acceptance.

## Dependency and reuse audit

The authoritative theorem DAG SHA-256 is
`39dc7ce5f668c527de899e74c99840aef50e6be4c576aaf146abed1b6749275c`.
Its direct hard parents, transitive hard ancestors, hard edges, reuse hints,
shared groups, and `parent_inspection_order` are all exactly empty. The empty
order was traversed exactly once before any possible proof work. No provider
artifact, declaration, receipt, checkbox, proof body, or acceptance was
consumed or inherited.

The refreshed schema `stage1-dependency-reuse-ledger/1.1` binds the current
graph, stable context
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`,
worker base, and claim tuple. Its inspections, decisions, and unresolved
compatibility obligations remain empty. Empty graph context is not a claim of
mathematical independence.

## Frozen architecture

The existing architecture bytes remain unchanged and content-bound:

- `obligation-registry.json` freezes 29 status-independent obligations with
  denominator
  `1726b8e6f6d48ec652a86fd62675be0ea4d8d3fe2f7ca5fb733adfa45e4e4ab5`.
- `typed-graphs.json` contains 122 indexed typed edges across separate proof,
  refinement, provenance, evidence, trust, documentation, and workflow
  graphs.
- Every node has a substantive semantic ledger and a step budget at most 100.
- `obligation-tree.md` exposes all mandatory S/N/B/C/L/X/T layers and an open
  boundary for every node.
- `ObligationTree.lean` is intentionally declaration-free. No exact source
  proposition or exact child signature exists, so a conditional composition
  harness would invent a substitute theorem. Composition certificates remain
  empty and are classified
  `not_machine_eligible_no_exact_parent_or_child_targets`.

No exact theorem, proof body, checked transport, closed obligation, audit
completion, or theorem completion is claimed. The root remains `H5/M4/R4`
with cut set `M0412-ROOT-IDENTITY`.

## Scheduler-owned validator blocker

The HEAD phase contract declares two candidates and exactly one exists:

- `Stage1_Instances/THM-M-0412/check_obligation_tree.py`
- `Stage1_Instances/THM-M-0412/validate_obligation_tree.py` (absent)

The selected file is tracked at HEAD with SHA-256
`68588dc92451fb7376d71a8a1ea220c433ae94f97e2af62807e1388bafe03af5`
and Git blob `d0eb027639ab658b76d66aca3b70db9ac3cb896a`. This worker did
not edit, copy, refresh, rename, replace, or delete it.

The validator is internally bound to historical base `a103f2e1...`, tree
`5988efc9...`, graph digest `d5b27da9...`, and the former `[ ] / attempts=0`
authority row. The exact contract argv at the current base exits 1 and emits
exactly one `stage1-validator-semantic-result/1.0` object:

```json
{"audit_complete":false,"blocked":true,"first_failed_gate":"G09-FRESHNESS","item_id":"S56-M-0412-OBLIGATION_TREE","message":"a frozen authority input changed","open_obligations":1,"phase":"obligation_tree","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":["Docs/Stage1_Theorem_DAG_v2.json"],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0412","verdict":"repair_required"}
```

Stdout is 465 bytes with SHA-256
`6d789e3cfa6a226d0dbc815cf52ed45120ec280f8f04e6d30704aa9bbf87da88`;
stderr is empty. Exit zero, narrow checks, or an undeclared adapter cannot
override that typed negative result. The first failed execution gate is
`G09-FRESHNESS.scheduler_owned_validator_internal_base_binding`.

## Checks

The automation-provided `.lake` symlink was used read-only. No `lake update`,
`lake build`, clone, fetch, dependency checkout, or network operation ran.

| Command | Exit | Result |
| --- | ---: | --- |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0412/check_obligation_tree.py` | 1 expected | one exact typed `repair_required` JSON object; stale theorem-DAG authority input |
| `lake env lean ../../Stage1_Instances/THM-M-0412/ObligationTree.lean` from `Formalizations/Lean` | 0 | declaration-free boundary elaborated; sandbox emitted three nonsemantic stream-fd diagnostics |
| `python3 -B Stage1_Instances/THM-M-0412/build_obligation_artifacts.py` | 0 | reproduced 29 obligations, 122 edges, and the frozen denominator |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and uniform L0/rework-required baseline |
| `python3 scripts/stage1_target.py show THM-M-0412` | 0 | rank 21, planned lifecycle, theorem incomplete |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | 7 phases, 12 common gates, and 23 source references |
| prohibited Lean construct scan | 1 expected no match | no `sorry`, `admit`, axiom declaration, unsafe, or oracle construct |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 expected after receipt refresh | refreshed receipt digest awaits scheduler-owned DAG regeneration |
| `python3 Docs/tools/check_stage1_standard.py` | 1 expected after receipt refresh | delegates to the same theorem-DAG freshness gate |
| `git diff --check -- Stage1_Instances/THM-M-0412 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Retry condition

The scheduler/master lane must publish a corrected declared validator and
launch a fresh claim from a base already containing that identical validator
blob. It must bind the current `[_] / attempts=1` authority row, current graph,
current canonical ledger, and sole phase receipt. Master topology separately
requires the anchor-audit predecessor to become `[x]`.

Proof work additionally requires an immutable independently reviewed source
identifying the exact Pierce/Nagell proposition, followed by registry version
2 with exact statement fingerprints and checked child-to-parent composition
certificates. Until then this packet is target-scoped blocker evidence only.
