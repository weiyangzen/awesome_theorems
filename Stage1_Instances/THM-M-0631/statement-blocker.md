# Exact-statement gate: blocked

Item: `S56-M-0631-STATEMENT`

Theorem: `THM-M-0631`

Base revision: `67d32ab26aba14b674ae8a1b919e6935812190c3` (tree
`8a1d264cf3331992fbbc3a4fffca285af0b88929`).

## Decision

The exact Lean 4 target cannot yet be truthfully adopted from the accepted inputs. The statement
item remains `[ ]`. Its prerequisite intake has provisional worker state `[_]`, not
master-accepted state `[x]`; its receipt has `accepted: false`, is not content-addressed, and has no
accepted receipt ID. Rev-5.6 section 10.2 permits this dependency-ordered provisional inspection,
but not master closure. The intake deliberately leaves the canonical claim, ordered binders, Lean
expression, minimal imports, expression fingerprint, and target-environment fingerprint open.

The repository supplies only the title Baire category theorem, Rene Baire, 1899, and the gloss
`完备度量空间是第二纲集` ("a complete metric space is of second category"). It cites no work,
edition, theorem/page/section, formula, definition chain, proof boundary, translation, correction,
erratum, or reviewer. The intake found bibliographic identity for Baire's 1899 paper, but no exact
proposition was admitted or independently reviewed.

Material proposition choices remain unresolved. `BaireSpace X` means that every natural-number-
indexed intersection of open dense sets is dense. Literal whole-space second category can instead
mean `Not (IsMeagre (Set.univ : Set X))`. These are not interchangeable on the empty complete
metric space: `BaireSpace Empty` holds while its whole set is meagre. The literal formulation thus
needs an explicit `Nonempty X` premise or a source-sanctioned empty-space exclusion. The catalog
also does not decide between a displayed complete separated metric, a complete pseudometric, and a
topology admitting some compatible complete metric or pseudometric. The pinned bridge accepts the
last and broadest pseudometric formulation, so adopting it would broaden the received wording.

Selecting any familiar candidate now would silently strengthen, repair, or broaden the catalog
claim. There is consequently no canonical expression whose direct imports can be certified
minimal, no approved alternate encoding for a checked transport, and no meaningful
removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation suite. Those
outputs are undefined, not passed. The root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

Both `IntakeProbe.lean` and the new `StatementBoundaryProbe.lean` elaborate under the direct import
`Mathlib.Topology.Baire.CompleteMetrizable`. The latter checks these pinned interfaces:

- `BaireSpace.of_completelyPseudoMetrizable`;
- `BaireSpace.baire_property`;
- `not_isMeagre_of_isOpen`;
- `IsMeagre.empty`;
- `nonempty_of_not_isMeagre`.

It synthesizes `MetricSpace Empty`, `CompleteSpace Empty`,
`TopologicalSpace.IsCompletelyMetrizableSpace Empty`, and `BaireSpace Empty`. It then checks both
the empty-space counterexample and the exact complete-metric boundary

```text
Not (IsMeagre (Set.univ : Set X)) <-> Nonempty X.
```

This is real kernel-checked discriminator evidence. It proves why the source decision is material;
it does not make that source decision, declare a canonical target, certify minimal imports for an
absent target, establish a checked source transport, or supply target-proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No update, build, clone, fetch, or other dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0631` | 0 | rank 1324; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 4678,4683 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0631/IntakeProbe.lean` | 0 | eleven interfaces elaborated; `BaireSpace Empty` synthesized; its whole set checked meagre; stdout SHA-256 `f15310c589d3edeff1ed2582ba4b11db365853276f95a50bf4e0928362b585ea` |
| initial draft of the `StatementBoundaryProbe.lean` command | 1 | lowercase `not` was parsed as Boolean negation, producing a line-28 type mismatch; stdout SHA-256 `54fae9c5654f541d9a288876c773a937dd3b36602276a9657eda4b386d904451`; spelling was corrected to `Not` before final validation |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0631/StatementBoundaryProbe.lean` | 0 | five APIs, four Empty instances, the counterexample, and complete-metric nonmeagreness iff nonemptiness elaborated; stdout SHA-256 `7d2d4c1f6c270f6d4e1c1353870deeb9acff8177d0db2ac11fac24ffc98c6697` |
| `LC_ALL=C TZ=UTC python3 -B Stage1_Instances/THM-M-0631/check_intake.py` | 1 | historical intake checker is bound to intake-time DAG state `[ ]`/attempts 0, while integration now records `[_]`/attempts 1; it was not edited or represented as statement evidence |
| prohibited Lean construct scan over the owned path | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0631/statement-blocker.json`; scoped JSON invariant checks | 0 | structured blocker parsed and its identity, null target/imports, unchanged vector, four undefined mutations, false completion flags, and no-self-test boundary agreed |
| scoped newline, trailing-whitespace, and `git diff --check` checks | 0 | the three new owned artifacts passed whitespace validation |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

The integration lane must master-accept the intake. Accountable reviewers must lawfully preserve
and hash an immutable primary or authoritative source, identify one exact proposition, and
independently approve every incorporated definition, domain, ordered binder, hypothesis,
conclusion, proof boundary, translation, correction, erratum, and boundary case. They must decide
the category formulation, empty-space/nonemptiness treatment, metric versus pseudometric versus
topological presentation, separation, and countable-family encoding.

A fresh statement run can then encode only that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change, statement receipt, worker `[_]`, proof credit, or
master acceptance is claimed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json` is emitted.
