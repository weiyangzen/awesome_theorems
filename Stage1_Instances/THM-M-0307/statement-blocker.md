# Exact-statement gate: blocked

Item: `S56-M-0307-STATEMENT`

Theorem: `THM-M-0307`

Base revision: `0e5ae82e6d507ee607c3f011900571ffd8096800` (tree
`400e6edf1f69b971b60a367e3ea29be359b07907`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0307-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`; its receipt says `accepted: false` and has no accepted
receipt ID. Rev-5.6 section 10.2 permits provisional preparation of a later node when concurrency is
enabled, but master closure remains dependency ordered.

Independently, the exact-statement gate fails. The repository supplies only the title `迹定理`
(`trace theorem`), the attribution Sergei Sobolev, the year 1936, and the gloss
`Sobolev函数在边界上的限制` (restriction of Sobolev functions to the boundary). It gives no
bibliography, truth-valued proposition, incorporated definitions, ordered binders, hypotheses,
conclusion, proof boundary, correction history, or independently reviewed source crosswalk. Its
`已验证` label is untrusted metadata under rev-5.6.

The intake records Zhonghai Ding's 1996 exact-topic paper as a modern bibliographic lead only. The
repository does not select that paper or one of its formulations as this Sobolev/1936 target, and
no accepted review maps its definitions, hypotheses, conclusion, genealogy, corrections, or
errata. A statement still must choose, among other proposition-changing alternatives:

- the Euclidean, manifold, half-space, or other ambient setting, dimension, domain, and regularity;
- the topological, reduced, measure-theoretic, or manifold boundary and its surface measure;
- the Sobolev model, order, exponent, endpoint range, value space, and representative semantics;
- an `L^p`, fractional Sobolev, Besov, Hilbert-scale, or other boundary trace codomain;
- the trace construction, dense-class agreement, norm estimate, and constant dependencies;
- existence and boundedness alone, or also uniqueness, surjectivity, a bounded right inverse, or a
  kernel characterization; and
- ordered binders, universes, typeclass context, empty or irregular domains and boundaries,
  low-dimensional cases, critical exponents, and every other degenerate case.

These variants are not notation changes. Selecting the familiar bounded-Lipschitz
`W^{1,p}`-to-`L^p` theorem, a sharper fractional-codomain theorem, or a smooth-domain Hilbert-scale
theorem would invent or substitute mathematics. Pointwise restriction of an arbitrary
almost-everywhere class or restriction of only smooth functions would not state the extension
of the trace map. The neighboring Sobolev embedding, Poincare, Friedrichs, extension, and
Rellich-Kondrachov targets cannot replace this root.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. There is consequently no canonical expression whose imports can be
certified minimal, no checked alternate transport, and no meaningful removed-hypothesis,
changed-domain, changed-binder-scope, or boundary-case mutation. Those mutations are undefined,
not passed. No `Statement.lean`, statement receipt, theorem declaration, or proof body was added.
The lifecycle stays `planned` and the provisional root vector stays `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated using the pinned environment. It imports:

```lean
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Geometry.Manifold.IsManifold.InteriorBoundary
import Mathlib.MeasureTheory.Function.LpSpace.Basic
```

It checks six adjacent `Lp`, measure-restriction, manifold-boundary, and smooth
Gagliardo-Nirenberg-Sobolev interfaces. These APIs do not select a Sobolev model, construct a
boundary surface measure or trace operator, state the source root, or supply a proof body. The
probe's imports therefore cannot be certified minimal for the absent canonical target. Its complete
stdout is 1,689 bytes with SHA-256
`fe2590907c8cf50882c7a2922ea3b85bad5a4628ef049606a80d89b2b6052ee5`.

A bounded exact-topic search of pinned mathlib found no `TraceOperator`, `SobolevTrace`, or Sobolev
boundary-trace declaration. Repository-local matches are legacy planning and boundary records,
including a dossier that explicitly says no terminal trace interface was located. This is narrow
discovery evidence only, not the downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was used read-only, and the pinned mathlib worktree remained
clean. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation ran.

## Validation Record

Commands ran in this isolated automation clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0307` | 0 | rank 1308; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| exact `sha256sum` command over authority, source, toolchain, lock, and intake inputs as listed in `statement-blocker.json` | 0 | all digests matched the structured fingerprints; inspection confirmed provisional intake, null target, source ambiguity, exclusions, and open downstream tasks |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0307/IntakeProbe.lean` | 0 | six adjacent interfaces elaborated; output size and hash recorded above; no canonical target or proof body |
| bounded exact-topic `rg` over pinned mathlib | 1 (expected no match) | no exact trace-operator or Sobolev boundary-trace declaration found; discovery only |
| bounded repository Lean `rg` | 0 | only nonterminal legacy planning/boundary records matched; no exact target declaration or proof body identified |
| `python3 -B Stage1_Instances/THM-M-0307/check_intake.py` | 1 | the historical intake replay stops at its first stale authority hash after integration changed the blueprint/DAG intake cursor; it was not modified or represented as statement validation |
| prohibited-declaration `rg` scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0307/statement-blocker.json` and scoped invariant assertions | 0 | structured blocker parses and its identity, null target/imports, unchanged vector, four undefined mutations, false completion fields, exact two-file scope, and absent self-test agree |
| scoped `git diff --check` and per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; each raw no-index exit 1 is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | root self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is bound to its intake worker's earlier revision, authority hashes,
and original nine-file inventory. Integration subsequently recorded intake `[_]` and changed those
authority files. Rewriting historical intake evidence is outside this phase and would not cure the
missing proposition.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake before accepting a future statement transition.
Accountable reviewers must preserve and hash a lawful immutable primary or authoritative source,
select one exact truth-valued trace proposition, map every incorporated definition and assumption,
fix every domain, boundary, surface-measure, Sobolev, parameter, trace-space, construction,
estimate, strength, binder, and degenerate-case choice, audit genealogy, translations, corrections,
and errata, reconcile the duplicate record and neighboring-target boundaries, and independently
approve the mapping.

A later statement worker can then encode precisely that approved claim, minimize pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport, and
run all four required mutation classes.

This records the first failed gate. It does not complete the statement node or any downstream node.
`audit_complete` and `theorem_complete` remain false, and no debt-vector change is proposed. Because
the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, node-specific
completion receipt, worker `[_]`, proof credit, or master acceptance is claimed.
