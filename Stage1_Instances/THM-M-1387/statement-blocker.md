# THM-M-1387 statement-phase blocker

- Item: `S56-M-1387-STATEMENT`
- Base revision: `9890b8ae7278d1978497acce2be86f8fc4072af3`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt or theorem-completion claim

## First Failed Gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully entered from the frozen intake boundary. The repository catalog gives only the family
label `振荡理论` (oscillation theory), the collective attribution "many mathematicians," the
twentieth century, and the gloss `解的振荡性` (oscillatory behavior of solutions). It supplies no
citation, equation, definition, ordered binders, hypotheses, conclusion, boundary cases, proof
boundary, correction history, or formal artifact. Stage0 likewise leaves the formal system,
definitions, premises, proof route, alternate forms, axioms, and machine artifact open. The
catalog's verified label is explicitly untrusted under rev-5.6.

This omission is mathematically material. An exact proposition must choose all of the following:

- a differential equation or operator, its order, coefficient assumptions, scalar or state space,
  independent-variable domain, endpoint convention, and any spectral parameter;
- a solution predicate and regularity, a nontriviality condition, and exact simple, repeated, or
  endpoint-zero semantics;
- whether oscillation means infinitely many zeros, arbitrarily large zeros, a zero in every tail,
  shared behavior of all nontrivial solutions, a relative zero count, or another definition;
- whether the conclusion is a classification, comparison implication, nodal count, spectral
  relation, sufficient or necessary criterion, asymptotic theorem, or something else; and
- singular endpoints, the zero solution, degenerate equations, empty intervals, threshold equality,
  and other boundary cases.

These choices produce inequivalent theorems. Selecting one from memory would invent or substitute
mathematics rather than elaborate the exact received target.

Gerald Teschl's *Ordinary Differential Equations and Dynamical Systems*, Section 5.5, printed
pages 166-174, and its official errata were inspected at intake as source-family discriminators.
That section separately presents Pruefer definitions, zero and nodal counts, Sturm comparison and
interlacing, spectral identities, the half-line definition of an oscillating equation, and Kneser
criteria. The errata also changes formulas and proof details in this range. The repository neither
cites this source nor selects one of those propositions; source-to-root mapping, corrections,
proof boundary, and independent approval remain open.

The neighboring IDs cannot resolve the ambiguity by title. `THM-M-1384` owns broader
Sturm-Liouville theory, `THM-M-1385` comparison, `THM-M-1386` separation, `THM-M-1388` eigenvalue
problems, and `THM-M-1391` the Pruefer transform. None of their statements or future proof evidence
may silently become this root.

The authoritative intake task is provisional `[_]`, its worker receipt declares `accepted: false`,
and it has no accepted receipt ID. A dependency-ordered worker attempt may record this blocker, but
no accepted statement transition can precede master acceptance. Independently, the intake freezes
`canonical_statement`, the formal target, binders, and hypotheses as absent at `[H5, M4, R4]`, so
exact source-statement identity is the first substantive statement gate failure.

Consequently there is no canonical expression to elaborate, no honest minimal-import set, and no
expression or environment fingerprint. Checked transports and the removed-hypothesis,
changed-domain, changed-binder-scope, and boundary mutation classes are not runnable before the
canonical proposition exists. The root vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated against the pinned environment. Its three direct
imports expose seven adjacent integral-curve, derivative, set-infinity, and filter APIs. All seven
checks passed. The probe defines no scalar second-order equation, solution predicate, zero set,
oscillation convention, quantifier, target declaration, or proof body. Its imports therefore
cannot be certified minimal for an unidentified target and receive no statement or proof credit.

A bounded search found no Sturm-Liouville, Sturm comparison or separation, ODE oscillatory-solution,
Kneser-oscillation, or Pruefer-transform declaration in the directly relevant pinned ODE,
iterated-derivative, and set sources. A broader search found only pointwise topological oscillation
and unrelated uses of the names. These results are discovery-only feasibility evidence, not the
downstream anchor audit or a global proof of absence. In particular,
`Mathlib.Analysis.Oscillation` concerns pointwise topological oscillation and cannot substitute for
the zero behavior of ODE solutions.

The environment was Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided `.lake` symlink and canonical
pinned artifacts were used read-only. No `lake update`, `lake build`, dependency clone or fetch, or
other `.lake` mutation was run.

## Commands And Exact Results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1387` | 0 | rank 997; `planned`; `L0/rework_required`; no legacy slot; theorem incomplete |
| `git status --short --untracked-files=all` (pre-edit) | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `9890b8ae7278d1978497acce2be86f8fc4072af3`; tree `b90a6c34f533284f14d1d71b0ba11c76095110d8` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386...eea95`; tree `bdc39a312...5e2b`; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1387/IntakeProbe.lean` | 0 | all seven adjacent APIs elaborated; stdout SHA-256 `760037e8...7c4`; no target declaration or proof body |
| bounded exact-topic `rg` over directly relevant pinned mathlib sources | 1 | expected no-match result; no exact-topic occurrence |
| `python3 -B Stage1_Instances/THM-M-1387/check_intake.py` | 1 | historical intake replay fails first because its provisional receipt binds an older authoritative-blueprint digest; historical evidence was not rewritten |
| `python3 -m json.tool Stage1_Instances/THM-M-1387/statement-blocker.json` | 0 | blocker is valid JSON |
| scoped Python blocker-invariant check | 0 | identity, base, null target fields, unchanged debt vector, false completion fields, four unrunnable mutations, owned paths, and absent self-test agree |
| prohibited declaration scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped `git diff --check` plus per-new-file no-index checks | 0 | no whitespace diagnostics; no-index exit 1 for each file is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test manifest is absent as required for a blocked phase |

## Unblocking Condition

The integration lane must master-accept refreshed intake evidence without manufacturing a target.
An accountable source owner must then preserve and hash one lawful complete source edition, select
and independently approve one exact proposition and proof boundary as the `THM-M-1387` root, audit
its corrections and errata, and resolve the neighboring target identities. Every incorporated
definition, ordered binder, hypothesis, conclusion, and boundary case must then be frozen. A later
statement run can encode that same claim, establish minimal pinned imports, serialize its
elaborated expression and environment, check every credited transport, and run all four mutation
classes.

Until those prerequisites hold, no exact statement, proof, audit completion, or theorem completion
is claimed. Because the assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted.
