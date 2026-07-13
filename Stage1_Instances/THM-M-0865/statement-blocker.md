# THM-M-0865 exact-statement gate: blocked

- Item: `S56-M-0865-STATEMENT`
- Base revision: `1168265f6eea33d947ff470fad2ca6fff9e1130b`
- Base tree: `0d35608cbc6e281a3d9935d452cf33c88c32aa7e`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully frozen from the received evidence. The prerequisite
`S56-M-0865-INTAKE` is provisional worker state `[_]`, not master-accepted `[x]`, and its
receipt is unaccepted and non-content-addressed. Rev-5.6 permits preparing this dependency-ordered
blocker, but accepted closure remains dependency ordered.

Independently, the catalog says only `平面图的禁用子图刻画` ("characterization of planar graphs by
forbidden subgraphs"). It does not distinguish literal subgraphs, subdivisions, topological minors,
or ordinary minors. It also does not fix finite versus infinite and simple versus multigraph scope,
planarity or embedding semantics, obstruction encodings, ordered binders, foundations, or boundary
cases.

The intake identifies the conventional Kuratowski family and a strong modern source lead. Diestel's
*Graph Theory*, 6th edition, Theorem 4.4.6 states that, for graphs `G`, planarity, absence of
`K5` and `K3,3` ordinary minors, and absence of those topological minors are equivalent. Its
notes say that Kuratowski's original theorem used only topological minors and that Wagner added the
ordinary-minor version in 1937. Because neighboring `THM-M-0866` separately owns Wagner's theorem,
silently selecting the convenient three-way equivalence or ordinary-minor clause would transfer
scope. Selecting only the finite-simple topological-minor clause would still require unaccepted
source-to-modern transport and representation decisions.

Those choices produce materially different propositions. Defining `Planar`,
`IsTopologicalMinor`, or subdivision witnesses during this phase would invent the semantic
substrate rather than elaborate an exact received target. A desired equivalence packaged as a
predicate, structure field, or premise would be circular. Therefore no `Statement.lean`,
canonical expression, minimal-import claim, expression fingerprint, alternate transport, or
mutation fixture was created. The four required mutations are undefined, not passed. The
provisional root remains `[H1, M4, R3]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with the single direct import
`Mathlib.Combinatorics.SimpleGraph.Bipartite`. It checks `SimpleGraph`, graph isomorphisms,
ordinary subgraph-copy containment, `completeGraph`, `completeBipartiteGraph`, one containment
lemma, and a predicate-parameterized theorem-family shape. All checks pass.

This authenticates only adjacent vocabulary. The `Planar` and `IsTopologicalMinor` parameters
have no semantics and provide no canonical-statement or proof credit. A bounded deterministic
search over pinned mathlib's `Combinatorics/SimpleGraph` and `Combinatorics/Graph` trees plus
repository-local Lean found only a planar-graphs documentation bullet in `Coloring.lean`. It
located no graph-planarity, subdivision, topological-minor, graph-minor, or Kuratowski declaration.
This is narrow statement-feasibility evidence, not the downstream anchor audit or a global absence
claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone or
fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0865` | 0 | rank 1419; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped inspection and exact JSON projections of the DAG and intake | 0 | dependency `[_]`, open statement node, null formal target fields, empty binders and alternates, H1/M4/R3, and no accepted receipts confirmed |
| `python3 -B Stage1_Instances/THM-M-0865/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]`, while integration records `[_]`; historical evidence was preserved |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0865/IntakeProbe.lean` | 0 | adjacent APIs and shape elaborated; stdout SHA-256 `a2aa28f936a224e63c48b05efc5de0eef1b59aa0c8c081173689f2c3fc144e23`; no target or proof |
| deterministic bounded `rg` recorded in the JSON | 0 aggregate | sole match was the planar-graphs documentation bullet; stdout SHA-256 `ca8e361a53fdcc39e822c28c684384afbe0772c7daf10300faf025036004789e` |
| prohibited-construct scan over owned Lean | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and scoped blocker invariant assertions | 0 each | identity, base, null target, unchanged vector, undefined mutations, false completion flags, exact paths, and absent self-test agree |
| scoped `git diff --check`, per-new-file no-index checks, and direct byte checks | 0 aggregate | no whitespace, final-newline, carriage-return, or NUL diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

The integration lane must first revalidate and master-accept the intake. Accountable independent
reviewers must then preserve and hash an immutable primary or approved authoritative source,
pinpoint and approve the exact proposition and definition chain, audit its proof and correction
boundaries, and approve the historical-to-modern graph transport and Kuratowski/Wagner ownership
split. They must freeze graph scope, planarity, subdivision or topological-minor semantics,
obstruction encodings, ordered binders, hypotheses, conclusion, logical profiles, and every
boundary case.

A fresh statement run can then encode only that approved claim, minimize pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and run all
four mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`,
proof, release, or master acceptance is claimed.
