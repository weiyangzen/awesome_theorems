# THM-M-0254 rev-5.6 statement blocker

## Decision

`S56-M-0254-STATEMENT` remains `[ ]`. Its prerequisite `S56-M-0254-INTAKE` is provisional worker
state `[_]`, not master-accepted state `[x]`; its receipt has `accepted: false`, is not
content-addressed, and has no accepted receipt ID. Rev-5.6 permits provisional preparation of a
later node, but master closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete catalog record is
the title `有界平均振动函数` (functions of bounded mean oscillation), the Fritz John/Louis
Nirenberg attribution, the year 1961, and the gloss `BMO函数的特征` (a characterization of BMO
functions). It gives no source edition, theorem or page locator, formula, incorporated definition,
domain, ordered binder, hypothesis, conclusion, constant, proof boundary, correction history, or
reviewer. Stage0 expressly leaves the precise definitions and premises, formal system, equivalent
forms, axiom policy, machine status, and artifacts open. The catalog label `已验证` is untrusted
metadata under rev-5.6 and supplies no source or kernel credit.

The gloss identifies a theorem family, not one binder-complete proposition. Materially different
roots fit it:

- membership in Euclidean BMO via uniformly finite mean absolute oscillation over cubes;
- the John-Nirenberg distribution inequality;
- local exponential integrability of centered BMO functions; and
- equivalence between `L^1` and `L^p` mean-oscillation seminorms.

The repository does not fix the Euclidean dimension or another carrier, real or complex values,
raw locally integrable functions or almost-everywhere classes, cubes or balls, the averaging basis,
the oscillation functional and exponent, real or extended-real bounds, constants, inequality
directions, or quotient convention. These choices change the proposition. Moreover,
`THM-M-0302` separately owns the John-Nirenberg inequality and the explicit gloss "exponential
integrability of BMO functions"; selecting that reading here would substitute or duplicate another
scheduled target without an integration-lane identity decision. `THM-M-0301` and `THM-M-0363`
separately own BMO-`H^1` duality and likewise supply no statement identity or proof credit.

Section 5 of the rev-5.6 blueprint makes statement ambiguity and a missing elaborated-expression
fingerprint hard blockers. There is therefore no canonical expression whose imports can honestly be
certified minimal, no credited alternate form for a checked transport, and no canonical target
against which the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary
mutations can run. Those mutations are undefined, not passed. No `Statement.lean`, declaration,
proof body, weakened special case, or broadened interface was added. The root remains
`[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its two direct imports:

- `Mathlib.MeasureTheory.Integral.Average`
- `Mathlib.MeasureTheory.Measure.Lebesgue.Basic`

It checks six adjacent set-average, centering, and Euclidean box-volume interfaces. All checks pass,
and representative axiom reports list only `propext`, `Classical.choice`, and `Quot.sound`, but the
probe deliberately defines no BMO predicate, canonical target, transport, or proof body. Its imports
are discovery-only and cannot be certified minimal for an absent target. A bounded exact-topic
search over repo-local Lean and pinned mathlib located no source-identical bounded-mean-oscillation
or John-Nirenberg declaration. This is narrow feasibility evidence, not the downstream anchor audit
and not a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation
was run.

## Validation Record

Commands ran from the isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0254` | 0 | rank 1264; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision `c2e294becadae6ce784f27ee69f2e8dbf57e0b30`, tree `3f567e7f76b189432b73444354070c0ff75925b9` |
| `git blame -L 1829,1834 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| authority, source, intake, probe, toolchain, lockfile, and relevant mathlib `sha256sum` checks | 0 | exact current hashes are preserved in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0254/check_intake.py` | 1 | the historical intake-only checker expects authoritative intake state `[ ]`; integration now records provisional `[_]`; this statement run records rather than rewrites the historical evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0254/IntakeProbe.lean` | 0 | six adjacent APIs and three axiom reports elaborated; no target declaration or proof body |
| bounded exact-topic `rg` over repo-local and pinned-mathlib Lean roots | 0 | only the intake disclaimer and an unrelated local variable named `Bmo` matched; no source-identical target declaration was located |
| prohibited-declaration `rg` over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0254/statement-blocker.json` and scoped `jq` assertions | 0 | valid JSON; identity, blocked state, null target/imports, unchanged vector, four undefined mutations, false completion flags, and exact two-file scope agree |
| `git diff --check -- Stage1_Instances/THM-M-0254` plus per-file no-index checks | 0; 1 expected difference | no whitespace diagnostics in the tracked scope or either new blocker file |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then lawfully preserve and hash one immutable primary or approved authoritative source, select and
independently approve one exact proposition, map every incorporated definition, ordered binder,
hypothesis, conclusion, constant, exceptional case, proof boundary, correction, and erratum, and
reconcile the identity boundary with `THM-M-0302`. They must freeze the domain and dimension,
function and almost-everywhere model, cube or ball basis, averaging and oscillation conventions,
bound and constant quantifiers, alternate encodings, and every degenerate case.

A fresh statement worker may then encode only that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
