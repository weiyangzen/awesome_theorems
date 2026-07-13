# Exact-statement gate: blocked

Item: `S56-M-1447-STATEMENT`

Theorem: `THM-M-1447`

Base revision: `be1f1d3c684eb883c819bcc968e0631d7f151bb0` (tree
`cff05d9f99014e6c54839589d4470f02df94a986`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1447-INTAKE` is provisional worker state
`[_]`, backed only by an unaccepted, non-content-addressed intake receipt, rather than
master-accepted `[x]`. Rev-5.6 section 10.2 permits this later-node blocker attempt while
concurrency is enabled, but dependency-ordered master closure still requires acceptance.

Independently, the exact Lean 4 target cannot be truthfully elaborated from the authoritative
repository record. The record supplies only the title `Cholesky` decomposition, the attribution
Andre-Louis Cholesky, the year 1910, and the gloss `对称正定矩阵的分解` ("decomposition of a symmetric
positive-definite matrix"). It cites no source and supplies no formula, definition, ordered binder,
hypothesis, conclusion, proof boundary, correction, erratum, or formal artifact. The catalog label
`已验证` is untrusted metadata under rev-5.6.

The gloss identifies a theorem family, not one proposition. It does not decide:

- real symmetric matrices versus complex Hermitian matrices or a more general scalar domain;
- a `Fin n` index versus another finite linearly ordered type, including the empty case;
- lower versus upper triangular factor orientation and the exact triangular predicate;
- transpose versus conjugate transpose and the multiplication order;
- existence alone versus uniqueness, and the positive-diagonal normalization needed for the usual
  uniqueness statement; or
- zero, identity, singular, positive-semidefinite, singleton, and other boundary conventions.

Choosing the familiar real claim `A = L * L.transpose`, a complex claim
`A = L * L.conjTranspose`, an upper-triangular form, or an existence-and-uniqueness theorem would
therefore add proposition-changing mathematics absent from the source. An `LDL^H` decomposition,
positive matrix square root, Gram representation, LU/QR/SVD result, fixed-size calculation, or
factor stored in a premise is not a source-identical replacement.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a missing expression
fingerprint hard blockers. Without a canonical proposition, there is no exact Lean expression for
which imports can be certified minimal, no elaborated expression or environment fingerprint, no
credited alternate transport, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation. Those mutation classes are undefined, not passed.
No surrogate theorem, weakened special case, axiom, placeholder, broadened interface, or proof body
was added.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its two direct
imports expose twelve positive-definite-matrix, Gram-matrix, and LDL interfaces and compile one
adjacent LDL-only wrapper. The wrapper proves only the existence of matrices `L` and diagonal `D`
with `L * D * L.transpose = S` over real `Fin d` matrices. It neither asserts triangularity of `L`
nor absorbs `D` into a positive-diagonal factor, and it is not the missing Cholesky target.

Pinned `Mathlib.Analysis.Matrix.LDL` states `LDL.lower_conj_diag`, but its source also explicitly
leaves triangularity of `LDL.lower` as a TODO. A bounded search found no Cholesky-named or
source-identical normalized `LL^H` factor-existence declaration in the searched repo-local and
pinned-mathlib Lean roots. This is scoped discovery evidence only, not the downstream immutable
anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The complete probe output has SHA-256
`a4d31abc707294d88f3595526d08177d0140011d7e5454df2ac5ceeae6919dc7`; the adjacent wrapper reports
the standard pinned-library axioms `propext`, `Classical.choice`, and `Quot.sound`.

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
| `python3 scripts/stage1_target.py show THM-M-1447` | 0 | rank 1124, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; the base revision and tree are recorded above |
| authority, source, intake, and task inspection commands recorded in `statement-blocker.json` | 0 | only a theorem-family gloss is authoritative; intake deliberately freezes a null canonical statement and target at `[H1, M4, R4]` |
| `sha256sum` over authority, source, intake, probe, toolchain, lockfile, and relevant mathlib sources | 0 | current fingerprints agree with `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-1447/check_intake.py` | 1 | the historical intake checker stops because it freezes intake authority state `[ ]`, while the current DAG has provisional worker state `[_]`; this statement run records rather than rewrites historical intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| pinned mathlib revision, tree, and package-status checks | 0 | revision and tree agree with the fingerprint; the package worktree is clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1447/IntakeProbe.lean` | 0 | twelve adjacent interfaces and the LDL-only wrapper elaborated; no canonical Cholesky target was stated |
| bounded repo-local and pinned-mathlib Lean search | 0 | only the adjacent LDL declaration and its triangularity TODO matched; no source-identical normalized Cholesky declaration was found in the searched roots |
| prohibited Lean construct scan over the owned path | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and exact scoped invariant command recorded in `statement-blocker.json` | 0 each | identity, open blocked state, null target and imports, unchanged vector, four undefined mutations, false completion flags, exact two-file change scope, and absent self-test agree |
| tracked and added-file whitespace checks recorded in `statement-blocker.json` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

The intake receipt pins older blueprint and execution-DAG snapshots, declares `accepted: false`, and
is not content-addressed. Its checker is intake-specific and freezes the original nine-file
inventory and old authoritative intake state. This statement run does not rewrite that historical
receipt, checker, instance manifest, target-local DAG, generated checklist, or authoritative DAG to
manufacture agreement.

## Retry condition and status boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers
must then preserve and hash an immutable primary or approved authoritative source, select and
independently approve one exact truth-valued Cholesky proposition, and map every incorporated
definition, binder, premise, conclusion, proof boundary, correction, and erratum. They must freeze
the scalar domain, finite index order, symmetry or Hermitian predicate, positive-definiteness
predicate, factor orientation, triangular predicate, transpose convention, diagonal normalization,
uniqueness clause, and every boundary case.

A fresh statement worker may then encode precisely that source-selected claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

The first failed statement gate is exact source-statement identity. The provisional catalog
assessment remains `[H1, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no
debt-vector change is proposed. This is blocked-attempt evidence, not completion of the statement
node or any downstream node. Because the assigned phase is not genuinely self-tested to its
completion gate, no `.stage1-worker-selftest.json` is emitted and no statement receipt, worker
`[_]`, or master acceptance is claimed.
