# Exact-statement gate: blocked

Item: `S56-M-0286-STATEMENT`

Theorem: `THM-M-0286` (Egorov's theorem)

Base revision: `d1b510bacab792f84a99231485cf4429fdb78978` (tree
`f77c4e4db196fc0ecc271815514a411d06ea6053`).

## Decision

The statement item remains `[ ]`. The repository identifies Egorov's theorem only by the gloss
"the relationship between almost-everywhere convergence and uniform convergence." It does not
provide or cite a binder-complete proposition. In particular, it does not fix:

- the direction of the claimed relationship;
- the domain, codomain, measure, and globally finite versus finite-subset setting;
- a natural-number sequence versus a generalized countable directed index;
- strong measurability of the functions and limit versus measurability of their pointwise
  extended distances;
- the exact almost-everywhere premise and its working set;
- the exceptional set's measurability, containment, and strict or non-strict measure bound;
- complement versus retained-set presentation and the exact uniform-convergence predicate; or
- the ordered quantifiers and empty, null, infinite-measure, nonseparated, and index boundary
  cases.

These choices change the proposition. The intake identified a modern statement in immutable
Encyclopedia of Mathematics revision 28515 and the bibliographic lead D. F. Egorov, *Sur les
suites de fonctions mesurables*, *C. R. Acad. Sci. Paris* 152 (1911), pages 244-246. But the
primary pages were not retrieved or admitted, and there is no reviewed French transcription,
incorporated-definition map, exact premise and conclusion map, translation, correction or errata
audit, proof boundary, or independent approval. The secondary source also distinguishes its
modern measure-space form from Egorov's original Lebesgue-measure-on-the-line scope.

Selecting a familiar classical formulation or the nearest pinned declaration would therefore
invent, narrow, broaden, or substitute mathematics. Rev-5.6 sections 5 and 5.1 make statement
ambiguity and a missing elaborated-expression fingerprint hard blockers. There is no canonical
expression for which minimal imports, checked transports, or the four required mutations can
truthfully be certified. The root vector remains `[H1, M3, R4]`.

The prerequisite intake is provisionally `[_]`, but its receipt is expressly unaccepted and
non-content-addressed and has no accepted receipt ID. This statement inspection is topologically
ordered, yet dependency acceptance and master acceptance would still be required after any future
statement self-test.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` re-elaborates with
`Mathlib.MeasureTheory.Function.Egorov` in the pinned environment. It exposes four materially
different exact-topic interfaces:

1. `MeasureTheory.tendstoUniformlyOn_of_ae_tendsto_of_measurable_edist` works on a measurable
   finite-measure subset and assumes measurable pointwise extended distances.
2. `MeasureTheory.tendstoUniformlyOn_of_ae_tendsto` uses the same subset conclusion but assumes
   strong measurability of every function and the limit.
3. The first primed declaration replaces the subset setting with a global `IsFiniteMeasure`
   instance and concludes uniform convergence on an exceptional set's complement.
4. The second primed declaration combines global finite measure with strong measurability.

All four use a `Countable`, `Nonempty`, `SemilatticeSup` index and a
`PseudoEMetricSpace` codomain. None is expression-identical to a source-selected natural-number,
real-valued theorem because no such source selection exists. The probe reports
`[propext, Classical.choice, Quot.sound]` for three representative candidates, but declares no
canonical target or proof body. Its import is minimal only for that discovery probe, not for an
absent canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symbolic link was used read-only. No `lake update`, `lake build`,
clone, fetch, or other dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0286` | 0 | rank 1292; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| `git blame -L 2055,2060 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean 4.29.0 and Lake 5.0.0 versions recorded above |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'` and `git status --short` | 0 | revision and tree above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0286/IntakeProbe.lean` | 0 | one supporting definition and four direct interfaces elaborated; combined output 3174 bytes, SHA-256 `464b3a706f14c55c7158b6e30b175ba6586a88618cdda1bf128c20bedcaf871f`; no target or proof body |
| bounded exact-topic `rg` search in repo-local Lean, the owned probe, and pinned `Egorov.lean` | 0 | 38 lines, 5515 bytes, SHA-256 `e7883aad0ae0146d10b5af767be037b77341a4c505d1bb0b685dd9c17b31fc1a`; only the pinned family module and owned probe matched |
| `python3 -B Stage1_Instances/THM-M-0286/check_intake.py` before these artifacts | 1 | historical intake replay stops at line 183 because it expects intake state `[ ]`; current authority records provisional `[_]` and attempts 1 |
| prohibited-construct scan over owned Lean files | 1 | expected no match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0286/statement-blocker.json` and the scoped invariant check | 0 each | blocker identity, null target/import/hash, unchanged vector, undefined mutations, false completion and receipt fields, exact two-file scope, and no-self-test boundary agree |
| scoped tracked and no-index whitespace checks | 0 / 1 per new file | no whitespace diagnostics; each no-index exit 1 is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest absent because the exact-statement deliverable did not pass |

The intake checker freezes the intake run's original authority state and nine-file artifact
inventory. It is historical intake evidence, not a statement-phase validator. This run records its
stale-state failure rather than rewriting the intake instance, receipt, checker, task DAG,
generated blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

An accountable source reviewer must preserve and hash a lawful complete primary or authoritative
source edition, select one exact result, transcribe all incorporated definitions, ordered binders,
hypotheses, conclusion, proof boundary, translations, corrections, and boundary cases, and
independently approve its identity with `THM-M-0286`. That review must explicitly decide the
original line/Lebesgue scope versus a modern measure-space generalization.

A later statement run can then encode precisely that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute the removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations. The integration lane must also revalidate and master-accept the intake dependency before
accepting that later transition.

This blocker is the assigned phase's truthful result, not completion. Lifecycle remains
`planned`; `audit_complete: false` and `theorem_complete: false`. No exact statement,
minimal-import claim, statement fingerprint, checked transport, mutation certificate, proof
credit, node receipt, worker `[_]`, debt-vector change, or master acceptance is claimed. Because
the assigned deliverable did not self-test, `.stage1-worker-selftest.json` remains absent.
