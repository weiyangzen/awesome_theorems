# Exact-statement gate: blocked

Item: `S56-M-0053-STATEMENT`

Theorem: `THM-M-0053`

Base revision: `a1c9974d7fb28cd680e6494b968544bf801a93a2` (tree
`1fa287bc821355aca2ca9e3ce107830a3eb58e64`).

## Decision

The statement item remains `[ ]`. Rev-5.6 permits dependency-ordered preparation while
`S56-M-0053-INTAKE` is only provisional worker state `[_]`, but its receipt has `accepted: false`,
is not content-addressed, and has no accepted receipt ID. It deliberately leaves the canonical
human statement and formal target null. Master acceptance of refreshed intake evidence remains
necessary before any future statement transition can be accepted.

Independently, the exact-statement gate fails closed. The repository record supplies only the title
`盖尔圆盘定理` (Gershgorin circle theorem), attribution Semyon Gershgorin, year 1931, and the
gloss `矩阵特征值的定位定理` (a localization theorem for matrix eigenvalues). It supplies no
bibliography, formula, definitions, ordered binders, hypotheses, conclusion, proof boundary,
correction history, or independent review. Its `已验证` label is untrusted inventory metadata.

The intake's inspected source leads identify two materially different results: the basic assertion
that every eigenvalue lies in a closed row disc, and the stronger assertion that a separated union
of `k` discs contains exactly `k` eigenvalues counting multiplicity. Neither lead has been admitted
as an immutable, independently reviewed canonical source proposition. The original 1931 paper,
translation, exact theorem boundary, corrections, and errata remain open.

The received record also does not decide:

- complex matrices as in the classical source lead versus arbitrary `NormedField` matrices;
- `n x n` matrices with `n >= 2`, `Matrix (Fin n) (Fin n) Complex`, an arbitrary nonempty finite
  index type, or the possibly empty finite type used by the pinned candidate;
- row discs versus column discs and any transpose transport;
- characteristic-polynomial roots, nonzero eigenvectors, or
  `Module.End.HasEigenvalue (Matrix.toLin' A) mu` as the eigenvalue encoding;
- closed-ball membership versus the norm inequality and the exact off-diagonal radius encoding;
- ordered binders, universes, typeclass context, multiplicity semantics, and the treatment of
  dimension zero or one, repeated eigenvalues, coincident or overlapping discs, zero radii, and
  boundary membership.

These choices change the proposition. Selecting pinned mathlib's generalized
`eigenvalue_mem_ball` would silently choose only basic row-disc inclusion, broaden the complex
source lead to arbitrary normed fields, adopt arbitrary finite and possibly empty indices, and fix
one eigenvalue and disc encoding. Conversely, adding the component-counting refinement because it
also bears Gershgorin's name would strengthen the target without source authority. Both violate the
rev-5.6 prohibition on broadened or substituted theorems.

Consequently there is no honest canonical declaration whose imports can be certified minimal. No
`Statement.lean`, exact expression fingerprint, checked alternate transport, or mutation fixture
was created. The required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations are undefined rather than passed. The lifecycle remains `planned`, and the provisional
root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with the single direct import
`Mathlib.LinearAlgebra.Matrix.Gershgorin`. It authenticates the pinned interface

```text
{K n : Type*} [NormedField K] [Fintype n] [DecidableEq n]
{A : Matrix n n K} {mu : K}
(hmu : Module.End.HasEigenvalue (Matrix.toLin' A) mu) ->
  exists k, mu in Metric.closedBall (A k k)
    (sum j in Finset.univ.erase k, norm (A k j))
```

and reports direct axioms `[propext, Classical.choice, Quot.sound]`. The complete output is 1,215
bytes with SHA-256 `0ea3f7d141ed4ecec7b0f0397d4e01677cb1f0c5465249e60b615631ea716e7b`.
It also checks the row and column strict-diagonal-dominance determinant corollaries. Those are
applications, not localization targets.

This is real pinned interface evidence only. The probe declares no canonical target, checked source
transport, mutation certificate, or proof body, and its import cannot be certified minimal for an
absent target. A bounded repository and pinned-mathlib search located this declaration and its
applications but no separate repo-local source-approved target. This bounded observation is not the
downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The pinned Gershgorin module has SHA-256
`d55fd47dd6fc18289d04c9ac628c74b6f3813bbc569efcfd276e308fe170cb79`.
The automation-provided `Formalizations/Lean/.lake` symlink was reused read-only. No update, build,
clone, fetch, or other dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0053` | 0 | rank 1521; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base identifiers appear above |
| authority, intake, scope, crosswalk, task-DAG, receipt, and source-record inspection | 0 | confirmed provisional dependency, null canonical target, unresolved source/domain/encoding/boundary choices, and all downstream tasks open |
| `git blame -L 398,403 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | pinned mathlib revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0053/IntakeProbe.lean` | 0 | six pinned APIs elaborated; exact generalized row-disc interface and direct axioms printed; output size and hash recorded above |
| bounded Gershgorin and declaration-name search in repo-local Lean and pinned mathlib | 0 | located the intake probe, defining module, determinant applications, and an importing module; no separate repo-local source-approved target identified |
| `python3 -B Stage1_Instances/THM-M-0053/check_intake.py` | 1 | historical intake validator expects authoritative intake state `[ ]`; integration now records provisional `[_]`, so it is stale and is not statement evidence |
| prohibited-declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0053/statement-blocker.json` and scoped invariants | 0 | valid JSON; identity, blocked/open state, null target/imports/fingerprints, unchanged vector, four undefined mutations, false completion flags, exact changed paths, and absent worker packet agree |
| scoped `git diff --check` plus per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker packet is absent because the exact-statement deliverable did not pass |

The intake checker is bound to intake-time state and was not modified to manufacture agreement with
the integrated DAG. The generated blueprint, authoritative execution DAG, intake instance, intake
receipt, and open per-target task DAG remain unchanged.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash one complete primary or authoritative source, select and independently
approve its exact proposition and proof boundary, and transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, correction, erratum, translation choice, and boundary case.
They must explicitly select basic inclusion versus component counting and settle the scalar field,
index and dimension conventions, row or column discs, eigenvalue and radius encodings, multiplicity,
and all degenerate cases.

A fresh statement run can then encode precisely that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`,
expression fingerprint, proof credit, or master acceptance is claimed.
