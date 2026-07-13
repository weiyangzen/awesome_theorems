# Exact-statement gate: blocked

Item: `S56-M-1441-STATEMENT`

Theorem: `THM-M-1441`

Base revision: `1944ddb6f503b699293e82f18d19efe0f32b4380` (tree
`e5004bc50d7e6fae75e8332fb00748a57e3bf622`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1441-INTAKE` is only provisional worker
state `[_]`, not master-accepted `[x]`. Rev-5.6 section 10.2 permits a later-node blocker attempt
while concurrency is enabled, but dependency-ordered master closure still requires acceptance.

Independently, the exact Lean 4 target cannot be truthfully elaborated from the authoritative
repository record. The record supplies only the method label `割线法` (secant method), the
collective attribution "many mathematicians," the twentieth century, and the gloss
`方程求根的超线性方法` ("a superlinear method for finding roots of equations"). It cites no source
and supplies no recurrence, definition, ordered binder, hypothesis, conclusion, proof boundary,
correction, erratum, or formal artifact. The catalog label `已验证` is untrusted metadata under
rev-5.6.

The secant method is a method family, not one proposition. The repository does not select among
recurrence well-definedness, local convergence to a simple root, Q-superlinear convergence, an
exact convergence-order theorem with order equal to the golden ratio, an error bound, or a
finite-precision solver-correctness theorem. It also does not fix:

- the scalar equation or system, domain and codomain, function, root, and root multiplicity;
- the two-point recurrence, indexing, starting pair, and partial-versus-total division policy;
- noncollision and nonzero-denominator invariants for initial and later iterates;
- continuity, differentiability, derivative nondegeneracy, neighborhood, basin, and invariance
  hypotheses;
- the convergence mode, selected definition of superlinearity, exact rate or error conclusion, and
  uniformity of constants; or
- ordered binders and universes, exact versus finite-precision arithmetic, and every degenerate or
  boundary case.

The adjacent targets separately own Newton iteration (`THM-M-1440`), bisection (`THM-M-1442`),
generic fixed-point iteration (`THM-M-1443`), and the Banach fixed-point theorem (`THM-M-1444`).
None can replace the missing secant-method proposition. A recurrence definition is likewise not a
convergence, rate, or solver-correctness theorem.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a missing expression
fingerprint hard blockers. Without a canonical proposition, there is no exact Lean expression for
which imports can be certified minimal, no elaborated expression or environment fingerprint, no
credited alternate transport, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation. Those mutation classes are undefined, not passed.
No surrogate theorem, weakened special case, axiom, placeholder, broadened interface, or proof body
was added.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its two direct
imports expose eight general asymptotic, convergence, division, iteration, and golden-ratio
interfaces. All checks pass. The probe does not define the secant recurrence or state a target
theorem, selects no candidate, supplies no checked source transport, and has no proof body. Its
imports therefore cannot be certified minimal for an absent canonical target and receive no
statement, anchor, or proof credit.

A bounded case-insensitive search found no secant-method declaration in the searched repo-local and
pinned-mathlib Lean roots. This is only scoped discovery evidence, not the downstream immutable
anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The complete probe output has SHA-256
`3277bc3a41b43734b1488b0691c26fcdf838218b00470ef5bdfc7b1e6523ad3c`.

The automation-provided `Formalizations/Lean/.lake` link points to canonical pinned artifacts and
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai), from the repository root
unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1441` | 0 | rank 1120, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; the base revision and tree are recorded above |
| authority, source, intake, and task inspection commands recorded in `statement-blocker.json` | 0 | only a method label and rate gloss are authoritative; intake deliberately freezes a null canonical statement and target at `[H5, M4, R4]` |
| `sha256sum` over authority, source, intake, probe, toolchain, lockfile, and relevant mathlib sources | 0 | current fingerprints agree with `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-1441/check_intake.py` | 1 | historical intake replay stops at stale `Docs/Stage1_Blueprint_rev-5.6.md` input hash; this statement run records rather than rewrites historical intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| pinned mathlib revision, tree, and package-status checks | 0 | revision and tree agree with the fingerprint; the package worktree is clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1441/IntakeProbe.lean` | 0 | eight adjacent interfaces elaborated; no canonical target was stated |
| bounded repo-local and pinned-mathlib Lean search | 1 | expected no-match result; no source-identical target-specific declaration was found in the searched roots |
| prohibited Lean construct scan over the owned path | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and exact scoped invariant command recorded in `statement-blocker.json` | 0 each | identity, open blocked state, null target and imports, unchanged vector, four undefined mutations, false completion flags, exact two-file change scope, and absent self-test agree |
| tracked and added-file whitespace checks recorded in `statement-blocker.json` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

The intake receipt pins an older blueprint and execution-DAG snapshot and declares
`accepted: false`; it is not content-addressed and has no accepted receipt ID. Its validator is
also intake-specific and freezes the original nine-file inventory. This statement run does not
rewrite that historical receipt, validator, instance manifest, target-local DAG, generated
checklist, or authoritative DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers
must preserve and hash an immutable primary or approved authoritative source, select and
independently approve one exact truth-valued secant-method proposition, and map every incorporated
definition, binder, premise, conclusion, proof boundary, correction, and erratum. They must freeze
the recurrence, scalar domain, function and root, two starts, denominator policy, regularity and
localization hypotheses, convergence and rate definition, conclusion, arithmetic model, boundary
cases, and separation from the neighboring targets.

A fresh statement worker may then encode precisely that source-selected claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

The first failed gate is exact source-statement identity. The provisional catalog assessment
remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. This is blocked-attempt evidence, not completion of the statement node or any
downstream node. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json` is emitted and no statement receipt, worker `[_]`, or master
acceptance is claimed.
