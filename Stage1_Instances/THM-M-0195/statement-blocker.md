# Exact-statement gate: blocked

Item: `S56-M-0195-STATEMENT`

Theorem: `THM-M-0195`

Base revision: `2eea98305d46266f078a50cf0e85853bf6a5e702` (tree
`02279a8caa5f31ed8e37e35c8584a336eed9b974`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0195-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits dependency-ordered
preparation, but master closure remains dependency ordered. Independently, the exact-statement
gate fails before target elaboration.

The repository supplies only the title Euler line theorem and the gloss that the orthocenter,
centroid, and circumcenter of a triangle are collinear. It gives no cited proposition, triangle or
center definitions, ordered binders, ambient dimension, nondegeneracy convention, exact conclusion,
proof boundary, correction history, or boundary-case policy. The `已验证` label is untrusted
metadata.

The intake located Euler's E325 and relevant historical center and ratio passages, but it did not
admit an immutable complete Latin statement, definition, assumption, proof, correction, translation,
or independent-review packet. In particular, it explicitly left open whether the root asserts only
set collinearity or also Euler-line order, the position equation, or the ratio.

Those omissions are proposition-changing. An exact target must still decide:

- a Euclidean plane or a general affine inner-product-space carrier and its dimension;
- an ordered affinely independent triangle or another exact triangle and nondegeneracy predicate;
- source-faithful definitions and Lean transports for orthocenter, centroid, and circumcenter;
- rank-based set collinearity, affine-span membership, existence of a line, ordered placement,
  position, ratio, or a source-approved conjunction; and
- repeated and collinear vertices, equilateral coincidence, right and obtuse triangles,
  higher-dimensional embeddings, and vertex reindexing.

Silently choosing the familiar `Affine.Triangle` candidate would exclude degenerate triangles and
permit arbitrary ambient dimension. Silently choosing the stronger equation
`H = 3 • (G - O) + O` would add position and ratio content beyond the catalog gloss. Conversely,
asserting a unique Euler line would mishandle an equilateral triangle, where all three centers
coincide. None of these choices may be inferred from a theorem name.

Rev-5.6 makes statement ambiguity and a missing expression fingerprint hard blockers. There is no
honest canonical declaration whose imports can be certified minimal, no approved alternate form
for a checked transport, and no canonical target against which removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can run. Those mutations are undefined, not
passed. The provisional vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with the single direct import
`Mathlib.Geometry.Euclidean.MongePoint`. It checks the triangle, centroid, circumcenter,
orthocenter, collinearity, affine-span, altitude, and position interfaces. All ten checks pass.
Both recorded theorem axiom diagnostics are exactly `propext`, `Classical.choice`, and
`Quot.sound`.

Pinned mathlib contains the stronger candidate
`Affine.Triangle.orthocenter_eq_smul_vsub_vadd_circumcenter`, and its module documentation describes
Euler-line order and ratio. This authenticates a useful formal surface only. The probe declares no
canonical target, checked transport, or proof body, and its import cannot be certified minimal for
an absent target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was reused;
no update, build, clone, fetch, or other dependency-mutation command was run.

## Validation Record

Commands ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0195` | 0 | rank 1224; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base revision and tree appear above |
| repository authority, source crosswalk, scope map, task DAG, and intake inspection | 0 | confirmed the sparse catalog wording, provisional dependency, null target, unresolved source boundary, and lack of an approved proposition |
| `sha256sum` over authority, source, intake, probe, toolchain, lock, and pinned mathlib inputs | 0 | exact current digests recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision and tree match the values above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0195/IntakeProbe.lean` | 0 | ten adjacent interfaces elaborated; output was 2,484 bytes with SHA-256 `b3cda0db83d11fcfdae2809de7adbdabe6b08cd0bd0e3b16bd8b0c6ba2c90796`; no target or proof body |
| bounded Euler-line and center search in pinned mathlib and repo-local Lean | 0 | found the expected mathlib position, order, and ratio interfaces but no repo-local canonical target; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-0195/check_intake.py` | 1 | historical intake checker expects the pre-integration intake state `[ ]` and attempts 0 while authority now records `[_]` and attempts 1; its frozen authority hashes also predate the current shared authority |
| prohibited declaration scan over owned Lean files | 0 | inner search returned expected no-match exit 1; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and scoped blocker-invariant assertions | 0 | identity, null target, unchanged vector, four undefined mutations, false completion flags, two-file scope, no receipt, and no-self-test boundary agree |
| scoped `git diff --check` and new-file no-index checks | 0 aggregate | no whitespace diagnostics; no-index exits were only expected new-file differences |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker is a historical receipt checker. It binds intake-time authority hashes, the
original authoritative state, and an intake-only file inventory. This phase records that stale
boundary rather than rewriting intake evidence to manufacture agreement.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash one lawful immutable primary or authoritative source,
locate and independently approve the exact proposition and proof boundary, and map every
incorporated definition, binder, hypothesis, conclusion, correction, translation, and boundary
case. They must explicitly settle ambient dimension, triangle nondegeneracy, center definitions,
bare collinearity versus order/position/ratio, equilateral coincidence, and all other degeneracies.
The integration lane must master-accept refreshed intake evidence before accepting a later statement
transition.

A fresh statement run can then encode only that approved claim, minimize pinned imports, serialize
the elaborated expression and environment, compile every credited transport, and run all four
required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
