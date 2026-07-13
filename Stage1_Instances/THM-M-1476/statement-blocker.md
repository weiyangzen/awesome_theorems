# THM-M-1476 exact-statement gate: blocked

Item: `S56-M-1476-STATEMENT`

Base revision: `fc0de001c634823043636f9380a991c027e42533` (tree
`b2e4d058036a1e9ec56bfc6aa5de3b015efe6330`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1476-INTAKE` is only provisional worker
state `[_]`: `intake-receipt.json` is unaccepted and non-content-addressed, has no accepted receipt
IDs, and binds the older repository revision `b4300806b9f337b5fa27a7787b8c0893eee48f30` and older
blueprint and execution-DAG hashes. There is no master-accepted dependency receipt. Section 10.2 of
the rev-5.6 blueprint permits preparation of later provisional evidence, but master closure remains
dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete repository record
is the title `刚性稳定性`, the collective attribution `众多数学家`, the period `20世纪`, and the
gloss `刚性问题的数值稳定性`: numerical stability of stiff problems. It supplies no definition of
stiffness, problem class, equation, exact or discrete solution, numerical method, stability notion,
norm, time horizon, step regime, ordered binders, hypotheses, exact conclusion, constants, or
boundary cases. Stage0 explicitly leaves exact definitions and premises, the proof route,
dependencies, alternate statements, axiom policy, formal system, machine status, and artifacts
open.

Materially inequivalent theorem families fit the gloss: stiff stability of a multistep or
multiderivative method, a relation with `A_0`- or `A(0)`-stability, stability or decay of an implicit
one-step, Runge-Kutta, or BDF scheme, or a stiffness-uniform error or contractivity result. Selecting
any one would invent, narrow, broaden, or substitute proposition-changing mathematics. It could
also collide with separately owned Runge-Kutta, A-stability, L-stability, stiff-equation, or BDF
targets.

Jeltsch's 1976 and 1977 stiff-stability papers and the 1979 corrigendum are useful bibliographic
leads, but the catalog cites none of them. Intake admitted only Crossref metadata, not an immutable
paper, exact definition or theorem passage, incorporated premises, proof boundary, correction
impact, source-to-root selection, or independent review. Consequently there is no canonical
expression to elaborate and no honest minimal-import claim. The canonical expression and
environment fingerprints, checked alternate transports, and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined, not passed.

No `Statement.lean`, theorem declaration, proof body, weakened special case, or broadened interface
was added. The root remains `[H5, M4, R4]`; `H5` classifies the received topic gloss as not yet a
stable proposition and does not refute correctly stated stiff-stability theorems.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its four direct
imports expose continuous integral-curve, Gronwall trajectory-comparison, Picard-Lindelof, and
complex-exponential interfaces. All nine checks elaborated, and the three representative axiom
reports contained only `propext`, `Classical.choice`, and `Quot.sound`.

Those declarations define neither stiffness nor a discrete numerical method or stiff-stability
predicate. Their imports cannot be certified minimal for an absent target and receive no statement
or proof credit; indeed, `Complex.Trigonometric` is transitively redundant for the probe's nine
checks. A bounded exact-topic search over the selected repo-local and pinned-mathlib Lean roots
found no stiff-stability, Dahlquist, Runge-Kutta, multistep, multiderivative, BDF, stability-region,
or amplification declaration. This is narrow statement-feasibility evidence, not the downstream
anchor audit or a global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-1476` | 0 | rank 1153; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 10770,10775 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| authority, source, intake, probe, toolchain, lockfile, and relevant mathlib `sha256sum` checks | 0 | exact current hashes are preserved in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1476/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; stdout SHA-256 `07d33b481d91855d1237e7e2745853ed0285c1b27a9005940d6885ca50838f87`; no target declaration |
| `rg -n -i --glob '*.lean' '\bstiff(ness)?\b\|stiff[ _-]?stabil\|dahlquist\|runge[ _-]?kutta\|multistep\|multiderivative\|backward differentiation\|\bbdf\b\|stability[ _-]?region\|amplification[ _-]?(factor\|function)\|\bA-stability\b\|\bL-stability\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis Formalizations/Lean/AwesomeTheorems` | 1, expected no match | no matching target declaration in the bounded roots |
| `python3 -B Stage1_Instances/THM-M-1476/check_intake.py` | 1 | its historical exact-row assertion freezes intake as `[ ]`, attempt 0, while current authority records `[_]`, attempt 1; this phase records rather than rewrites stale intake evidence |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1476` | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, scoped-change, dependency-status, and absent-self-test checks are
recorded in the structured blocker beside this report.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then lawfully preserve one immutable primary or approved authoritative source and independently
select one exact numbered proposition or explicitly sourced conjunction. They must map every
incorporated definition, assumption, proof boundary, correction, and erratum, and freeze the
stiffness criterion, equation and solution model, numerical method and coefficients, stability
notion, norm, time and step domains, hypotheses, ordered binders, conclusion, constants, arithmetic
and solver boundary, neighboring-target boundaries, alternate encodings, and every degenerate case.

A fresh statement worker may then encode precisely that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
