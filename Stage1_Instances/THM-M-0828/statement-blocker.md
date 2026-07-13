# Exact-statement gate: blocked

Item: `S56-M-0828-STATEMENT`

Theorem: `THM-M-0828`

Base revision: `39704171d88ffcdc33a47365ae9791f855fa3a44` (tree
`050ab5c6392560337051d2eadd1b82277dbe1c4f`).

## Decision

The statement item remains `[ ]`. The Stage1-bearing repository record gives only the name
`Edmonds-Karp算法`, Jack Edmonds and Richard Karp, the year 1972, and the gloss
`最大流的多项式算法` (a polynomial-time algorithm for maximum flow). It supplies no cited
truth-valued proposition, network or capacity domain, ordered binders, hypotheses, conclusion,
algorithm semantics, output contract, cost model, proof boundary, correction, or erratum. Stage0
repeats the gloss while explicitly leaving precise definitions and premises open. The catalog's
`已验证` label is untrusted metadata under rev-5.6.

The recognizable Edmonds-Karp theorem family still contains proposition-changing choices:

- a finite directed graph, an edge-indexed multigraph, or a capacity matrix, including self-loops,
  parallel and antiparallel edges, and whether the source must differ from the sink;
- natural, integer, rational, real, or nonnegative-real capacities, together with exact feasible
  flow, conservation, value, residual-edge, reverse-capacity, and augmentation conventions;
- an executable deterministic queue algorithm or an abstract relational process that chooses any
  breadth-first shortest residual path, including path identity and tie behavior;
- flow-only output or a value, minimum cut, or certificate, and whether correctness means feasible
  preservation, termination, maximum flow, minimum-cut certification, or their conjunction; and
- merely some polynomial bound or the usual worst-case `O(V * E^2)` result, with exact definitions
  of `V`, `E`, primitive operations, arithmetic cost, input encoding, and small-instance behavior.

Empty or singleton vertex types, source equal to sink, absent paths or edges, zero capacities,
zero-length paths, disconnected components, and zero maximum flow also have no approved policy.
Different choices yield inequivalent Lean propositions.

A separate non-Stage1 computer-science UID, `THM-C-0097`, says `O(VE^2)最大流算法`. That record is
useful ambiguity evidence, but it cannot silently redefine this target. Joining its complexity
gloss to a remembered correctness theorem would broaden or substitute the received mathematics.

The intake identifies Edmonds and Karp's 1972 JACM paper, *Theoretical Improvements in Algorithmic
Efficiency for Network Flow Problems*, DOI `10.1145/321694.321699`, as a primary source lead.
Bibliographic metadata was crosschecked, but the primary PDF endpoint again returned HTTP 403 in
this run. No exact statement, incorporated definitions, proof pages, corrections, or errata were
available for independent review. Bibliographic identity alone does not select a binder-complete
root proposition.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. The intake correctly leaves the canonical human statement, Lean module
and expression, ordered binders, hypotheses, minimal imports, and expression/environment
fingerprints null at `[H1, M4, R4]`. Without a canonical target, credited transports and the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are
undefined, not passed. No `Statement.lean`, axiom, placeholder, assumed correctness structure,
fixed example, weakened target, or broadened theorem was introduced.

The prerequisite `S56-M-0828-INTAKE` has only provisional worker state `[_]`, not master-accepted
state `[x]`. Its receipt says `accepted: false`, is not content-addressed, and lists no accepted
receipt ID. It is also stale against current authority: `check_intake.py` stops at its assertion
that the intake-time canonical target-DAG-row hash matches the current seven rows. The stored hash
is `dabe349a068056bf01aea6195d76ceccca9d04cf6f20af38507e6a04875bfd0e`; the current hash is
`8e1d4c722cba355e3136a23aefbe0c01b516b807ebd7a8087aa0507598873f18`. Dependency-ordered blocker
inspection is still meaningful, but no statement transition can be accepted before refreshed
intake evidence receives master acceptance.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with these direct imports:

- `Mathlib.Combinatorics.Quiver.Path.Weight`;
- `Mathlib.Combinatorics.Digraph.Basic`;
- `Mathlib.Combinatorics.SimpleGraph.Metric`; and
- `Mathlib.Combinatorics.SimpleGraph.Walks.Counting`.

It checks twelve generic interfaces for directed adjacency, dependent paths, additive path
weights, undirected shortest-walk distance, and finite bounded-walk enumeration. None defines a
capacitated flow, directed residual network, breadth-first execution, bottleneck augmentation,
maximum-flow conclusion, or complexity bound. Additive path weight is not residual bottleneck
capacity, and an undirected `SimpleGraph` metric is not a directed residual network. The probe
states no target, so these imports are discovery inputs and cannot be certified minimal for an
absent target.

A bounded source search over repository-local Lean and pinned mathlib found no declaration matching
Edmonds-Karp, Ford-Fulkerson, maximum flow, minimum cut, residual network, or augmenting path. This
is narrow feasibility evidence, not the downstream anchor audit and not an absence claim outside
the searched closure.

The checked environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link was used read-only, and the pinned mathlib worktree remained clean.
No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0828` | 0 | rank 1386; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| repository source, Stage0, manifest, blueprint, skill, guidelines, intake, scope, and companion-record inspection | 0 | confirmed a non-propositional polynomial-algorithm gloss, null target, unresolved correctness/complexity choices, and no admitted exact proposition |
| `python3 -B Stage1_Instances/THM-M-0828/check_intake.py` | 1 | historical intake replay stopped at line 198 because its canonical target-DAG-row fingerprint is stale against current authority; prior evidence was not rewritten |
| `cd Formalizations/Lean && lake env lean --version` | 0 | pinned Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | pinned Lake version recorded above |
| pinned mathlib revision/tree and package status checks | 0 | revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0828/IntakeProbe.lean` | 0 | all twelve generic interfaces elaborated; stdout SHA-256 `26db1cd1e80c5e67d57d285af0cbb92b463c563abbd3320e70f294bab3b65434`; no target declared |
| bounded Edmonds-Karp/maximum-flow/residual-network Lean search | 1 | expected no-match exit over pinned mathlib and repository-local Lean |
| primary paper PDF request | 22 | ACM endpoint returned HTTP 403; no primary theorem statement was admitted |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| finalized JSON parse and scoped blocker assertions | 0 | blocker identity, base, dependency, source and pin hashes, null target/imports, unchanged vector, undefined mutations, false completion flags, and owned two-file change agree |
| whitespace checks over both new blocker files | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must first refresh and master-accept the intake dependency. Accountable
reviewers must then lawfully preserve one immutable primary or approved authoritative source,
identify and independently approve the exact root theorem, and map every incorporated definition,
ordered binder, hypothesis, conclusion, network/capacity/flow/residual/BFS convention, algorithm
variant, output contract, cost model, boundary case, proof boundary, correction, and erratum. The
selection must explicitly reconcile the broad Stage1 polynomial gloss with the separate
`THM-C-0097` `O(VE^2)` wording without importing that UID as authority.

A fresh statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required semantic mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
