# Exact-statement gate: blocked

Item: `S56-M-0854-STATEMENT`

Theorem: `THM-M-0854`

Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e` (tree
`6434a20532ae7c523ad293e67a6228ab384bfb8a`).

## Decision

The exact Lean 4 target cannot be truthfully selected from the authoritative repository record.
That record gives only `Ore定理`, Oystein Ore, 1960, and the gloss `Hamilton圈存在的度和条件` (a
degree-sum condition for the existence of a Hamiltonian cycle). It supplies no formula, graph
model, order boundary, pair convention, ordered binders, proof boundary, correction, or erratum;
its `已验证` label is untrusted under rev-5.6. Stage0 explicitly leaves exact definitions and
premises open.

The intake identifies the likely primary source as Oystein Ore, *Note on Hamilton Circuits*, *The
American Mathematical Monthly* 67(1), page 55 (1960), DOI `10.2307/2308928`. Only bibliographic
metadata was admitted. The article passage, incorporated definitions, corrections, and an
independent source review were not. A versioned secondary paper corroborates the familiar theorem,
but secondary corroboration does not override the intake's deliberately null canonical target.

Consequently, the received record does not decide:

- the finite simple undirected graph carrier, universes, and decidability presentation;
- whether the graph order is a separate binder or exactly `Fintype.card V`;
- whether the lower boundary is exactly three vertices and how smaller orders are excluded;
- whether nonadjacent pairs are ordered or unordered and whether distinctness is explicit;
- the exact degree-sum binder order and natural-number inequality; or
- whether the source's Hamilton circuit maps directly to `SimpleGraph.IsHamiltonian` or requires
  a checked transport to an explicit cycle witness.

These decisions change proposition identity. Distinctness is particularly material: simple graphs
are loopless, so quantifying only `not G.Adj u v` includes `u = v` and adds diagonal degree
conditions. The source-visible `SimpleGraph.ore_theorem` on the divergent old mathlib branch has
exactly this stronger premise, targets Lean 4.12.0-rc1, is outside the pinned closure, and has no
reproduced kernel receipt. It cannot select or close this root.

Sections 5 and 5.1 of the rev-5.6 blueprint make ambiguity and a missing expression fingerprint
hard blockers. The intake therefore correctly leaves the canonical statement, Lean module and
expression, minimal imports, and expression/environment fingerprints null. Without a canonical
target, alternate transports and the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined, not passed. No `Statement.lean`,
axiom, placeholder, substituted theorem, weakened special case, or broadened target was retained.

The prerequisite `S56-M-0854-INTAKE` has provisional `[_]` state. Rev-5.6 section 10.2 permits
provisional later-node preparation in topological order, so that state did not prevent this
inspection. Its receipt is still mutable, non-content-addressed, and explicitly unaccepted;
recording this blocker does not constitute intake or statement master acceptance.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned environment with the single direct
import `Mathlib.Combinatorics.SimpleGraph.Hamiltonian`. It checks ten graph, degree, Hamiltonicity,
and small-order interfaces. The probe declares no Ore target, source transport, or proof body. Its
import is a substrate feasibility import, not a minimal-import certificate for an absent target,
and receives no statement or proof credit.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, dependency
checkout, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository root unless
another directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0854` | 0 | rank 1408, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `python3 -B Stage1_Instances/THM-M-0854/check_intake.py` | 1 | expected historical-snapshot failure: the integrated authoritative intake state is now `[_]`, while the intake checker is frozen to original `[ ]`; it was preserved rather than rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree agree and the dependency worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0854/IntakeProbe.lean` | 0 | ten adjacent interfaces elaborated; output SHA-256 `20de440dc41f5b86d6b82713d3174a775c49089e230af80187d228266de1fbce`; no target or proof declared |
| prohibited declaration scan over `IntakeProbe.lean` | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0854/statement-blocker.json` | 0 | valid structured blocker |
| scoped blocker-invariant and whitespace checks | 0 | identity, null target, unchanged `[H1,M4,R4]`, false completion flags, two-file change scope, byte hygiene, and absent worker packet agree |
| `test ! -e .stage1-worker-selftest.json` | 0 | no packet because the assigned statement deliverable did not pass |

## Retry Condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must then
lawfully preserve and hash an immutable primary or accepted authoritative source, pinpoint and
independently approve its theorem passage and incorporated definitions, and crosswalk every graph
convention, ordered binder, hypothesis, conclusion, proof boundary, correction, erratum, and
boundary case. They must freeze the order bound, pair distinctness/order, degree-sum scope, and
Hamiltonicity convention.

A fresh statement worker can then encode exactly that source-selected claim, minimize pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is blocker evidence, not completion of the statement node or any downstream node. The root
remains `[H1, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt change
is proposed. Because the assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
