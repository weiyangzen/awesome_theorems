# Exact-statement gate: blocked

Item: `S56-M-0745-STATEMENT`

Theorem: `THM-M-0745`

Base revision: `be8701e88e791545c16a262edd1909486d5cef4b`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is the title "recursively enumerable sets" and the gloss "properties
of recursively enumerable sets." That wording names a topic family, not one truth-valued
proposition. Stage0 leaves the precise definitions, premises, proof route, dependencies, alternate
forms, axioms, machine state, and artifact links pending. The intake accordingly freezes
`canonical_statement`, `canonical_claim`, and the canonical Lean target as null.

Choosing a familiar result would invent or substitute mathematics. The gloss could refer to a
definition by partial-recursive domain, a range or semidecision characterization, a closure law,
the fact that a computable predicate is r.e., the r.e./co-r.e. characterization of decidability, a
halting example, or a completeness result. These claims have different carriers, models, binders,
hypotheses, conclusions, encoding assumptions, and boundary cases. Several nearby results also
belong to separately owned targets, including the halting problem, creative and simple sets,
Post's problem, c.e. degrees, and MRDP.

Section 5.1 of the rev-5.6 standard therefore fails before proof evidence may be inspected. There
is no canonical expression on which to establish minimal imports, compute an expression or target
environment fingerprint, compile alternate transports, or run meaningful removed-hypothesis,
changed-domain, binder-scope, and boundary mutations. The intake dependency is additionally only
provisional `[_]`, not master-accepted `[x]`. The root remains `[H5, M4, R4]`; statement acceptance,
audit completion, and theorem completion are false.

## Checked Lean boundary

The existing `IntakeProbe.lean` was re-elaborated against the pinned environment. Its sole direct
import, `Mathlib.Computability.Halting`, exposes `REPred`, partial-recursive domains, transports,
computable predicates, a decidability characterization, and halting examples. All eight checked
interfaces elaborate, with complete stdout SHA-256
`b746af8b19b99cb1e1df3b9e7388d23271f6dde108025046903cb59c74d9ccd9`.
Their materially different types confirm rather than resolve the missing property selection.

The probe is adjacent API evidence only. Its import cannot be certified minimal for an absent
canonical target, and it declares no theorem, checked transport, or proof body. The scoped Lean
scan found no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque declaration, or unsafe
declaration.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). The automation-provided canonical
`.lake` symlink and pinned mathlib package were used read-only. No `lake update`, `lake build`,
dependency clone/fetch, or package mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0745` | 0 | rank 1332, planned, legacy artifacts unaccepted, theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation `.lake` symlink was untracked; base revision and tree are recorded in the JSON blocker |
| scoped blueprint, skill, manifest, DAG, source, Stage0, and full intake inspection | 0 | only a topic gloss exists; the canonical claim, target, imports, binders, and fingerprints remain null |
| `git blame -L 5493,5498 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| current authority, source, intake, toolchain, lockfile, probe, and pinned-source SHA-256 checks | 0 | exact input digests are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0745/check_intake.py` | 1 | known historical replay failure: it expects intake `[ ]`/attempt 0 while current authority records provisional `[_]`/attempt 1 |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 at `98dc76e3...16740`; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` plus status | 0 | pinned mathlib `8a178386...e95`, tree `bdc39a31...e2b`, clean package worktree |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0745/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; no canonical target or proof body declared |
| bounded pinned-mathlib search for r.e. definitions and results | 0 | found several inequivalent interfaces and a topic-level bibliography lead; none is source-selected |
| scoped prohibited-construct scan over `Stage1_Instances/THM-M-0745/*.lean` | 1 | expected no-match result; no prohibited declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0745/statement-blocker.json` plus scoped blocker assertions | 0 | valid JSON; identity, current base, null target/imports, unchanged vector, four undefined mutations, false completion fields, exact two-file scope, and absent self-test agree |
| direct byte-hygiene assertions; tracked and added-file `git diff --check` checks | 0 | both blocker artifacts are newline-terminated and have no CR, NUL, trailing whitespace, or whitespace diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake validator freezes the intake-time DAG state and exact nine-file intake
inventory. It was not edited to manufacture agreement with the later authoritative state or these
statement artifacts.

## Retry condition

First, the integration lane must master-accept fresh intake evidence. An accountable source
reviewer must then preserve and hash one immutable primary or approved authoritative source,
select and transcribe one exact proposition, and independently approve every incorporated
definition, assumption, conclusion, proof boundary, correction, erratum, translation, and
boundary case. The selection must also freeze the computable-enumerability model, carrier,
universes, encodings, binder order, foundation and computation profiles, and neighbor scope.

Only then can a fresh statement run encode that exact claim, minimize its pinned imports,
serialize the elaborated expression and environment, compile checked transports, and execute all
four required mutation classes. This phase is blocked rather than complete, so no statement
receipt and no `.stage1-worker-selftest.json` are emitted.
