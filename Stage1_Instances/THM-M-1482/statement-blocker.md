# THM-M-1482 exact-statement gate: blocked

Item: `S56-M-1482-STATEMENT`

Base revision: `2b649e7f3c2c6e3617cfb58c680e29f34d2ca5d7` (tree
`c9dfabc312a58c05c89917f6d7298a8e140356fc`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1482-INTAKE` has only provisional worker
state `[_]`: `intake-receipt.json` has `accepted: false`, is not content-addressed, and contains no
accepted receipt IDs. It also binds earlier blueprint and execution-DAG hashes. There is no
master-accepted dependency receipt.

Independently and decisively, the exact-statement gate fails. The complete repository record is the
family label `genetic algorithm`, an attribution to John Holland in 1975, and the gloss `an
optimization algorithm based on evolution`. It supplies no bibliography, exact result, stable
truth-valued proposition, genotype or phenotype space, population carrier or size, fitness or
objective, selection rule, crossover or mutation kernel, replacement or elitism policy, random
semantics, generation or stopping convention, correctness relation, convergence mode, optimizer
claim, cost model, ordered binders, hypotheses, conclusion, or boundary cases. Stage0 leaves the
exact definitions and premises open, and intake accordingly records a null human claim and null
formal target.

Materially inequivalent theorem families fit the gloss: Holland's schema theorem, preservation or
well-definedness of one generation operator, reachability or convergence of a finite-state genetic
process, implementation refinement, and complexity or approximation bounds. None is selected by
an admitted immutable source or an independent review. Choosing any one would invent, narrow,
broaden, or substitute proposition-changing mathematics.

There is therefore no canonical Lean expression whose imports can be minimized, no expression or
environment fingerprint, no approved alternate encoding, and no meaningful removed-hypothesis,
changed-domain, changed-binder-scope, or boundary-case mutation. All four mutation classes are
undefined, not passed. No `Statement.lean`, theorem declaration, proof body, toy special case,
circular interface, or broadened substitute was added. The root remains `[H5, M4, R4]`.

## Source And Lean Boundary

Holland's 1975 book *Adaptation in Natural and Artificial Systems* is a plausible historical lead,
and the 1973 article *Genetic Algorithms and the Optimal Allocation of Trials*, DOI
`10.1137/0202009`, is another lead. The catalog cites neither. No lawful immutable edition, exact
theorem passage, incorporated definitions, assumption and proof boundary, correction record, or
independent review is admitted, so neither selects this target.

The existing `IntakeProbe.lean` imports `Mathlib.Data.Multiset.Bind` and
`Mathlib.Probability.ProbabilityMassFunction.Constructions` and checks eight adjacent multiset and
probability-mass-function APIs. These are possible substrate only. The probe defines no fitness,
selection, crossover, mutation, replacement, or complete genetic transition and declares no
canonical target. Its imports cannot be certified minimal for a target that does not exist.

A bounded exact-topic search over the repo-local, pinned-mathlib, and owned Lean roots found only
one explanatory line in the intake probe and located no source-identical terminal declaration.
This is narrow feasibility evidence, not the downstream anchor audit or a global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-1482` | 0 | rank 1159; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| authority and null-target assertions over the manifest, execution DAG, intake receipt, and `instance.json` | 0 | rank, dependency, intake `[_]`, statement `[ ]`, unaccepted receipt, null canonical claim and target, and H5/M4/R4 agree |
| `git blame -L 10833,10838 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-1482/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]`, while integration now records provisional `[_]`; this phase records rather than rewrites stale intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && env LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1482/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `55d44374d805ad698f9cdb8b2d69bc13df27e1c7075286182c637dfec70e83a7`; axiom reports list only `propext`, `Classical.choice`, and `Quot.sound`; no target declaration |
| `rg -n -i --glob '*.lean' '(genetic algorithm\|genetic programming\|evolutionary algorithm\|evolutionary computation\|schema theorem\|Holland)' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib Stage1_Instances/THM-M-1482` | 0 | only one explanatory intake-probe line matched; output SHA-256 `7b5de02d203d7be3c4531ba65260a493eb133f25e6286b6ce35b39388ca2a82f`; no source-identical declaration located |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition

The integration lane must master-accept refreshed intake evidence. Accountable source and
evolutionary-computation reviewers must admit an immutable pinpoint source and independently select
one exact proposition. That selection must fix the genotype and phenotype carriers, population,
fitness or objective, selection, crossover, mutation, replacement and elitism, randomness,
horizon, optimizer or correctness notion, quantifier order, assumptions, conclusion, arithmetic or
cost model, and every degenerate case.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
