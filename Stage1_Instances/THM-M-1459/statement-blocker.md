# THM-M-1459 exact-statement gate: blocked

Item: `S56-M-1459-STATEMENT`

Base revision: `2d82479e32843fd52283dcd9bb305954729c1199` (tree
`30134b43ab41e973d2558be90371bf18d6edb259`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1459-INTAKE` is provisional worker
state `[_]`, not master-accepted state `[x]`. Its receipt has `accepted: false`, is not content
addressed, and contains no accepted receipt ID. The historical intake checker also fails closed
because it expects the authority's former `[ ]` state while the current execution DAG records
`[_]`. This statement-only work does not rewrite intake evidence.

Independently and decisively, the exact-statement gate cannot pass. The complete repository claim is
only `N-body problem fast algorithm`, under the method-family title `Fast multipole method`. A
method name and purpose are not a truth-valued proposition. They do not select:

- static potential evaluation, force evaluation, a matrix-vector product, or N-body time evolution;
- two-dimensional logarithmic, three-dimensional Laplace/Coulomb/gravitational, screened, or
  another interaction kernel;
- particle and strength types, sources and targets, self-interaction, or collision behavior;
- a fixed or adaptive hierarchy, separation rule, expansion order, translations, or interaction
  lists;
- an analytic identity, truncation bound, end-to-end correctness theorem, error guarantee, work or
  storage result, numerical-stability theorem, or a sourced conjunction; or
- accuracy, norm, arithmetic, cost, ordered-binder, conclusion, and boundary conventions.

Those choices change the theorem. The inspected later source leads contain distinct planar and
three-dimensional expansion/error results, translation lemmas, hierarchy conditions, resource
arguments, and experiments. They confirm rather than resolve the ambiguity. The historically
relevant 1987 article has been identified bibliographically, but intake did not lawfully preserve
and inspect its body, select an exact result, map all assumptions, audit corrections, or obtain
independent source approval.

Choosing a familiar planar expansion, three-dimensional error theorem, adaptive algorithm, or
linear-work slogan would therefore invent or substitute mathematics. Encoding an abstract premise,
oracle, hierarchy, approximation, or cost certificate that already contains the desired conclusion
would be a placeholder rather than an FMM theorem.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard
blockers. There is no canonical Lean expression whose imports can be minimized, no target
environment-expression fingerprint, and no approved alternate encoding to transport. The required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not passed. The lifecycle remains `planned`, and the root vector remains `[H5, M4, R4]`.

## Lean Boundary

The discovery-only `IntakeProbe.lean` was re-elaborated against the existing pinned environment. Its
three direct imports expose nine adjacent finite-sum, geometric-series, complex-norm, logarithmic
Taylor-series, and remainder-bound interfaces. The complete stdout SHA-256 was
`3b73bb355540cf5aaf30c21257f47cbb4f69f6e825b1dcbe6576ddce9a95eef6`. Representative axiom reports
name only `propext`, `Classical.choice`, and `Quot.sound`.

That probe declares no particles, kernel, hierarchy, approximation, resource theorem, canonical
target, checked source transport, or proof body. Its imports cannot be certified minimal for an
absent target and receive no statement or proof credit. A bounded exact-topic search found no fast
multipole, multipole, Greengard, or Rokhlin declaration in pinned mathlib or repository-local Lean.
This is limited discovery evidence, not the downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1459` | 0 | rank 1136; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped `jq` assertions over the manifest, execution DAG, and `instance.json` | 0 | rank and dependency agree; intake is `[_]`; statement is `[ ]`; claim and target fields are null; root is H5/M4/R4 |
| `git blame -L 10651,10656 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-1459/check_intake.py` | 1 | historical intake replay expects authoritative intake state `[ ]`; integration now records `[_]`; this known stale-intake failure is not statement evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and `git status --short` | 0 | pinned revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1459/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; stdout digest recorded above; no target theorem |
| bounded exact-topic `rg` search in pinned mathlib and repository-local Lean | 1 | expected no-match; no source-identical terminal declaration; discovery only |
| prohibited-declaration scan over owned Lean files | 1 | expected no-match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1459/statement-blocker.json` | 0 | finalized blocker is valid JSON |
| scoped blocker invariant check | 0 | identity, null target/import/fingerprints, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, and no-self-test boundary agree |
| owned-file inventory and `git status --short --untracked-files=all` | 0 | exactly nine historical intake files plus two blocker files; only `.lake` and the two blocker files are untracked |
| scoped whitespace checks | 0 | no whitespace diagnostics in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must first accept fresh intake evidence. Accountable reviewers must then
preserve an immutable source, independently approve one exact FMM proposition, map its definitions,
assumptions, proof boundary, corrections, and errata, and freeze every task, dimension, kernel,
particle-data, collision, hierarchy, separation, expansion, translation, accuracy, cost, arithmetic,
binder, conclusion, and boundary choice.

A later statement run can encode only that approved proposition, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four mutation classes.

This blocker is the assigned phase's truthful result, not completion of this node or a downstream
node. No statement receipt, root worker self-test packet, worker `[_]`, proof credit, anchor audit,
audit completion, theorem completion, or master acceptance is claimed.
