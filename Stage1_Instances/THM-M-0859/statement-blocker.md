# THM-M-0859 exact-statement gate: blocked

- Item: `S56-M-0859-STATEMENT`
- Base revision: `0c019b7194c9c43fa5f683fa82d637a0b275410d`
- Base tree: `43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully frozen from the received source record. The catalog
supplies only the title Vizing theorem and the gloss "the edge chromatic number of a graph." It
does not state an inequality or decide what kind of graph is meant. The immutable secondary source
inspected during intake states two related results:

- for finite undirected loopless multigraphs,
  `Delta(G) <= chi'(G) <= Delta(G) + mu(G)`; and
- for finite simple graphs, the specialization
  `Delta(G) <= chi'(G) <= Delta(G) + 1`.

These are not interchangeable encodings of one already selected root. The general theorem permits
parallel edges and uses maximum multiplicity; mathlib's `SimpleGraph` representation discards that
case. Selecting the convenient simple statement
`G.lineGraph.Colorable (G.maxDegree + 1)` would therefore narrow the source-backed theorem family
without an accepted source or ownership decision. Conversely, inventing a multigraph
representation would decide graph, edge, degree, multiplicity, coloring, and finiteness conventions
that the repository never fixed.

The 1964 Russian primary paper was not obtained or inspected. No accepted edition or translation,
pinpoint theorem and proof boundary, definition map, correction/errata disposition, or independent
source review is available. Even after choosing a variant, the source record does not decide
whether the root includes both bounds or only the characteristic upper bound, whether chromatic
index is a minimum or an existence statement, whether edge coloring is direct or transported
through a line graph, or how empty, edgeless, disconnected, maximum-degree-zero, and parallel-edge
cases are represented. These choices affect the proposition, ordered binders, hypotheses,
conclusion, imports, and kernel expression.

The prerequisite intake has only the authoritative provisional cursor `[_]`, not accepted `[x]`:
its receipt records `proposed_state: "[_]"` and `accepted: false`, is not content-addressed, and has
no accepted receipt ID. Current replay of its
historical checker fails because integration committed the intake artifacts and advanced the
repository base and authority hashes; this statement phase preserved the intake artifacts rather
than rewriting them as fresh intake evidence. Dependency master acceptance would independently be
required for closure.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing canonical expression fingerprint
hard blockers. With no canonical target, canonical import minimality, checked alternate transports,
and the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations
are undefined, not successful statement tests. The vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates under the pinned environment with
these direct imports:

- `Mathlib.Combinatorics.SimpleGraph.Coloring`
- `Mathlib.Combinatorics.SimpleGraph.Finite`
- `Mathlib.Combinatorics.SimpleGraph.LineGraph`

It checks the edge-set, line-graph, coloring, colorability, maximum-degree, and degree-bound APIs,
and confirms that the prospective simple proposition
`G.lineGraph.Colorable (G.maxDegree + 1)` is well-formed. Those three modules appear necessary for
that candidate surface: they respectively supply `Colorable`, `maxDegree`, and `lineGraph`, and do
not publicly import one another. They are not certified as the minimal imports of an absent
canonical target.

A bounded exact-topic search of pinned mathlib and repository-local Lean found no Vizing,
chromatic-index, chromatic-class, or proper-edge-coloring declaration. The only relevant match is
documentation in `SimpleGraph.EdgeLabeling` that expressly distinguishes arbitrary edge labels
from proper edge coloring. This is narrow feasibility evidence only, not the downstream anchor
audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other dependency mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Lean commands ran from
`Formalizations/Lean`; all other commands ran from the repository root unless noted. Exact command
and result records, current authority hashes, intake hashes, and pinned-source hashes are preserved
in `statement-blocker.json`. That JSON is a worker blocker report, not a node receipt or accepted
state authority.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0859` | 0 | rank 1413; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped reads of the blueprint, skill, manifest, catalog, Stage0 record, execution DAG, and complete intake dossier | 0 | confirmed provisional dependency, null target, inequivalent variants, and unresolved proposition-defining inputs |
| `sha256sum` over current authority, source, intake, toolchain, lockfile, and relevant pinned mathlib inputs | 0 | current digests for all named inputs are recorded in the structured blocker |
| pinned Lean, Lake, and mathlib revision/tree/status checks | 0 | Lean 4.29.0, Lake 5.0.0, and the expected clean pinned mathlib revision and tree |
| `lake env lean ../../Stage1_Instances/THM-M-0859/IntakeProbe.lean` | 0 | seven adjacent APIs and the prospective simple proposition elaborated; output SHA-256 `08181e2e...bffd`; no canonical target or proof body was declared |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 0 | one documentation match distinguishing edge labeling from proper coloring; output SHA-256 `35428597...179b`; no target declaration found |
| `python3 -B Stage1_Instances/THM-M-0859/check_intake.py` | 1 | historical intake replay stopped at its intake-only worktree inventory after integration committed those artifacts and advanced authority bytes; this phase did not rewrite it |
| JSON parse, scoped blocker invariants, and prohibited-construct scan | 0 aggregate | blocker identity, null target, unchanged vector, false completion fields, exact owned scope, and no proof escape agree |
| scoped whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement completion gate failed |

The intake checker was authored for an earlier untracked nine-file intake packet at revision
`464759128569180ab640c412cd80bc5dd2c3b44a`. Those files are now committed and the generated
blueprint and execution DAG have changed. Adding statement blocker artifacts also exceeds its
frozen intake-only inventory. This phase records that stale replay honestly rather than modifying
the intake checker, receipt, instance, task DAG, generated blueprint, or authoritative execution
DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first master-accept current intake evidence. Accountable independent
reviewers must then lawfully preserve and hash the 1964 primary source and any necessary
translation; pinpoint and approve its definitions, assumptions, theorem, proof, and correction
boundaries; and decide whether this target owns the loopless-multigraph `Delta + mu` theorem, the
finite-simple-graph `Delta + 1` specialization, or a checked relationship between them.

A fresh statement worker can then freeze graph and edge types, loop and multiplicity policies,
finiteness and decidability presentation, proper edge adjacency and coloring, maximum degree and
multiplicity, chromatic-index versus coloring-existence formulation, lower-bound composition,
ordered binders, hypotheses, conclusions, and all boundary cases. It must elaborate exactly that
approved proposition with minimal pinned imports, serialize and hash its kernel expression and
environment, compile each credited direct/line-graph or general/simple transport, and execute all
four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt change is proposed. Because the exact-statement deliverable did
not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, accepted state, or
master acceptance is claimed.
