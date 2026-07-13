# Exact-statement gate: blocked

Item: `S56-M-0306-STATEMENT`

Theorem: `THM-M-0306`

Base revision: `464759128569180ab640c412cd80bc5dd2c3b44a` (tree
`8da3c9130640d08d4e179450a0418368d0454745`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete mathematical wording is only the title `弗里德里希斯不等式` (Friedrichs inequality)
and the gloss `紧支集Sobolev函数的估计` ("an estimate for compactly supported Sobolev
functions"), attributed to Kurt Friedrichs and dated 1929. The record supplies no formula,
bibliography, incorporated definitions, assumptions, conclusion, proof boundary, correction
history, or reviewer. Its `已验证` label is explicitly untrusted under rev-5.6 and gives no source
or machine credit.

An exact proposition would have to resolve at least:

- the ambient Euclidean space, bounded domain, manifold, or other setting, its dimension, measure,
  regularity, boundary, and local, closure, domain, or whole-space scope;
- smooth, continuously differentiable, weak Sobolev, zero-trace Sobolev, or another function model,
  plus scalar field, codomain, universes, representatives, and typeclasses;
- all exponent parameters and endpoints, compact support versus bounded support versus zero trace,
  and any density or trace convention;
- the derivative or gradient, both norm operands, inequality direction, constant value or
  existence, and every constant dependency;
- ordered binders, every hypothesis, one exact conclusion, alternate encodings, and foundation and
  trusted-computing-base profiles; and
- empty, null, zero-dimensional, endpoint, unbounded, irregular, disconnected, zero-function,
  zero-gradient, infinite-norm, and unavailable-trace cases.

These choices change the proposition rather than merely its notation. Selecting a familiar
compact-support smooth estimate, a zero-trace `W_0^{1,p}` domain theorem, a boundary-term norm
equivalence, or a Poincare inequality would invent or substitute mathematics.

The source and target identity are also unresolved. The inspected *Encyclopedia of Mathematics*
revision 46991 states a modern boundary-term family on a bounded locally Lipschitz domain. Its
historical reference is Friedrichs's gravitation article, *Eine invariante Formulierung des
Newtonschen Gravitationsgesetzes und des Grenzueberganges vom Einsteinschen zum Newtonschen
Gesetz*, DOI `10.1007/BF01451608`, whose metadata date it to 1928 rather than 1929. The inspected
scan does not visibly identify the requested compact-support Sobolev proposition. This conflict
does not authorize selecting either formulation.

A distinct manifested target, `THM-M-1240`, repeats the same attribution, year, and gloss. No
accepted decision makes the targets aliases, chooses distinct variants, deduplicates them, or
assigns terminal statement and proof ownership. The neighboring Poincare, trace, and extension
targets cannot replace this root either.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. There is consequently no canonical expression whose imports can be
certified minimal, no checked alternate transport, and no meaningful removed-hypothesis,
changed-domain, changed-binder-scope, or boundary-case mutation. Those mutations are undefined, not
passed. No `Statement.lean`, statement receipt, theorem declaration, or proof body was added. The
lifecycle stays `planned` and the provisional root vector stays `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. It directly imports:

```lean
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
```

It checks `MeasureTheory.eLpNorm`, `fderiv`, `HasCompactSupport`, and four smooth compact-support or
bounded-support Gagliardo-Nirenberg-Sobolev inequalities. These APIs do not select a source-specific
Sobolev model, support or trace convention, exponents, constants, or conclusion. The probe import
therefore cannot be certified minimal for the absent canonical target. Its complete stdout is 2,921
bytes with SHA-256
`e2b66eb5552365ecc3f112e19b4c205f0c3c2b4ddb3b57d8a368e1912e4cde7a`.

A bounded case-insensitive search for Friedrichs names in pinned mathlib and repository-local Lean
returned no matches. This is narrow discovery evidence only, not the downstream immutable anchor
audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was used read-only, and the pinned mathlib worktree remained
clean. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation ran.

## Validation Record

Commands ran in this isolated automation clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0306` | 0 | rank 1307; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `sha256sum Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Blueprint_rev-5.6.md Docs/Stage1_Execution_DAG_rev-5.6.json skills/execute-stage1-rev56/SKILL.md Docs/Blueprint_Guidelines.md Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` plus the nine intake artifacts, toolchain, lockfile, and pinned Sobolev source listed in `statement-blocker.json` | 0 | every recorded fingerprint agrees; scoped inspection fixes only an underspecified family, chronology and citation conflict, duplicate boundary, and null canonical target |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0306/IntakeProbe.lean` | 0 | seven adjacent interfaces elaborated; output size and hash recorded above; no canonical target or proof body |
| bounded exact-topic `rg` over pinned mathlib and repository-local Lean | 1 (expected no match) | no Friedrichs occurrence; discovery only |
| `python3 -B Stage1_Instances/THM-M-0306/check_intake.py` | 1 | historical intake replay stops at line 144 because it freezes intake authority state `[ ]` while the integrated authoritative DAG records `[_]`; it was not modified or represented as statement validation |
| prohibited-declaration `rg` scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0306/statement-blocker.json`; exact `jq -e` expression recorded in `commands_and_results` | 0 each | structured blocker parses and its identity, null target and imports, unchanged vector, four undefined mutations, false completion fields, exact two-file scope, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-0306 .stage1-worker-selftest.json` | 0 | no scoped tracked whitespace diagnostics |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0306/statement-blocker.json` | 1 (expected new-file difference) | no whitespace diagnostics |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0306/statement-blocker.md` | 1 (expected new-file difference) | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | root self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is bound to its intake worker's earlier cursor. Integration later
recorded intake `[_]`. Rewriting historical intake evidence is outside this phase and would not
cure the missing proposition.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence; resolve the source chronology
and encyclopedia-citation conflict; and reconcile `THM-M-0306` versus `THM-M-1240` identity,
variant, deduplication, and proof ownership. Accountable reviewers must preserve and hash a lawful
immutable primary or authoritative source, select one exact truth-valued proposition, map every
incorporated definition and assumption, freeze every domain, dimension, function model, exponent,
endpoint, support or trace, derivative, norm, constant, binder, and boundary-case choice, audit the
proof boundary, corrections, and errata, and independently approve the mapping.

A later statement worker can then encode precisely that approved claim, minimize pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport, and
run all four required mutation classes.

This records the first failed gate. It does not complete the statement node or any downstream node.
`audit_complete` and `theorem_complete` remain false, and no debt-vector change is proposed. Because
the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, node-specific
completion receipt, worker `[_]`, proof credit, or master acceptance is claimed.
