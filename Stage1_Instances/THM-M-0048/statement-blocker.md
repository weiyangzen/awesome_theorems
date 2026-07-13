# Exact-statement gate: blocked

Item: `S56-M-0048-STATEMENT`

Theorem: `THM-M-0048`

Base revision: `a16584a808446057f9ca2f2f26e76230cf45b84f` (tree
`af0da30f285b30a34f3ead4689f614670d8bef98`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0048-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt is non-content-addressed, declares
`accepted: false`, and has no accepted receipt ID. More importantly, that intake deliberately
leaves the canonical mathematical statement and Lean target null.

The exact-statement gate cannot pass from the received claim. The catalog supplies only the name
"Cauchy-Binet formula" and the gloss "determinant formula for a matrix product," attributed to
Cauchy and Binet in 1812. It gives no source locator, displayed formula, coefficient domain,
dimensions, dimension inequality, minor orientation and ordering, or degenerate-case policy. It
does not distinguish the full rectangular minor-sum identity from square determinant
multiplicativity.

The intake did inspect a strong modern source lead: Konstantopoulos, arXiv `1305.0644v1`, formula
(1), Theorem 1/formula (6), and formula (9) on printed pages 1 and 3-4. It states a rectangular
field-valued formula with the smaller dimension no greater than the intermediate dimension and
provides a complete proof route. But the intake explicitly records it as unaccepted: it is neither
catalog-cited nor a primary Cauchy/Binet source, independent review and the full definition/errata
crosswalk are open, and the zero-dimensional boundary remains unresolved. Promoting it now would
override the frozen intake boundary rather than elaborate an exact admitted claim.

Consequently there is no honest canonical Lean expression whose imports can be certified minimal,
no credited alternate encoding, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation suite. Those mutations are undefined, not passed.
The lifecycle remains `planned`, and the root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

`IntakeProbe.lean` was re-elaborated with the pinned toolchain. Its direct imports are
`Mathlib.LinearAlgebra.Matrix.Determinant.Basic` and `Mathlib.Order.Hom.PowersetCard`. It
authenticates determinant, multiplication, submatrix, and naturally ordered finite-subset APIs and
elaborates two candidate proposition shapes:

- a rectangular minor-sum formula over a commutative ring without a dimension premise; and
- a field-valued version with `m <= n`, following the modern source lead.

Neither is canonical. The first is a source-unapproved generalization. The second is a
source-shaped candidate pending admission, exact boundary mapping, and independent review.
`Matrix.det_mul` is only the square specialization. Its axiom report is `[propext,
Classical.choice, Quot.sound]`; it is not proof credit for the rectangular root.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone, fetch,
or other dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0048` | 0 | rank 1088; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree and package-status checks | 0 | revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0048/IntakeProbe.lean` | 0 | seven adjacent APIs and two candidate shapes elaborated; `Matrix.det_mul` reported the three axioms above; no canonical target was declared |
| `python3 -B Stage1_Instances/THM-M-0048/check_intake.py` | 1 | historical intake replay stops because it expects authority state `[ ]` while current authority records provisional `[_]`; its frozen base and exact inventory are also intake-only |

The integrated intake artifacts and their relevant inputs are content-fingerprinted in
`statement-blocker.json`. Final scoped checks additionally validate that JSON, reject prohibited
Lean constructs by an expected no-match scan, require the root self-test manifest to remain absent,
and run whitespace checks over the two blocker reports.

## Retry Condition And Status Boundary

An accountable source reviewer must preserve and hash a lawful immutable primary or authoritative
source, select and independently approve one exact theorem passage, and transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, convention,
attribution decision, erratum, and boundary case. The review must settle rectangular versus square
scope, coefficient domain, dimension premise, minor order and orientation, and all zero or oversize
cases. A fresh statement worker can then encode exactly that claim, minimize pinned imports,
serialize and hash the elaborated expression and environment, compile each credited transport, and
execute all four mutation classes. The integration lane must master-accept the intake dependency
before accepting that future statement transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
