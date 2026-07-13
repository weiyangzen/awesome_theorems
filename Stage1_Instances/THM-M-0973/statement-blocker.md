# Exact-statement gate: blocked

Item: `S56-M-0973-STATEMENT`

Theorem: `THM-M-0973`

Base revision: `d849f42c82f9da2e07c481c7beaeba6d92f86e19` (tree
`874c7795eb7b2cc49d6c8479c316b09b039e9786`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0973-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, has no
accepted receipt ID, and deliberately leaves the canonical mathematical statement and formal
target null. Dependency-ordered investigation is possible, but master acceptance remains required
before any eventual statement transition can be accepted.

Independently, the exact-statement gate cannot pass. The repository record supplies only the title
"Kim-Vu inequality," the incorrect attribution `Jeong Han Han/Van Vu`, the year 2000, and the gloss
"polynomial concentration inequality." It gives no source, selected theorem, definitions, binders,
hypotheses, constants, conclusion, proof boundary, corrections, reviewer, or boundary conventions.
The adjacent `verified` label is explicitly untrusted under rev-5.6.

The intake identifies Jeong Han Kim and Van H. Vu's 2000 article *Concentration of Multivariate
Polynomials and Its Applications* as the likely primary paper. Only bibliographic metadata and a
formula-stripped abstract were admitted. The formula-bearing theorem text was access-controlled,
and attempted author-hosted PDF endpoints remained unavailable. Consequently no numbered theorem,
incorporated definitions, exact assumptions, derivative parameters, numerical constants, tail
formula, proof boundary, correction, or erratum has been inspected or independently approved.

The proposition-changing choices remain open: Bernoulli laws and the probability space; formal
versus multilinear polynomial representation; coefficient and degree conventions; the family of
partial derivatives; maximum versus average derivative expectations; normalization and auxiliary
parameters; numerical constants; one-sided versus two-sided tail event; and every zero, constant,
degree-zero, vanishing-parameter, empty-index, and endpoint case. Remembered or secondary Kim-Vu
formulas differ on these points. Selecting one would invent or substitute mathematics rather than
elaborate the exact received target.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard
blockers. There is therefore no honest canonical expression for which imports can be certified
minimal, no credited alternate encoding for a checked transport, and no canonical target against
which the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations can run. Those mutation results are undefined, not passed. The root vector remains
`[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with four direct imports for multivariate-polynomial
evaluation, partial derivatives, independent functions, and Bernoulli product measures. Eight
adjacent APIs check successfully. The probe defines no random-polynomial model, derivative
expectation parameters, canonical target, transport, or proof body, so its imports cannot be
certified minimal for an absent Kim-Vu target.

A bounded exact-topic search over pinned mathlib and repository-local Lean found no target-specific
declaration; only the probe's disclaimer matched. This is discovery-only evidence, not the later
immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or other
dependency mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0973` | 0 | rank 1507; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, blueprint, skill, and intake inspection | 0 | confirmed the sparse catalog claim, uninspected exact source, null canonical target, and open proposition-changing choices |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0973/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `a048f43a0f87ea112ff2d786dce0c806a60a1afe1838cd9893ed684fdf05fbab`; empty stderr; no canonical target or proof body |
| bounded search for Kim-Vu or polynomial-concentration declarations | 0 | only two discovery disclaimer lines matched; no target-specific declaration located |
| `python3 -B Stage1_Instances/THM-M-0973/check_intake.py` | 1 | historical intake checker rejects the integration-updated authoritative DAG hash/state; it is stale evidence and was not rewritten |
| scoped prohibited-construct scan over owned Lean files | 0 | inner search returned expected no-match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured blocker
beside this report.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash a complete immutable primary or approved authoritative source, select
one exact numbered proposition, and independently approve its definitions, ordered binders,
hypotheses, conclusion, proof boundary, author correction, corrections, errata, and all boundary
cases. They must freeze the probability model, polynomial and coefficient conventions, degree,
derivative controls, expectation extrema, constants, parameter ranges, tail event, and degenerate
cases.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
