# THM-M-1492 exact-statement gate: blocked

Item: `S56-M-1492-STATEMENT`

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1492-INTAKE` is only provisional worker
state `[_]`: `intake-receipt.json` is unaccepted and non-content-addressed and has no accepted
receipt IDs. There is no master-accepted dependency receipt. Section 10.2 of the rev-5.6 blueprint
permits preparation of later provisional evidence, but master closure remains dependency ordered.

Independently and decisively, the exact source-statement gate fails. The complete repository record
is the title `线性规划` (linear programming), the George Dantzig attribution, the year 1947, and the
gloss `线性目标函数的优化` (optimization of a linear objective function). This names an optimization
problem family, not a truth-valued proposition. It provides no bibliography, model, ordered
binders, hypotheses, conclusion, or proof boundary. Stage0 explicitly leaves the precise
definitions and premises, proof route, dependencies, alternate forms, axiom policy, formal system,
machine status, and artifacts open. The catalog status `已验证` is untrusted metadata under
rev-5.6.

Materially inequivalent roots fit that gloss: attainment of an optimum, optimality at an extreme
point or basic feasible solution, an infeasible/unbounded/optimal alternative, weak or strong
duality, complementary slackness, a certificate theorem, or correctness or complexity of an
algorithm. Choosing among them changes the minimization or maximization orientation, data form,
decision and coefficient domains, objective, constraint directions, feasibility and boundedness
premises, witnesses, conclusion, and boundary cases. Selecting any familiar result would invent,
narrow, broaden, or substitute proposition-changing mathematics. It could also absorb separately
scheduled convex-optimization, simplex, interior-point, ellipsoid, or Lagrangian-duality targets.

Consequently there is no canonical expression to elaborate and no honest minimal-import claim. The
elaborated expression and environment fingerprints, credited alternate transports, and required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are
undefined, not passed. No `Statement.lean`, theorem declaration, proof body, weakened special case,
or broadened generic interface was added. The root remains `[H5, M4, R4]`; `H5` classifies only the
received problem-family gloss as not yet a stable proposition and does not refute correctly stated
linear-programming theorems.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its two direct
imports expose proper-cone duality and Farkas-style separation together with the `linarith` simplex
certificate-search implementation. All seven checked declarations elaborated.

Those declarations are adjacent substrate only. Mathlib's cone module explicitly lists definitions
of linear programs and LP duality as future work. `stateLP` and `findPositiveVector` are meta-level
tactic computation, not a kernel theorem for this target. The probe imports cannot be certified
minimal for an absent canonical target and receive no statement or proof credit. A bounded topic
search found only the intake disclaimer, cone-module prose and TODO, and the meta simplex
implementation. It located no source-selected kernel LP root declaration. This is narrow
statement-feasibility evidence, not the downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1492` | 0 | rank 1169; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 10903,10908 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| authority, source, intake, probe, toolchain, lockfile, and relevant mathlib SHA-256 checks | 0 | exact current hashes are preserved in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1492/IntakeProbe.lean` | 0 | seven adjacent APIs elaborated; stdout SHA-256 `afe16cb8bf7b69ccfe66c78b007bd89c06b10c712cd8ddadbfb1417678387133`; no target declaration |
| bounded linear-programming target-pattern search | 0 | only the intake disclaimer, cone prose and TODO, and meta simplex implementation matched; no source-selected kernel LP root was located |
| `python3 -B Stage1_Instances/THM-M-1492/check_intake.py` | 1 | historical intake checker expects authoritative intake `[ ]`, attempt 0, while integration records `[_]`, attempt 1; this phase records rather than rewrites stale intake evidence |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, scoped invariant, whitespace, exact-change, dependency-status, and absent-self-test
checks are recorded in the structured blocker beside this report.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then lawfully preserve one immutable primary or approved authoritative source and independently
select one exact truth-valued linear-programming proposition. They must map every incorporated
definition, assumption, proof boundary, correction, and erratum, and freeze the LP form and
orientation, domains, indices, coefficients, objective, constraints, ordered binders, hypotheses,
conclusion, witnesses, computation boundary, alternate encodings, neighboring-target boundaries,
and every degenerate case.

A fresh statement worker may then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, audit completion, theorem completion, or master acceptance is claimed.
