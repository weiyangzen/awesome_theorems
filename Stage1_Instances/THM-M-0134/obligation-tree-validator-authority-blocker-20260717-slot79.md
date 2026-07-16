# THM-M-0134 obligation-tree validator-authority blocker

## Scope

This is the target-scoped fail-closed result for
`S56-M-0134-OBLIGATION_TREE` at worker base
`76eafe8a281129b49022878b685c5abf0c0e071c` (tree
`149043af61224fe5b06fec4e2da210e15b17e383`). It changes no theorem source,
prior phase receipt, task-state authority, theorem-DAG projection, lifecycle,
debt vector, or acceptance state.

The authoritative claim tuple is
`(v2_execution_rank=284, phase_layer=3,
phase_item_id=S56-M-0134-OBLIGATION_TREE)`. The theorem-DAG SHA-256 is
`39dc7ce5f668c527de899e74c99840aef50e6be4c576aaf146abed1b6749275c`,
and the dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## First failed gate

`T01-ARTIFACTS.scheduler_owned_obligation_tree_validator_missing_at_worker_base`
is the first mechanically unrepairable worker gate. The mandatory HEAD phase
contract (SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`)
declares exactly these scheduler-owned candidate paths:

- `Stage1_Instances/THM-M-0134/check_obligation_tree.py`
- `Stage1_Instances/THM-M-0134/validate_obligation_tree.py`

Neither path exists in the immutable worker base or current worktree. The
contract requires exactly one candidate already present at the worker base and
requires its base and HEAD Git blobs to agree. The worker is expressly
forbidden to create, copy, refresh, rename, replace, or delete either path.
Consequently there is no lawful validator argv and no possible semantic stdout
object with schema `stage1-validator-semantic-result/1.0`. Ordinary JSON, graph,
Lean substrate, and repository checks cannot replace the missing authority
replay or justify a `[_]` proposal.

No `.stage1-worker-selftest.json` is emitted. The phase remains `[ ]`, and the
blocked receipt records `accepted=false`, `phase_predicate_proven=false`, and
`phase_accepted=false`.

## Obligation architecture boundary

The target-owned architecture inventories 40 provisional obligations and all
mandatory ROOT/S/N/B/C/L/X/T layers before assigning status. The provisional
denominator is
`e83388972fd731594f2526367155c05f33e13a646f211e6e9b4c2c097de31086`.
This hash freezes only the candidate-guarded projection; it is explicitly not
the canonical exact-theorem denominator required by T02.
`typed-graphs.json` records 182 indexed typed edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs.
Proof and refinement relations have reciprocal planned edges, every node has
the rev-5.6 node fields, and every compact semantic ledger has three substantive
steps with a budget no greater than 28.

This does not satisfy the phase predicate. The repository label does not
identify one exact Burnside-Young proposition, so the required exact theorem
root and canonical expression fingerprint are missing. The representation
isomorphism-class classification, irreducible-character classification,
Young's rule, branching rule, orthogonal form, hook-length theorem, and other
Burnside or Young results are non-equivalent variants. The current C/L route is
explicitly guarded as a partition-classification candidate; it cannot be an
exhaustive canonical denominator until an immutable source passage selects it.

The legacy `BurnsideYoungProofPackage` is inspected only as architecture
guidance. Its `specht`, `irreducible`, `pairwise_nonisomorphic`, and
`exhaustive` fields are assumptions, and no package inhabitant exists. Its
checked equivalence and statement wrappers therefore receive no terminal-body,
composition, proof, or acceptance credit. In particular, the legacy `Rep.{0}`
encoding does not by itself express the candidate prose's finite-dimensionality
restriction.

No `ObligationTree.lean` role is selected. Without exact parent and child Lean
targets, a harness would invent a proxy theorem. Composition certificates are
empty and classified
`not_machine_eligible_no_exact_parent_or_child_targets`; this is not a passed
composition check. The root stays `H4 / M4 / R4`, with no closed obligation,
`audit_complete=false`, and `theorem_complete=false`.

## Dependency and reuse audit

The complete `parent_inspection_order`, direct-parent list, transitive-ancestor
list, hard-edge list, reuse-hint list, and shared-group list are all empty. The
empty sequence was traversed exactly once before architecture work. No provider
phase state, receipt, declaration, reusable artifact, terminal body, checkbox,
proof credit, or acceptance was consumed or inherited.

The phase-scoped
`obligation-tree-dependency-reuse-ledger.json` uses schema
`stage1-dependency-reuse-ledger/1.1` and binds the assigned graph, dependency
context, base revision, and claim tuple with empty inspections, decisions, and
unresolved compatibility lists. This records an empty audited closure, not a
mathematical independence claim.

The canonical `dependency-reuse-ledger.json` already exists in HEAD and belongs
to the earlier anchor-audit claim. A scheduler blocked snapshot cannot replace
an existing master path, so this run leaves it byte-identical and emits the
new phase-scoped snapshot instead. A later self-tested obligation-tree retry
must refresh the canonical path before phase acceptance or proof work. This
known integration boundary is an additional reason not to claim completion.

## Checks run

All commands ran inside this worker clone on 2026-07-17 (Asia/Shanghai). The
automation-provided untracked `.lake` symlink was used read-only. No `lake
update`, `lake build`, dependency clone/fetch, checkout, or network operation
ran.

| Command | Exit | Result |
| --- | ---: | --- |
| `python3 Docs/tools/check_stage1_standard.py` | 0 before owned edits | rev-5.6 structure, target set, v2 DAG, phase contract, and execution skill passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 before owned edits | 1546 theorem nodes, 10822 phase states, typed edges, and acyclicity passed |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | seven phases, twelve common gates, and scheduler-owned validator rules passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0134` | 0 | rank 50, planned lifecycle, legacy evidence unaccepted, theorem incomplete |
| `git cat-file -e HEAD:Stage1_Instances/THM-M-0134/check_obligation_tree.py` | 128 expected | first declared validator is absent from the immutable worker base |
| `git cat-file -e HEAD:Stage1_Instances/THM-M-0134/validate_obligation_tree.py` | 128 expected | second declared validator is absent from the immutable worker base |
| `lake env lean --trust=0 ../../Stage1_Instances/THM-M-0134/StatementInfrastructure.lean` from `Formalizations/Lean` | 0 | unchanged candidate object vocabulary and quotient infrastructure elaborated; no canonical theorem was declared |
| `python3 -m json.tool` on the new structured artifacts | 0 | registry, graph, phase-scoped dependency ledger, and phase receipt parse as JSON |
| target-scoped architecture invariant check | 0 | 40 unique provisional obligations, all mandatory candidate layers, complete node records, 182 unique indexed edges, reciprocal planned proof/refinement relations, all 26 required candidate-route machine nodes reachable from the root, substantive budgets at most 28, and empty composition certificates passed; it deliberately reports the exact root and phase predicate missing |
| repository `validate_dependency_reuse_ledger` on the phase-scoped ledger | 0 | schema 1.1 and the exact empty dependency context passed at graph `39dc7ce5...9275c` and base `76eafe8a...071c` |
| `git diff --check -- Stage1_Instances/THM-M-0134` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no positive handoff was manufactured |

The aggregate theorem-DAG freshness checks are expected to fail after these new
target-owned artifacts are present, because they change the generated evidence
inventory and this worker is forbidden to rewrite the theorem-DAG projection.
Scheduler integration must regenerate that projection after preserving the
blocked snapshot.

## Retry condition

The scheduler/master lane must commit exactly one declared obligation-tree
validator and issue a fresh claim whose base already contains that identical
tracked blob. A fresh worker can then refresh the canonical dependency ledger,
bind the authority-owned role map, execute the exact contract argv in a
read-only repository, and require one schema-exact semantic JSON result.

Even then, the phase predicate remains blocked until an immutable independently
reviewed source passage identifies the exact theorem variant and supplies the
definition, assumption, conclusion, correction, errata, and translation
boundary needed for an exact root. Registry version 2 must replace the
candidate guard with exact fingerprints and an append-only mapping, expand the
source-selected proof route, and add consumer-owned Lean composition
certificates for every nonleaf. Master topology separately requires the
anchor-audit predecessor to become `[x]`; its current `[_]` status and receipt
are observation only.

This blocker grants no state transition, phase acceptance, proof credit,
provider acceptance transfer, audit completion, theorem completion, or master
acceptance.
