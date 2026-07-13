# THM-M-0050 exact-statement gate: blocked

Item: `S56-M-0050-STATEMENT`

Base revision: `7d0965498598e684e3e3d0a01836c2bf36a02959` (tree
`753e16a89fce09f051af066f8b58d3e6b2722ade`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0050-INTAKE` is only in provisional
worker state `[_]`; `intake-receipt.json` has `accepted: false` and no accepted receipt IDs. The
intake also deliberately leaves the canonical human statement, Lean module, declaration,
expression fingerprint, and canonical-target environment fingerprint null.

The catalog says only that the positive and negative inertia indices of a real symmetric matrix
are invariant under congruence. It does not fix the finite index type, dimension binders,
congruence witness or equation orientation, or whether inertia means eigenvalue multiplicity,
signs in a diagonal form, or maximal definite-subspace dimensions. It also does not decide whether
the zero index is explicit or derived, or how zero-dimensional, singular, and repeated-zero cases
are represented.

Treil, *Linear Algebra Done Wrong* (2017), Chapter 7 Section 3, printed pages 206-208, is a complete
modern proof lead for a Hermitian diagonalization formulation. The inspected PDF has SHA-256
`d4659dd7b1c1f9d6a8f78cda7a636354d191eb8a8cbd40f12042d59e83c4074f`. The catalog does not cite
it, however, and no accepted independent review covers its real specialization, arbitrary
congruence transport, correction status, or identity with the catalog claim. The historical 1852
paper is only a bibliographic lead because its text was not inspected.

Selecting a convenient `Fin n` statement using `B = P.transpose * A * P` and `sigPos`/`sigNeg`
would therefore make proposition-changing decisions that the
received source and intake do not authorize. Selecting the abstract quadratic-form equivalence
theorem instead would substitute a different surface before a checked matrix transport exists.
Rev-5.6 treats this missing exact source identity and scope freeze as a hard stop. There is no
truthful canonical expression whose imports can be minimized or fingerprinted, and the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations are not meaningful
rather than passed. The root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` was re-elaborated against the existing pinned environment. It
authenticated eleven adjacent APIs: matrix symmetry and quadratic-map conversion, the matrix shape
of composition, abstract quadratic-map equivalence, `sigPos` and `sigNeg`, equivalence invariance,
weighted-sum uniqueness, and real `-1/0/1` diagonalization. These are useful substrate, not an exact
matrix target or checked matrix-to-equivalence transport.

A bounded repo-local and pinned-mathlib search found the real quadratic-form classification wrapper
in `S1_M_067.lean`, the signature-pair wrapper in `S1_M_252.lean`, and the relevant mathlib
signature declarations. None is an exact, source-ratified theorem for arbitrary congruent real
symmetric matrices. Consequently the probe's three imports cannot establish minimal imports for a
nonexistent canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0050` | 0 | rank 1089; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all; git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided untracked `Formalizations/Lean/.lake`; base revision and tree appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'; git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0050/IntakeProbe.lean` | 0 | eleven adjacent APIs elaborated; stdout SHA-256 `5ca2a7332ba033e2df9c61c5e3f834f2c6194dc0488d0f73673a5c1339e77a74`; no target declaration |
| bounded `rg` search for Sylvester/inertia/signature declarations in repo-local Lean and pinned mathlib | 0 | located abstract classification, signature, and uniqueness surfaces; no exact source-ratified real symmetric matrix congruence target was found |
| `python3 -B Stage1_Instances/THM-M-0050/check_intake.py` | 1 | historical intake validator is stale: it freezes authoritative intake state `[ ]`, while integration now records provisional `[_]`; it is not statement evidence |
| prohibited-construct scan over target-owned Lean files | 0 | inner `rg` returned the expected no-match result; no `sorry`, `admit`, `sorryAx`, custom `axiom`, `constant`, `opaque`, or `unsafe` declaration was found |
| `python3 -m json.tool Stage1_Instances/THM-M-0050/statement-blocker.json` plus scoped blocker invariant checks | 0 | blocker identity, null target/imports/fingerprints, unchanged vector, four undefined mutations, false completion flags, and no-self-test boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-0050` plus new-file whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest was emitted because the assigned statement deliverable did not pass |

The inherited intake checker is bound to its intake-time authority state, base, and exact file
inventory. Its fail-closed result is recorded rather than repaired from this statement-only
assignment.

## Retry Condition

Accountable reviewers must lawfully preserve and hash an authoritative source, independently
approve one exact real symmetric-matrix proposition, and freeze its index domain, symmetry
hypotheses, invertible congruence representation and orientation, inertia definitions, zero-index
policy, ordered binders, and every degenerate case. A later statement run can then encode only that
proposition, minimize its pinned imports, serialize the elaborated expression and environment,
compile the matrix/quadratic-form transport and every credited alternate, and run all four mutation
classes. Master acceptance of the intake is also required before an accepted statement transition.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
No statement receipt, root worker self-test packet, worker `[_]`, proof credit, audit completion,
theorem completion, or master acceptance is claimed.
