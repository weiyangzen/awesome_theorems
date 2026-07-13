# Exact-statement gate: blocked

Item: `S56-M-0868-STATEMENT`

Theorem: `THM-M-0868`

Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e` (tree
`6434a20532ae7c523ad293e67a6228ab384bfb8a`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete catalog claim is the title `图子式定理`, the attribution Robertson/Seymour, the period
1983-2004, and the gloss `Wagner猜想的证明` ("proof of Wagner's conjecture"). It gives no exact
proposition, graph model, minor definition, ordered binders, hypotheses, conclusion, proof
boundary, correction history, formal artifact, or reviewer. Stage0 repeats the gloss while
explicitly leaving the formal system, definitions, premises, proof route, dependencies, alternate
forms, axioms, machine status, and artifacts open. The catalog's `已验证` label is untrusted
inventory metadata under rev-5.6.

This attempt inspected, but did not vendor, the author-hosted 34-page Robertson-Seymour draft of
*Graph Minors. XX. Wagner's conjecture*. Its abstract states that every infinite set of finite
graphs contains one member isomorphic to a minor of another. The introduction says that all graphs
in the paper are finite. Theorem 10.5 instead states a countable-sequence theorem for directed
graphs: there are
`j > i >= 1` such that `G_i` is isomorphic to a minor of `G_j`. The preceding sentence defines the
directed minor relation by taking a subgraph and contracting edges and says that this result
immediately implies the standard undirected form.

Those passages identify the theorem family but do not select one source-identical Lean root. In
particular, the paper's Section 2 models a graph through finite vertex and edge sets with an
incidence relation, allowing one-ended and distinct parallel edges. Mathlib's `SimpleGraph` is an
irreflexive binary relation without edge multiplicity. Using `SimpleGraph` directly would therefore
require a checked model and contraction transport, not an unstated simplification. The repository
also does not decide:

- the abstract infinite-set form, Theorem 10.5's directed countable-sequence form, the standard
  undirected form, or a `WellQuasiOrdered` encoding as the canonical root;
- the set-to-sequence and directed-to-undirected implications, including choice, repetitions,
  isomorphism representatives, and relation orientation;
- edge contraction, deletion, loop and parallel-edge behavior, subgraph semantics, branch-set
  alternatives, or simplification into a simple graph;
- varying finite graph carriers, universes, finiteness and decidability inputs, binder order,
  boundary cases, foundation/TCB/computation profiles, and credited alternate encodings; or
- whether this target is independent from or a duplicate/redirect of `THM-M-0867`, which names the
  same Robertson-Seymour graph-minor WQO family and already points to the same primary work.

Selecting a familiar finite-simple-graph WQO statement would therefore invent, narrow, or
substitute proposition-changing mathematics. A deletion-only, induced-subgraph, matroid-minor,
planar-graph, bounded-treewidth, fixed-size, or hypothesis-stored result is also not the target.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. The intake correctly leaves the canonical human statement,
Lean module and expression, minimal imports, and expression/environment fingerprints null at
`[H1, M4, R4]`. Without a canonical target, checked transports and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined, not passed. No
`Statement.lean`, axiom, placeholder, invented graph-minor interface, weakened theorem, or broadened
theorem was introduced.

The prerequisite `S56-M-0868-INTAKE` has only provisional worker state `[_]`, not master-accepted
state `[x]`. Its receipt is unsigned, non-content-addressed, declares `accepted: false`, and contains
no accepted receipt ID. Rev-5.6 permits recording this dependency-ordered blocker attempt, but
master acceptance remains independently required before any future statement transition.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates in the pinned environment. Its four direct imports
authenticate six adjacent `SimpleGraph` deletion/isomorphism/induced-graph and generic WQO APIs.
They do not define the source graph category, edge contraction, a graph-minor relation, the
directed-to-undirected transport, a canonical target, or a proof body. Consequently these imports
are substrate evidence only and cannot be certified minimal for an absent canonical target.

A bounded exact-topic search over repository-local and pinned-mathlib Lean sources found no direct
Graph Minor Theorem, Robertson-Seymour/Wagner-conjecture declaration, or graph-minor/contraction
interface. This is narrow discovery evidence, not the downstream immutable anchor audit or a claim
of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link to canonical pinned artifacts was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository root unless
a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0868` | 0 | rank 1422; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| scoped manifest, blueprint, skill, guidelines, catalog, Stage0, and complete intake inspection | 0 | the repository does not select an exact graph model, minor encoding, formulation, or duplicate disposition; intake deliberately leaves the canonical claim and target null |
| author PDF retrieval plus `wc -c`, `sha256sum`, `pdfinfo`, and `pdftotext -layout` in `/tmp` | 0 | 34 pages, 251,605 bytes, SHA-256 `327694f043a8809dfb0255171c470ae4ba5b15d7fedbad861c43f1f3a05caa91`; abstract, introduction, Section 2 graph convention, and paper-page-29 Theorem 10.5 inspected as a source lead only |
| authority, source, intake, toolchain, lockfile, probe, and pinned-mathlib `sha256sum` checks | 0 | exact current fingerprints are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0868/check_intake.py` | 1 | the historical intake checker expects authoritative INTAKE state `[ ]`, attempts 0; integration now records provisional `[_]`, attempts 1, so historical evidence was preserved rather than rewritten |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions agree with the recorded environment |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree agree; the dependency worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0868/IntakeProbe.lean` | 0 | all six adjacent APIs elaborated; complete stdout SHA-256 `df9641e4f2a8f4eb12f09993327e1251f3b571dda24c5111a888faa3d45b2a8d`; no canonical target or proof body |
| bounded exact-topic search over repository-local and pinned-mathlib Lean | 1, expected no match | no direct target interface was located; discovery only |
| prohibited Lean construct scan over the owned path | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse, scoped blocker assertions, and whitespace checks | 0 | identity, null target/imports, unchanged vector, undefined mutations, false completion flags, exact two-file scope, and clean whitespace agree |
| `test ! -e .stage1-worker-selftest.json` | 0 | the self-test manifest is intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must first master-accept refreshed intake evidence, durably admit a lawful
immutable primary source, and resolve the
`THM-M-0867` duplicate/ownership boundary. Accountable independent reviewers must preserve and
approve an immutable primary edition, reconcile it with the version of record and corrections,
select one exact source proposition and incorporated definition chain, and freeze every graph
carrier, incidence and finiteness convention, minor operation, contraction behavior, formulation,
transport, binder, hypothesis, conclusion, foundation profile, and boundary case.

A fresh statement worker can then define or pin precisely that approved graph/minor model, encode
the same claim, minimize its pinned imports, serialize and hash its elaborated expression and
environment, compile every credited transport, and execute all four required mutation classes.

This is a truthful blocked-attempt record, not completion of the statement node or any downstream
node. Lifecycle remains `planned`; the item remains `[ ]`; the root remains `[H1, M4, R4]`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, proof credit, or master acceptance is claimed.
