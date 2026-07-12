# Exact-statement gate: blocked

Item: `S56-M-1391-STATEMENT`

Theorem: `THM-M-1391`

Base revision: `9890b8ae7278d1978497acce2be86f8fc4072af3` (tree
`b90a6c34f533284f14d1d71b0ba11c76095110d8`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete mathematical wording is only the title `Prufer变换` ("Pruefer transformation") and
the gloss `Sturm-Liouville问题的相位分析` ("phase analysis of Sturm-Liouville problems"). It
provides an attribution and year but no citation, binder-complete proposition, hypotheses, or
conclusion. Stage0 explicitly leaves the definitions and premises, proof route, dependencies,
alternate forms, axioms, machine status, and artifacts open. The catalog label `已验证` is
untrusted under rev-5.6.

The wording does not select among materially different propositions:

- existence and gauge uniqueness of amplitude and a continuous lifted phase;
- derivation of forward amplitude and phase equations from a second-order equation;
- an iff or reconstruction theorem for the transformed first-order system;
- correspondence between solution zeros and phase crossings;
- phase monotonicity in position or spectral parameter; or
- an oscillation, eigenvalue-ordering, asymptotic, or expansion consequence.

The inspected historical source lead is Heinz Pruefer's 1926 paper. Its pages 503-504 use the
state equations `u' = v/k`, `v' = -(l + lambda r) u` and coordinates
`v = rho cos theta`, `u = rho sin theta`; later pages use phase behavior for oscillation and
spectral conclusions. A modern Teschl formulation uses a differently normalized regular
Sturm-Liouville operator and separately distinguishes the transform equations, their equivalence,
and a zero-count lemma. Neither source, edition, passage, convention, or result has been selected
and independently approved as this catalog item's canonical root. Choosing any one would invent,
narrow, broaden, or substitute mathematics rather than elaborate the exact received target.

The intake therefore deliberately leaves the canonical statement and Lean target null and records
`[H5, M4, R4]`. Rev-5.6 makes statement ambiguity and a missing expression fingerprint hard
blockers. There is no honest canonical declaration for which minimal imports can be claimed.
Checked transports and the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations are undefined rather than passed. No `Statement.lean`, assumed transform
field, convenient oscillator special case, axiom, placeholder, or broadened theorem was introduced.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated using the pinned environment. It directly imports
`Mathlib.Analysis.ODE.Basic` and `Mathlib.Analysis.SpecialFunctions.PolarCoord`; eighteen generic
ODE, derivative, polar-coordinate, complex-argument, and quotient-angle APIs elaborated. The probe
states no Sturm-Liouville problem, continuous real phase lift, transformed equation, or canonical
target, so these imports cannot be certified minimal for the absent proposition and receive no
statement, anchor, or proof credit. In particular, a principal complex argument is not silently a
continuous lifted Pruefer phase along a nonvanishing solution-state curve.

A bounded exact-topic search of pinned mathlib found only the unrelated group-theoretic Pruefer
subgroup, a Pruefer-domain TODO, and the subgroup's import. The sole repo-local Lean hit was a
planning string about Sturm-Liouville search. This is scoped feasibility evidence only, not the
downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai), from the repository root
unless a different working directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1391` | 0 | rank 1001; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, blueprint, DAG, intake, and source-lead inspection | 0 | confirmed the method-family gloss, null target, distinct candidate roots, and unresolved source selection |
| `sha256sum` over authority, source, intake, probe, toolchain, Lake manifest, and relevant pinned mathlib sources | 0 | exact hashes are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-1391/check_intake.py` | 1 | the historical intake checker freezes intake authority state `[ ]`, while the integrated DAG now records provisional `[_]`; it was not rewritten during statement work |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | the pinned revision and tree agree; the package worktree is clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1391/IntakeProbe.lean` | 0 | eighteen adjacent APIs elaborated; complete output SHA-256 `68584c0aad837fd65c6e07d09dc40e19102ea81d1e39e312be21f90fa6a62117`; no target or proof body |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 0 | only unrelated Pruefer terminology and one planning string; discovery evidence only |
| prohibited Lean construct scan over the owned path | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1391/statement-blocker.json` plus scoped blocker invariants | 0 | identity, blocked/open state, null target/import/hash, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, and absent self-test agree |
| scoped whitespace checks for both blocker files | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the exact-statement deliverable did not pass |

The intake prerequisite has provisional worker state `[_]`, not master-accepted state `[x]`; its
receipt declares `accepted: false`, is not content-addressed, and contains no accepted receipt ID.
Section 10.2 permits this dependency-ordered investigation, so that boundary did not replace the
substantive statement assessment. It remains an acceptance prerequisite. The first substantive
statement failure is exact source-statement and scope identity.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash a lawful immutable primary or authoritative edition,
select and transcribe one exact proposition or explicit conjunction and every incorporated
definition with pinpoint locators, audit translation, corrections, errata, and proof boundary, and
independently approve the mapping. They must fix the Sturm-Liouville equation and signs,
coefficients and regularity, interval and endpoints, real solution notion, state pair, nontriviality
and simultaneous-zero policy, amplitude normalization, phase period and continuous lift,
transformed equations, implication or reconstruction direction, zero treatment, boundary
conditions, parameter convention, and the boundary between transform and oscillation or spectral
consequences. The integration lane must also master-accept the intake dependency before accepting a
future statement transition.

A later statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; the vector remains `[H5, M4, R4]`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, or master acceptance is claimed.
