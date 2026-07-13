# Exact-statement gate: blocked

Item: `S56-M-0826-STATEMENT`

Theorem: `THM-M-0826`

Base revision: `1c0c5fc6f43e6ae5ecc3b50589b45c3628e0ead4` (tree
`61214aa2a03c032134ddc4958b1df63df3430a85`).

## Decision

The statement item remains `[ ]`. The repository's complete mathematical wording is
`带负权边的最短路径算法`, an algorithm-purpose gloss meaning "a shortest-path algorithm with
negative-weight edges." Together with the title, attribution, year, importance, and untrusted
`已验证` label, it identifies the Bellman-Ford family but contains no connective or conclusion
whose truth Lean can check. Stage0 repeats the gloss while leaving definitions, premises, proof,
dependencies, foundation, axioms, machine status, and artifacts open.

This is not a notational omission. At least the following non-equivalent proposition families fit
the catalog record:

- equality of final single-source distance estimates with shortest-path weights;
- correctness of predecessor/path reconstruction;
- soundness and completeness of reachable or global negative-cycle detection;
- termination or an exact pass bound for a specified relaxation schedule;
- an `O(|V||E|)` bound under a specified representation and cost model; and
- refinement of one executable implementation to a mathematical recurrence.

Even distance correctness requires proposition-changing choices that the catalog does not make:
the graph and edge model, signed weight domain, source and reachability contract, infinity or
unbounded-below semantics, initialization, in-place versus snapshot relaxation, edge order,
number of passes, early stopping, output, tie behavior, and whether negative cycles are forbidden
globally, from the source, or only on source-to-query routes. Empty graphs, self-loops, parallel
edges, unreachable vertices, zero-weight cycles, reachable and unreachable negative cycles, and
equal shortest paths likewise have no approved boundary policy.

The intake found useful source leads but admitted none as the canonical root. Bellman's 1958
*On a routing problem* is identified by DOI `10.1090/qam/102435`, but only mutable bibliographic
metadata was available; its abstract describes a minimum-time route between two cities and does
not supply the catalog's modern negative-edge correctness theorem. The publisher text was not
available to the intake worker. MIT 6.006 Fall 2011 Lecture 17 gives a concrete algorithm and the
theorem that, when `G` contains no negative-weight cycles, Bellman-Ford finishes with
`d[v] = delta(s,v)` for all vertices, plus a reachable-negative-cycle corollary. The catalog cites
neither that handout nor any other source, and the handout does not decide whether its distance
theorem, detector corollary, path output, or complexity boundary is this repository target.
Lester Ford's 1956 work remains an uninspected historical lead, while the secondary inventory's
date `1958-56` leaves the Bellman/Ford chronology unresolved.

Selecting the familiar MIT theorem or another textbook formulation would therefore invent or
substitute mathematics. The rev-5.6 source and statement rules require a lawful immutable edition,
pinpoint result and incorporated-definition map, correction/errata audit, and independent source
review before freezing one canonical claim. The current intake deliberately records
`canonical_statement: null`, null ordered binders and hypotheses, and null Lean module,
declaration/expression, expression hash, and canonical-target environment fingerprint. There is
accordingly no honest target whose imports can be certified minimal, no credited alternate
encoding, and no meaningful removed-hypothesis, changed-domain, changed-binder-scope, or boundary
mutation suite.

The prerequisite `S56-M-0826-INTAKE` has authoritative worker state `[_]`, not master-accepted
state `[x]`. Its provisional receipt declares `accepted: false` and `content_addressed: false`.
It also cannot be replayed at this revision: the historical checker expects intake state `[ ]`
while the current authoritative DAG records `[_]`, and its recorded blueprint and execution-DAG
hashes are stale. Dependency-ordered blocker inspection is still possible, but no statement
transition could be accepted before the integration lane refreshes and accepts that prerequisite.

The first substantive failure is exact source-statement identity, independently of the stale
dependency evidence. Lifecycle remains `planned`; the root vector remains `[H5, M4, R4]`; no
statement declaration, statement receipt, proof body, axiom, placeholder, accepted receipt, audit
completion, or theorem completion is introduced or claimed.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates in the pinned environment with the
two direct imports
`Mathlib.Combinatorics.Digraph.Basic` and
`Mathlib.Combinatorics.Quiver.Path.Weight`. It checks `Digraph`, dependent quiver paths, path
length, additive path weights, and their nil, cons, and composition behavior. The representative
path-weight lemmas report only `[propext, Quot.sound]` through `#print axioms`.

Those interfaces do not define Bellman-Ford, relaxation, a distance table, a shortest-distance
minimum, negative-cycle handling, algorithm execution, or any correctness or complexity result.
A bounded case-insensitive search of repo-local Lean and pinned mathlib found no Bellman-Ford or
negative-weight shortest-path occurrence under the recorded query. This is adjacent-API and
feasibility evidence only, not an exact target, minimal-import result, anchor audit, or proof
credit.

The checked environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other dependency mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0826` | 0 | rank 1384; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided untracked `.lake` symlink existed; base revision and tree are recorded above |
| source, blueprint, skill, guidelines, and intake-dossier inspection | 0 | confirmed the non-propositional gloss, null canonical target, unaccepted source leads, and unresolved proposition families |
| `python3 -B Stage1_Instances/THM-M-0826/check_intake.py` | 1 | historical intake replay stops at its assertion that authoritative intake state is `[ ]`; the current DAG records provisional `[_]` and its stored authority hashes are also stale |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0826/IntakeProbe.lean` | 0 | ten adjacent directed-graph/path-weight APIs elaborated; output SHA-256 `1b63986ff72da4809fb8d328b95298d4f268b874a7e2c695a6eedd065b384be5` |
| bounded exact-topic `rg` search in repo-local Lean and pinned mathlib | 1 | expected no-match exit; no Bellman-Ford or negative-weight shortest-path occurrence under the recorded query |
| finalized JSON parse and scoped blocker assertions | 0 | item identity, base, provisional dependency, source and pin hashes, null target/imports, unchanged vector, undefined mutations, false completion flags, and owned two-file scope agree |
| prohibited-construct scan over owned Lean files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped tracked and per-added-file whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

First, the integration lane must refresh and master-accept the intake dependency. Accountable
reviewers must then lawfully preserve one immutable primary or approved authoritative source,
resolve Bellman/Ford chronology, identify the exact theorem and proof boundary, map every imported
definition, premise, conclusion, correction, and erratum, and independently approve the choice.
That review must fix the graph, weight, path, reachability, infinity, negative-cycle, algorithm,
output, complexity, arithmetic, binder, and degenerate-case decisions above.

A fresh statement worker can then encode exactly that approved claim, minimize its pinned imports,
serialize and hash its elaborated expression and environment, compile each credited transport, and
run all four required semantic mutation classes.

This blocker is the truthful result of the assigned phase, not completion of the statement node or
any downstream node. `audit_complete: false` and `theorem_complete: false`; no debt-vector change
is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, worker `[_]`, or master acceptance is claimed.
