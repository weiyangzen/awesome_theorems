# THM-M-1480 rev-5.6 statement blocker

## Decision

`S56-M-1480-STATEMENT` remains `[ ]`. Its prerequisite `S56-M-1480-INTAKE` is only
provisional worker state `[_]`: `intake-receipt.json` is unaccepted and non-content-addressed,
contains no accepted receipt ID, and binds repository revision
`fc0de001c634823043636f9380a991c027e42533` rather than this attempt's base revision
`9e2ab501f9bd297b7bda1d222aec4e6f2029019a`. It also binds older blueprint and execution-DAG
hashes. There is no master-accepted dependency receipt. Rev-5.6 section 10.2 permits preparation of
this later-node blocker, but master closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete repository record
is the label `拟Monte Carlo方法`, the Harald Niederreiter attribution, the year 1978, and the gloss
`低差异序列的积分`: integration using low-discrepancy sequences. It fixes no finite point set or
infinite sequence convention, dimension, domain, measure, endpoint convention, discrepancy notion,
integrand or variation class, estimator and normalization, ordered binders, hypotheses, inequality,
convergence or rate conclusion, constants, arithmetic boundary, or degenerate cases. Stage0
explicitly leaves exact definitions and premises, the proof route, dependencies, alternate forms,
axiom policy, formal system, machine status, and artifacts open.

Materially inequivalent theorem families fit the gloss: a Koksma-Hlawka finite-sample error bound,
convergence of quadrature along a uniformly distributed sequence, a low-discrepancy construction
and its integration-error rate, or a weighted, randomized, scrambled, lattice, or digital-net
variant. Selecting any one would invent, narrow, broaden, or substitute proposition-changing
mathematics. Monte Carlo and simulated annealing are separately owned neighboring targets and
cannot supply statement identity here.

Niederreiter's 1978 survey, *Quasi-Monte Carlo methods and pseudo-random numbers*, is a strong
bibliographic lead. The intake admitted only Crossref metadata because the publisher full-text route
returned HTTP 403. No immutable source body, exact definition or theorem passage, incorporated
premises, proof boundary, correction record, source-to-root choice, or independent review was
admitted. Consequently there is no canonical expression to elaborate and no honest minimal-import
claim. The expression and canonical-target environment fingerprints, checked alternate transports,
and the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations are undefined, not passed.

No `Statement.lean`, theorem declaration, proof body, weakened special case, or broadened interface
was added. The root remains `[H5, M4, R4]`; `H5` classifies the received theorem-family gloss as not
yet one stable proposition and does not refute correctly stated quasi-Monte Carlo theorems.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its four direct
imports expose integration averages, weighted Dirac-sum integration, probability-density uniformity,
and tagged box-integral convergence. All seven checked declarations elaborated, and the three
representative axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound`.

Those declarations define no low-discrepancy sequence or point set, discrepancy or variation
functional, quasi-Monte Carlo estimator, or source-selected target. Their imports cannot be certified
minimal for an absent target and receive no statement or proof credit. A bounded exact-topic search
over the selected repo-local and pinned-mathlib Lean roots found no quasi-Monte Carlo,
low-discrepancy, star-discrepancy, Koksma-Hlawka, or equidistributed-sequence integration declaration.
This is narrow statement-feasibility evidence, not the downstream anchor audit or a global absence
claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from the isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1480` | 0 | rank 1157; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 10798,10803 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| authority, source, intake, probe, toolchain, lockfile, and relevant mathlib `sha256sum` checks | 0 | exact current hashes are preserved in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1480/IntakeProbe.lean` | 0 | seven adjacent APIs elaborated; stdout SHA-256 `4c37116a63ff938ed6d13c5a4c6be16e139c4c5517d799e6c14667cfc0066c8c`; no target declaration |
| bounded exact-topic `rg` over repo-local and pinned-mathlib Lean roots | 1, expected no match | no source-selected target declaration under the recorded QMC and discrepancy terms |
| `python3 -B Stage1_Instances/THM-M-1480/check_intake.py` | 1 | the historical intake checker binds its original base revision and therefore rejects this newer integrated revision; this phase records rather than rewrites historical intake evidence |
| prohibited-declaration `rg` over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, scoped-change, dependency-status, and absent-self-test checks are
recorded in the structured blocker beside this report.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then lawfully preserve one immutable primary or approved authoritative source and independently
select one exact numbered proposition or explicitly sourced conjunction. They must map every
incorporated definition, assumption, proof boundary, correction, and erratum, and freeze the sample
object, dimension, domain and measure, endpoint convention, discrepancy and variation definitions,
integrand class, estimator and normalization, ordered binders, hypotheses, exact inequality,
convergence or rate conclusion, constants, arithmetic and computation boundary, alternate encodings,
neighboring-target boundaries, and every degenerate case.

A fresh statement worker may then encode precisely that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
