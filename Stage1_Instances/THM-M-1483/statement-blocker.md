# THM-M-1483 exact-statement gate: blocked

Item: `S56-M-1483-STATEMENT`

Base revision: `2b649e7f3c2c6e3617cfb58c680e29f34d2ca5d7` (tree
`c9dfabc312a58c05c89917f6d7298a8e140356fc`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1483-INTAKE` is only provisional worker
state `[_]`: `intake-receipt.json` declares `accepted: false`, is not content-addressed, contains no
accepted receipt ID, and binds the older base revision `e552e0758e29de307cf357a703e6ecd16e40fb69`.
Section 10.2 of the rev-5.6 blueprint permits preparation of later provisional evidence, but master
closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete repository record
is the title `粒子群优化` (particle swarm optimization), attribution to James Kennedy and Russell
Eberhart, year 1995, and the gloss `基于群体智能的优化` (optimization based on swarm intelligence).
It supplies no recurrence, state or objective domain, swarm size, neighborhood topology, random
law, initialization, coefficients, ordered binders, hypotheses, conclusion, proof boundary,
corrections, or formal artifact. Stage0 explicitly leaves the precise definitions and premises,
formal system, proof route, dependencies, alternate forms, axioms, machine status, and artifact
links open. The catalog's `已验证` label is untrusted metadata under rev-5.6.

Kennedy and Eberhart's 1995 ICNN paper *Particle swarm optimization*, DOI
`10.1109/ICNN.1995.488968`, is a strong bibliographic lead matching the catalog. Intake obtained
bibliographic and abstract metadata only. No article body, exact update rule or proposition,
incorporated definitions and assumptions, proof, correction history, or independent source review
was admitted. The lead therefore cannot select a canonical root.

Several inequivalent targets remain compatible with the label: a definition or well-definedness
result for the original update, an invariant for stored best values, deterministic stability of a
selected recurrence, stochastic convergence in one of several modes, eventual global-optimum
discovery on a finite domain, or a rate or hitting-time bound. These require different variants,
domains, random semantics, hypotheses, observables, and conclusions. Convergence of positions,
velocities, stored best positions, and best objective values are distinct; convergence to an
equilibrium need not mean convergence to an optimum. Selecting any branch would invent, narrow,
broaden, or substitute proposition-changing mathematics rather than elaborate the received target.

Consequently there is no canonical human proposition or Lean expression on which to certify
minimal imports, serialize an expression and environment fingerprint, compile alternate
transports, or execute the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations. Those tests are undefined, not passed. No `Statement.lean`, theorem
declaration, proxy predicate, proof body, special case, or broadened interface was added. The root
remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its three direct
imports expose finite-image minimum, fixed-point, and contraction-iteration APIs. All five checks
elaborated, and the three axiom reports contained only `propext`, `Classical.choice`, and
`Quot.sound`. These APIs define no particle, swarm, velocity or position update, personal or
neighborhood best, objective, random process, convergence mode, or optimization conclusion. They
cannot be certified minimal for an absent target and receive no statement or proof credit.

A bounded case-insensitive search over the repo-local Lean tree, pinned mathlib, and this owned path
matched only the intake probe's disclaimer. It located no particle-swarm, Kennedy-Eberhart,
personal-best, or global-best target declaration. This is narrow statement-feasibility evidence,
not the downstream anchor audit and not a global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-1483` | 0 | rank 1160; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 10840,10845 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| authority, source, intake, toolchain, lockfile, and pinned-mathlib `sha256sum` checks | 0 | exact current hashes are preserved in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1483/IntakeProbe.lean` | 0 | five adjacent APIs elaborated; stdout SHA-256 `9855c6b2ece2f818591c2113f5f999b1d540f798018463cb5d767b5513f066bc`; empty stderr; no target declaration |
| bounded particle-swarm exact-topic search | 0 | only the intake probe disclaimer matched; output SHA-256 `d00cc4a3aa137c32d18e25a5a1bab2d22d11351609706b3f96fbfb4fc72962e4` |
| `python3 -B Stage1_Instances/THM-M-1483/check_intake.py` | 1 | historical intake checker expects authoritative intake `[ ]`/attempt 0, while integration records provisional `[_]`/attempt 1; this phase records rather than rewrites stale intake evidence |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, scoped-change, and absent-self-test checks are recorded in the
structured blocker beside this report.

## Retry Condition

The integration lane must master-accept refreshed intake evidence. Accountable source,
optimization/stochastic-algorithm, and formal reviewers must then lawfully preserve one immutable
primary or approved authoritative source, select and independently approve one exact truth-valued
proposition, and crosswalk every incorporated definition, assumption, proof boundary, correction,
and erratum. The selection must freeze the PSO variant and recurrence, state and objective domains,
swarm and topology, randomness and resampling semantics, initialization, coefficients, observable,
conclusion and convergence mode, arithmetic model, ordered binders, alternate encodings, and every
degenerate case.

A fresh statement worker may then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
