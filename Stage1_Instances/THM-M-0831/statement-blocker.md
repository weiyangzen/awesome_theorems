# THM-M-0831 exact-statement gate: blocked

Item: `S56-M-0831-STATEMENT`

Base revision: `748243faadc15828fb087059337fd05b7be9fdeb` (tree
`e46d642646f80980838b6f016f5d69b817bd464d`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0831-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, is not
content-addressed, and has no accepted receipt IDs. Rev-5.6 section 10.2 permits preparation of
this blocker while concurrency is enabled, but master closure remains dependency ordered.

Independently and decisively, the exact-statement gate fails. The complete catalog record is the
label `Karger algorithm`, the attribution David Karger, the year 1993, and the gloss "a randomized
algorithm for global minimum cut." That identifies an algorithm family and purpose, not a stable
truth-valued proposition. It supplies no citation, graph or cut definition, contraction semantics,
ordered binder, hypothesis, conclusion, probability or complexity convention, proof boundary,
correction, erratum, or formal artifact. Its verified label is untrusted metadata under rev-5.6.

The inspected primary-source lead is David R. Karger's SODA 1993 paper *Global Min-cuts in RNC,
and Other Ramifications of a Simple Min-Cut Algorithm*. Section 2 defines random contraction on a
connected undirected multigraph. Theorem 2.1 says that one run returns a particular fixed minimum
cut with probability `Omega(n^-2)`; its proof gives the explicit lower bound
`1 / binom(n, 2)`. Corollary 2.1 instead amplifies independent runs to obtain a high-probability
claim. Weighted implementation, correctness, sequential cost, and RNC claims are further distinct
members of the source family.

The repository does not cite or independently approve one of those roots. It also does not freeze:

- finite connected undirected multigraph data, unused carrier elements, input loops, and parallel
  edges;
- nontrivial cuts, crossing multiplicity, complement equality, a particular minimum cut, and
  minimum-cut existence;
- uniform selection among current edge instances, endpoint quotienting, preservation of parallel
  edges, loop deletion, state invariants, output, and termination at two supervertices;
- exact versus asymptotic probability, the probability codomain and coercions, single-run versus
  repeated execution, independence, trial count, and failure parameter; or
- ordered binders, typeclass context, small graphs, disconnected or edgeless graphs, multiple
  minimum cuts, stuck states, denominator-zero behavior, and all weighted or cost-model cases.

Selecting Theorem 2.1, its explicit proof bound, Corollary 2.1, or a familiar end-to-end correctness
theorem would therefore invent, narrow, broaden, or substitute proposition-changing mathematics.
Under rev-5.6 sections 5 and 5.1, there is no canonical Lean expression whose imports can be
minimized, no expression or canonical-target environment fingerprint, no approved alternate
transport, and no meaningful removed-hypothesis, changed-domain, changed-binder-scope, or
boundary-case mutation. Those four mutation classes are undefined, not passed. The root remains
`[H5, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated using the pinned environment. Its
two direct imports are:

- `Mathlib.Combinatorics.Graph.Basic`
- `Mathlib.Probability.Distributions.Uniform`

The probe authenticates a multigraph representation with explicit edge identities and finite
uniform sampling interfaces. It does not define cuts, contraction states or transitions, a
trajectory, output equality, or a Karger probability theorem. These probe imports are not a
minimal-import result for an absent canonical target and receive no statement or proof credit.

A bounded exact-topic search over repo-local Lean and pinned mathlib found no Karger, global
minimum-cut, or random-contraction declaration. This is scoped feasibility evidence, not the later
anchor audit or a global absence proof.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The exact probe-output SHA-256 is
`91f3035c7ca8b77949624c692bc49f833a487aa5cf8f0c02ae157515d86b7a1d`.

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
| `python3 scripts/stage1_target.py show THM-M-0831` | 0 | rank 1389; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| authority, source, and intake-dossier inspection plus catalog `git blame` | 0 | the catalog contains only an algorithm-family gloss; all six lines originate in corpus commit `bcf3f9fa...`; intake leaves the exact claim and formal target null |
| `python3 -B Stage1_Instances/THM-M-0831/check_intake.py` | 1 | historical intake checker expects authoritative intake `[ ]` with zero attempts; current authority records provisional `[_]` with one attempt; prior evidence was not rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions agree with the environment above |
| pinned mathlib revision, tree, source hashes, and package-status checks | 0 | revision and tree agree with the lock; package worktree was clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0831/IntakeProbe.lean` | 0 | ten adjacent APIs elaborated; exact output hash is recorded above; no canonical target or proof body was introduced |
| bounded exact-topic Lean search excluding the owned dossier | 1 | expected no-match result; output was empty with SHA-256 `e3b0c442...b855`; no exact-topic declaration was found in the searched roots |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must first master-accept fresh intake evidence. Accountable source and graph-
algorithm reviewers must then preserve and hash an immutable primary or approved authoritative
source, select and independently approve one exact Karger proposition, and map every incorporated
definition, binder, premise, conclusion, algorithm step, probability or resource convention, proof
boundary, correction, and erratum. They must freeze the graph, cut, contraction, output,
probability, repetition, arithmetic, boundary-case, foundation, TCB, and computation profiles.

A later statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; the vector `[H5, M4, R4]` is unchanged; `audit_complete: false` and
`theorem_complete: false`. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
