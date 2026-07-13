# Exact-statement gate: blocked

Item: `S56-M-0281-STATEMENT`

Theorem: `THM-M-0281`

Base revision: `997541734bb32f987fb15f163335a82512992120` (tree
`2c866b9d840d48c48ac839740c62d3b9440be0e5`).

## Decision

The statement item remains `[ ]`. Its prerequisite, `S56-M-0281-INTAKE`, has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt is explicitly unaccepted and
non-content-addressed and has no accepted receipt ID. It deliberately leaves both the canonical
mathematical statement and Lean target null. The provisional dossier can be inspected in dependency
order, but it cannot be treated as accepted statement authority.

Independently, the complete repository claim is only `延森不等式` (Jensen's inequality), attributed
to Johan Jensen in 1906, with the gloss `凸函数的积分不等式` ("integral inequality for convex
functions"). It supplies no formula, bibliography, theorem locator, incorporated definition chain,
ordered binders, assumptions, exact conclusion, proof boundary, correction history, boundary
policy, or independent review. The catalog's `已验证` label is untrusted under rev-5.6.

The missing choices change the proposition rather than its notation:

- a probability-measure integral, a normalized nonzero finite-measure average, or a restricted-set
  average;
- the measurable source space, scalar field, target normed space, measure, and integral convention;
- global convexity or `ConvexOn`, together with the exact convex domain;
- closedness, continuity or weaker regularity, measurability, integrability of the input and
  composite, and almost-everywhere range assumptions;
- a convex non-strict inequality, concave dual, strict form, equality characterization, or finite
  convex-combination result; and
- zero measures, empty restricted sets, constant and affine functions, null-set exceptions,
  nonintegrable inputs, and other boundary cases.

Jensen's 1906 Acta Mathematica paper is a matching bibliographic lead, but intake preserved only
Crossref metadata. No article bytes, pinpoint theorem passage, incorporated definitions, exact
premise and proof boundary, correction or errata disposition, translation, or independent review
were admitted. A modern familiar formulation cannot fill those gaps without source approval.

Section 5 of the rev-5.6 blueprint makes statement ambiguity and a missing elaborated-expression
fingerprint hard blockers. There is consequently no canonical expression for which minimal imports,
fixed binders and typeclass context, checked alternate transports, or removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations can be certified. Those mutation
tests are undefined, not passed. The root remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its single direct import,
`Mathlib.Analysis.Convex.Integral`. Eight exact-topic interfaces elaborated:

- `ConvexOn.map_integral_le` uses a probability measure;
- `ConvexOn.map_average_le` uses a nonzero finite measure and normalized average;
- `ConvexOn.map_set_average_le` averages over a restricted set;
- `ConvexOn.map_centerMass_le` and `ConvexOn.map_sum_le` are finite forms; and
- the checked concave, strict, and equality declarations have still different hypotheses and
  conclusions.

This confirms rather than resolves the ambiguity. The probe's complete output has SHA-256
`916d4f48a8cb821d7ff8e4bc1a9ed45b4dadc90820233feec8b44922aed577ea`.
The two axiom diagnostics both report `[propext, Classical.choice, Quot.sound]`. The probe declares
no canonical target, source transport, or proof body, so its import cannot be certified minimal for
the absent target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink exposed the canonical pinned artifacts and was used read-only.
No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0281` | 0 | rank 1287; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD`; `git rev-parse 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided untracked `.lake` symlink existed; base revision and tree appear above |
| `git blame -L 2020,2025 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD`; corresponding tree and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0281/IntakeProbe.lean` | 0 | eight exact-topic interfaces and two axiom reports elaborated; output hash recorded above; no target or proof body declared |
| bounded `rg` search for Jensen declarations in repo-local Lean and pinned mathlib | 0 | distinct integral, normalized-average, restricted-set, finite, concave, strict, and equality families found; no repo-local canonical target |
| `python3 -B Stage1_Instances/THM-M-0281/check_intake.py` | 1 | historical intake replay stops at its old assertion that authoritative intake is `[ ]`; integration now records provisional `[_]`; this stale-intake failure is not statement evidence |

The structured blocker was also parsed and checked for item identity, null target/import/fingerprint,
unchanged debt, four undefined mutation classes, false completion flags, and the no-self-test
boundary. A prohibited declaration scan over the owned Lean probe found no `sorry`, `admit`,
`sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration. New-file and scoped whitespace
checks passed.

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve and hash an immutable primary or authoritative source,
select and independently approve one exact integral Jensen theorem, and transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
erratum, translation, and boundary case. They must fix measure normalization, spaces, convex-domain
convention, continuity and closedness, integrability, almost-everywhere range, inequality variant,
and degenerate cases. The intake dependency must also be refreshed and master-accepted.

A later statement run can then encode exactly that claim, minimize its pinned imports, serialize and
hash the elaborated expression and environment, compile every credited transport, and execute all
four mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. No `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, accepted state, statement fingerprint, or proof credit is claimed.
