# Exact-statement gate: blocked

Item: `S56-M-0059-STATEMENT`

Theorem: `THM-M-0059`

Base revision: `48abbb2d2eeb89816c5ffc0ad8faafa4b9d24dd0` (tree
`0f26e2c78fb5fff9277cbbdfef5e145fd4ef06f1`).

## Decision

The statement item remains `[ ]`. Rev-5.6 section 10.2 permits dependency-ordered preparation
while `S56-M-0059-INTAKE` is only provisional worker state `[_]`. Its receipt declares
`accepted: false`, is not content addressed, has no accepted receipt ID, and deliberately leaves
the canonical human and Lean statements null. Master acceptance of that dependency remains
necessary before any later statement transition can be accepted.

Independently and decisively, the received record cannot identify one exact proposition. The
repository supplies only the name Hadamard's inequality, Jacques Hadamard's attribution, the year
1893, and the gloss `行列式的上界估计` (an upper-bound estimate for a determinant). It contains no
bibliography, formula, definition chain, ordered binders, hypotheses, conclusion, proof boundary,
correction history, or accountable review. Its `已验证` label is untrusted under rev-5.6.

The commonly cited historical lead is Jacques Hadamard, "Resolution d'une question relative aux
determinants," *Bulletin des Sciences Mathematiques*, second series 17 (1893), pages 240-246.
The intake did not admit a lawful immutable scan or an exact theorem passage, incorporated
definitions, proof crosswalk, correction audit, translation, or independent review. The citation
therefore supports a provisional `H1` family assessment, not exact statement identity or `H0`.

The proposition-changing choices left open include:

- real versus complex matrices or a coordinate-free real inner-product-space theorem;
- `Matrix (Fin n) (Fin n)` versus an arbitrary finite index, with the universe and dimension
  witnesses fixed explicitly;
- row norms versus column norms and the checked transpose or coordinate transport between them;
- the precise Euclidean norm and determinant encodings, and an unsquared inequality versus a
  squared Gram-determinant form;
- inequality only, equality for an orthogonal family, or a full equality characterization; and
- zero dimension, the empty product and zero-by-zero determinant, dimension one, zero and singular
  matrices, zero rows or columns, proportional rows, determinant sign or phase, and equality with
  zero factors.

Choosing the familiar real row form, the complex form, the squared Gram form, or the pinned
coordinate-free volume-form theorem would therefore add, narrow, or substitute mathematics that
the received record does not select. Rev-5.6 sections 5 and 5.1 make statement ambiguity and a
missing expression fingerprint hard blockers. There is no honest canonical target whose imports
can be certified minimal, no credited alternate encoding for a checked transport, and no
meaningful removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation.
The lifecycle remains `planned`, and the provisional family vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates from the single direct import
`Mathlib.Analysis.InnerProductSpace.Orientation`. It checks the pinned candidate

```text
Orientation.abs_volumeForm_apply_le
  (o : Orientation Real E (Fin n)) (v : Fin n -> E) :
  abs (o.volumeForm v) <= product i, norm (v i)
```

together with `Orientation.volumeForm_robust'`, the orthogonal-family equality,
`Module.Basis.det_apply`, `Pi.basisFun_det_apply`, and `Matrix.det`. The candidate theorem reports
the direct axioms `[propext, Classical.choice, Quot.sound]`. Its exact probe output has SHA-256
`6abe3a526a275542f689b99a45c2d0b0663be12f939cdc204d833ab12cd4756b`.

This is real statement-feasibility evidence only. The probe declares no canonical matrix target,
checked row/column or matrix/volume-form transport, expression fingerprint, mutation suite, or
proof body. A bounded repo-local and pinned-mathlib search found the same volume-form theorem,
the weaker factorial uniform-entry bound `Matrix.det_le`, and the unrelated entrywise
`Matrix.hadamard` product; it did not resolve the source-selected root. The single probe import
cannot be certified as the minimal import for an absent canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone, fetch,
or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0059` | 0 | rank 1526; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base identifiers appear above |
| `git blame -L 440,445 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0059/IntakeProbe.lean` | 0 | seven adjacent pinned interfaces elaborated; direct candidate axioms reported; no canonical target or proof body; stdout hash recorded above |
| bounded Hadamard determinant-bound search over repo-local and pinned-mathlib Lean | 0 | found the volume-form candidate, weaker factorial entry bound, and unrelated entrywise product; no source-root selection or exact matrix target |
| `python3 -B Stage1_Instances/THM-M-0059/check_intake.py` | 1 | historical intake validator expects its intake item still to be `[ ]`; integrated authority now records provisional `[_]`, so it is stale and is not statement evidence |
| prohibited-declaration scan of owned Lean files | 0 | the inner `rg` returned expected no-match exit 1; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration was found |
| `python3 -m json.tool Stage1_Instances/THM-M-0059/statement-blocker.json` plus scoped Python invariants | 0 | valid JSON; identity, blocked/open state, null target/import/hash/fingerprint, unchanged H1/M3/R4 vector, four undefined mutations, false completion fields, and no-receipt/no-self-test boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-0059` plus per-new-file `git diff --no-index --check /dev/null ...` | 0 | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker is bound to intake-time state and deliberately was not modified to make this
statement attempt pass. The statement blocker is validated separately; the generated blueprint,
authoritative execution DAG, intake instance, intake receipt, and open task DAG remain unchanged.

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve and hash a complete primary or authoritative source,
select and independently approve one exact inequality and proof boundary, and transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, correction, erratum, translation,
transport, equality clause, and boundary case. They must explicitly resolve the scalar, finite
index and dimension, rows versus columns, norm, determinant, squared versus unsquared form,
matrix/volume-form relation, and equality scope.

A fresh statement run can then encode exactly that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile each credited transport, and
execute all four required mutation classes. The integration lane must also revalidate and
master-accept the intake dependency before accepting that future statement transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`,
expression fingerprint, proof credit, or master acceptance is claimed.
