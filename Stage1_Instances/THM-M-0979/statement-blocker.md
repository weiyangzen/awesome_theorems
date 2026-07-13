# Exact-statement gate: blocked

Item: `S56-M-0979-STATEMENT`

Theorem: `THM-M-0979`

Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b` (tree
`64c5aacf7cf3eb79008f5a1970151e3e53cb9966`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0979-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Its receipt is non-content-addressed, declares
`accepted: false`, has no accepted receipt ID, and deliberately leaves the canonical human claim
and Lean target null. Rev-5.6 permits preparation of this blocker, but an eventual statement
transition remains dependency ordered.

Independently, the exact-statement gate cannot pass. The complete catalog record supplies only the
title "Bernstein inequality," Sergei Bernstein, 1924, and the gloss "tail probability of a sum."
It gives no cited work or passage, formula, summand model, dependence assumptions, ordered binders,
hypotheses, constants, conclusion, proof boundary, corrections, reviewer, or boundary conventions.
Its `verified` label is untrusted metadata under rev-5.6.

The proposition-changing choices include:

- bounded, subexponential, moment-controlled, martingale, vector, or matrix summands;
- a finite range or arbitrary finite index, scalar domain, common measure, measurability, and
  integrability conventions;
- independence or another dependence model, centering, almost-sure bounds, and common versus
  summand-specific bounds;
- exact variance sum, a variance budget, conditional variance, second moments, or another proxy;
- upper, lower, or two-sided tails, strictness of the event, and the threshold range; and
- the leading prefactor, exponent constants, denominator normalization, binder order, and every
  empty, zero-threshold, zero-bound, zero-variance, and totalized-zero-denominator case.

The source corpus also has a duplicate-looking translated-title row retained as the separately
owned `THM-M-0995`. Matching catalog metadata does not authorize merging the IDs or transferring
that target's statement and evidence. Its candidate is a one-sided bounded-summand form with
leading prefactor `1`; the modern Vershynin source lead inspected at intake displays prefactor `2`
for its bounded variance-sensitive theorem and also contains distinct subexponential and weighted
forms. The historical 1924 source was not inspected or admitted. Selecting either candidate would
therefore invent a source and scope decision rather than elaborate the received target.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard
blockers. There is no canonical expression whose imports can be certified minimal, no credited
alternate encoding, and no target against which removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutations can be assessed. Those four mutation classes are
undefined, not passed. The root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated in the pinned environment. Its
two imports expose MGF, Chernoff, sub-Gaussian-sum, independence, and variance interfaces. The
probe also elaborates `CandidateBoundedUpperTailShape` with an explicit unresolved `prefactor` and
checks both `1` and `2`. This deliberately noncanonical proposition proves nothing, and its imports
are not a minimal-import result for the absent target.

A bounded search over repository-local and pinned-mathlib Lean found the foreign `THM-M-0995`
candidate and adjacent or unrelated Bernstein APIs, but no separately named terminal scalar
Bernstein sum-tail theorem. This is discovery evidence only, not the downstream anchor audit or a
global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The probe output SHA-256 is
`caa6a4b8d61e829d1a406866b15dd86d0d9b216006bbd60382b951d32bae12e7`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or other
dependency mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0979` | 0 | rank 1513; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, blueprint, skill, duplicate, source-lead, and intake inspection | 0 | confirmed the family-only claim, duplicate ownership boundary, conflicting candidates, null canonical target, and open proposition choices |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0979/IntakeProbe.lean` | 0 | adjacent APIs and the prefactor-parameterized candidate elaborated; output hash recorded above; no canonical target or proof body |
| bounded Bernstein search in pinned mathlib and repository Lean | 0 | found adjacent, unrelated, legacy, and foreign-target surfaces; no separately named terminal scalar theorem was credited |
| `python3 -B Stage1_Instances/THM-M-0979/check_intake.py` | 1 | historical intake checker expects the pre-integration intake state `[ ]`; current authority records provisional `[_]`; historical evidence was not rewritten |
| scoped prohibited-construct scan over owned Lean | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0979/statement-blocker.json` and scoped invariant assertions | 0 | structured blocker identity, hashes, null target, unchanged vector, false completion flags, exact scope, and absent self-test agree |
| whitespace checks over both added blocker files | 0 | no whitespace diagnostics; `git diff --no-index --check` returned `1` only because each untracked file differs from `/dev/null` |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the statement phase did not pass |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must first master-accept fresh intake evidence. Accountable source and target
reviewers must then decide the `THM-M-0979`/`THM-M-0995` relationship, lawfully preserve and hash an
immutable primary or approved authoritative source, select and independently approve one exact
proposition, and crosswalk every incorporated definition, binder, premise, constant, conclusion,
proof boundary, translation, correction, erratum, and boundary case.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
