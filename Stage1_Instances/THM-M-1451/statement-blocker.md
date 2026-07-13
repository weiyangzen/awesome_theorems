# Exact-statement gate: blocked

Item: `S56-M-1451-STATEMENT`

Theorem: `THM-M-1451`

Base revision: `22a0a0cce5163426b024f44f1a7ac09fa81c64a6` (tree
`08e2b7d76500c77153cb79a6c9de86989d879cc8`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1451-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, is not
content addressed, has no accepted receipt ID, and leaves the canonical mathematical claim and
Lean target unresolved. Rev-5.6 section 10.2 permits preparation of this blocker while concurrency
is enabled, but master closure remains dependency ordered.

Independently, the exact Lean 4 target cannot be truthfully elaborated from the repository record.
That record supplies only the title `QR算法`, the attribution John Francis/Vera Kublanovskaya, the
year 1961, and the gloss `特征值的QR迭代` ("QR iteration for eigenvalues"). It provides no
bibliography, formula, definition, ordered binder, hypothesis, conclusion, proof boundary,
correction, erratum, or formal artifact. Its `已验证` label is untrusted metadata under rev-5.6.

The gloss identifies an algorithm family, not one truth-valued proposition. It does not decide:

- real or complex scalars, finite index order, matrix class, dimension, or topology;
- full or reduced QR, the orientation and normalization of the unitary factor, or how a
  rank-deficient step selects factors;
- unshifted, shifted, implicit, double-step, deflating, or another QR variant;
- whether the conclusion is one-step similarity or characteristic-polynomial invariance,
  cumulative similarity, Hessenberg preservation, convergence, rate, termination, stability, or
  eigenvalue-recovery correctness;
- spectral separation, diagonalizability, Jordan, normality, initial-flag genericity, shift, or
  nonbreakdown assumptions; or
- exact versus floating-point arithmetic and the zero-size, repeated-eigenvalue, equal-modulus,
  defective, real-conjugate-pair, shift-collision, and stalled-iteration cases.

The inspected Arbenz Chapter 4 lead gives the basic complex recurrence and its one-step unitary
similarity identity, then discusses a conditional convergence route. It is not the catalog's
citation, the observed author-hosted file is not an admitted immutable source, its full proof and
hypothesis mapping are not frozen here, and no independent review selects its invariant or
convergence claim as this target. Choosing either would narrow or substitute the catalog family.
The Francis and Kublanovskaya leads currently provide bibliography-level identity only.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a missing expression
fingerprint hard blockers. Without a canonical proposition, no imports can be certified minimal,
no target expression or canonical-target environment can be fingerprinted, no alternate transport
can be credited, and no removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case
mutation is meaningful. Those mutation classes are undefined, not passed. No surrogate theorem,
weakened special case, opaque predicate, axiom, placeholder, broadened interface, or proof body was
added.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its three direct
imports expose nine adjacent Gram-Schmidt, unitary, characteristic-polynomial, spectrum, and
triangular-matrix interfaces. They do not define a QR factor sequence, algorithm variant,
convergence endpoint, rate, stopping rule, or numerical semantics. These are probe imports, not
minimal imports for the absent canonical target, and receive no statement or proof credit.

In particular, `Matrix.charpoly_mul_comm` checks the candidate one-step equality
`(Q * R).charpoly = (R * Q).charpoly` using
`Mathlib.LinearAlgebra.Matrix.Charpoly.Basic`. That is a useful boundary fact but selecting it as
the target would advertise a convenient invariant as the unspecified QR algorithm theorem.

A bounded exact-topic search found no QR-iteration, QR-algorithm, Francis-step, or Kublanovskaya
declaration in the searched repo-local and pinned-mathlib Lean roots; only the intake probe's
disclaimer matched. This is scoped discovery evidence, not the downstream anchor audit or a global
absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The complete probe output has SHA-256
`06ee28738236b3f79dbc49d828936301c21f819d075bb6d4b60eebb55e8cbcee`; representative imported
theorems report only `propext`, `Classical.choice`, and `Quot.sound`.

The automation-provided `Formalizations/Lean/.lake` link points to canonical pinned artifacts and
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Record

Commands ran on 2026-07-13 (Asia/Shanghai), from the repository root unless a different working
directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1451` | 0 | rank 1128; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| source, blueprint, manifest, skill, and full intake-dossier inspection | 0 | the authoritative record is only a method-family gloss; intake leaves the exact claim and formal target open |
| `sha256sum` over authority, source, intake, probe, toolchain, lockfile, and relevant mathlib sources | 0 | exact fingerprints are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions agree with the environment above |
| pinned mathlib revision, tree, and package-status checks | 0 | revision and tree agree; the package worktree is clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1451/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; output SHA-256 `06ee2873...e8cbcee`; no canonical target was stated |
| bounded exact-topic Lean search | 0 | only the local probe disclaimer matched; no exact-topic declaration was found in the searched roots |
| `python3 -B Stage1_Instances/THM-M-1451/check_intake.py` | 1 | historical intake checker stops at line 121 because it freezes intake state `[ ]`, while current authority records provisional `[_]`; prior evidence was not rewritten |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and scoped blocker invariant check | 0 each | identity, null target/imports, undefined mutations, unchanged vector, false completion flags, exact two-file scope, and no-self-test state agree |
| scoped tracked and new-file whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is intake-specific: it freezes the original nine-file inventory,
the pre-integration `[ ]` cursor, and older authority fingerprints. This statement attempt records
its failed replay rather than rewriting the prior instance, receipt, checker, target-local DAG,
generated checklist, or authoritative DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first master-accept fresh intake evidence. Accountable reviewers must
then preserve and hash an immutable primary or approved authoritative source, select and
independently approve one exact QR-algorithm proposition, and map every incorporated definition,
binder, premise, conclusion, algorithm step, proof boundary, correction, and erratum. They must
freeze the scalar and matrix domain, factorization convention, algorithm and shift/deflation
variant, spectral and genericity assumptions, endpoint and topology, rate or correctness claim,
arithmetic model, neighboring-target boundary, and every degenerate case.

A later statement worker can then encode precisely that source-selected claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

The first failed statement gate is exact source-statement identity and algorithm/conclusion
selection. Lifecycle remains `planned`; the intake vector `[H1, M3, R3]` is unchanged, with
`audit_complete: false` and `theorem_complete: false`. This is blocked-attempt evidence, not
completion of the statement node or any downstream node. Because the exact-statement deliverable
did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master
acceptance is claimed.
