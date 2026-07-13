# Exact-statement gate: blocked

Item: `S56-M-0823-STATEMENT`

Theorem: `THM-M-0823`

Base revision: `561d83df037004ceb2259292d7c63be930b40391` (tree
`6eb02475bf5a70139d60615c924b31c930efc2bb`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record gives only the label `Kruskal算法` (Kruskal's algorithm), Joseph Kruskal, the year 1956,
and the gloss `最小生成树的贪心算法` (a greedy algorithm for a minimum spanning tree). It supplies no
citation, truth-valued proposition, graph or edge model, ordered binders, hypotheses, conclusion,
algorithm semantics, proof boundary, correction history, or formal artifact. Stage0 explicitly
leaves precise definitions and premises open, and rev-5.6 treats the catalog's `已验证` label as
untrusted metadata.

Kruskal's 1956 paper *On the shortest spanning subtree of a graph and the traveling salesman
problem* is a strong source-family lead. It discusses finite connected graphs with positive real
edge lengths, initially distinct, states uniqueness, gives Construction A, and proves the selected
edges form a shortest spanning tree by an exchange argument. The catalog does not cite that paper
or select one of its results as the root. The inspected discovery copy is not an admitted immutable
source edition, and its definitions, assumptions, tie generalization, proof boundary, corrections,
errata, and source-to-target mapping have not received independent review.

An exact statement would still have to choose:

- correctness of Construction A, minimum-tree existence, distinct-weight uniqueness, bundled total
  correctness, complexity, or another explicitly sourced root;
- finite simple graphs or multigraphs, connected input or componentwise forests, and the precise
  undirected-edge and returned-subgraph representation;
- positive distinct real weights or a broader ordered weight type, together with a tie policy;
- deterministic, nondeterministic, relational, or sorted-list algorithm semantics, including state,
  cycle rejection, termination, and accepted and rejected edges;
- the spanning-tree feasibility predicate, total-weight objective, minimality quantification, and
  whether uniqueness is concluded; and
- empty and singleton vertex types, disconnected graphs, absent edges, loops or parallel edges,
  negative, zero, or repeated weights, and equality of returned structures.

Those choices yield inequivalent propositions. Importing the stronger Stage0 `THM-C-0094`
correctness gloss, proving generic unweighted spanning-tree existence, selecting only uniqueness, or
choosing a convenient modern tied-weight variant would invent, narrow, broaden, or substitute
mathematics rather than elaborate this target.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. The intake therefore correctly leaves the canonical human claim, Lean
module and expression, minimal imports, and expression/environment fingerprints null at
`[H5, M4, R4]`. Without a canonical target, checked transports and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined, not passed. No
`Statement.lean`, axiom, placeholder, assumed correctness interface, weakened example, or
broadened theorem was introduced.

The prerequisite `S56-M-0823-INTAKE` is provisional worker state `[_]`, not master-accepted `[x]`.
Its receipt is unaccepted and has no accepted receipt ID. Rev-5.6 section 10.2 permits this
dependency-ordered blocker attempt, but master acceptance remains required before a future statement
transition can be accepted.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with the pinned environment. Its direct imports are:

```lean
import Mathlib.Combinatorics.SimpleGraph.Acyclic
import Mathlib.Combinatorics.SimpleGraph.Subgraph
```

All six checks for acyclicity, trees, spanning subgraphs, edge sets, spanning coercion, and
unweighted spanning-tree existence pass. The probe defines no weights or Kruskal transition,
selects no source root, gives no optimality statement or checked transport, and contains no proof
body. Its imports cannot be certified minimal for a target that has not been selected and receive no
statement or proof credit. The complete probe output is 556 bytes with SHA-256
`cf37199a03bacae12b728135a872ec7aecb8ae16879eb9d28a13b6196d6fc9de`.

A bounded exact-topic search of pinned mathlib and repository-local Lean found no minimum-spanning-
tree algorithm or correctness declaration. The only surname matches are the unrelated
Kruskal-Katona set-family theorem. This is discovery-only feasibility evidence, not the downstream
immutable anchor audit or a claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link points to canonical pinned artifacts and was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0823` | 0 | rank 1381, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped manifest, blueprint, skill, catalog, Stage0, intake, scope, and crosswalk inspection | 0 | only an algorithm-family gloss is authoritative; every proposition-changing choice remains open |
| `git blame -L 6047,6052 -- Docs/researches/math_theorems.md` and source excerpt hashing | 0 | all six uncited catalog lines originate at `bcf3f9fa...`; the current excerpt SHA-256 is `e771798d...f408` |
| `sha256sum` over authority, intake, toolchain, lock, and pinned mathlib inputs | 0 | current hashes are recorded in `statement-blocker.json`; historical intake evidence was not rewritten |
| `python3 -B Stage1_Instances/THM-M-0823/check_intake.py` | 1 | historical intake replay stops at its frozen blueprint hash after integration changed the generated authority cursor; it is not statement validation |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree agree with the fingerprint; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0823/IntakeProbe.lean` | 0 | six adjacent APIs elaborated; output size and hash are recorded above; no canonical target was stated |
| bounded exact-topic searches over repo-local Lean and pinned mathlib | 1 each (expected no match) | no minimum- or shortest-spanning-tree algorithm target matched; a separate pinned-mathlib surname search found only unrelated Kruskal-Katona material |
| prohibited Lean construct scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| JSON parse and scoped invariant check for `statement-blocker.json` | 0 each | IDs, open state, null canonical target expression/imports, unchanged vector, four undefined mutations, false completion fields, exact paths, and absent self-test agree |
| whitespace checks for both added blocker artifacts | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash a lawful immutable primary or authoritative source, select and independently
approve one exact result and every incorporated definition, and freeze the graph, edge, weight,
tie, transition, termination, output, objective, binder, hypothesis, conclusion, proof-boundary,
correction, erratum, neighbor-boundary, and degenerate-case conventions.

A fresh statement worker can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master
acceptance is claimed.
