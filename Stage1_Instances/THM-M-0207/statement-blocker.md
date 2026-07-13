# Exact-statement gate: blocked

Item: `S56-M-0207-STATEMENT`

Theorem: `THM-M-0207`

Base revision: `48abbb2d2eeb89816c5ffc0ad8faafa4b9d24dd0` (tree
`0f26e2c78fb5fff9277cbbdfef5e145fd4ef06f1`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0207-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Its receipt is explicitly unaccepted and
non-content-addressed, and it supplies no accepted receipt ID. Dependency-ordered preparation is
possible, but master closure remains dependency ordered.

Independently, the exact-statement gate fails. The repository supplies only the title
`拿破仑定理` (Napoleon's theorem), an attribution and date, and the gloss `三角形外正三角形中心构成正三角形`
(the centers of equilateral triangles constructed externally on a triangle form an equilateral
triangle). It gives no bibliography, exact proposition, definition chain, ordered binders,
hypotheses, conclusion, proof boundary, corrections, errata, or independent reviewer. Its
`已验证` value is untrusted catalog metadata under rev-5.6.

The gloss identifies the classical external Napoleon-theorem family, but it does not fix one
formal proposition. The following proposition-changing choices remain open:

- a Euclidean plane, `Complex`, a two-dimensional oriented real inner-product affine space, or a
  more general ambient space;
- ordered points versus an affine-independent `Affine.Triangle`, and whether coincident or
  collinear inputs are excluded;
- the meaning of "external," including the orientation or opposite-half-plane rule and the
  endpoint order for each side;
- the construction and side correspondence of all three equilateral triangles;
- centroid, circumcenter, incenter, orthocenter, or another meaning of "center";
- an output `Affine.Triangle` with `Equilateral`, three distance equalities, or another conclusion
  encoding, including whether output nondegeneracy is asserted; and
- clockwise versus counterclockwise input, zero-length sides, the two equilateral third-vertex
  choices, coincident centers, and other boundary cases.

These are not notation choices. `Affine.Triangle` itself bundles affine independence, so selecting
it would silently add nondegeneracy. Choosing centroids because the classical centers coincide in
an equilateral triangle would still require a source decision or a checked transport. Reversing an
ordered input can change a naive orientation-based selection of the outward vertices. Selecting a
customary formulation from mathematical familiarity would therefore invent or strengthen missing
parts of the received proposition.

The intake correctly leaves the canonical human statement, Lean module and expression, minimal
imports, and expression and environment fingerprints null. Rev-5.6 sections 5 and 5.1 make
statement ambiguity and a missing elaborated-expression fingerprint hard blockers. Consequently
there is no canonical target whose imports can be certified minimal, no credited alternate form
for a checked transport, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation. Those mutations are undefined, not passed. No
`Statement.lean`, statement receipt, theorem declaration, proof body, or debt-vector change was
created. The provisional vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the single direct import
`Mathlib.Geometry.Euclidean.Simplex`. It checks eight adjacent affine-triangle, equilateral,
distance, centroid, and angle interfaces. All checks pass, and the three printed support lemmas
report only `propext`, `Classical.choice`, and `Quot.sound`.

The probe constructs no outward equilateral triangle, chooses no center convention, states no
Napoleon target, and supplies no proof body. Its import is sufficient for the probe but cannot be
certified minimal for an absent canonical target. A bounded exact-topic search found no Napoleon
or outward-equilateral construction declaration in pinned mathlib or repository-local Lean. This
is narrow statement-feasibility evidence, not the downstream immutable anchor audit or a global
absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only, and the pinned mathlib worktree remained
clean. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation ran.

## Validation Record

Commands ran in this isolated automation clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0207` | 0 | rank 1538; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` before editing | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| authority, source, intake, scope, crosswalk, receipt, and task-DAG inspection | 0 | confirmed provisional dependency, sparse catalog claim, null canonical target, and unresolved domain/orientation/construction/center/conclusion/boundary choices |
| exact `sha256sum` over authority, source, intake, toolchain, lock, and pinned source inputs | 0 | digests agree with `statement-blocker.json` |
| `git blame -L 1492,1497 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision, tree, and worktree inspection | 0 | revision and tree match the recorded fingerprint; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0207/IntakeProbe.lean` | 0 | eight adjacent interfaces elaborated; stdout 3,013 bytes, SHA-256 `6809bfc4d703ae1d14369f617c6b533e4ae446dbca2e1454ef2b784a50ef39f5`; no target or proof body |
| bounded exact-topic `rg` over pinned mathlib and repository-local Lean | 0 overall | only the intake probe disclaimer matched; no target-specific pinned declaration was found; discovery only |
| `python3 -B Stage1_Instances/THM-M-0207/check_intake.py` | 1 | the historical checker expects its intake-time authoritative state `[ ]`; integration now records provisional `[_]`, so this phase records rather than rewrites stale intake evidence |
| prohibited Lean declaration scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0207/statement-blocker.json` and scoped invariant assertions | 0 | structured blocker parses; identity, hashes, null target/imports, unchanged vector, four undefined mutations, false completion fields, exact two-file scope, and absent self-test agree |
| scoped `git diff --check` plus per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; each raw no-index exit 1 is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is bound to its intake worker's earlier authoritative cursor and
artifact inventory. Integration subsequently recorded the intake as provisional `[_]`. Rewriting
the checker, receipt, instance, local task DAG, generated blueprint, or authoritative execution DAG
would be outside this phase and would not cure the missing proposition.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before accepting a later
statement transition. Accountable reviewers must lawfully preserve and hash one immutable primary
or approved authoritative source, select and independently approve one exact proposition, and map
every incorporated definition, domain, ordered binder, hypothesis, conclusion, proof boundary,
translation, correction, erratum, and boundary case. They must fix the Euclidean model and
dimension, input order and nondegeneracy, outward construction and orientation, side
correspondence, center convention, output predicate, and degenerate cases.

A fresh statement worker can then encode precisely that approved claim, minimize pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, node-specific completion receipt,
worker `[_]`, statement fingerprint, proof credit, or master acceptance is claimed.
