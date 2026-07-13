# Exact-statement gate: blocked

Item: `S56-M-0974-STATEMENT`

Theorem: `THM-M-0974`

Base revision: `48abbb2d2eeb89816c5ffc0ad8faafa4b9d24dd0` (tree
`0f26e2c78fb5fff9277cbbdfef5e145fd4ef06f1`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0974-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, is not
content-addressed, has no accepted receipt ID, and deliberately leaves the canonical mathematical
statement and formal target null. Dependency-ordered investigation is possible, but master
acceptance remains required before any eventual statement transition can be accepted.

Independently, the exact-statement gate cannot pass. The repository record supplies only the title
"Talagrand concentration inequality," Michel Talagrand, the year 1995, and the gloss
"concentration of convex Lipschitz functions." It gives no bibliography, displayed proposition,
definitions, ordered binders, hypotheses, constants, conclusion, proof boundary, corrections,
reviewer, or boundary conventions. The adjacent `verified` label is explicitly untrusted under
rev-5.6.

The intake inspected Talagrand's 1995 paper *Concentration of measure and isoperimetric
inequalities in product spaces*. Its introduction says that the Part I concentration results are
stated for sets and that it gives no abstract functional statement; Section 4.1 begins with a
convex-hull-distance inequality for sets. Later literature describes functional consequences while
jointly citing the 1995 paper and Talagrand's 1996 *A new look at independence*. No exact functional
theorem, source-reviewed derivation from the set theorem, or 1995/1996 relationship has been
selected and independently approved.

The remaining choices change the proposition: coordinate index and laws, product and independence
encoding, support bounds, ambient normed space, convexity domain, Lipschitz convention,
measurability, median or expectation center, one- or two-sided tail event, strictness, constants,
scaling, quantifier order, and degenerate cases. Choosing the uniform cube, bounded intervals, a
median-centered universal-constant result, or a remembered exact constant would invent or
substitute mathematics rather than elaborate the received target.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard
blockers. There is therefore no honest canonical expression whose imports can be certified
minimal, no credited alternate encoding for a checked transport, and no canonical target against
which the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations can run. Those mutation results are undefined, not passed. The root vector remains
`[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with four direct imports for convex functions,
Lipschitz maps, product measures, and sub-Gaussian moments. Six adjacent APIs check successfully.
The probe defines no probability model, Talagrand distance, functional concentration target,
transport, or proof body, so its imports cannot be certified minimal for an absent canonical
target. In particular, assuming `HasSubgaussianMGF` would store rather than prove the desired
concentration property.

A bounded exact-topic search over pinned mathlib and repository-local Lean found only the intake
disclaimer, an unrelated legacy Talagrand `T2` transportation interface, adjacent convex-Lipschitz
analysis APIs, and an unrelated Talagrand citation. It located no source-identical convex-Lipschitz
concentration target. This is discovery-only evidence, not the downstream immutable anchor audit or
a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or other
dependency mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0974` | 0 | rank 1508; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, blueprint, skill, and intake inspection | 0 | confirmed the sparse catalog claim, null canonical target, 1995 set-theorem versus later functional-source boundary, and open proposition-changing choices |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0974/IntakeProbe.lean` | 0 | six adjacent APIs elaborated; stdout SHA-256 `02f935b90ba94b004bab0ec8a73453a4f48034d0c97b26938b8145f07c9b7512`; empty stderr; no target or proof body |
| bounded search for Talagrand and convex-Lipschitz concentration declarations | 0 | only discovery disclaimers, unrelated `T2` infrastructure, adjacent APIs, and an unrelated citation matched; no source-identical target located |
| `python3 -B Stage1_Instances/THM-M-0974/check_intake.py` | 1 | historical intake checker rejects its frozen pre-integration DAG row because integration changed intake from `[ ]`/attempt 0 to `[_]`/attempt 1; it is stale evidence and was not rewritten |
| scoped prohibited-construct scan over owned Lean files | 0 | inner search returned expected no-match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured blocker
beside this report.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash one complete immutable primary or approved authoritative source, select
and independently approve one exact functional proposition or an explicit derivation from a
pinpoint set theorem, and map every incorporated definition, ordered binder, hypothesis,
conclusion, proof boundary, correction, erratum, and boundary case. They must resolve the 1995/1996
source relationship and freeze the coordinate laws, product model, support, norm, convexity and
Lipschitz predicates, measurability, center, tail event, constants, scaling, and degenerate cases.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
