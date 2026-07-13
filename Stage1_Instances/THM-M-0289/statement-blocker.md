# Exact-statement gate: blocked

Item: `S56-M-0289-STATEMENT`

Theorem: `THM-M-0289`

Base revision: `997541734bb32f987fb15f163335a82512992120` (tree
`2c866b9d840d48c48ac839740c62d3b9440be0e5`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0289-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`; its receipt is unaccepted and not content-addressed.
Rev-5.6 section 10.2 permits provisional preparation of a later node when concurrency is enabled,
but master closure remains dependency ordered.

Independently, the exact-statement gate fails. The catalog supplies only the title
"Hardy-Littlewood maximal function theorem", the Hardy/Littlewood attribution, the year 1930, and
the gloss "weak-type estimate for the maximal function". It supplies no exact formula, source
locator, incorporated definitions, ordered binders, hypotheses, conclusion, proof boundary,
correction history, or independently reviewed source crosswalk. Its catalog `verified` label is untrusted
metadata under rev-5.6.

The intake verified bibliographic metadata for Hardy and Littlewood, "A maximal theorem with
function-theoretic applications", *Acta Mathematica* 54 (1930), 81-116, DOI
`10.1007/BF02547518`. Direct article requests returned access HTML rather than the source text, so
no theorem, definition, hypothesis, proof, correction, or errata locator was inspected or
preserved. That is an `H1` primary-source lead, not an exact statement.

The missing choices are proposition-changing:

- centered versus uncentered maximal operator and balls, closed balls, cubes, or another family;
- the ambient domain, dimension, metric or norm structure, measure, and scalar codomain;
- the function model, measurability and integrability conditions, and representative semantics;
- radii, zero-measure averages, normalization, threshold type and positivity, and strictness;
- the explicit or existential constant and its dimension or doubling dependence;
- weak `(1,1)` alone versus any strong-type consequence; and
- zero or infinite thresholds, zero functions, dimension zero, infinite values and integrals, and
  all other boundary cases.

The repository also schedules `THM-M-0368` with the same family, attribution, year, and weak-type
gloss. That is compelling duplicate evidence, but there is no accepted identity, canonical-root
ownership, or evidence-transport decision. Reusing its scope would cross target ownership without
authority.

Choosing the familiar centered Euclidean statement, an uncentered cube statement, or a generalized
doubling-space statement would therefore invent or substitute mathematics. Sections 5 and 5.1 of
the blueprint make this ambiguity and the missing expression fingerprint hard blockers. There is
no canonical expression whose imports can be certified minimal, no credited alternate encoding,
and no meaningful removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case
mutation. Those mutation classes are undefined, not passed. No `Statement.lean`, theorem
declaration, proof body, or completion receipt was added. The lifecycle stays `planned` and the
root vector stays `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. It imports:

```lean
import Mathlib.MeasureTheory.Covering.Besicovitch
import Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar
```

It checks six adjacent ball, Haar-measure, lower-integral, Besicovitch, and Vitali interfaces. The
probe completed with 1,002 stdout bytes and SHA-256
`5ca1eab26e3bd0816d4ff5fe9d65b17d305e39706da332e2155d38a9c3501ccd`. It defines no maximal
operator, source root, checked transport, or proof body. These imports therefore cannot be called
minimal imports for the absent canonical target.

A bounded exact-topic search of pinned mathlib found no Hardy-Littlewood maximal-function
definition or weak-type theorem. The only repo-local Lean match was an unrelated Birkhoff
maximal-function planning phrase. These are narrow statement-surface observations, not the
downstream immutable anchor audit or a global absence claim.

The intake also records immutable source inspection of
`fpvandoorn/carleson@fdcce451.../Carleson/ToMathlib/HardyLittlewood.lean`, including
`hasWeakType_maximalFunction_one`. That is a credible external formal lead, but it uses a newer Lean
and mathlib, is absent from the local dependency closure, and has no accepted transport to an
inspected exact human claim. It receives no statement or proof credit here.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation ran.

## Validation Record

Commands ran in this isolated automation clone on 2026-07-13 (`Asia/Shanghai`). Full structured
arguments, input hashes, and exact result boundaries are in `statement-blocker.json`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0289` | 0 | rank 1295; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| authority, source, toolchain, lock, and nine intake-artifact SHA-256 checks | 0 | all digests agree with the structured blocker |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision, tree, and package-status checks | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0289/IntakeProbe.lean` | 0 | six adjacent interfaces elaborated; output size and digest recorded above; no canonical target or proof body |
| bounded exact-topic `rg` over pinned mathlib | 1 (expected no match) | no exact-topic maximal-function definition or weak-type theorem matched; discovery only |
| bounded repository Lean `rg` | 0 | only an unrelated Birkhoff planning phrase matched; no exact target or proof body |
| `python3 -B Stage1_Instances/THM-M-0289/check_intake.py` | 1 | historical intake replay stops at its frozen `[ ]` cursor because integration now records intake `[_]`; it was not changed or used as statement evidence |
| prohibited-declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parsing and scoped blocker assertions | 0 | identity, null target/imports, unchanged vector, four undefined mutations, false completion fields, exact scope, and absent self-test agree |
| scoped whitespace checks | 0 aggregate | no whitespace diagnostics; raw no-index exit 1 is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test packet intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

The integration lane must master-accept the intake before accepting a later statement transition.
Accountable reviewers must preserve and hash a lawful immutable primary or authoritative source,
inspect one exact theorem and all incorporated definitions, map and independently approve every
operator, averaging family, domain, function, threshold, normalization, constant, ordered binder,
hypothesis, conclusion, proof boundary, correction, erratum, and degenerate case, and resolve
`THM-M-0368` identity and root ownership.

A fresh statement worker can then encode precisely that approved claim, minimize pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This records the first failed gate. It does not complete the statement node or any downstream node.
`audit_complete` and `theorem_complete` remain false, and no debt-vector change is proposed. Because
the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, node-specific
completion receipt, worker `[_]`, proof credit, or master acceptance is claimed.
