# Exact-statement gate: blocked

Item: `S56-M-0629-STATEMENT`

Theorem: `THM-M-0629`

Base revision: `444860f481e8bbf64a3357008fd4d01a52006f08` (tree
`dee24a14497f877ebd81712a99d2da08de62d7ad`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0629-INTAKE` is provisional worker
state `[_]`, which permits this dependency-ordered statement attempt but is not master-accepted
`[x]` evidence for a final accepted transition. The decisive blocker here is that the exact Lean 4
target cannot be truthfully elaborated from the available source record.

The repository catalog supplies only the title `一点紧化定理`, the 1924 Alexandrov attribution,
and the gloss `局部紧Hausdorff空间的一点紧化` (one-point compactification of a locally compact
Hausdorff space). It supplies no formula, definition chain, ordered binders, hypotheses, exact
conclusion, proof boundary, correction, erratum, or independent statement review. The catalog
label `已验证` is untrusted metadata under rev-5.6.

The intake did locate Alexandroff's 1924 `Fundamentalsatz 1`, journal page 296. The displayed
passage says that every locally `bikompakt` topological space which is not itself `bikompakt` can
be completed by adjoining one point to a `bikompakt` space, uniquely. Page 297 warns that the
analogous merely `kompakt` construction need not be unique. This is a strong primary-source lead,
but it has not been independently approved as an exact modern compact-Hausdorff proposition. Its
historical terminology, imported definitions and results, translation, proof boundary,
correction/errata status, and precise meaning of completion and uniqueness remain open.

Those open decisions change the proposition. In particular, the source and formal review must
still fix:

- whether the input convention is weak or strong local compactness plus Hausdorffness;
- whether `NoncompactSpace X` is an explicit premise and whether density belongs to the root;
- whether compactification is a construction, an existence claim, bundled embedding data, or an
  exact conjunction of compactness, separation, embedding, density, and singleton complement;
- whether uniqueness is equality, equivalence, or homeomorphism over the selected embedding; and
- universes, binder order, typeclass context, boundary cases, and every credited alternate form.

Mathlib deliberately adds an isolated infinity when `X` is compact, so the canonical embedding is
not dense in that case. Adding noncompactness or omitting density without source approval would
therefore change the theorem. Selecting a convenient conjunction of available interfaces would
invent rather than elaborate the target.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a missing expression
fingerprint hard blockers. There is consequently no canonical expression for which imports can be
certified minimal, no elaborated expression or target-environment fingerprint, no credited
alternate transport, and no meaningful removed-hypothesis, changed-domain, changed-binder-scope,
or boundary-case mutation. These mutation classes are undefined, not passed. No statement, Lean
declaration, import claim, axiom, placeholder, broadened theorem, or proof body was added. The root
remains `[H1, M3, R4]`; audit and theorem completion are false.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with the pinned environment. Its
single direct import, `Mathlib.Topology.Compactification.OnePoint.Basic`, exposes the construction,
extra point, singleton-complement equation, canonical open embedding, density and dense embedding
under `NoncompactSpace`, unconditional compactness, T4 separation under weak local compactness and
Hausdorffness, and the homeomorphism interface
`OnePoint.equivOfIsEmbeddingOfRangeEq`.

The probe succeeds and its complete output has SHA-256
`078ac09e10ddbbb1299c74f8037a72b898ad42dd99723e492b19ed6d50632384`. The four diagnostic
declarations report only `propext`, `Classical.choice`, and `Quot.sound`. It nevertheless declares
no target or proof body, composes no source-approved property bundle, and supplies no checked
historical-to-modern transport. The module is the exact-topic candidate, but cannot be certified
as the canonical target's minimal import until that target exists.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused read only. No update, build, clone, fetch, or
dependency mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai), from the repository root
unless another working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0629` | 0 | rank 1322, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| manifest, blueprint, execution skill, intake, source crosswalk, and primary-passage inspection | 0 | intake deliberately freezes a null canonical claim and target at `[H1, M3, R4]`; proposition-changing source decisions remain open |
| `git blame -L 4664,4669 -- Docs/researches/math_theorems.md` and scoped SHA-256 checks | 0 | all six uncited catalog lines originate at `bcf3f9fa...`; authority, source, intake, toolchain, and mathlib fingerprints are recorded in the JSON blocker |
| `python3 -B Stage1_Instances/THM-M-0629/check_intake.py` | 1 | historical intake replay stops at its frozen execution-DAG intake-entry hash after authority regeneration; this phase records rather than rewrites prior evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| pinned mathlib revision, tree, and package-status checks | 0 | revision and tree agree with the fingerprint; the package worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0629/IntakeProbe.lean` | 0 | direct adjacent OnePoint interfaces elaborated; no canonical target was declared |
| prohibited Lean construct scan over the owned path | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse, scoped blocker invariants, and whitespace checks | 0 | identity, open state, null target/imports, unchanged vector, undefined mutations, false completion flags, exact two-file scope, and text hygiene passed |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable did not pass |

The historical intake receipt declares `accepted: false`, is provisional and non-content-addressed,
and has no accepted receipt ID. That does not prevent provisional later-node preparation, but it
cannot support master acceptance. This statement phase does not rewrite that receipt, its
validator, the target-local task DAG, the generated checklist, or the authoritative execution DAG
to create agreement.

## Retry Condition And Status Boundary

For a fresh provisional statement attempt, accountable reviewers must preserve and hash an
immutable primary or approved authoritative source, independently approve one exact modern
proposition and locator, and map every incorporated definition, binder, premise, conclusion, proof
dependency, correction, erratum, translation, and boundary case. The review must fix the
historical compactness terminology, local-compactness convention, noncompactness/density policy,
property bundle, completion convention, and exact uniqueness notion. The integration lane must
also refresh, revalidate, and master-accept the intake evidence before any accepted `[x]`
transition.

A fresh statement worker may then encode precisely that source-selected claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

The first failed gate is exact source-statement identity. This is blocked-attempt evidence, not
completion of the statement node or any downstream node. No statement receipt, worker `[_]`, proof,
audit completion, theorem completion, or master acceptance is claimed. Because the assigned phase
did not pass its completion gate, no `.stage1-worker-selftest.json` is emitted.
