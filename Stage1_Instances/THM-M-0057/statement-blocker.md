# THM-M-0057 exact-statement gate: blocked

Item: `S56-M-0057-STATEMENT`

Base revision: `48abbb2d2eeb89816c5ffc0ad8faafa4b9d24dd0` (tree
`0f26e2c78fb5fff9277cbbdfef5e145fd4ef06f1`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0057-INTAKE` is only in provisional
worker state `[_]`; `intake-receipt.json` has `accepted: false` and no accepted receipt IDs. More
importantly, the intake deliberately leaves the canonical human statement, Lean module,
declaration, expression fingerprint, and canonical-target environment fingerprint null.

The repository catalog gives only the name Hoffman-Wielandt theorem and the gloss "perturbation
of the eigenvalues of normal matrices." It does not state an inequality or fix the complex matrix
domain, dimension/index type, definition of normality, eigenvalue enumerations with algebraic
multiplicity, matching-permutation direction, Frobenius norm, square-root versus squared form,
ordered binders, or zero-dimensional behavior.

Hoffman and Wielandt's 1953 paper is identified bibliographically, but its theorem text was not
available for inspection in this environment. Xu and Zhang, arXiv `1612.05759v2`, abstract and
introduction pages 1-2, state the familiar square-root Frobenius inequality for two normal complex
matrices. That inspected paper is an uncited secondary source lead. The intake assigns it `H1` and
explicitly requires a lawfully preserved, pinpoint primary or authoritative proposition plus
independent review before statement freeze. It does not authorize choosing the remaining clauses.

A noncredited feasibility probe confirms that one conventional `Fin n` encoding can elaborate:
it uses two complex normal matrices, two functions whose multisets enumerate the respective
characteristic-polynomial roots, and an existential `Equiv.Perm (Fin n)` satisfying the
square-root matching bound. The candidate elaborates with
`Mathlib.Analysis.Matrix.Normed` and
`Mathlib.LinearAlgebra.Matrix.Charpoly.Basic`. This does not make it the received exact target.
Freezing it would still decide `n = 0`, the enumeration equality orientation, the permutation
orientation, the norm instance and difference orientation, and the square-root form without an
accepted source crosswalk.

Rev-5.6 treats unresolved statement identity and a missing expression fingerprint as hard
tree-construction blockers. Therefore there is no truthful canonical expression whose imports can
be certified minimal, serialized, or mutation-tested. The required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary mutations are not meaningful rather than
passed. The root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` was re-elaborated against the existing pinned environment.
It authenticated `IsStarNormal`, Frobenius matrix-norm declarations, matrix spectrum, and the
indexed Hermitian eigenvalue/spectral-theorem interface. Its output SHA-256 is
`39f6cf219e00f6dda383339f1e48a749e9db454ae00f3bac13ad4da397c0b9a6`.
These declarations are adjacent substrate, not a complete eigenvalue enumeration for arbitrary
normal matrices and not a Hoffman-Wielandt proof body.

A bounded repo-local and pinned-mathlib search found no Hoffman-Wielandt declaration. The
noncredited candidate probe ran from `/tmp` only and changed no repository artifact. Its two-import
surface is locally irredundant among the tested pair, but cannot establish minimal imports for an
absent canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and exactly 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0057` | 0 | rank 1524; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all; git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided untracked `Formalizations/Lean/.lake`; base revision and tree appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'; git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0057/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; no canonical target or proof body; output hash recorded above |
| `cd Formalizations/Lean && lake env lean /tmp/HWProbeMinimal.lean` | 0 | noncredited conventional candidate elaborated with two imports; output SHA-256 `db7dc5e55e9aeb6e4a63be88d4b6d57f80f13ca4716d8a60f89140f886255331` |
| bounded `rg` search for Hoffman-Wielandt declarations in repo-local Lean and pinned mathlib | 0 | only the target's intake-probe commentary matched; no formal declaration was found |
| `python3 -B Stage1_Instances/THM-M-0057/check_intake.py` | 1 | historical intake validator is stale: it freezes authoritative intake state `[ ]`/attempt 0 while integration now records provisional `[_]`/attempt 1; it is not statement evidence |
| prohibited-construct scan over target-owned Lean files | 0 | inner `rg` returned the expected no-match result; no `sorry`, `admit`, `sorryAx`, custom `axiom`, `constant`, `opaque`, or `unsafe` declaration was found |
| `python3 -m json.tool Stage1_Instances/THM-M-0057/statement-blocker.json` plus scoped blocker invariants | 0 | blocker identity, null target/imports/fingerprints, unchanged vector, four undefined mutations, false completion flags, and no-self-test boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-0057` plus new-file whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest was emitted because the assigned statement deliverable did not pass |

The inherited intake checker is bound to its intake-time authority state and exact file inventory.
Its fail-closed result is recorded rather than repaired from this statement-only assignment.

## Retry Condition

Accountable reviewers must lawfully preserve and hash a primary or authoritative theorem passage,
incorporated definitions, proof boundary, and errata disposition; independently approve its
mapping to the catalog; and freeze the complex matrix domain, dimension boundary, normality
predicate, complete eigenvalue enumerations with multiplicity, permutation convention, Frobenius
norm and difference orientation, inequality form, ordered binders, and degenerate cases. A later
statement run can then encode only that proposition, minimize its pinned imports, serialize the
elaborated expression and environment, compile every credited transport, and execute all four
mutation classes. Master acceptance of the intake is also required before an accepted statement
transition.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
No statement receipt, root worker self-test packet, worker `[_]`, proof credit, audit completion,
theorem completion, or master acceptance is claimed.
