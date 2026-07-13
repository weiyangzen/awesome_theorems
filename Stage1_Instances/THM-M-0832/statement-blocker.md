# THM-M-0832 exact-statement gate: blocked

Item: `S56-M-0832-STATEMENT`

Base revision: `748243faadc15828fb087059337fd05b7be9fdeb` (tree
`e46d642646f80980838b6f016f5d69b817bd464d`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0832-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, is not
content-addressed, has no accepted receipt IDs, and says review is due before dependent statement
work. Rev-5.6 section 10.2 permits preparation of this blocker while concurrency is enabled, but
master closure remains dependency ordered.

Independently and decisively, the exact-statement gate fails. The complete catalog record names the
Stoer-Wagner algorithm and calls it a deterministic algorithm for global minimum cut. That is an
algorithm family and purpose, not a truth-valued proposition with fixed binders and semantics. The
intake therefore deliberately leaves the canonical mathematical claim and Lean target null.

The inspected expanded primary source contains several related results that cannot be silently
conflated:

- Theorem 2.1 is a recurrence comparing a minimum `s`-`t` cut with a minimum cut after merging
  `s` and `t`.
- Lemma 3.1 says a maximum-adjacency phase cut is a minimum `s`-`t` cut for the last two vertices.
- Repeated phases and contractions, with the lightest phase cut retained, give the end-to-end
  algorithmic correctness route.
- Section 4 separately states a priority-queue running-time bound.

The catalog does not choose one of these or an exact conjunction. Selecting the likely end-to-end
result would still require proposition-changing choices that the admitted source crosswalk has not
approved: whether the root includes termination, a cut witness, only its value, the phase lemma,
the contraction recurrence, or complexity.

## Semantic Choices Still Open

The paper works with an ordinary undirected graph and nonnegative real edge weights, but a Lean
target must still choose a simple graph with a partial edge-weight function, a weighted multigraph,
or a total symmetric capacity matrix. That choice controls absent and zero-weight edges, parallel
edges, loops, and contraction.

The paper asks for a most tightly connected outside vertex and permits an arbitrary phase start.
It does not freeze tie breaking. Here, "deterministic" distinguishes this family from randomized
algorithms; it does not by itself choose one Lean function. Adding a vertex linear order or a
classical argmax would add unsourced semantics. A relational formulation instead has to state
which starts and tied choices are valid and whether correctness is quantified over every valid
run.

The target also must define:

- nontrivial cuts, complement symmetry, crossing-edge weight, and multiple-minimum behavior;
- maximum-adjacency state, phase output, stopping, and failure behavior;
- contraction by summing incident weights and removing the internal edge;
- nested supervertices and how a phase cut is lifted to the original vertex set;
- whether the output is a subset, bipartition, weight, certified pair, or execution trace; and
- if runtime is selected, the representation, priority queue, arithmetic and unit-cost model,
  Fibonacci-heap assumptions, input-size measures, and asymptotic conclusion.

Empty and singleton carriers have no nontrivial cut and do not fit the paper's uninitialized
current-minimum pseudocode. A two-vertex input runs one phase. The paper does not add connectedness,
so disconnected, edgeless, isolated-vertex, and zero-weight cases appear to remain in scope, while
negative weights are outside its stated domain. These boundaries need accountable approval rather
than an implementation guess.

Consequently there is no canonical expression to elaborate, no honest minimal-import result, no
expression or canonical-target environment fingerprint, and no checked alternate transport. The
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not passed. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with the pinned environment. Its
two direct imports expose nine adjacent finite-simple-graph and unweighted edge-connectivity APIs.
They do not define weighted cuts, maximum-adjacency phases, weighted contraction, original-vertex
provenance, a Stoer-Wagner output, or a correctness theorem. The probe imports are not a
minimal-import result for an absent target and receive no statement or proof credit.

A bounded exact-topic search over repo-local Lean and pinned mathlib returned no matching weighted
global-minimum-cut, maximum-adjacency, weighted-contraction, or Stoer-Wagner declaration. A
temporary exploratory relational shape confirmed that supervertex partitions, nondeterministic
maximum-adjacency orders, lifted phase cuts, contractions, an inductive run, and an end-to-end
correctness proposition are expressible in the pinned environment. It commits to unapproved graph,
run, quantifier, start, tie, output, and boundary choices, so it is not a candidate canonical target
and receives no statement or proof credit. Likewise, `SimpleGraph.map` does not itself sum collapsed
edge weights or retain original-vertex provenance.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The exact intake-probe stdout SHA-256 is
`6d9de3d924737eeb3046bbcf4c522021415b2ff06678d8cd65d5974c19529f44`.

The automation-provided `Formalizations/Lean/.lake` link points to canonical pinned artifacts and
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Record

Commands ran on 2026-07-13 (Asia/Shanghai), from the repository root unless another working
directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0832` | 0 | rank 1390; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| authority, source, intake, and primary-text inspection plus catalog `git blame` | 0 | the catalog does not select one proposition; all six catalog lines originate at corpus commit `bcf3f9fa...`; intake leaves the exact claim and target null |
| `python3 -B Stage1_Instances/THM-M-0832/check_intake.py` | 1 | historical intake checker expects authoritative intake `[ ]`; current authority records provisional `[_]`; prior evidence was not rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions agree with the environment above |
| pinned mathlib revision, tree, source-hash, and package-status checks | 0 | revision and tree agree with the lock; package worktree was clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0832/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; exact output hash is recorded above; no canonical target or proof body was introduced |
| bounded exact-topic Lean search over the local project and pinned mathlib | 1 | expected no-match result; empty output SHA-256 `e3b0c442...b855` |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean /tmp/slot12_stoer_wagner_trace_probe.lean` | 0 | a prospective relational shape elaborated; source SHA-256 `8e29aca2...4985`; noncanonical feasibility only |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must first revalidate and master-accept the intake. Accountable source and
graph-algorithm reviewers must then preserve and hash one lawful immutable primary or approved
authoritative edition, select and independently approve one exact proposition or conjunction, and
map every incorporated definition, premise, proof boundary, correction, and erratum. They must
freeze graph and weight representation, cut and output semantics, maximum-adjacency starts and
ties, contraction and original-vertex provenance, termination, any resource claim, ordered
binders, hypotheses, conclusion, transports, and every degenerate case.

A later statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; the vector `[H1, M4, R4]` is unchanged; `audit_complete: false` and
`theorem_complete: false`. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
