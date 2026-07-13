# THM-M-0231 rev-5.6 statement blocker

## Decision

`S56-M-0231-STATEMENT` remains `[ ]`. Its prerequisite `S56-M-0231-INTAKE` is
provisional worker state `[_]`, not master accepted; the intake receipt declares
`accepted: false`, is not content-addressed, and contains no accepted receipt ID. Rev-5.6 section
10.2 permits preparation of this later-node blocker while concurrency is enabled, but master closure
remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete catalog record is
the name `米塔格-勒夫勒定理`, attribution to Magnus Mittag-Leffler, year 1884, and the gloss
`亚纯函数的部分分式分解`: partial-fraction decomposition of meromorphic functions. It supplies no
source edition, theorem locator, formula, incorporated definition, ordered binder, hypothesis,
conclusion, proof boundary, correction history, or reviewer. Stage0 expressly leaves the precise
definitions and premises, formal system, proof route, dependencies, alternate forms, axiom policy,
machine status, and artifacts open. The catalog label `已验证` is untrusted metadata under rev-5.6
and supplies no source or kernel credit.

The gloss identifies a classical theorem family, not one binder-complete proposition. Materially
different roots fit it: existence of a meromorphic function realizing prescribed principal parts,
decomposition of a given meromorphic function into a corrected locally convergent partial-fraction
series plus a holomorphic function, and a whole-plane pole-sequence specialization. Selecting any
one from mathematical memory would invent or substitute proposition-changing choices. The
repository does not fix:

- the complex plane, a connected open subset, or another analytic domain;
- a sequence without finite accumulation points, a discrete set, or locally finite indexed data,
  including duplicate-center and boundary-accumulation policies;
- how finite principal parts, their orders and coefficients, and zero data are represented;
- whether local matching means a holomorphic difference, Laurent-coefficient equality, or another
  source-defined condition;
- the correction polynomials, summation order, and locally uniform convergence claim; or
- uniqueness modulo a holomorphic function, normalization, ordered binders, and degenerate cases.

These choices are not merely notation and are not definitionally interchangeable. Sections 5 and
5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated-expression
fingerprint hard blockers. There is therefore no canonical expression whose direct imports can
honestly be certified minimal, no credited alternate form for a checked transport, and no target
against which the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary
mutations can run. Those mutations are undefined, not passed. No `Statement.lean`, declaration,
proof body, assumed interface, weakened special case, or broadened theorem was added. The root
remains `[H1, M4, R3]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its three direct imports:

- `Mathlib.Analysis.Meromorphic.FactorizedRational`
- `Mathlib.Analysis.SpecialFunctions.Trigonometric.Cotangent`
- `Mathlib.CategoryTheory.CofilteredSystem`

Its ten checks authenticate pinned meromorphic predicates and divisors, finite-support factorized
rational functions, the concrete cotangent expansion, and the category-theory homonym. All checks
pass, but the probe deliberately defines no arbitrary principal-part data, canonical analytic
Mittag-Leffler target, checked transport, or proof body. The cotangent formula is a special case,
and `CategoryTheory.Functor.IsMittagLeffler` is an unrelated inverse-system condition. These imports
are discovery-only and cannot be certified minimal for an absent target.

A bounded exact-topic search over repository-local Lean and pinned mathlib found the cotangent
expansion, the category-theory homonym, unrelated uses of the phrase "principal part," and no
arbitrary analytic prescribed-principal-parts declaration under the recorded terms. This is narrow
statement-feasibility evidence, not the downstream anchor audit and not a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation
was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0231` | 0 | rank 1243; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision `c2e294becadae6ce784f27ee69f2e8dbf57e0b30`, tree `3f567e7f76b189432b73444354070c0ff75925b9` |
| `git blame -L 1668,1673 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| authority, source, intake, probe, toolchain, lockfile, and relevant mathlib `sha256sum` checks | 0 | exact current hashes are preserved in `statement-blocker.json`; historical intake evidence was not rewritten |
| `python3 -B Stage1_Instances/THM-M-0231/check_intake.py` | 1 | the historical intake-only checker expects its pre-integration `[ ]`, attempts-0 DAG row; current authority records provisional `[_]`, attempts 1, so replay fails at that frozen row before its original inventory check |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0231/IntakeProbe.lean` | 0 | ten adjacent APIs elaborated; stdout SHA-256 `26c136f8abf6d14c6bc02df15d6cdd8d728a3201257cb647cd137c00cbc5ca15`; empty stderr; no target declaration |
| bounded exact-topic `rg` over repository-local and pinned-mathlib Lean roots | 0 | only the special case, homonym, probe disclaimer, and unrelated phrase matches; output SHA-256 `7206782121ad7088d55ab030784a6a1f08f530e176aead4af258621da3f27dcd` |
| prohibited-declaration `rg` over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and scoped invariant checks for `statement-blocker.json` | 0 | identity, blocked open state, null target/imports, unchanged vector, four undefined mutations, false completion flags, and exact two-file scope agree |
| whitespace checks for both added blocker artifacts | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is immutable evidence for an earlier phase. Rewriting it, the intake
receipt, `instance.json`, or the target-local DAG would manufacture agreement rather than validate
this blocked statement attempt.

## Retry Condition

The integration lane must master-accept refreshed intake evidence before accepting a statement
transition. Accountable reviewers must lawfully preserve and hash an immutable primary or approved
authoritative source, select and independently approve one exact proposition, and map every
incorporated definition, ordered binder, hypothesis, conclusion, exceptional case, proof boundary,
correction, and erratum. They must freeze the analytic domain, pole indexing and local-finiteness
condition, principal-part encoding, theorem direction, local matching relation, correction and
convergence clauses, uniqueness and normalization boundary, alternate encodings, and every
degenerate case.

A fresh statement worker may then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
