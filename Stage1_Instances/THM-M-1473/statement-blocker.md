# THM-M-1473 exact-statement gate: blocked

Item: `S56-M-1473-STATEMENT`

Base revision: `fc0de001c634823043636f9380a991c027e42533` (tree
`b2e4d058036a1e9ec56bfc6aa5de3b015efe6330`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1473-INTAKE` is only provisional worker
state `[_]`: `intake-receipt.json` is unaccepted and non-content-addressed, has no accepted receipt
IDs, and binds an older repository revision and older blueprint and execution-DAG hashes. There is
no master-accepted dependency receipt. Section 10.2 of the rev-5.6 blueprint permits preparation of
later provisional evidence, but master closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete repository record
is the label `CFL condition`, the Courant/Friedrichs/Lewy attribution, the year 1928, and the gloss
`a stability condition for hyperbolic equations`. It supplies no PDE or system, coefficients,
domain or data, solution regularity, grid, scheme, mesh ratio, dependence regions, convergence or
stability predicate, norm, ordered binders, hypotheses, conclusion direction, or boundary cases.
Stage0 explicitly leaves exact definitions and premises, the proof path, dependencies, alternate
forms, axiom policy, formal system, machine status, and artifacts open.

The inspected 1928 paper is a strong matching source-family lead, but it contains materially
different claims. Printed page 33 discusses characteristic-dependent mesh-ratio inequalities.
Part II section 2, printed page 61, compares numerical and differential domains of dependence and
describes a nonconvergence regime for a wave-equation grid. Part II section 3, printed pages 62-65,
proves convergence in another regime under additional source-specific hypotheses. None has been
selected as the target, fully crosswalked, admitted from an immutable edition, checked for
translations, corrections and errata, or independently approved.

A modern generic domain-of-dependence necessity theorem, either source-specific wave result, a
scalar-advection Courant-number bound, and a stability theorem for a named scheme are not
interchangeable. Choosing one would invent, narrow, broaden, or substitute proposition-changing
mathematics. Consequently there is no canonical expression to elaborate and no honest
minimal-import claim. The elaborated expression and environment fingerprints, checked alternate
transports, and required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations are undefined, not passed.

No `Statement.lean`, theorem declaration, proof body, weakened special case, or broadened generic
interface was added. The root remains `[H1, M4, R4]`: `H1` records a matching source family and
passages, not an exact admitted theorem. `audit_complete` and `theorem_complete` remain false.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its direct imports
expose forward-difference identities and abstract coercive-form bounds. All eight checks elaborated,
and four representative axiom reports contained only `propext`, `Classical.choice`, and
`Quot.sound`.

Those declarations are adjacent substrate only. They define no hyperbolic evolution, numerical
scheme, continuous or discrete domain of dependence, convergence or stability predicate, or CFL
target. Their imports cannot be certified minimal for an absent target and receive no statement or
proof credit.

A bounded exact-topic search over repo-local `AwesomeTheorems` and pinned mathlib Lean sources found
no Courant-Friedrichs-Lewy, CFL, numerical-domain-of-dependence, or hyperbolic finite-difference
target declaration. This is narrow statement-feasibility evidence, not the downstream anchor audit
or a global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-1473` | 0 | rank 1150; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 10749,10754 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| authority, source, intake, probe, toolchain, lockfile, and relevant mathlib `sha256sum` checks | 0 | exact current hashes are preserved in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1473/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `c336880f81ad216f1a8f1268726aaa9c1523ba536ded7c7ba72388fec53e23cc`; empty stderr |
| bounded CFL and domain-of-dependence target-pattern search | 1, expected no match | empty-output SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; no exact-topic target declaration in the bounded roots |
| `python3 -B Stage1_Instances/THM-M-1473/check_intake.py` | 1 | historical intake validator expects authoritative intake state `[ ]`, while integration now records provisional `[_]`; this phase records rather than rewrites stale intake evidence |
| bash-wrapped prohibited-construct scan over owned Lean files | 0 (inner `rg` 1, expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, scoped invariant, whitespace, exact-change, dependency-status, and absent-self-test
checks passed and are recorded in the structured blocker beside this report.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then lawfully preserve one immutable primary or approved authoritative source and independently
select one exact proposition or explicitly sourced conjunction. They must map every incorporated
definition, assumption, proof boundary, translation, correction, and erratum, and freeze the PDE,
data and regularity, grid, numerical scheme, mesh parameters and refinement, dependence regions,
convergence or stability notions, norm, ordered binders, hypotheses, conclusion direction,
arithmetic boundary, neighboring-target boundaries, alternate encodings, and every degenerate case.

A fresh statement worker may then encode precisely that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
