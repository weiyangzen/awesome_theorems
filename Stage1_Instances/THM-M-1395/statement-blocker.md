# THM-M-1395 statement-phase blocker

- Item: `S56-M-1395-STATEMENT`
- Base revision: `9890b8ae7278d1978497acce2be86f8fc4072af3`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt or theorem-completion claim

## First failed gate

The exact-source-statement and root-selection gate in sections 5 and 5.1 of
`Docs/Stage1_Blueprint_rev-5.6.md` fails because the received target is not a truth-valued
proposition. The workflow dependency is also not accepted: `S56-M-1395-INTAKE` is provisional
`[_]`, not master-accepted `[x]`. Section 10.2 permits preparation of later provisional work, so the
dependency does not replace the substantive statement diagnosis; it independently prevents master
closure.

The repository supplies only the title "finite difference method" and the gloss "a numerical
method for ODEs." It gives no initial- or boundary-value problem, state space, time domain, vector
field or data, exact-solution notion, grid, step policy, stencil or recurrence, discrete-solution
predicate, hypotheses, or conclusion. The Stage0 projection explicitly leaves precise definitions,
premises, proof route, dependencies, equivalent forms, axioms, and machine artifacts open.

Those omissions are proposition-changing. A derivative consistency estimate, Euler local or global
error bound, zero- or absolute-stability result, convergence theorem, or boundary-value scheme
solvability theorem are different roots. Selecting one familiar result would invent or substitute
mathematics. The same-name PDE scope belongs to `THM-M-1465`; shooting, Runge-Kutta, Adams, stiff
equations, and backward differentiation also have separate target ownership.

Consequently there is no canonical expression to elaborate and no honest minimal-import claim.
Expression and canonical-target environment fingerprints, checked transports, and the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not passed. The vector remains `[H5, M4, R4]`: `H5` classifies the supplied family label as unstable,
not a correctly stated finite-difference theorem as false.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its three direct
imports expose the algebraic `fwdDiff` operator and Newton identities, exact ODE integral-curve
predicates, and a generic Taylor remainder estimate. All eight checks passed. These APIs define no
numerical ODE scheme or discrete solution and prove no consistency, stability, convergence,
solvability, or scheme-specific error theorem. Their imports therefore cannot be certified minimal
for an absent target and receive no statement or proof credit.

A bounded repository-local and pinned-mathlib search found no finite-difference ODE scheme,
Euler-method convergence or error theorem, or target-specific numerical ODE declaration under the
recorded terms. This is feasibility evidence only, not the downstream anchor audit or a claim of
global absence.

The environment was Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink
and artifacts were used read-only. No update, build, clone, fetch, or dependency mutation was run.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1395` | 0 | rank 1005; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision/tree are recorded above and in the JSON blocker |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned mathlib revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1395/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `0a8fbc5b...bd9f`; no target or proof body declared |
| exact bounded target-pattern `rg` argv serialized in `statement-blocker.json` over repo-local Lean and pinned mathlib | 1 | expected no-match result under the documented finite-difference ODE, numerical ODE, Euler convergence/error, and difference-scheme terms |
| `python3 -B Stage1_Instances/THM-M-1395/check_intake.py` | 1 | historical intake checker expects intake state `[ ]`; the integrated authority now records provisional `[_]`; its nine-file inventory is also historical after this phase |
| exact prohibited-declaration `rg` argv serialized in `statement-blocker.json` over owned Lean files | 1 | expected no-match result; no prohibited declaration or proof escape occurs in the probe |
| `python3 -m json.tool Stage1_Instances/THM-M-1395/statement-blocker.json` and scoped blocker invariants | 0 | structured blocker parses and its identity, null target, unchanged vector, four undefined mutations, false completion fields, and no-self-test boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-1395` plus the two exact per-added-file no-index argv records in `statement-blocker.json` | 0 / expected 1 | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test manifest intentionally absent because the statement completion gate failed |

The intake checker is historical evidence and freezes its original authority state and exact intake
inventory. This statement attempt records the limitation rather than rewriting the intake checker,
intake receipt, instance, task DAG, generated blueprint, or authoritative execution DAG to
manufacture agreement.

## Retry condition and status boundary

Accountable reviewers must preserve and hash one lawful immutable primary or authoritative source,
select and independently approve one exact theorem or explicitly sourced conjunction, and freeze
every incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
and boundary case. The decision must fix the ODE problem, state and solution model, grid and
recurrence, arithmetic, regularity and well-posedness assumptions, conclusion, norm, constants,
quantifier dependencies, and the `THM-M-1465` and neighboring-method boundaries.

A fresh statement run can then encode precisely that claim, minimize its pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and execute
all four mutation classes. The integration lane must also master-accept the intake dependency
before accepting any resulting statement transition. Until then, the statement node remains open.
No exact statement, proof, audit completion, theorem completion, worker `[_]`, or master acceptance
is claimed. Because this phase is not genuinely self-tested complete, no
`.stage1-worker-selftest.json` is emitted.
