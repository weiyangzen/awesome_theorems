# THM-M-1478 exact-statement gate: blocked

Item: `S56-M-1478-STATEMENT`

Base revision: `2b649e7f3c2c6e3617cfb58c680e29f34d2ca5d7` (tree
`c9dfabc312a58c05c89917f6d7298a8e140356fc`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1478-INTAKE` is only provisional worker
state `[_]`: `intake-receipt.json` is unaccepted and non-content-addressed, has no accepted receipt
IDs, and binds the older repository revision `fc0de001c634823043636f9380a991c027e42533` and older
blueprint and execution-DAG hashes. There is no master-accepted dependency receipt. Section 10.2 of
the rev-5.6 blueprint permits preparation of later provisional evidence, but master closure remains
dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete repository record
is the title `L-稳定性`, the collective attribution `众多数学家`, the period `20世纪`, and the generic
gloss `数值方法的稳定性`: stability of numerical methods. It supplies no claim kind, method or
problem class, method coefficients, stability object, stability-function construction or domain,
pole or implicit-stage-solvability policy, A-stability component, limiting filter or path, decay
predicate, logical direction, ordered binders, hypotheses, conclusion, constants, or boundary
cases. Stage0 explicitly leaves exact definitions and premises, the proof route, dependencies,
alternate statements, axiom policy, formal system, machine status, and artifacts open.

Materially inequivalent propositions fit the label: a definition for scalar stability functions, a
characterization of a method family, a proof that one named method is L-stable, a parameter-range
theorem, or an existence, order, or impossibility result. Even the familiar slogan "A-stable and
decays at infinity" leaves source-dependent choices about method scope, poles, stage solvability,
left-half-plane boundaries, and whether decay is negative-real, sectorial, left-half-plane, or
complex-cocompact. Selecting any one would invent, narrow, broaden, or substitute
proposition-changing mathematics. It could also collide with the separately owned Runge-Kutta,
stiff-stability, A-stability, stiff-equation, or BDF targets.

Hairer and Wanner's *Solving Ordinary Differential Equations II* is a useful source-family lead,
and its correction sheet confirms that exact method and parameter choices matter. The catalog does
not cite it, however. Intake admitted no immutable full source, exact proposition or incorporated
definition chain, premise and conclusion mapping, proof boundary, correction impact,
source-to-root selection, or independent review. Consequently there is no canonical expression to
elaborate and no honest minimal-import claim. The canonical expression and environment
fingerprints, checked alternate transports, and required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined, not passed.

No `Statement.lean`, theorem declaration, proof body, weakened special case, or broadened interface
was added. The root remains `[H5, M4, R4]`; `H5` classifies the received topic gloss as not yet a
stable proposition and does not refute correctly stated L-stability definitions or theorems.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its four direct
imports expose generic complex limits, reduced rational-function evaluation, finite matrices, and
exact ODE trajectories. All sixteen checks elaborated, and the three representative axiom reports
contained only `propext`, `Classical.choice`, and `Quot.sound`.

Those declarations define no numerical method, stability function, A-stability predicate, decay
predicate, or L-stability theorem. Their imports cannot be certified minimal for an absent target
and receive no statement or proof credit. In particular, the complex cocompact filter is not
definitionally a negative-real or left-half-plane path, and totalized `RatFunc.eval` returns zero
when its reduced denominator evaluates to zero; neither behavior may silently choose the source's
limit or implicit-stage-solvability policy.

A bounded exact-topic search over selected repo-local and pinned-mathlib roots located no
source-selected numerical L-stability declaration. This is narrow statement-feasibility evidence,
not the downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1478` | 0 | rank 1155; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 10784,10789 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| authority, source, intake, probe, toolchain, lockfile, and relevant mathlib `sha256sum` checks | 0 | exact current hashes are preserved in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1478/IntakeProbe.lean` | 0 | sixteen adjacent APIs elaborated; stdout SHA-256 `b666076db0ff86f8f2f4f5d7fed24ead6c3e9742cbfa2e96150b879cf7598456`; no target declaration |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 1, expected no match | empty output; no source-selected numerical L-stability declaration was located |
| `python3 -B Stage1_Instances/THM-M-1478/check_intake.py` | 1 | its historical exact-row assertion freezes intake as `[ ]`, attempt 0, while current authority records `[_]`, attempt 1; this phase records rather than rewrites stale intake evidence |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1478` | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, scoped-change, dependency-status, and absent-self-test checks are
recorded in the structured blocker beside this report.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then lawfully preserve one immutable primary or approved authoritative source and independently
select one exact numbered proposition or explicitly sourced conjunction. They must map every
incorporated definition, assumption, proof boundary, correction, and erratum, and freeze the claim
kind, method and problem classes, stability object, function and stage-solvability domains, pole
policy, A-stability component, decay filter or path, hypotheses, ordered binders, conclusion,
constants, arithmetic boundary, neighboring-target boundaries, alternate encodings, and every
degenerate case.

A fresh statement worker may then encode precisely that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
