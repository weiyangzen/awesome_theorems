# Exact-statement gate: blocked

Item: `S56-M-1392-STATEMENT`

Theorem: `THM-M-1392`

Base revision: `a07fc18923e20fd2876d04809a15d5b31e55512f` (tree
`1268491c8f2677e1c8e38754fa93dd190892e69e`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1392-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. The intake receipt
also declares `accepted: false`, has no accepted receipt ID, and deliberately leaves the canonical
mathematical statement and Lean target null.

Independently, the authoritative repository record cannot support an exact Lean 4 target. Its
complete mathematical wording is only the title `Green函数` ("Green function") and the gloss
`边值问题的积分表示` ("integral representation of boundary-value problems"). It gives an
attribution and year but no cited theorem or binder-complete proposition. Stage0 explicitly leaves
the definitions and premises, proof, dependencies, alternate forms, axioms, and machine artifact
open. The catalog label `已验证` is untrusted under rev-5.6.

The record does not select:

- a differential operator, order, sign convention, coefficients, regularity, or scalar field;
- an interval, endpoint order, boundary functionals, or solution and forcing spaces;
- existence, uniqueness, invertibility, or nonresonance hypotheses;
- a kernel construction, normalization, branch, diagonal convention, or derivative jump;
- an integral measure and pointwise, almost-everywhere, norm, or operator equality; or
- one representation identity, one or both inverse identities, an existence theorem, a uniqueness
  theorem, or an equivalence as the conclusion.

These choices produce inequivalent propositions. Gerald Teschl's *Ordinary Differential Equations
and Dynamical Systems*, Section 5.4, is an inspected authoritative discovery lead for one regular
weighted Sturm--Liouville realization with separated boundary conditions. The catalog neither
cites it nor selects its piecewise kernel, integral resolvent, or inverse identities. Adopting that
realization, a convenient Dirichlet special case, or an interface that assumes the representation
would invent, narrow, or circularly package mathematics rather than elaborate the exact received
target. The separately scheduled PDE Green-function, symmetry, and eigenfunction-expansion targets
also transfer no scope.

The first substantive statement failure is therefore exact source-statement and scope identity.
Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. Consequently there is no honest canonical declaration for which minimal
imports can be claimed. No `Statement.lean`, exact expression, checked transport, or mutation suite
was created. Removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
are undefined rather than passed. The intake vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` directly imports `Mathlib.Analysis.ODE.Basic` and
`Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus`. It re-elaborates six adjacent
integral-curve, derivative, and interval-integral APIs. Those APIs define no boundary-value
operator, Green kernel, or representation theorem, and the two imports cannot be certified minimal
for an absent canonical target. The successful probe receives discovery-only interface evidence,
not statement, anchor, or proof credit.

A bounded exact-topic search found no matching Green-function boundary-value declaration in pinned
mathlib. The repository-local Lean hits are unrelated predicate fields or prose. This is scoped
feasibility evidence only, not the downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1392` | 0 | rank 1002; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository source, Stage0, target-manifest, blueprint, DAG, and intake inspection | 0 | found the sparse catalog family wording, explicit null intake target, and inequivalent candidate meanings; no source-selected proposition |
| `sha256sum` over authority, source, intake, probe, toolchain, and dependency inputs | 0 | hashes are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-1392/check_intake.py` | 1 | the historical provisional intake receipt's blueprint hash is stale after integration; this statement phase does not rewrite historical evidence |
| `cd Formalizations/Lean && lake env lean --version` and `lake --version` | 0 each | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1392/IntakeProbe.lean` | 0 | all six generic adjacent APIs elaborated; no canonical target was declared |
| bounded exact-topic searches of pinned mathlib and repository-local Lean | 1; 0 | no target candidate in mathlib; only unrelated repository-local fields or prose |
| prohibited-construct scan over owned Lean files | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and scoped invariant check for `statement-blocker.json` | 0 each | blocker identity, null target and imports, unchanged vector, four undefined mutations, false completion flags, and absent-self-test boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-1392` plus per-new-file no-index checks | 0; 1 each | no whitespace diagnostics; both no-index exits are only the expected new-file differences |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

The integration lane must first accept refreshed intake evidence. Accountable reviewers must then
preserve and hash an immutable primary or authoritative edition, select and independently approve
one exact root theorem or explicit conjunction, and transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, operator and coefficient convention, interval and boundary
condition, space and regularity requirement, nonresonance condition, kernel normalization and
diagonal rule, measure and equality convention, exceptional case, proof boundary, correction, and
erratum. The selection must preserve the boundaries with the generic ODE boundary-value,
Sturm--Liouville, PDE Green-function, symmetry, eigenfunction-expansion, and Fredholm targets.

A fresh statement run can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
