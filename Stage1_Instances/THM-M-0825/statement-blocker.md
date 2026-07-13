# THM-M-0825 exact-statement gate: blocked

- Item: `S56-M-0825-STATEMENT`
- Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e`
- Base tree: `6434a20532ae7c523ad293e67a6228ab384bfb8a`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully frozen from the received repository record. The
complete catalog wording is the label `Dijkstra算法` and the gloss `单源最短路径算法`
(`single-source shortest-path algorithm`). This identifies an algorithm family and purpose, not a
truth-valued proposition. It supplies no graph or edge representation, weight domain, ordered
binders, hypotheses, conclusion, implementation contract, proof boundary, correction, or reviewer.
The catalog's `已验证` label is untrusted metadata under rev-5.6.

The inspected primary paper sharpens the historical family but does not resolve the target. Page
269 assumes finitely many nodes, given branch lengths, and a path between every pair. Page 270
states Problem 2 as finding a minimum-total-length path between two given nodes `P` and `Q`. It
constructs minimum paths from `P` in increasing length, relaxes paths to frontier nodes, selects a
node of minimum tentative distance, and stops when `Q` is settled. Remark 1 permits branch length
to depend on traversal direction.

That is a one-pair source-to-target procedure, whereas the catalog uses a modern single-source
gloss that can naturally mean output for all reachable vertices. The paper gives no separately
named binder-complete correctness theorem or formal invariant, and its image-only scan is an
inspected, hashed lead rather than an accepted immutable source packet. No independently reviewed
transport selects one-pair correctness, all-distance correctness, predecessor correctness,
termination and total correctness of an implementation, or complexity as this target's exact
root. Choosing one would invent, narrow, broaden, or substitute proposition-changing mathematics.

The unresolved decisions also include directed versus undirected and simple versus multi-edge
graphs; the finite carrier and edge identity; the weight carrier, order, addition and nonnegativity
conditions; unreachable and infinity conventions; paths versus walks; state, relaxation, minimum
selection and tie semantics; output and stopping behavior; and zero-size, disconnected,
source-equals-target, zero-weight, cycle and multiple-shortest-path cases.

The prerequisite intake is only provisional `[_]`, not master-accepted `[x]`. Its receipt is
unaccepted, non-content-addressed, and contains no accepted receipt ID. Its historical checker now
fails because it freezes the pre-integration intake cursor `[ ]` with zero attempts, while current
authority records `[_]` with one attempt. Rev-5.6 section 10.2 permits preparation of this blocker,
but accepted closure remains dependency ordered.

Under sections 5 and 5.1, statement ambiguity and a missing expression fingerprint are hard
blockers. With no canonical expression, minimal canonical imports, checked alternate transports,
and the required removed-hypothesis, changed-domain, changed-binder-scope and boundary-case
mutations are undefined, not passed. The vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates under the pinned environment. Its
three direct imports expose unweighted simple-graph distance, additive quiver-path weights, and a
noncomputable edge-count-minimal quiver path. Fifteen adjacent APIs elaborate, but none defines a
Dijkstra state or execution and none proves Dijkstra correctness. These are discovery imports, not
a minimal-import result for an absent canonical target.

A bounded exact-name search found no Dijkstra-named declaration in repository-local Lean or pinned
mathlib. That is narrow feasibility evidence, not the downstream immutable anchor audit or a
global absence proof.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other dependency mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Lean commands ran from
`Formalizations/Lean`; other commands ran from the repository root. Exact hashes and command
records are preserved in `statement-blocker.json`, which is a worker blocker report rather than a
node receipt or accepted state authority.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0825` | 0 | rank 1383; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped authority, source, primary-scan and complete intake inspection | 0 | confirmed provisional dependency, null target, one-pair versus modern single-source mismatch, and unresolved proposition-defining inputs |
| `python3 -B Stage1_Instances/THM-M-0825/check_intake.py` | 1 | historical intake replay stopped at its frozen `[ ]`/zero-attempt cursor after integration advanced authority to `[_]`/one attempt; this phase did not rewrite intake evidence |
| pinned Lean, Lake, mathlib revision/tree/status and source-hash checks | 0 | expected toolchain and clean pinned dependency confirmed |
| `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0825/IntakeProbe.lean` | 0 | fifteen adjacent APIs elaborated; stdout 2465 bytes, SHA-256 `4d50b36c...01783a`; no canonical target or proof body |
| bounded case-insensitive `Dijkstra` search over repository-local Lean and pinned mathlib | 1 | expected no-match result; no Dijkstra-named declaration found in the searched roots |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON parsing, blocker-invariant, whitespace, and absent-self-test checks are recorded in the
structured blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable independent
source and graph-algorithm reviewers must then lawfully preserve and hash an immutable primary or
approved authoritative source, select one exact proposition and any transport from the 1959
one-pair procedure to a modern single-source formulation, and map every incorporated definition,
premise, algorithm step, proof boundary, correction and erratum. They must freeze the graph, edge,
weight, reachability, path, state, relaxation, tie, termination, output, complexity, binder,
hypothesis, conclusion, foundation-profile and degenerate-case conventions.

A fresh statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt change is proposed. Because the exact-statement deliverable did
not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, accepted state, proof
credit, or master acceptance is claimed.
