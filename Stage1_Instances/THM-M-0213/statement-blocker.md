# Exact-statement gate: blocked

Item: `S56-M-0213-STATEMENT`

Theorem: `THM-M-0213`

Base revision: `940588d30669014430d5a1beb187f2bca118e816` (tree
`42d80725ccbabcdd826ed2bc8b3622ac31ac7695`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository record. The statement
item remains `[ ]`. Its prerequisite intake is provisional worker state `[_]`, not master-accepted
state `[x]`; the intake receipt declares `accepted: false`, is not content-addressed, has no
accepted receipt ID, and deliberately leaves the canonical mathematical statement, Lean module,
expression, expression hash, and environment-expression fingerprint null.

The complete catalog wording is only the title `双曲平行公设` (hyperbolic parallel postulate), the
Lobachevsky/Bolyai attribution, the year 1830, and the gloss `过直线外一点可作无数条平行线`
("through a point outside a line, infinitely many parallel lines can be drawn"). It supplies no
bibliography, axiom system, incorporated definitions, ordered binders, hypotheses, conclusion,
proof boundary, correction history, or boundary policy. Its `已验证` label is untrusted inventory
metadata under rev-5.6.

The wording does not choose among proposition-changing decisions, including:

- a synthetic neutral or hyperbolic incidence geometry versus the Klein, Poincare disk,
  Poincare upper-half-plane, or another analytic model;
- primitive lines versus complete geodesic images, with the required incidence, equality or
  quotient, nondegeneracy, and ideal-boundary conventions;
- parallel as finite-point disjointness, limiting or asymptotic parallelism, ultraparallelism, or
  a source-defined union of those relations;
- `Set.Infinite`, a natural-number injection, arbitrarily large finite families, or a stronger
  cardinality assertion for distinct through-lines;
- an axiom stored in a synthetic geometry, a result derived from another axiom system, or a theorem
  proved inside one selected model; and
- whether the root is the literal infinite-family claim, existence of at least two parallels, two
  limiting parallels plus an intervening fan, or a classification theorem.

These choices change the domain, assumptions, logical role, and conclusion. Existence of two
parallels is not definitionally the catalog's literal infinitude claim, while counting parameters
without extensional line equality can count duplicate representations. Selecting any familiar
formulation would therefore invent, narrow, broaden, or substitute mathematics rather than
elaborate the exact received target.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression fingerprint
hard blockers. With no canonical proposition, there is no honest import set to minimize, no target
or environment-expression fingerprint, no credited alternate transport, and no meaningful
removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation. Those outputs
are undefined, not passed. The root vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with these direct imports:

```lean
import Mathlib.Analysis.Complex.UpperHalfPlane.Metric
import Mathlib.Data.Set.Finite.Basic
import Mathlib.LinearAlgebra.AffineSpace.AffineMap
```

Its eight adjacent API checks pass. Pinned mathlib supplies an upper-half-plane carrier and metric,
a vertical-line isometry, generic affine `lineMap`, and set-infinitude interfaces. These APIs do
not define the source-selected hyperbolic lines, incidence, externality, parallel relation, line
identity, or candidate set. `AffineMap.lineMap` is ordinary affine interpolation, not a hyperbolic
geodesic. Consequently the probe's imports cannot be certified minimal for an absent canonical
target and receive no statement or proof credit.

A bounded exact-topic search of pinned mathlib, repo-local Lean, and the owned probe found no
hyperbolic-parallel-postulate declaration. This is discovery-only feasibility evidence, not the
downstream immutable anchor audit and not a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0213` | 0 | rank 1228; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 1536,1541 -- Docs/researches/math_theorems.md` and source/dossier inspection | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; no other authoritative input selects an exact proposition |
| `sha256sum` over authority, source, intake, toolchain, probe, and pinned mathlib inputs | 0 | exact current fingerprints are recorded in `statement-blocker.json`; historical intake evidence was not rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0213/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `b9a55cac40cde7375da298ebf9b21333c44857980e8d1a94068762ac05d87587`; no canonical target or proof body was declared |
| bounded exact-topic `rg` over pinned mathlib, repo-local Lean, and the owned probe | 1 | expected no-match result; no hyperbolic-parallel-postulate occurrence found; discovery-only search |
| `python3 -B Stage1_Instances/THM-M-0213/check_intake.py` before blocker creation | 0 | integrated intake identity, source and pin invariants, null target, `[H5,M4,R4]` boundary, and six open tasks passed |
| prohibited-construct `rg` over owned Lean files | 1 | expected no-match result: no `sorry`, `admit`, `sorryAx`, bodyless declaration, `opaque`, or `unsafe` construct |
| `python3 -m json.tool Stage1_Instances/THM-M-0213/statement-blocker.json` plus scoped blocker invariant checks | 0 | valid JSON; item identity, provisional dependency, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact change scope, and no-self-test boundary agree |
| scoped tracked and no-index whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker freezes the original nine-file intake inventory. After the two
statement-blocker files are added it is intentionally not a statement-phase validator; this run
does not rewrite the earlier checker or receipt.

## Retry Condition

The integration lane must master-accept the prerequisite before accepting a later statement
transition. Accountable source reviewers must preserve and hash one lawful immutable primary or
authoritative source; select and independently approve its exact proposition, axiom system or
model, line and incidence definitions, externality premise, parallel vocabulary, extensional line
identity, infinitude encoding, logical role, ordered binders, hypotheses, conclusion, proof
boundary, corrections, and exceptional cases; and reconcile the separately cataloged hyperbolic
model targets.

A fresh statement run can then encode precisely that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change, node receipt, worker `[_]`, or master acceptance
is claimed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json` is emitted.
