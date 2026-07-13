# THM-M-0251 rev-5.6 statement blocker

## Decision

`S56-M-0251-STATEMENT` remains `[ ]`. Its prerequisite `S56-M-0251-INTAKE` is provisional worker
state `[_]`, not master-accepted state `[x]`; its receipt has `accepted: false`, is not
content-addressed, and contains no accepted receipt ID. Rev-5.6 permits preparation of a later-node
blocker under explicit concurrency, but master closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete repository record
provides the title "inner-outer factorization," attribution to Arne Beurling, the year 1949, and
only the phrase "inner-outer factorization of Hardy spaces." It gives no source edition, theorem
locator, verbatim proposition, incorporated definition, ordered binder, hypothesis, conclusion,
proof boundary, correction history, or reviewer. Stage0 expressly leaves the precise definitions
and premises, formal system, alternate forms, axiom policy, machine status, and artifacts open. The
catalog label `verified` is untrusted metadata under rev-5.6 and supplies no source or kernel credit.

The phrase names a family of classical results rather than one binder-complete proposition. A
familiar orientation is that a nonzero `H^p` function on the unit disk factors as an inner function
times an outer function, perhaps uniquely up to a unimodular constant. That sentence is not a
source-selected target. The repository does not fix:

- the Hardy class, exponent, endpoint range, scalar field, and analytic domain;
- analytic functions versus radial or nontangential boundary representatives, the boundary measure,
  and pointwise versus almost-everywhere equality;
- the definitions of inner and outer, including integral-representation versus cyclicity variants;
- a single inner factor versus explicit Blaschke, singular-inner, and outer components;
- the nonzero premise, zero case, factor normalization, uniqueness relation, ordered binders,
  hypotheses, exact conclusion, and all boundary cases.

Beurling's 1949 paper *On two problems concerning linear transformations in Hilbert space* is only
an intake bibliographic candidate matching the catalog author and year. The catalog does not cite
it, and no lawful immutable primary copy, pinpoint proposition, definition map, correction audit, or
independent review was admitted. The attribution may refer to or conflate individual-function
factorization with related invariant-subspace theory. Selecting either family, or choosing a
standard modern variant from mathematical memory, would invent or substitute proposition-changing
mathematics.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. There is therefore no canonical expression whose imports can
honestly be certified minimal, no alternate expression eligible for a checked transport, and no
canonical target against which the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can run. Those mutations are undefined, not
passed. No `Statement.lean`, declaration, proof body, weakened special case, or broadened interface
was added. The provisional dossier vector remains `[H5, M4, R4]`; `H5` classifies the received
result-family label, not the standard mathematics or any future corrected target.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its three direct imports:

- `Mathlib.Analysis.Complex.CanonicalDecomposition`
- `Mathlib.Analysis.Complex.UnitDisc.Basic`
- `Mathlib.MeasureTheory.Function.LpSpace.Basic`

It checks eight adjacent unit-disk, analyticity, generic `Lp`, and canonical-factor interfaces. All
checks pass, but the probe deliberately defines no Hardy space, boundary convention, inner or outer
predicate, factorization target, transport, or proof body. Its imports are discovery-only and
cannot be certified minimal for an absent target. The pinned canonical-decomposition module itself
contains `TODO: Formulate the canonical decomposition.` A bounded exact-topic search over
repo-local Lean and pinned mathlib found no Hardy-space inner-outer declaration under the recorded
terms. A broader phrase search found the canonical-decomposition module and one unrelated use of
"inner function" and "outer function." This is narrow feasibility evidence, not the downstream
immutable anchor audit and not a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation
was run.

## Validation Record

Commands ran from the isolated worker clone on 2026-07-13 (`Asia/Shanghai`). Base revision:
`d257e1e5e5fa003d6e1f26344c0331bf99374fa9`; tree:
`fa06b50b528e038d182d5479a18296f63fa5eae5`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0251` | 0 | rank 1261; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| repository source, Stage0, manifest, blueprint, DAG, skill, guidelines, and intake-dossier inspection | 0 | the source is a result-family phrase; intake leaves the proposition and formal target null; the statement node depends on provisional intake |
| `git blame -L 1808,1813 -- Docs/researches/math_theorems.md` and scoped hashes | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; exact current hashes are in `statement-blocker.json` |
| pre-artifact `python3 -B Stage1_Instances/THM-M-0251/check_intake.py` | 0 | the historical intake invariants replayed successfully before statement artifacts were added |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0251/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `0d8ce274c32f2602642048df11b5ad21945afc33c247d19c939f51be51c08bba`; empty stderr; no target declaration |
| bounded exact-topic `rg` over repo-local and pinned-mathlib Lean roots | 1, expected no match | no Hardy-space inner-outer declaration under the recorded terms; bounded discovery evidence only |
| broader canonical/Blaschke/inner-function phrase `rg` | 0 | found the canonical-decomposition source and one unrelated inner/outer variable comment; the module explicitly leaves decomposition formulation as a TODO |
| prohibited-declaration `rg` over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| post-artifact `python3 -B Stage1_Instances/THM-M-0251/check_intake.py` | 1, expected historical limitation | the intake-only checker rejected the two blocker files because it freezes the original nine-file inventory; historical evidence was not rewritten |
| `python3 -m json.tool Stage1_Instances/THM-M-0251/statement-blocker.json` and scoped assertions | 0 | valid JSON; identity, blocked state, null target/imports, unchanged vector, four undefined mutations, false completion flags, and exact two-file scope agree |
| final standard, manifest, and target-show replays | 0 each | authority projections still pass; target remains planned, uniform `L0/rework_required`, and theorem-incomplete |
| scoped `git diff --check` and per-new-file `git diff --no-index --check` | 0; 1 expected difference | no whitespace diagnostics; no-index exit 1 is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker freezes its original nine-file intake inventory. Adding these two
statement blocker artifacts necessarily makes its post-artifact inventory check inapplicable.
Rewriting that checker or its receipt would alter historical intake evidence, so this statement run
records rather than edits that limitation.

## Retry Condition

The integration lane must master-accept the intake before accepting a statement transition.
Accountable reviewers must preserve and hash a lawful immutable primary or approved authoritative
source, select and independently approve one exact proposition, and map every incorporated
definition, ordered binder, hypothesis, conclusion, exceptional case, proof boundary, correction,
and erratum. They must reconcile the Beurling/1949 attribution and freeze the Hardy class and
exponent, domain, boundary convention, inner and outer definitions, factor components, nonzero and
zero cases, equality, normalization, uniqueness, alternate encodings, and all degenerate cases.

A fresh statement worker may then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
