# Exact-statement gate: blocked

Item: `S56-M-1453-STATEMENT`

Theorem: `THM-M-1453`

Base revision: `58fbed45d2c785466ee920c7696f0f7b3686d9a5` (tree
`36198f7c90045b3b21d338a3d0ce47aa4ff930f1`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1453-INTAKE` is provisional worker state
`[_]`, backed only by an unaccepted, non-content-addressed intake receipt, rather than
master-accepted `[x]`. Rev-5.6 section 10.2 permits preparation of a later-node blocker while
concurrency is enabled, but master closure remains dependency ordered.

Independently, the exact Lean 4 target cannot be truthfully elaborated from the authoritative
repository record. The record supplies only the title `Arnoldi` iteration, the attribution Walter
Arnoldi, the year 1951, and the gloss `非对称矩阵的特征值` ("eigenvalues of nonsymmetric matrices"). It
cites no source and supplies no formula, definition, ordered binder, hypothesis, conclusion, proof
boundary, correction, erratum, or formal artifact. The catalog label `已验证` is untrusted metadata
under rev-5.6.

The gloss identifies a method family and intended application, not one proposition. It does not
decide:

- real or complex scalars and whether nonsymmetric means non-Hermitian or merely no symmetry
  assumption;
- square matrices versus endomorphisms, finite indices, inner-product convention, and dimension;
- the start vector, normalization, iteration count, Krylov convention, and orthogonalization
  variant;
- recurrence coefficients, conjugation orientation, basis representation, projected matrix, and
  breakdown policy;
- whether the conclusion is an orthonormal Krylov basis, entrywise recurrence, matrix Arnoldi
  relation, projected Hessenberg identity, Ritz residual, exactness at breakdown, convergence,
  restart behavior, or floating-point stability; or
- the Ritz selection and error metric, spectral conditions, arithmetic model, and degenerate cases.

Choosing any conventional variant would add proposition-changing mathematics absent from the
source. Gram-Schmidt span preservation alone, an arbitrary Hessenberg or Schur reduction, Lanczos,
power or QR iteration, GMRES, a premise storing the desired construction, or a numerical example
is not a source-identical replacement.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a missing expression
fingerprint hard blockers. Without a canonical proposition, there is no exact Lean expression for
which imports can be certified minimal, no elaborated expression or environment fingerprint, no
credited alternate transport, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation. Those mutation classes are undefined, not passed.
No surrogate theorem, weakened special case, axiom, placeholder, broadened interface, or proof body
was added.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its two direct
imports expose nine adjacent Gram-Schmidt, span, orthonormality, linear-map power, and matrix
representation interfaces. They state no Krylov-space, Arnoldi recurrence, Hessenberg projection,
Ritz, exactness, convergence, or eigenvalue theorem. The two imports are therefore probe imports,
not minimal imports for the absent canonical target, and receive no statement or proof credit.

A bounded search found no Arnoldi- or Hessenberg-named declaration and no matrix/eigenvalue/Ritz use
of Krylov terminology in the searched repo-local and pinned-mathlib Lean roots. This is scoped
discovery evidence only, not the downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The complete probe output has SHA-256
`ddd27121197695cbd7b60f231dced63bb802e1f38d76bcec0b444dadeb4632f2`; representative imported
theorems report the standard pinned-library axioms `propext`, `Classical.choice`, and `Quot.sound`.

The automation-provided `Formalizations/Lean/.lake` link points to canonical pinned artifacts and
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation evidence

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai), from the repository root
unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1453` | 0 | rank 1130, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; the base revision and tree are recorded above |
| authority, source, intake, and task inspection commands recorded in `statement-blocker.json` | 0 | only a method-family gloss is authoritative; intake deliberately freezes a null canonical statement and target at `[H5, M4, R4]` |
| `sha256sum` over authority, source, intake, probe, toolchain, lockfile, and relevant mathlib sources | 0 | current fingerprints agree with `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-1453/check_intake.py` | 1 | the historical intake checker stops because it freezes intake state `[ ]`, while the current authoritative DAG records provisional worker state `[_]`; this run records rather than rewrites historical intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| pinned mathlib revision, tree, and package-status checks | 0 | revision and tree agree with the fingerprint; the package worktree is clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1453/IntakeProbe.lean` | 0 | nine adjacent interfaces elaborated; no canonical Arnoldi target was stated |
| bounded repo-local and pinned-mathlib Lean search | 1 | expected no-match result; no exact-topic named declaration was found in the searched roots |
| prohibited Lean construct scan over the owned path | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and exact scoped invariant command recorded in `statement-blocker.json` | 0 each | identity, open blocked state, null target and imports, unchanged vector, four undefined mutations, false completion flags, exact two-file change scope, and absent self-test agree |
| tracked and new-file whitespace checks recorded in `statement-blocker.json` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

The intake receipt pins older authority snapshots, declares `accepted: false`, and is not content
addressed. Its checker is intake-specific and freezes the original nine-file inventory and old
authoritative intake state. This statement run does not rewrite that historical receipt, checker,
instance manifest, target-local DAG, generated checklist, or authoritative DAG to manufacture
agreement.

## Retry condition and status boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers
must then preserve and hash an immutable primary or approved authoritative source, select and
independently approve one exact truth-valued Arnoldi proposition, and map every incorporated
definition, binder, premise, conclusion, algorithm step, breakdown branch, proof boundary,
correction, and erratum. They must freeze the field, matrix or operator representation, finite
indices, start vector, iteration count, Krylov and orthogonalization conventions, projected data,
breakdown policy, exact conclusion, arithmetic model, neighboring-target boundary, and every
degenerate case.

A fresh statement worker may then encode precisely that source-selected claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

The first failed statement gate is exact source-statement identity. The provisional catalog
assessment remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no
debt-vector change is proposed. This is blocked-attempt evidence, not completion of the statement
node or any downstream node. Because the assigned phase is not genuinely self-tested to its
completion gate, no `.stage1-worker-selftest.json` is emitted and no statement receipt, worker
`[_]`, or master acceptance is claimed.
