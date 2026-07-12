# Exact-statement gate: blocked

Item: `S56-M-1348-STATEMENT`

Theorem: `THM-M-1348`

Base revision: `531673f2e97293dd22e5727b12fc7e13eca7d6e5` (tree
`4acbd91f6e676b2b89949bb52992c0be522de40f`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1348-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. Rev-5.6 section
10.2 permits this dependency-ordered attempt from a provisional predecessor, so pending master
acceptance did not prevent the work. The intake receipt is non-content-addressed, declares
`accepted: false`, has no accepted receipt ID, and intentionally leaves the canonical mathematical
statement and Lean target null. Master acceptance remains required before any eventual accepted
statement transition.

Independently, the exact-statement gate cannot be passed from the authoritative repository record.
It supplies only the title Poincare-Bendixson theorem, the attribution Henri Poincare/Ivar
Bendixson, the year 1901, and the gloss `二维系统的极限集` ("limit sets of two-dimensional
systems"). It contains no citation, formula, definition, ordered binder, hypothesis, conclusion,
boundary case, proof boundary, or correction history. The catalog's `已验证` label is explicitly
untrusted under rev-5.6.

The inspected authoritative source lead confirms rather than removes the ambiguity. Gerald
Teschl's *Ordinary Differential Equations and Dynamical Systems*, Section 7.3, has at least two
materially different roots:

- Lemma 7.13 says that a nonempty compact forward or backward omega-limit set containing no fixed
  points is a regular periodic orbit.
- Theorem 7.16 gives a generalized classification when the omega-limit set contains finitely many
  fixed points: a fixed orbit, a regular periodic orbit, or fixed points together with nonclosed
  connecting orbits.

The official page-222 erratum is mathematically substantive. It says the printed proof of Lemma
7.13 proves only containment of a regular periodic orbit; equality additionally uses Lemma 7.14
after connectedness is derived from compactness as in Lemma 6.6. It also says the connectedness
hypothesis printed in Theorem 7.16 is superfluous. The catalog does not cite Teschl, select either
result, or bind this erratum.

The encoding model is also unresolved. Teschl works with a `C1` vector field on an open subset of
the plane and a source-defined maximal local flow on point-dependent maximal time intervals.
Mathlib's `Flow` is global on its carrier. Replacing the source model with a global flow on all of
`R x R` or on an open-domain subtype would strengthen or specialize the source assumptions, not
merely change notation. The statement must also choose forward or backward time, completeness,
the omega-limit convention, which compactness properties are assumed or derived, the fixed-point
predicate, positive/minimal period and orbit-range equality, and every stationary, empty,
noncompact, boundary-escape, and zero-period case.

There is a further identity blocker. `THM-M-1400` has a translated Poincare-Bendixson title and the
same attribution, year, gloss, importance, and untrusted status. No accepted alias, deduplication,
correction, or canonical-root ownership decision exists. Its legacy file
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_297.lean` explicitly presents a loose statement
boundary and denies terminal theorem completion. Reusing it would substitute another target's
unaccepted scope.

These choices yield inequivalent propositions. Selecting the familiar no-fixed-point form, the
generalized form, a convenient global-flow specialization, or the duplicate's packaged structure
would invent, broaden, strengthen, or substitute mathematics rather than elaborate the exact
received target. Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing
expression fingerprint hard blockers. There is consequently no honest canonical expression for
which minimal imports, checked transports, or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can be certified. Those mutations are undefined,
not passed. The vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates in the pinned environment. Its direct imports expose
generic integral-curve, global-flow, orbit, omega-limit, closedness, invariance, and discrete
fixed/periodic-point interfaces. All eleven checks pass. This is real substrate validation, but the
probe defines no planar maximal local flow, source-mapped fixed or regular orbit, canonical
classification proposition, checked source transport, or proof body. Its imports therefore cannot
be certified minimal for an absent target.

A bounded exact-topic search of pinned mathlib found only unrelated Cantor-Bendixson material. The
only repo-local exact-topic file is the nonterminal `THM-M-1400` legacy boundary described above.
These are discovery observations, not the downstream immutable anchor audit or a claim of global
absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1348` | 0 | rank 959; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository, Teschl Sections 6.2/6.3/7.3, and official errata inspection | 0 | confirmed the sparse catalog record, maximal-local-flow source model, distinct Lemma 7.13 and Theorem 7.16 roots, material page-222 erratum, and unresolved duplicate |
| `sha256sum` over authority, intake, source, probe, toolchain, and pinned mathlib inputs | 0 | exact hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1348/IntakeProbe.lean` | 0 | eleven adjacent pinned APIs elaborated; no canonical target or proof body was declared |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 0 | only unrelated Cantor-Bendixson material and the nonterminal `THM-M-1400` legacy file appeared; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-1348/check_intake.py` | 1 | historical intake replay stops at line 156 because it freezes intake state `[ ]` while current authority records `[_]`; its original nine-file inventory is also intentionally historical after this phase |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1348/statement-blocker.json` plus scoped blocker invariants | 0 | identity, dependency state, null target/imports, unchanged vector, four undefined mutations, false completion flags, and no-self-test boundary agree |
| scoped whitespace checks for both new files and `git diff --check -- Stage1_Instances/THM-M-1348` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is frozen to its original authority bytes and nine-file intake
inventory. The integration lane subsequently changed the generated intake state to `[_]`, so replay
already fails before its inventory assertion. Adding these two statement artifacts also makes that
intake-only inventory historical. This statement run records the limitation instead of rewriting
the intake checker, intake receipt, instance, task DAG, generated blueprint, or authoritative
execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash a lawful immutable primary or authoritative source and
official errata, select and independently approve one exact proposition, transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction, and
boundary case, and issue an accountable `THM-M-1400` identity and canonical-root ownership
decision. The integration lane must also master-accept the intake dependency before it can accept a
future statement transition.

A fresh statement worker can then encode precisely that source model, including maximal-local-flow
semantics if the selected source requires it, minimize pinned imports, serialize and hash the
elaborated expression and environment, compile every credited transport, and execute all four
required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
