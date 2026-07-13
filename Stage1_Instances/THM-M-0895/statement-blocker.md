# Exact-statement gate: blocked

Item: `S56-M-0895-STATEMENT`

Theorem: `THM-M-0895`

Base revision: `46a0f2a3ea74765a0467c489264b838ffbb70675` (tree
`7b1b5269d7da840fd086da731d6f92903c209c35`).

## Decision

The assigned statement item remains `[ ]`. Its prerequisite `S56-M-0895-INTAKE` has provisional
worker state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits preparation of a
later node, but dependency-ordered master acceptance is still required.

Independently, the exact-statement gate cannot pass. The complete catalog record supplies only the
title "strongly regular graphs," Raj Chandra Bose, the year 1963, and the plural gloss "parameter
constraints of strongly regular graphs." It does not select one truth-valued proposition. The
inspected 1963 Bose paper confirms that this is a real ambiguity: Section 2 gives equations
(2.1)-(2.5), while later sections contain distinct partial-geometry and integrality constraints.
The repository does not cite one of those results, delimit a conjunction, or provide an accepted
definition and assumption crosswalk, correction or errata disposition, and independent review.

Materially different conclusions fit the received gloss: the elementary scalar feasibility
equation, an adjacency-matrix identity, complement parameters, restricted-eigenvalue equations and
multiplicities, integrality or divisibility conditions, feasibility bounds, or specialized
partial-geometry relations. They have different hypotheses and boundaries. Selecting
`SimpleGraph.IsSRGWith.param_eq` merely because it is already available would reverse the required
source-to-formal direction and substitute missing mathematics.

The record also does not fix the finite graph model, parameter order, natural versus integer
arithmetic, nontriviality, positivity, connectedness, binder order, or the treatment of empty,
complete, and vacuous cases. Statement ambiguity and a missing elaborated-expression fingerprint
are hard blockers under rev-5.6 sections 5 and 5.1. Consequently there is no canonical target for
which minimal imports, checked alternate transports, or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can truthfully be certified. No statement,
theorem declaration, proof body, or substitute special case was added. The vector remains
`[H1, M3, R4]`.

## Source And Lean Boundary

The intake records the primary lead as Raj Chandra Bose, *Strongly regular graphs, partial
geometries and partially balanced designs*, *Pacific Journal of Mathematics* 13(2), 389-419
(1963), DOI `10.2140/pjm.1963.13.389`. The inspected publisher PDF has SHA-256
`2d73e39655a2f2b1ba3827e901a20fe40521fa0e4118db856b530451b37be614`. This identifies a source
family, not an accepted exact root, so the human status remains H1.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains
`Mathlib.Combinatorics.SimpleGraph.StronglyRegular`. The existing `IntakeProbe.lean` imports that
module and checks `IsSRGWith`, `param_eq`, `matrix_eq`, `compl`, and the empty and complete graph
interfaces. It elaborates under Lean 4.29.0. This is discovery-only substrate evidence. The import
cannot be declared minimal for an absent canonical target, and no candidate receives statement or
proof credit here.

The automation-provided `Formalizations/Lean/.lake` symlink was used read-only. No `lake update`,
`lake build`, dependency clone or fetch, or other dependency mutation was run.

## Validation Record

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0895` | 0 | rank 1444; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| exact manifest, blueprint, skill, catalog, Stage0, and intake-dossier reads | 0 | confirmed the assigned gate and the null, source-ambiguous canonical target |
| `git blame -L 6551,6556 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-0895/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]`; integration now records `[_]`; this statement run does not rewrite intake evidence |
| Lean/Lake version, mathlib revision/tree, and package-status checks | 0 | Lean 4.29.0 commit `98dc76e3...`; Lake 5.0.0; pinned mathlib revision/tree matched; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0895/IntakeProbe.lean` | 0 | ten adjacent strongly regular graph APIs elaborated; stdout SHA-256 `94e1c153b7c72776755d12346ffa6af6402b085cef84450356f5a15262bb68df` |
| bounded exact-topic `rg` over repository-local Lean and pinned mathlib | 0 | the pinned module and materially different candidates were found; no repo-local source-approved target was found |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition And Status Boundary

Accountable reviewers must preserve a lawful immutable source and independently approve one exact
proposition or explicit conjunction with pinpoint locator, incorporated definitions, proof
boundary, corrections, and errata. They must freeze the graph model, parameter order and origin,
arithmetic domain, ordered binders, every hypothesis and conclusion, nontriviality and positivity
conditions, and all empty, complete, vacuous, disconnected, and subtraction boundary cases.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes. The intake prerequisite must also be
master-accepted before an eventual statement transition can be accepted.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, `.stage1-worker-selftest.json` is intentionally absent.
