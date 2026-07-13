# Exact-statement gate: blocked

Item: `S56-M-0907-STATEMENT`

Theorem: `THM-M-0907`

Base revision: `fb0baac89ea0633612be3b47448464b4b8e4bef7` (tree
`018557070da18ea1733a82de81a238750c59aa84`). Attempt date: 2026-07-13
(Asia/Shanghai).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0907-INTAKE` is only provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, has no
accepted receipt ID, and is stale against the current authoritative blueprint. Replaying
`check_intake.py` stops at
`stale receipt input hash: Docs/Stage1_Blueprint_rev-5.6.md`. This statement attempt preserves the
historical intake artifacts rather than rewriting them.

Independently, the exact Lean 4 target cannot be truthfully elaborated from the received repository
record. The catalog fixes the name `Alon-Tarsi定理`, Noga Alon and Michael Tarsi, 1992, and only the
gloss `列表着色的组合Nullstellensatz方法` (a combinatorial-Nullstellensatz method for list coloring).
That is a theorem-family/method description, not a binder-complete proposition. It gives no
bibliography, definitions, assumptions, conclusion, proof boundary, correction, or erratum.

Alon and Tarsi's 1992 paper *Colorings and orientations of graphs* supplies a strong candidate:
Theorem 1.1 says, in the paper's notation, that unequal counts of even and odd Eulerian
subdigraphs imply a legal coloring from per-vertex integer sets of size outdegree plus one. But the
catalog does not select Theorem 1.1 over its ordinary-colorability corollary, the graph-polynomial
coefficient result, the separate Nullstellensatz-type proposition, a choosability application, or
an explicitly bundled theorem. The paper candidate has not been admitted through an independent
source-root review, so selecting it here would add mathematics rather than elaborate an exact
received target.

Even for Theorem 1.1, proposition-changing decisions remain open:

- whether the finite digraph is a loopless orientation of a simple graph and whether loops,
  antiparallel arcs, or parallel edges are allowed;
- whether Eulerian subdigraphs are spanning edge-subset objects, how degrees and parity are counted,
  and whether the disconnected and empty subdigraph conventions are represented exactly;
- whether allowed colors are finite sets of exactly outdegree plus one distinct integers or an
  at-least-size/list/multiset encoding with a checked transport;
- which underlying undirected adjacency defines proper coloring, and how empty, isolated,
  disconnected, zero-outdegree, and singleton-list cases behave; and
- every ordered binder, finiteness/decidability instance, universe, coercion, foundation choice,
  source correction, and 1992-interpolation versus 1999-Nullstellensatz route boundary.

Section 5 of the rev-5.6 blueprint makes statement ambiguity and a missing elaborated-expression
fingerprint hard blockers. There is therefore no canonical expression against which to certify
minimal imports, checked alternate transports, or the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations. Those tests are undefined, not passed. The root
vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with these direct imports:

- `Mathlib.Combinatorics.Digraph.Orientation`
- `Mathlib.Combinatorics.Nullstellensatz`
- `Mathlib.Combinatorics.SimpleGraph.Coloring`

It checks eight adjacent digraph, ordinary-coloring, and generic polynomial APIs. It does not
define list coloring, Eulerian-subdigraph parity counts, a graph polynomial, an Alon-Tarsi target,
or a proof body. Its imports are candidate substrate only and cannot be called minimal for an
absent canonical target.

A bounded exact-topic search of pinned mathlib and repository-local Lean found no Alon-Tarsi,
choosability/list-coloring, Eulerian-parity-subdigraph, or graph-polynomial declaration. This is
narrow discovery evidence, not the downstream anchor audit and not a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link was used read-only. No `lake update`, `lake build`, dependency
clone/fetch, or other dependency mutation was run; the pinned mathlib package remained clean.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13. Lean commands used `Formalizations/Lean`; other
commands used the repository root unless noted. Exact structured command results and current input
hashes are recorded in `statement-blocker.json`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0907` | 0 | rank 1449; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped reads and SHA-256 checks over authority, source, and the complete intake dossier | 0 | confirmed a provisional dependency, null canonical claim/target, stale intake authority hashes, and unresolved root/encoding decisions |
| `python3 -B Stage1_Instances/THM-M-0907/check_intake.py` | 1 | historical intake replay stopped at its stale blueprint hash; this phase did not rewrite intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree/status checks | 0 | expected revision and tree; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0907/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; output SHA-256 `c6cbcc520887f5ecec3451983202beb85d518181bcb6df532d82a35232077cf9`; no canonical target or proof body |
| bounded exact-topic search in pinned mathlib and repository-local Lean | 1 | expected no-match result; discovery only |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse, scoped blocker invariant check, and whitespace checks | 0 aggregate | blocker identity, null target/imports, unchanged vector, false completion fields, exact changed paths, and absent-self-test boundary agree |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must first accept fresh intake evidence. Accountable reviewers must then
lawfully preserve and hash an immutable primary or approved authoritative source, select and
independently approve one exact Alon-Tarsi root, and transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, graph/orientation convention, Eulerian-subdigraph and
parity convention, list and coloring representation, boundary case, proof boundary, correction,
and erratum. They must also freeze the relationship among the 1992 theorem, its coefficient and
colorability corollaries, the later generic Nullstellensatz route, and neighboring targets.

A fresh statement worker can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, accepted state, proof credit, or
master acceptance is claimed.
