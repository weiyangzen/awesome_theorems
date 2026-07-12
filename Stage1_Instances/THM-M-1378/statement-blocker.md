# THM-M-1378 statement-phase blocker

- Item: `S56-M-1378-STATEMENT`
- Base revision: `1fc66febfddf404bb914cec34962d66862b96f2b`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be entered
truthfully from the received source record. `Docs/researches/math_theorems.md:10041-10046` gives
only the name "Euler-Lagrange equation," the Euler/Lagrange attribution, the year 1755, and the
gloss "a differential equation for extrema of functionals." It supplies no cited proposition,
formula, definitions, hypotheses, conclusion, proof boundary, or errata. The Stage0 projection
explicitly leaves the exact definitions and assumptions open.

This omission is proposition-defining. The record does not select a scalar or vector-valued
unknown, a one- or multidimensional independent domain, an action functional, an autonomous or
time-dependent integrand, an admissible path and variation space, local minimality versus
stationarity, regularity and integrability assumptions, fixed or free endpoints, a derivative
convention, or a classical, weak, coordinate, or operator conclusion. These choices produce
materially different Euler-Lagrange theorems. Selecting the familiar one-dimensional
fixed-endpoint formula would invent or substitute mathematics rather than elaborate the exact
received target.

The predecessor intake is provisional `[_]`, has no accepted receipt ID, and itself records the
canonical statement, formal module, exact expression, expression hash, and environment
fingerprint as null at `[H5, M4, R4]`. Its required retry condition is an independently reviewed,
immutable source correction selecting one binder-complete proposition. Consequently there is no
canonical expression to elaborate, no honest minimal-import claim, and no meaningful checked
transport or removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation.
The statement node remains open and is not self-tested complete.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated in the pinned environment. Its four direct
imports expose eight adjacent local-extremum and integration-by-parts declarations. All checks
passed, but the probe explicitly defines no functional, admissible variation, Euler-Lagrange
target, or proof body. Its imports therefore are not claimed minimal for an unidentified target.

A bounded exact-topic search found no Euler-Lagrange declaration in pinned mathlib. Repo-local
matches belong to distinct targets or legacy discovery artifacts. In particular,
`THM-M-1518/Statement.lean` selects a fixed-endpoint stationary-action statement for a different
least-action target; `S1_M_186.lean` stores the decisive implication as input data;
`S1_M_187.lean` primarily encodes the converse direction; and `S1_M_184.lean` has only a
zero-Lagrangian special case. None supplies source identity or statement credit for THM-M-1378.
This bounded search is feasibility evidence, not the downstream anchor audit or proof of absence.

The environment was Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided `.lake` symlink and pinned
artifacts were used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other
`.lake` mutation was run.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1378` | 0 | rank 988; `planned`; `L0/rework_required`; no legacy slot; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before this attempt, only the automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `1fc66febfddf404bb914cec34962d66862b96f2b`; tree `49ae48302378d63f3c54b2a43eeca26433c6b7c5` |
| `git blame -L 10041,10046 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions recorded above |
| `cd Formalizations/Lean && git -C .lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above; package status was clean |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | SHA-256 `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1378/IntakeProbe.lean` | 0 | all eight adjacent APIs elaborated; no target declaration or proof body |
| exact-topic `rg` search in pinned mathlib | 1 | expected no-match result; no Euler-Lagrange topic match in Lean sources |
| exact-topic `rg` search in repo-local Lean | 0 | matches were distinct targets and legacy boundaries; none receives target statement credit |
| `python3 -B Stage1_Instances/THM-M-1378/check_intake.py` | 1 | historical intake replay detects its stale recorded hash for the since-regenerated normative blueprint; the historical intake receipt was not rewritten |
| `rg -n --glob '*.lean' -e '\\bsorry\\b' -e '\\badmit\\b' -e '\\bsorryAx\\b' -e '^\\s*axiom\\s+' -e '^\\s*constant\\s+' -e '^\\s*opaque\\s+' -e '^\\s*unsafe\\b' Stage1_Instances/THM-M-1378` | 1 | expected no-match result; no prohibited declaration token |
| `python3 -m json.tool Stage1_Instances/THM-M-1378/statement-blocker.json` | 0 | blocker parsed as valid JSON |
| `python3 - <<'PY'` (load the blocker; assert identity/base, null target, unchanged vector, four unrunnable mutations, false completion fields, current source hashes, owned paths, and absent worker packet) `PY` | 0 | `statement_blocker_invariants: ok` |
| scoped new-file whitespace checks plus `git diff --check` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test manifest is absent as required for a blocked phase |

## Unblocking condition

An accountable source owner must preserve and hash a lawful complete source edition, select one
exact theorem and proof boundary, transcribe every incorporated definition, ordered binder,
hypothesis, conclusion, convention, correction, and boundary case, and obtain independent source
and scope approval. A fresh statement run can then encode that same proposition, minimize its
pinned imports, serialize and hash its elaborated expression and environment, compile all credited
transports, and run all four required mutation classes. The integration lane must also accept the
intake dependency before accepting any later statement transition.

Until those conditions hold, no exact statement, proof, audit completion, or theorem completion is
claimed. Because the assigned phase did not pass its completion gate, no
`.stage1-worker-selftest.json` is emitted.
