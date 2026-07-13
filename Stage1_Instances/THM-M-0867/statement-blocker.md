# THM-M-0867 exact-statement gate: blocked

- Item: `S56-M-0867-STATEMENT`
- Base revision: `39704171d88ffcdc33a47365ae9791f855fa3a44`
- Base tree: `050ab5c6392560337051d2eadd1b82277dbe1c4f`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot yet be truthfully elaborated. The repository supplies the title
`Robertson-Seymour图子式定理` and the gloss `图子式良拟序定理`. The inspected Robertson-Seymour
paper identifies the intended theorem family, but neither the catalog nor the provisional intake
freezes the proposition-changing choices needed for one canonical Lean expression.

The author-hosted draft of Neil Robertson and P. D. Seymour, *Graph Minors. XX. Wagner's
conjecture*, says in the abstract:

> for every infinite set of finite graphs, one of its members is isomorphic to a minor of another.

Its introduction repeats that wording and says all graphs in the paper are finite. Section 2 defines
a graph as a hypergraph whose edges have one or two ends, a representation that admits loops and
parallel edge identities and is not definitionally a mathlib `SimpleGraph`. Paper Theorem 10.5
instead states a countable-sequence result for directed graphs and says it immediately implies the
standard undirected form. The preceding sentence defines the directed minor operation through a
subgraph and edge contraction. These passages identify the family, but a statement freeze still has
to decide and check all of the following:

- the undirected finite graph model and whether loops or parallel edges are admitted during or after
  contraction;
- a heterogeneous, canonical `Fin n`, sigma, or isomorphism-class representation of finite graphs;
- the exact minor predicate and argument orientation, including how the source's subgraph plus
  contractions are encoded;
- the infinite-set, countable-sequence, or `WellQuasiOrdered` root and the checked transports among
  them; and
- universes, ordered binders, finiteness and decidability data, and empty, singleton, edgeless,
  isolated-vertex, constant-sequence, and repeated-isomorphism boundaries.

Choosing a convenient `SimpleGraph` branch-set definition now would add a definition and transport
not selected or independently approved by the received source record. Choosing the directed
Theorem 10.5 verbatim would strengthen and change the catalog's conventional undirected target.
Using induced-subgraph containment, embeddings, homomorphisms, or edge deletion alone would
substitute a different relation. Rev-5.6 sections 5 and 5.1 therefore require this attempt to fail
closed: the intake deliberately leaves `canonical_statement`, the Lean module and expression, the
expression hash, and the canonical-target environment fingerprint null.

The prerequisite intake is also only provisional worker state `[_]`. Its receipt has
`accepted: false`, so any future accepted statement transition must remain dependency ordered. The
first failure of this attempt is nevertheless the exact source-to-formal statement identity and
definition-chain gate. With no canonical target, minimal imports and the removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined rather than passed.
The root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` re-elaborates with these direct imports:

- `Mathlib.Order.WellQuasiOrder`
- `Mathlib.Combinatorics.SimpleGraph.DeleteEdges`
- `Mathlib.Combinatorics.SimpleGraph.Maps`

It checks `WellQuasiOrdered`, its monotone-subsequence characterization, `SimpleGraph`, graph
isomorphism, induced graphs, edge deletion, and graph maps. These interfaces do not define graph
minors, edge contraction, a carrier of finite graphs up to isomorphism, or the Robertson-Seymour
closure. A bounded topic search of repository-local Lean and pinned mathlib found no such target
declaration. This is narrow feasibility evidence, not the downstream anchor audit or a global
nonexistence claim. Since no canonical target has been selected, the probe's imports cannot be
certified as minimal target imports and receive no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other dependency mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Lean commands ran from
`Formalizations/Lean`; all others ran from the repository root unless noted. Exact arguments,
results, authority hashes, and pinned-source hashes are recorded in `statement-blocker.json`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0867` | 0 | rank 1421; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| author PDF download, `sha256sum`, `wc -c`, `pdfinfo`, and `pdftotext` outside the repository | 0 | 34 pages, 251,605 bytes, SHA-256 `327694f043a8809dfb0255171c470ae4ba5b15d7fedbad861c43f1f3a05caa91`; abstract, introduction, and Theorem 10.5 rechecked |
| pinned Lean, Lake, and mathlib revision/tree/status checks | 0 | expected versions and a clean mathlib package worktree |
| `lake env lean ../../Stage1_Instances/THM-M-0867/IntakeProbe.lean` | 0 | seven adjacent APIs elaborated; stdout SHA-256 `3a1d6846c2c0fc5f993b635f2fcb9f10cf4a1adaa0a2ddbdc7eab75488acf5b5`; no target or proof declared |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 1 expected | no target match under the recorded patterns; discovery-only feasibility evidence |
| `python3 -B Stage1_Instances/THM-M-0867/check_intake.py` | 1 | historical intake replay expects authoritative intake state `[ ]` and attempt 0, while integration now records `[_]` and attempt 1; this phase did not rewrite historical evidence |
| JSON parse, scoped blocker invariants, and prohibited-construct scan | 0 aggregate | blocker identity, null target, unchanged vector, false completion fields, exact scope, and no proof escape agree |
| scoped whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable failed |

The intake checker is bound to the intake-time authority state and its original nine-file inventory.
Integration changed the generated execution state, and adding this blocker also makes the original
inventory historical. This statement attempt records that boundary rather than editing the intake
checker, intake receipt, instance, task DAG, blueprint, or authoritative execution DAG to
manufacture a replay pass.

## Retry Condition And Status Boundary

The integration lane must master-accept a fresh intake receipt bound to the current authority.
Accountable reviewers must admit and independently approve an immutable source proposition and its
complete graph/minor definition chain, correction and errata disposition, and proof boundary. They
must then freeze the finite-graph representation, graph and contraction conventions, exact minor
orientation, formulation and checked source transports, binders, assumptions, and all boundary
cases.

A fresh statement attempt can encode exactly that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt change is proposed. Because the exact-statement deliverable did
not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance
is claimed.
