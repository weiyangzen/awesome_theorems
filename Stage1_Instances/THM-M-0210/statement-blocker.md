# Exact-statement gate: blocked

Item: `S56-M-0210-STATEMENT`

Theorem: `THM-M-0210`

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0210-INTAKE` is provisional `[_]`, not
master accepted. Independently, the authoritative repository record does not identify one exact
proposition that can be elaborated without inventing or substituting mathematics.

The catalog supplies only the title Desargues's theorem, the attribution Girard Desargues, the
year 1648, and the gloss `两个三角形透视的条件` ("the condition for two triangles to be in
perspective"). It gives no bibliography, theorem locator, formula, direction, definitions,
ordered binders, hypotheses, proof boundary, correction history, or reviewer. Stage0 explicitly
leaves the exact definitions and premises open, and rev-5.6 treats `已验证` as untrusted metadata.

The intake deliberately leaves unresolved choices that materially change the proposition:

- point-perspective implies line-perspective, the converse, an equivalence, or Hilbert's affine
  parallel-side specialization and converse;
- an abstract projective plane, a coordinatized projective plane, an affine or Euclidean plane,
  or a spatial incidence model;
- ambient dimension, scalar field or division ring, commutativity, characteristic, and incidence
  or coordinatization axioms;
- representations of triangles, correspondence, joins, meets, concurrency, and collinearity;
- finite side intersections versus points at infinity, with exact binder order and transports; and
- all distinctness, noncollinearity, noncoincidence, coplanarity, and degenerate cases.

The inspected Magaud-Narboux-Schreck paper states a conventional projective point-to-line
implication and stresses the abstract-plane/dimension boundary. Hilbert's Section 22, Theorem 32
states a different affine parallel-side specialization and its converse. Neither source is cited
by the catalog or independently accepted as its exact proposition. Selecting either now would
silently choose a theorem rather than elaborate the received target.

Section 5 of the rev-5.6 blueprint makes statement ambiguity and a missing expression fingerprint
hard blockers. There is consequently no canonical expression for which minimal imports, checked
alternate transports, or the removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations can be certified. Those mutations are not runnable, not passed. The root
vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated using its three direct imports:

- `Mathlib.LinearAlgebra.AffineSpace.FiniteDimensional`;
- `Mathlib.LinearAlgebra.Projectivization.Constructions`; and
- `Mathlib.LinearAlgebra.Projectivization.Subspace`.

Its eleven `#check` commands passed for adjacent affine-collinearity, projectivization,
projective-subspace, and three-coordinate cross-product interfaces. The probe declares no
canonical Desargues target, checked transport, or proof body. Because the target is unidentified,
these imports cannot be called minimal for it and receive no statement or proof credit.

A bounded exact-topic search of repo-local Lean and pinned mathlib found no declaration or
documentation match for Desargues or perspective triangles. This narrow result is feasibility
evidence only, not the downstream precommitted anchor audit and not proof of global absence. The
inspected Coq formalization is outside this repository's pinned Lean closure.

The environment was Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink and pinned
artifacts were used read-only. No update, build, clone, fetch, or other dependency mutation ran.

## Commands And Exact Results

Commands ran in the isolated worker checkout on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0210` | 0 | rank 1226; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before edits; `git rev-parse HEAD 'HEAD^{tree}'` | 0 each | only the automation-provided `.lake` symlink was untracked; base revision and tree are above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | 0 each | pinned mathlib revision and tree above; package status output empty |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0210/IntakeProbe.lean` | 0 | eleven adjacent APIs elaborated; stdout SHA-256 `07f989ac9c58115650558ee1ad5764b88d3f3b29ff34a7bfda38378ff69ed483`; no target declaration or proof body |
| exact-topic `rg` over repo-local Lean and pinned mathlib, with the pattern and paths recorded in `statement-blocker.json` | 1 | expected no-match result; no Desargues or perspective-triangle match |
| `python3 -B Stage1_Instances/THM-M-0210/check_intake.py` | 1 | historical intake checker expects the authoritative intake item to remain `[ ]`; the integrated DAG now records `[_]`; it is not a statement gate and was not modified |
| prohibited-declaration `rg` over owned Lean files, with the pattern recorded in `statement-blocker.json` | 1 | expected no match; no prohibited declaration token in the owned Lean probe |
| `python3 -m json.tool Stage1_Instances/THM-M-0210/statement-blocker.json` plus the scoped blocker invariant check | 0 each | identity, null target/imports/fingerprints, unchanged vector, false completion fields, four unrunnable mutations, and absent worker self-test agree |
| scoped `git diff --check` and new-file whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake receipt remains provisional, mutable worker evidence with `accepted=false`.
Rewriting its earlier snapshot or checker is outside the statement phase and would not resolve the
missing proposition.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake before an accepted statement transition.
Accountable reviewers must preserve and hash one lawful immutable primary or authoritative source,
select and independently approve its exact proposition and incorporated definitions, and freeze
the direction, incidence model and axioms, dimension and scalars, ordered binders, hypotheses,
conclusion, intersection and infinity conventions, transports, corrections, and all boundary
cases. A later worker can then encode only that claim, minimize its pinned imports, serialize and
hash the elaborated expression and environment, compile every credited transport, and run all four
required mutation classes.

This artifact records the first failed gate. It does not complete this or any downstream node. No
canonical statement, node receipt, proof credit, accepted state, audit completion, theorem
completion, or master acceptance is claimed. Because the assigned phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json` is emitted.
