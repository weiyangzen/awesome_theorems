# THM-M-1452 exact-statement gate: blocked

Item: `S56-M-1452-STATEMENT`

Base revision: `58fbed45d2c785466ee920c7696f0f7b3686d9a5` (tree
`36198f7c90045b3b21d338a3d0ce47aa4ff930f1`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1452-INTAKE` has only provisional worker
state `[_]`: `intake-receipt.json` has `accepted: false`, no accepted receipt IDs, and stale hashes
for the current blueprint and execution DAG. There is no master-accepted dependency receipt.

Independently of that workflow boundary, the exact-statement gate fails. The complete catalog claim
is `大型稀疏矩阵的特征值` ("eigenvalues of large sparse matrices") under the method label
`Lanczos算法`. It is a computational topic, not a truth-valued proposition. It specifies no scalar
field, matrix dimension, symmetry premise, mathematical meaning of sparsity, start vector,
recurrence, iteration count, nonbreakdown condition, output, invariant, approximation or convergence
claim, arithmetic model, ordered binders, or boundary cases. Stage0 leaves the exact definitions and
premises open, and the intake accordingly records a null human claim and null formal target.

The inspected 1950 Lanczos paper is a credible source lead, but the catalog selects no theorem or
formula from it. Its symmetric three-term recurrence, orthogonality, Krylov-span, tridiagonalization,
finite-termination, Ritz-value, and numerical-analysis consequences are inequivalent theorem
families. Selecting one in this phase would invent or substitute proposition-changing mathematics.

Therefore there is no canonical Lean expression whose imports can be minimized, no expression or
environment fingerprint, no approved alternate encoding, and no meaningful removed-hypothesis,
changed-domain, changed-binder-scope, or boundary-case mutation. The root vector remains
`[H5, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with the pinned environment. It
checks Hermitian spectral and Gram-Schmidt APIs, but it defines no Lanczos algorithm and states no
canonical target. A bounded repo-local and pinned-mathlib name/topic search found no Lanczos,
Krylov-subspace, tridiagonalization, three-term-recurrence, or Ritz-value terminal declaration.
Those observations do not constitute the later anchor audit or prove global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1452` | 0 | rank 1129; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all; git rev-parse HEAD; git rev-parse 'HEAD^{tree}'` | 0 | before statement edits only the automation-provided untracked `Formalizations/Lean/.lake` existed; base revision and tree are recorded above |
| `git blame -L 10602,10607 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD; git -C Formalizations/Lean/.lake/packages/mathlib rev-parse 'HEAD^{tree}'; git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | pinned revision and tree recorded above; mathlib worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1452/IntakeProbe.lean` | 0 | eleven adjacent APIs elaborated; stdout SHA-256 `3a3c3ebee49919f4a27c6e9c5483dbe064286d646cc89a4f925aba9c7d041251`; representative axiom reports list only `propext`, `Classical.choice`, and `Quot.sound`; no target declaration |
| bounded `rg` searches in repo-local Lean and pinned mathlib | 1 each, expected no match | no relevant named declaration matched; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-1452/check_intake.py` | 1 | historical intake validator rejected the stale recorded blueprint hash; this statement-only run does not rewrite prior intake evidence |
| prohibited Lean declaration scan over the owned `*.lean` files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration matched |
| `python3 -m json.tool Stage1_Instances/THM-M-1452/statement-blocker.json` | 0 after finalization | structured blocker is valid JSON |
| blocker invariant check | 0 after finalization | identity, null target/imports/fingerprints, unchanged vector, four undefined mutations, false completion flags, exact changed paths, and no-self-test boundary agree |
| scoped `git diff --no-index --check /dev/null <file>` checks | 1 after finalization (expected added-file diff status) | no whitespace diagnostics in either blocker artifact; exit 1 denotes that each added file differs from `/dev/null` |
| `test ! -e .stage1-worker-selftest.json` | 0 after finalization | no self-test manifest was emitted because the assigned deliverable did not pass |

## Retry Condition

The integration lane must accept fresh intake evidence. Accountable reviewers must lawfully preserve
an immutable source proposition and independently approve its article/section/page/formula locators,
correction disposition, definitions, ordered binders, hypotheses, conclusion, and boundary cases.
They must explicitly reconcile the catalog's "large" and "sparse" wording with the selected exact
theorem and fix the recurrence, breakdown, output, and arithmetic conventions. A later statement run
can then encode only that proposition, minimize its pinned imports, preserve its elaborated
expression and environment fingerprint, compile every credited transport, and execute all four
mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
No statement receipt, root worker self-test packet, worker `[_]`, proof credit, audit completion,
theorem completion, or master acceptance is claimed.
