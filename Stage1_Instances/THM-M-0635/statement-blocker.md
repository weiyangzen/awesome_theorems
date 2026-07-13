# THM-M-0635 rev-5.6 statement blocker

## Verdict

`S56-M-0635-STATEMENT` is blocked at the exact source-statement and variant-selection gate. The
repository record names the extreme value theorem, attributes it to Karl Weierstrass in 1860, and
gives only the gloss `紧集上连续函数可取到最大最小值` (a continuous function on a compact set
attains maximum and minimum values). It contains no bibliography, formula, binder-complete
proposition, incorporated definitions, proof boundary, correction history, or independently
approved source crosswalk. Its `已验证` label is untrusted metadata under rev-5.6.

The existing intake therefore correctly leaves the canonical human claim, Lean declaration or
expression, elaborated-expression hash, and target environment fingerprint null. In particular,
the catalog does not select:

- an arbitrary topological space with a compact subset, a compact carrier, a compact metric set,
  or a closed interval;
- `Real` or a generic ordered codomain with additional order-topology assumptions;
- global `Continuous`, `ContinuousOn` on a subset, or continuity of a subtype function;
- an explicit nonemptiness hypothesis or a carrier convention incorporating nonemptiness;
- `IsMinOn` and `IsMaxOn`, explicit inequalities, extrema of the image, or another paired form;
- ordered binders, universes, coercions, quantifier order, and the relationship between the two
  extrema witnesses; or
- treatment of the empty, singleton, constant-function, noncompact, wrong-continuity-domain, and
  unsuitable-codomain cases.

These choices change the proposition or require checked transports. The literal witness claim is
false for the empty compact set. Selecting the familiar real-valued formulation would add missing
domain and nonemptiness conventions; selecting mathlib's generic ordered-codomain pair would also
add two source-unstated topology assumptions. Neither may be inferred merely because it elaborates.

Consequently there is no canonical Lean expression whose imports can be certified minimal, no
normalized expression fingerprint, and no approved alternate form for a checked transport. The
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are
undefined rather than passed. Sections 5 and 5.1 of the rev-5.6 blueprint make these absences hard
statement blockers before proof evidence can be inspected.

The prerequisite intake is only provisional worker state `[_]`, not master-accepted state `[x]`.
Its receipt declares `accepted: false`, is not content-addressed, and supplies no accepted receipt
ID. Section 10.2 permits this dependency-ordered blocker attempt while concurrency is enabled, but
master acceptance remains a separate prerequisite for any eventual accepted statement transition.
The absent source-approved exact proposition is the first substantive statement blocker.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` imports only `Mathlib.Topology.Order.Compact`. In the pinned
environment it elaborates the compactness, continuity, nonemptiness, `IsMinOn`, and `IsMaxOn`
interfaces together with `IsCompact.exists_isMinOn` and `IsCompact.exists_isMaxOn`. The latter
declarations are explicitly documented by mathlib as the extreme value theorem and have types:

- a nonempty compact set and a function continuous on it have a minimum when the linearly ordered
  codomain has `ClosedIicTopology`; and
- the analogous hypotheses give a maximum when the codomain has `ClosedIciTopology`.

Both diagnostic axiom reports are `[propext, Classical.choice, Quot.sound]`. With `LC_ALL=C` and
`TZ=UTC`, the deterministic probe output is 1,475 bytes with SHA-256
`ed046c98904c8e4aec5d72f1a823f5dcca767138f9a69984f6a6958f0d39b929`.

This authenticates exact-topic pinned interfaces only. A theorem name and module comment do not
supply the missing source-to-root identity. The two declarations are separate one-sided results,
while the catalog wording is two-sided; their generic codomain hypotheses and result encoding have
not been admitted by a source or connected to a canonical combined root. The probe declares no
target, checked transport, mutation fixture, or proof body, and its import cannot be certified
minimal for a target that has not been selected. The interfaces remain `M3` support only.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or other
dependency mutation was run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai), from the repository root
unless another working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0635` | 0 | rank 1328, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation `.lake` symlink was untracked; base revision `67d32ab26aba14b674ae8a1b919e6935812190c3`, tree `8a1d264cf3331992fbbc3a4fffca285af0b88929` |
| repository authority, catalog, Stage0, intake, scope, crosswalk, task-DAG, and receipt inspection | 0 | confirmed provisional intake, null target, exact-source ambiguity, two candidate-only interfaces, and six open downstream tasks |
| `git blame -L 4706,4711 -- Docs/researches/math_theorems.md`; catalog-block hash | 0 | all six uncited fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; block SHA-256 `9ff5f5c6dd52b607c93c31450931bcecacbc64ac4513a6d631979f500a666414` |
| `python3 -B Stage1_Instances/THM-M-0635/check_intake.py` | 1 | the historical intake checker expects its item to remain `[ ]`, while current authority records provisional `[_]`; it was not modified or represented as statement evidence, and its closed intake inventory would also reject later-phase files |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree and package-status checks | 0 | revision and tree agree with the environment fingerprint; package worktree is clean |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0635/IntakeProbe.lean)` | 0 | nine adjacent interfaces elaborated; both candidate axiom reports and deterministic output hash recorded above; no target theorem stated |
| bounded `rg` search for the target and compact extrema interfaces in repo-local Lean and pinned mathlib | 0 | found the two pinned generic candidates and uses in other targets, but no source-approved `THM-M-0635` root; discovery only |
| prohibited declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and scoped invariant check for `statement-blocker.json` | 0 each | null target, unchanged vector, false completion flags, four undefined mutations, exact two-file change scope, and no-self-test boundary agree |
| scoped whitespace checks for both added blocker artifacts | 0 aggregate | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before accepting a future
statement transition. Accountable reviewers must preserve and hash one lawful immutable primary or
authoritative source, select and independently approve its exact proposition and proof boundary,
and transcribe every incorporated definition, ordered binder, premise, conclusion, correction,
erratum, translation, and boundary case. They must explicitly settle the domain, codomain and its
order-topology assumptions, nonemptiness convention, continuity encoding, two extrema encodings,
witness and quantifier order, transports, and all degenerate cases.

A fresh statement attempt can then encode precisely that approved claim, minimize pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. The root remains `[H1, M3, R4]`; `audit_complete` and `theorem_complete` remain
false; no debt-vector change, statement receipt, worker `[_]`, or master acceptance is claimed.
Because the exact-statement deliverable did not pass, `.stage1-worker-selftest.json` is deliberately
absent.

The historical intake checker is bound to intake-time state and its closed artifact inventory.
This worker did not rewrite intake history, and that expected phase-evolution failure neither
validates nor invalidates this separate blocked statement decision.
