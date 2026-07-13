# Exact-statement gate: blocked

Item: `S56-M-0238-STATEMENT`

Theorem: `THM-M-0238`

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0238-INTAKE` has provisional worker
state `[_]`, not master acceptance. The intake receipt has `accepted: false` and
`content_addressed: false`, and deliberately leaves the canonical human claim and Lean target
null. That dependency cannot support an accepted statement transition.

Independently, no exact Lean 4 target can be truthfully elaborated from the authoritative record.
`Docs/researches/math_theorems.md:1717-1722` gives only the title `阿贝尔定理`, Abel, 1827, and the
gloss `椭圆积分的反演` ("inversion of elliptic integrals"). It supplies no formula, bibliography,
definitions, binders, hypotheses, conclusion, proof boundary, corrections, errata, or reviewer.
`Docs/Stage0_Blueprint.md:6599-6624` repeats the gloss while explicitly leaving the precise
definitions and premises, proof route, formal system, axioms, machine status, and artifacts open.
The catalog's `已验证` label is untrusted under rev-5.6.

The intake authenticated Abel's 1827 *Recherches sur les fonctions elliptiques* only as a primary
source lead and inspected its opening topic discussion. It did not admit an exact proposition,
complete incorporated definition and proof chain, translation relationship, correction or errata
disposition, or independent review. It therefore cannot resolve the proposition-changing choices:

- the integral or algebraic curve, coefficient or modulus, and nonsingularity assumptions;
- real or complex scope, basepoint, integration paths, square-root branches, and continuation;
- a local, multivalued, planar meromorphic, quotient-valued, or curve-valued inverse;
- normalization, period lattice, ordered periods, domain, codomain, and inverse direction;
- existence, construction, meromorphicity, double periodicity, a differential equation, an
  addition law, or another source-selected conclusion; and
- repeated roots, degenerate or limiting moduli, branch points, endpoints, poles, lattice points,
  path dependence, and empty-domain cases.

These are not notation choices. Selecting a familiar Legendre, Jacobi, or Weierstrass formulation
would invent scope or require unproved transports. It could also substitute `THM-M-0239`, which
separately owns general Jacobi inversion for Abelian integrals, or `THM-M-0240`, which separately
owns the Abel-Jacobi/Jacobian target.

Rev-5.6 section 5 makes statement ambiguity and a missing elaborated-expression fingerprint hard
blockers. Consequently there is no canonical expression whose imports can be certified minimal,
no alternate encoding to transport, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation. Those mutations are undefined, not passed. The
provisional intake root vector remains `[H1, M4, R4]`; it is not an accepted classification.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its one direct import,
`Mathlib.Analysis.SpecialFunctions.Elliptic.Weierstrass`. It checks `PeriodPair`, the Weierstrass
P function, its derivative identity, lattice periodicity, meromorphicity, pole order, and cubic
differential equation. All eight APIs elaborate. The four axiom reports are exactly `propext`,
`Classical.choice`, and `Quot.sound`; the complete stdout SHA-256 is
`c70df6104c1727f2d0d0c3bfc871724eab29907aa72d6e9cbbbcba6738bf8eb2`.

This is real pinned interface evidence, but it is only output-side substrate. The probe defines no
selected elliptic integral, branch, inverse relation, canonical target, checked transport, or proof
body. Its import may be appropriate for the probe, but cannot be called minimal for an absent
canonical target. Bounded repo-local and pinned-mathlib searches likewise identified no
source-selected inversion root. This is discovery evidence, not the downstream anchor audit or a
global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone or
fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`). Exact structured
arguments, results, authority hashes, and the current known failures are also recorded in
`statement-blocker.json`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0238` | 0 | rank 1249; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 1717,1722 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0238/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; four axiom reports contain the three axioms above; no target theorem was stated |
| bounded exact-topic `rg` searches over repo-local Lean and pinned mathlib | 0 | only the probe disclaimer, unrelated legacy prose, and unrelated integral/inverse uses matched; no source-selected root was credited |
| `python3 -B Stage1_Instances/THM-M-0238/check_intake.py` | 1 | historical intake replay stops at its frozen base assertion (`c6fd6d...` versus current `bd81d4...`); intake evidence was not rewritten |
| JSON parse and scoped blocker-invariant checks | 0 | identity, null target/imports, four undefined mutations, unchanged provisional vector, false completion flags, and no-self-test boundary agree |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped `git diff --check` plus no-index checks for both new blocker files | 0 / 1 each | no whitespace diagnostics; no-index exit 1 is the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker freezes the intake run's original commit and artifact inventory. It is
historical evidence, not a later-phase statement validator. This run records the stale-base failure
instead of modifying the intake instance, receipt, checker, task DAG, generated blueprint, or
authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake before accepting a later statement transition.
Accountable reviewers must preserve and hash a lawful immutable source, transcribe and
independently approve one exact proposition with every incorporated definition, ordered binder,
hypothesis, conclusion, inverse and period convention, proof boundary, correction, erratum, and
boundary case, and reconcile `THM-M-0239` and `THM-M-0240`.

A fresh statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile each credited
transport, and run the removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
