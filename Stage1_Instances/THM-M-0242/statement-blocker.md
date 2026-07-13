# Exact-statement gate: blocked

Item: `S56-M-0242-STATEMENT`

Theorem: `THM-M-0242`

Base revision: `db6914155f1f63e835364b89ba0a3b25f1d7f936` (tree
`a5488edccb2687c4ff0bbdccf4650e06b2e45337`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0242-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`: its receipt has `accepted: false`, is not
content-addressed, and names no accepted receipt. More fundamentally, no exact Lean 4 target can be
truthfully elaborated from the repository record. That record supplies only the title
`希尔伯特第21问题` (Hilbert's twenty-first problem), David Hilbert, the year 1900, and the gloss
`Fuchs方程的单值群` ("monodromy group of Fuchsian equations"). It gives no formula, bibliography,
incorporated definitions, ordered binders, assumptions, conclusion, correction history, or formal
artifact. The catalog status `已验证` is explicitly untrusted under rev-5.6.

The intake's discovery copy of Hilbert's Problem 21 asks for a linear differential equation of the
Fuchsian class with given singular points and prescribed monodromic group. That identifies the
historical problem family but does not select one later corrected true theorem. The following
proposition-changing choices remain unresolved:

- scalar equation, first-order matrix system, or regular-singular connection;
- a connection on an arbitrary holomorphic vector bundle or a system on the trivial bundle;
- the curve, singular set, treatment of infinity, basepoint, coefficient field, and rank;
- representation, generators, local conjugacy classes, or data modulo simultaneous conjugacy;
- fixed singularities or permission to add apparent singularities;
- arbitrary, irreducible, or otherwise restricted monodromy data;
- regular-singular and Fuchsian conventions, including pole, resonance, and determinant conditions;
- equivalence up to basis conjugacy, gauge transformation, or bundle isomorphism; and
- unrestricted positive existence, restricted existence, classification, obstruction, or a
  counterexample to unrestricted existence.

These choices change binders, hypotheses, conclusions, boundary behavior, and sometimes the truth
value. Selecting one from mathematical memory would invent missing scope or substitute a different
theorem. `THM-M-0241` separately owns the broader Riemann-Hilbert inverse-monodromy record, and
`THM-M-1559` separately owns an integrable-systems contour-jump record; neither may supply this
target's statement or proof credit.

Sections 5 and 5.1 of the rev-5.6 blueprint make ambiguity and a missing elaborated-expression
fingerprint hard blockers. There is consequently no canonical expression for which minimal imports,
checked alternate transports, or removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations can be certified. Those mutation tests are undefined, not passed. The
first failed gate is exact source-statement identity and its definition chain. The root remains
`[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated in the pinned environment. Its three direct
imports expose `OnePoint ℂ`, fundamental groups, and matrix general linear groups; the file checks a
type for finite-dimensional complex monodromy representations. It deliberately defines no
Fuchsian differential equation or system, bundle or connection, regular-singularity predicate,
monodromy construction for such an object, realization relation, or target theorem. Its imports are
therefore discovery-only and cannot be certified minimal for a canonical target that has not been
selected.

A bounded pinned-mathlib source search found only abstract path-lifting and covering-space monodromy
declarations for the queried Riemann-Hilbert, Fuchsian, regular-singular, and monodromy terms. It
found no prescribed-monodromy realization statement or corresponding differential-equation
interface. This is narrow feasibility evidence, not the downstream anchor audit and not proof of
global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `Formalizations/Lean/.lake`
symlink was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other
`.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`). Exact argv, exit codes, input
hashes, and results are serialized in `statement-blocker.json`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0242` | 0 | rank 1252; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base identifiers appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib revision, tree, and package status checks | 0 | pinned revision and tree recorded above; package worktree clean |
| `python3 -B Stage1_Instances/THM-M-0242/check_intake.py` before blocker files | 0 | planned intake invariants passed with `H5/M4/R4` and six open tasks |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0242/IntakeProbe.lean` | 0 | five adjacent substrate checks elaborated; no target theorem or proof body |
| bounded pinned-mathlib exact-topic search | 0 | only abstract path-lifting and covering-space monodromy hits; discovery evidence only |
| `python3 -B Stage1_Instances/THM-M-0242/check_intake.py` after blocker files | 1 (expected limitation) | historical intake-only checker rejected the two statement artifacts because it freezes the original nine-file inventory |
| prohibited-construct `rg` scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| blocker JSON parse and scoped invariant checks | 0 | identity, null target/imports, undefined mutations, unchanged debt, false completion flags, and no-self-test gate agree |
| scoped tracked and new-file whitespace checks | 0 / 1 expected | no whitespace diagnostics; no-index exit 1 only reports that each new file differs from `/dev/null` |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The structured blocker was also parsed and checked for target identity, null canonical target and
minimal imports, four undefined mutation classes, unchanged debt, false completion flags, and the
no-self-test gate. A prohibited Lean construct scan found no `sorry`, `admit`, `sorryAx`, `axiom`,
`constant`, `opaque`, or `unsafe` declaration. Scoped whitespace checks passed. The original
`check_intake.py` intentionally freezes the nine-file intake inventory and therefore fails after
these statement artifacts are added; this statement run records that historical-checker boundary
rather than rewriting intake evidence.

## Retry Condition And Status Boundary

The integration lane must first master-accept the intake dependency. Accountable reviewers must
then preserve and hash an immutable primary or authoritative source, select one exact corrected true
positive, restricted, obstruction, classification, or counterexample proposition, transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, exceptional case, proof boundary,
correction, and erratum, reconcile the duplicate-target boundary, and independently approve the
source-to-target mapping.

A later statement worker can then encode that same claim with concrete Lean definitions, minimize
its pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
