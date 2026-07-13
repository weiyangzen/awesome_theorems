# THM-M-1485 rev-5.6 statement blocker

## Decision

`S56-M-1485-STATEMENT` remains `[ ]`. Its prerequisite `S56-M-1485-INTAKE` is only
provisional worker state `[_]`: `intake-receipt.json` is unaccepted and non-content-addressed,
contains no accepted receipt ID, and binds repository revision
`e552e0758e29de307cf357a703e6ecd16e40fb69` rather than this attempt's base revision
`04d551db74b7e1d7d9d261bba4727b3daf8a70d5`. It also binds older blueprint and execution-DAG
hashes. There is no master-accepted dependency receipt. Rev-5.6 section 10.2 permits preparation of
this later-node blocker, but master closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete repository record
is the label `反向传播算法`, the David Rumelhart, Geoffrey Hinton, and Ronald Williams attribution,
the year 1986, and the gloss `神经网络的训练算法`: a training algorithm for neural networks. This is
an algorithm-family and purpose label, not a truth-valued proposition. It fixes no graph or layer
representation, node/edge/case/parameter index types, scalar and parameter carriers, activation,
loss, data semantics, bias or shared-weight convention, forward semantics, reverse derivative
recurrence, update rule, optimizer, learning rate, derivative representation, arithmetic model,
ordered binders, hypotheses, conclusion, or boundary cases. Stage0 explicitly leaves exact
definitions and premises, the proof route, dependencies, alternate forms, axiom policy, formal
system, machine status, and artifacts open.

Materially inequivalent roots fit the gloss: correctness of the 1986 paper's derivative recurrences,
generic reverse-mode derivative or gradient correctness for a finite computation graph, correctness
and termination of an executable backward sweep, correctness of a particular parameter-update
rule, a complexity bound, or a convergence or minimization theorem. The inspected primary-source
lead explicitly distinguishes plain-gradient and momentum updates and disclaims guaranteed global-
minimum convergence. Selecting a familiar finite sigmoid-network gradient theorem, or an optimizer
claim owned by a neighboring target, would invent, narrow, broaden, or substitute proposition-
changing mathematics.

Rumelhart, Hinton, and Williams's 1986 Nature article, *Learning representations by
back-propagating errors*, is a strong bibliographic and mathematical lead. Intake recorded the
observed facsimile SHA-256 and formula loci, but the catalog does not cite or select a result, the
remote facsimile is not an admitted immutable source body, corrections and variants have not been
audited, and no independent source, neural-network optimization, or formal review is recorded.
Consequently there is no canonical expression to elaborate and no honest minimal-import claim. The
expression and canonical-target environment fingerprints, checked alternate transports, and the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are
undefined, not passed.

No `Statement.lean`, theorem declaration, proof body, weakened special case, or broadened interface
was added. The root remains `[H5, M4, R4]`; `H5` classifies the received algorithm-family gloss as
not yet one stable proposition and does not refute correctly stated backpropagation results.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its five direct
imports expose generic Frechet chain rules, finite-sum differentiation, the real sigmoid derivative,
the squared-norm derivative, and matrix-vector linear semantics. All nine checked declarations
elaborated, and the three representative axiom reports contained only `propext`,
`Classical.choice`, and `Quot.sound`.

Those declarations define no neural-network graph or layers, data or loss model, backward recurrence,
parameter-gradient theorem, update algorithm, or source-selected target. Their imports cannot be
certified minimal for an absent target and receive no statement or proof credit. A bounded exact-topic
search over the repo-local and pinned-mathlib Lean roots found no backpropagation or neural-network
gradient target declaration under the recorded terms. This is narrow statement-feasibility evidence,
not the downstream anchor audit or a global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-1485` | 0 | rank 1162; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear in `statement-blocker.json` |
| `git blame -L 10854,10859 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| authority, source, intake, probe, toolchain, lockfile, and relevant mathlib `sha256sum` checks | 0 | exact current hashes are preserved in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1485/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; stdout SHA-256 `243818375ceb737f1723af65b9c871378159f436dbb4644741eeafbd19fdfa5e`; no target declaration |
| bounded exact-topic `rg` over repo-local and pinned-mathlib Lean roots | 1, expected no match | no source-selected backpropagation target declaration under the recorded terms |
| `python3 -B Stage1_Instances/THM-M-1485/check_intake.py` | 1 | the historical checker freezes intake authority state `[ ]`, attempts 0, while the current execution DAG records `[_]`, attempts 1; this phase records rather than rewrites historical intake evidence |
| prohibited-declaration `rg` over owned Lean files | 1, expected no match | no prohibited proof or declaration construct was found |
| scoped statement-blocker invariant assertions | 0 | item identity, open state, null target/imports, unchanged `H5/M4/R4`, four undefined mutations, current fingerprints, exact two-file scope, file hygiene, and absent self-test agree |
| `python3 -m json.tool Stage1_Instances/THM-M-1485/statement-blocker.json` | 0 | the finalized structured blocker parsed as valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1485` plus new-file whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

Final JSON, invariant, whitespace, scoped-change, dependency-status, and absent-self-test checks are
recorded in the structured blocker beside this report.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then lawfully preserve one immutable primary or approved authoritative source and independently
select one exact numbered proposition or explicitly sourced conjunction. They must map every
incorporated definition, assumption, proof boundary, correction, and erratum, and freeze the network
graph or layers, index and parameter types, activation, loss, data, forward semantics, reverse
recurrence, bias and parameter-sharing convention, derivative representation, update and optimizer
semantics, ordered binders, hypotheses, exact conclusion, arithmetic boundary, alternate encodings,
neighbor-target boundaries, and every degenerate case.

A fresh statement worker may then encode precisely that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
