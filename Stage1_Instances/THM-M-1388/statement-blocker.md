# Exact-statement gate: blocked

Item: `S56-M-1388-STATEMENT`

Theorem: `THM-M-1388`

Base revision: `9890b8ae7278d1978497acce2be86f8fc4072af3` (tree
`b90a6c34f533284f14d1d71b0ba11c76095110d8`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1388-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt is explicitly provisional and
unaccepted, and its accepted-receipt list is empty. Rev-5.6 permits this dependency-ordered attempt,
but no statement transition can be accepted before the prerequisite is accepted.

Independently, the exact-statement gate cannot be entered truthfully. The repository's complete
mathematical wording is the title `特征值问题` ("eigenvalue problem") and the gloss
`Sturm-Liouville特征值` ("Sturm-Liouville eigenvalues"), with an attribution, twentieth-century
date, importance label, and untrusted `已验证` status. It contains no cited proposition. Stage0
explicitly leaves the precise definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open.

The record does not select:

- a finite regular interval, a singular interval, a half-line, or an abstract operator setting;
- real or complex scalars, coefficient functions and regularity, positivity and nonvanishing
  conditions, or equality-almost-everywhere conventions;
- the differential-expression sign and normalization, weighted space, operator domain, derivative
  notion, or endpoint classification;
- Dirichlet, Neumann, Robin, mixed, periodic, antiperiodic, separated, or coupled boundary data;
- eigenvalue, eigenfunction, nonzero-vector, normalization, and multiplicity conventions; or
- existence, reality, simplicity, discreteness, enumeration, lower boundedness, accumulation,
  eigenfunction completeness, convergence, or a reviewed conjunction as the conclusion.

These choices yield inequivalent propositions. Gerald Teschl's *Ordinary Differential Equations
and Dynamical Systems*, Section 5.4, was inspected at intake only as an authoritative source-family
lead. Its Theorem 5.11 combines several spectral and expansion clauses for one regular separated
Sturm-Liouville realization, while nearby results carry distinct hypotheses and proof boundaries.
The catalog neither cites this book nor selects that conjunction. Adopting it, one of its clauses,
a familiar special case, or an abstract structure that assumes the desired spectral conclusion
would invent, narrow, substitute, or circularly package mathematics.

The neighboring targets are also material boundaries: `THM-M-1384` owns broader Sturm-Liouville
theory; `THM-M-1385`, `THM-M-1386`, and `THM-M-1387` own comparison, separation, and oscillation;
`THM-M-1389` owns Weyl asymptotics; and `THM-M-1390` owns a min-max principle. None can select or
replace this root by title proximity.

The first substantive failure is therefore exact source-statement and target identity. Sections 5
and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression fingerprint hard
blockers. There is no canonical proposition for which minimal imports can honestly be claimed. No
`Statement.lean`, target declaration, expression hash, checked transport, or mutation fixture was
added. Removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are
undefined rather than passed. The intake vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` directly imports four pinned mathlib modules and checks thirteen
adjacent derivative, ODE, partial-operator, eigenvalue, symmetric/compact spectral, and Rayleigh
interfaces. It re-elaborates successfully, but it defines no Sturm-Liouville differential
expression, coefficient package, weighted space, operator domain, boundary conditions, eigenvalue
problem, target theorem, or proof body. Its imports therefore cannot be certified minimal for the
absent target and receive only discovery-interface evidence.

A bounded exact-topic search found no Sturm-Liouville occurrence in pinned mathlib. The only
repo-local Lean occurrence outside this dossier was a nonterminal planning string in legacy
`S1_M_207.lean`. These are scoped feasibility observations, not the downstream immutable anchor
audit or a global proof-of-absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was pre-existing and used read-only. No update, build, clone,
fetch, or dependency mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1388` | 0 | rank 998; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| source, Stage0, target-manifest, blueprint, execution-DAG, skill, and intake inspection | 0 | found only the sparse family wording, an explicit null intake target, and materially different candidate meanings |
| `git blame -L 10111,10116 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over authority, source, intake, probe, toolchain, and dependency inputs | 0 | exact hashes are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-1388/check_intake.py` | 1 | the historical provisional intake receipt's blueprint hash is stale after integration; it also freezes the original intake-only inventory and was not rewritten by this statement attempt |
| `cd Formalizations/Lean && lake env lean --version` and `lake --version` | 0 each | pinned Lean and Lake versions recorded above |
| mathlib `rev-parse HEAD 'HEAD^{tree}'` and package `git status --short` | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1388/IntakeProbe.lean` | 0 | all thirteen generic adjacent APIs elaborated; stdout SHA-256 `ac028e1169b8e992d0aac97fb938547024be09f08fea05ac3f1bbe994c2e0008` |
| bounded exact-topic searches of pinned mathlib and repo-local Lean | 1; 0 | no pinned-mathlib occurrence; only the dossier and one nonterminal legacy planning string locally |
| `python3 -m json.tool Stage1_Instances/THM-M-1388/statement-blocker.json` | 0 | the finalized structured blocker parsed as valid JSON |
| scoped Python blocker-invariant check | 0 | identity, base, open blocked state, null target and imports, unchanged vector, false completion fields, four unrunnable mutations, two-file ownership, and absent self-test agree |
| prohibited-declaration scan over owned Lean files | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1388` plus per-new-file no-index checks | 0; 1 each | no whitespace diagnostics; both no-index exits are only the expected new-file differences |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

The integration lane must first accept refreshed intake evidence. Accountable reviewers must then
preserve and hash an immutable primary or authoritative edition, select and independently approve
one exact root theorem or explicit conjunction, and transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, coefficient and regularity condition, differential
expression, interval and endpoint convention, weighted space and operator domain, boundary
condition, eigenvalue and multiplicity convention, exceptional case, proof boundary, correction,
and erratum. The decision must preserve every neighboring target boundary.

A fresh statement run can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

This blocker is the truthful outcome of the assigned attempt, not completion of the statement or
any downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
