# THM-M-0824 exact-statement gate: blocked

Item: `S56-M-0824-STATEMENT`

Base revision: `444860f481e8bbf64a3357008fd4d01a52006f08` (tree
`dee24a14497f877ebd81712a99d2da08de62d7ad`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0824-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, is not
content-addressed, has no accepted receipt IDs, and is bound to an earlier base and authority
snapshot. Rev-5.6 section 10.2 permits preparation of this blocker while concurrency is enabled,
but master closure remains dependency ordered.

Independently and decisively, the exact-statement gate fails. The complete catalog record is the
label `Prim algorithm`, the attribution Robert Prim, the year 1957, and the gloss "another
algorithm for minimum spanning trees." That identifies an algorithm family and purpose, not a
stable truth-valued proposition. It supplies no cited work or passage, graph representation,
weight domain, ordered binder, hypothesis, conclusion, proof boundary, correction, erratum, or
formal artifact. Its verified label is untrusted metadata under rev-5.6.

The missing choices alter the proposition:

- finite simple graph, multigraph, or another undirected representation, including loops and
  parallel-edge policy;
- connectedness, nonemptiness, forest behavior, start vertex, and empty or singleton inputs;
- weight carrier, order and addition laws, exact or machine arithmetic, and tie semantics;
- frontier, state transition, failure and stopping rules, and deterministic or nondeterministic
  execution;
- output as an edge set, subgraph, parent map, trace, or executable result; and
- termination, spanning-tree validity, minimum-weight optimality, uniqueness, implementation
  refinement, complexity, or an exact conjunction as the conclusion.

Prim's 1957 paper is a credible bibliographic lead, but the repository does not cite it and no
immutable article body, exact algorithm passage or proposition, incorporated definitions, proof
mapping, correction audit, or independent review has been admitted. The related Stage0 row
`THM-C-0095` says that Prim's minimum-spanning-tree algorithm is correct, but it is outside the
rev-5.6 target set and likewise omits the computation model and exact premises. There is no
accepted alias or deduplication crosswalk.

Selecting a familiar textbook correctness theorem would therefore invent, narrow, broaden, or
substitute proposition-changing mathematics. Encoding the desired conclusion as a premise,
opaque predicate, axiom, or placeholder would not repair the missing statement. Under rev-5.6
sections 5 and 5.1, there is no canonical Lean expression whose imports can be minimized, no
expression or canonical-target environment fingerprint, no approved alternate transport, and no
meaningful removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation.
Those four mutation classes are undefined, not passed. The root remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated using the pinned environment. Its
single direct import exposes six adjacent finite-simple-graph, spanning-subgraph, tree, and finite
edge APIs. These interfaces do not define weights, Prim iteration, a frontier or tie rule, an
output tree, minimum total weight, or a correctness theorem. The probe import is not a
minimal-import result for an absent target and receives no statement or proof credit.

A bounded exact-topic search over repo-local Lean and pinned mathlib found no Prim-algorithm or
minimum-spanning-tree declaration. This is scoped feasibility evidence, not the later anchor audit
or a global absence proof.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The exact probe output SHA-256 is
`bc531cbb8d28a50e48f0465276955cf6b32ee3af75f44c61dc083350e2aa4cba`; the two imported theorem
axiom reports list only `propext`, `Classical.choice`, and `Quot.sound`.

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
| `python3 scripts/stage1_target.py show THM-M-0824` | 0 | rank 1382; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| authority, source, and intake-dossier inspection plus catalog `git blame` | 0 | the catalog contains only an algorithm-family gloss; all six lines originate in corpus commit `bcf3f9fa...`; intake leaves the exact claim and formal target null |
| `python3 -B Stage1_Instances/THM-M-0824/check_intake.py` | 1 | historical intake checker expects authoritative intake `[ ]` with zero attempts; current authority records provisional `[_]` with one attempt; prior evidence was not rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions agree with the environment above |
| pinned mathlib revision, tree, source hashes, and package-status checks | 0 | revision and tree agree with the lock; package worktree was clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0824/IntakeProbe.lean` | 0 | six adjacent APIs elaborated; exact output hash is recorded above; no canonical target or proof body was introduced |
| bounded exact-topic Lean search excluding the owned dossier | 1 | expected no-match result; no exact-topic declaration was found in the searched roots |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must first master-accept fresh intake evidence. Accountable source and graph-
algorithm reviewers must then preserve and hash an immutable primary or approved authoritative
source, select and independently approve one exact Prim proposition, and map every incorporated
definition, binder, premise, conclusion, algorithm step, proof boundary, correction, and erratum.
They must freeze the graph and weight models, start, frontier, tie, transition, stopping, failure,
output, correctness and resource claims, arithmetic policy, neighboring-target boundary, and all
degenerate cases.

A later statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; the vector `[H5, M4, R4]` is unchanged; `audit_complete: false` and
`theorem_complete: false`. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
