# Exact-statement gate: blocked

Item: `S56-M-0863-STATEMENT`

Theorem: `THM-M-0863`

Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e` (tree
`6434a20532ae7c523ad293e67a6228ab384bfb8a`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the currently accepted repository
record. The target catalog supplies only `Whitney定理`, the attribution Hassler Whitney, the year
1932, and the gloss `2-连通图的耳分解` ("ear decomposition of 2-connected graphs"). It does not
define 2-connectivity or an ear, select a graph model or theorem direction, state ordered binders,
hypotheses, coverage, or boundary cases, or provide an accepted source transport. Stage0 repeats
that gloss while leaving these mathematical and formal choices open. The catalog's `已验证` label
is explicitly untrusted metadata under rev-5.6.

The intake inspected a strong primary-source lead. Whitney's 1932 *Non-separable and planar
graphs*, Theorem 19, states that any non-separable graph containing at least two arcs can be built
from a circuit by successively adding arcs or suspended chains while every partial graph remains
non-separable; the immediately following sentence states the converse. Whitney's finite graphs may
have loops and parallel arcs, however, whereas Lean's `SimpleGraph` excludes both. Whitney also
uses a historically qualified non-separability predicate rather than one already checked to equal
the modern at-least-three-vertices, connected-after-one-vertex-deletion convention.

The repository therefore does not yet fix any one of these proposition-changing decisions:

- Whitney's historical graph carrier or a source-approved finite `SimpleGraph` specialization;
- non-separability, vertex-deletion connectivity, or internally vertex-disjoint paths as the exact
  2-connectivity predicate, including all size qualifications;
- a cyclic walk, cycle subgraph, or cycle-graph isomorphism as the initial object;
- the precise open-ear path conditions, distinct endpoints, single-edge ears, new internal
  vertices and edges, ordered partial unions, and exact final vertex and edge coverage;
- forward construction, converse, or biconditional as the canonical root; and
- universes, finiteness and decidability presentation, binder order, hypotheses, and degenerate
  cases such as an initial cycle with no additional ears.

Choosing the familiar finite-simple-graph biconditional would consequently substitute an
unapproved modern theorem for the received target. Choosing only forward existence, the historical
multigraph theorem, or the converse would choose a different unresolved direction. Sections 5 and
5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression fingerprint hard
blockers; the execution skill requires a hard stop when identifying a statement would invent
missing mathematics. The intake accordingly leaves the canonical claim, formal module and
expression, minimal imports, and expression/environment fingerprints null at `[H1, M4, R4]`.

Without a canonical proposition, checked alternate transports and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined rather than passed.
No `Statement.lean`, axiom, placeholder, invented graph interface, weakened result, or broadened
theorem was introduced.

The prerequisite `S56-M-0863-INTAKE` is only provisional worker state `[_]`, not master-accepted
state `[x]`. Its receipt is unsigned, non-content-addressed, declares `accepted: false`, and has no
accepted receipt ID. Section 10.2 permits this dependency-ordered blocker attempt, but any future
statement transition remains dependency ordered and requires independent master acceptance.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with the sole direct import
`Mathlib.Combinatorics.SimpleGraph.Connectivity.Subgraph`. It authenticates nine adjacent APIs for
ordinary connectivity, paths and cycles, walk-to-subgraph conversion, induced support, induced
subgraphs, and vertex deletion. The probe does not define 2-vertex-connectivity, an ear, an ordered
ear decomposition, a canonical target, a graph-model transport, or a proof body. Its import is
therefore substrate evidence only and cannot be certified minimal for an absent target.

A bounded exact-topic search over repository-local and pinned-mathlib Lean sources found no direct
ear-decomposition, suspended-chain, non-separable-graph, biconnected-graph, or named vertex-2-
connectivity declaration. This is narrow discovery evidence, not the downstream immutable anchor
audit or a claim of global absence.

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
| `python3 scripts/stage1_target.py show THM-M-0863` | 0 | rank 1417; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| scoped manifest, blueprint, skill, guidelines, catalog, Stage0, and complete intake inspection | 0 | the repository does not select an exact theorem direction, graph-model transport, or encoding; the intake deliberately leaves the canonical claim and formal target null |
| authority, source, intake, toolchain, lockfile, probe, and pinned-mathlib `sha256sum` checks | 0 | exact current fingerprints are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0863/check_intake.py` | 1 | the historical intake checker expects its own authoritative intake item to remain `[ ]`; integration has advanced it provisionally to `[_]`; historical evidence was preserved rather than rewritten |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions agree with the recorded environment |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree agree; the dependency worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0863/IntakeProbe.lean` | 0 | all nine adjacent APIs elaborated; complete stdout SHA-256 `fb9e46a5268e0922d4e3691657e756d5e8324f700f823b4f9d0275fa5dbdf7cf`; no canonical target or proof body |
| bounded exact-topic search over repository-local and pinned-mathlib Lean sources | 1, expected no match | no direct target interface was located; discovery only |
| prohibited Lean construct scan over the owned path | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse, scoped blocker assertions, and whitespace checks | 0 | identity, null target/imports, unchanged vector, undefined mutations, false completion flags, exact two-file scope, and clean whitespace agree |
| `test ! -e .stage1-worker-selftest.json` | 0 | the self-test manifest is intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable independent
reviewers must then lawfully preserve and hash an immutable primary or approved authoritative
source; approve the construction, converse, or biconditional root; and approve the historical-to-
modern graph transport plus every connectivity, cycle, ear, order, partial-union, coverage,
binder, hypothesis, correction, erratum, and boundary choice.

A fresh statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a truthful blocked-attempt record, not completion of the statement node or any downstream
node. Lifecycle remains `planned`; the item remains `[ ]`; the root remains `[H1, M4, R4]`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, proof credit, or master acceptance is claimed.
