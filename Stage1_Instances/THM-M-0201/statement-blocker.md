# Exact-statement gate: blocked

Item: `S56-M-0201-STATEMENT`

Theorem: `THM-M-0201`

Base revision: `48abbb2d2eeb89816c5ffc0ad8faafa4b9d24dd0` (tree
`0f26e2c78fb5fff9277cbbdfef5e145fd4ef06f1`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0201-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt has `accepted: false`, is
non-content-addressed, and provides no accepted receipt ID. Rev-5.6 permits dependency-ordered
preparation from provisional work, but master closure remains dependency ordered.

Independently, the exact-statement gate fails. The repository record supplies only the title
`托勒密定理`, Claudius Ptolemy attribution, the approximate date 150 CE, and the gloss that for a
quadrilateral inscribed in a circle the product of the diagonals equals the sum of the products of
opposite sides. It supplies no bibliography, immutable edition, exact proposition, definitions,
ordered binders, hypotheses, proof boundary, corrections, errata, or independent reviewer. Its
`已验证` label is untrusted metadata.

The intake therefore correctly leaves the canonical human statement and Lean target null. Its
scope map records proposition-changing choices that remain unresolved:

- whether the ambient domain is exactly the Euclidean plane or a higher-dimensional inner-product
  affine space containing a planar quadrilateral;
- how the ordered cyclic quadrilateral, circle or concyclicity, and side/diagonal roles are encoded;
- whether convexity, simple cyclic order, or a strict interior intersection of the diagonals is
  explicit or derived;
- whether all vertices, only consecutive vertices, or no vertices must be distinct; and
- how repeated or collinear points, zero-radius circles, boundary intersections, self-crossing
  orders, and other degenerate cases are treated.

These choices are not notation. Four unordered cospherical points do not select which pairs are
sides and diagonals. In ambient dimension above two, cosphericity is not by itself a planar-circle
condition. A strict diagonal-intersection witness excludes cases that a weak cyclic-polygon
definition may include. Selecting the convenient pinned declaration as the root would therefore
add hypotheses and ambient scope that the catalog did not specify. Selecting Ptolemy's inequality
would substitute a different theorem.

Rev-5.6 treats statement ambiguity and a missing expression fingerprint as hard blockers.
Consequently no canonical declaration, `Statement.lean`, minimal-import certificate, elaborated
expression, checked transport, or mutation fixture was created. The required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined, not passed. The
provisional root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned environment. Its exact-topic equality
candidate comes from `Mathlib.Geometry.Euclidean.Sphere.Ptolemy`:

```text
{a b c d p : P} ->
Cospherical {a, b, c, d} ->
angle a p c = pi -> angle b p d = pi ->
dist a b * dist c d + dist b c * dist d a = dist a c * dist b d
```

The fifth point and two `angle = pi` assumptions encode a point strictly inside both diagonal
segments. The module itself says this statement works around the absence of a cyclic-polygon API
and distinguishes strict from weak cyclicity. The probe also checks
`EuclideanGeometry.mul_dist_le_mul_dist_add_mul_dist`, the inequality for arbitrary four points,
only to confirm that it is a non-substitute. Both declarations report `propext`,
`Classical.choice`, and `Quot.sound` through Lean's axiom printer.

This is direct pinned interface feasibility evidence, not a source-approved root. The probe imports
both exact-topic modules for discovery; it does not establish the minimal imports for an absent
canonical target, compile a source transport, or install proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No update, build, clone, fetch, or other
dependency-mutation command was run. The pinned mathlib worktree was clean after validation.

## Validation Record

Commands ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0201` | 0 | rank 1533; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base revision and tree appear above |
| authority, source, scope, crosswalk, task DAG, receipt, and intake inspection | 0 | confirmed provisional dependency, sparse catalog claim, null canonical target, and unresolved source/domain/order/boundary choices |
| `sha256sum` over authority, intake, toolchain, lock, probe, and pinned exact-topic source inputs | 0 | exact digests are recorded in `statement-blocker.json` |
| `git blame -L 1450,1455 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision/tree match the values above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0201/IntakeProbe.lean` | 0 | `Cospherical`, `Concyclic`, the Ptolemy equality, and the distinct inequality elaborated; stdout was 1,198 bytes with SHA-256 `9c1e0319372fdbbb58abe6459b039e5da8a6bee5e6220d623ca9b82fd72af898`; no canonical root was declared |
| bounded exact-topic `rg` search in repo-local and pinned Lean | 0 | located the defining equality and inequality modules and no separate repo-local `THM-M-0201` target; discovery only, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-0201/check_intake.py` | 1 | historical intake replay stops at stale receipt input hash `Docs/Stage1_Blueprint_rev-5.6.md`; this statement phase did not rewrite historical intake evidence |
| prohibited declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0201/statement-blocker.json` and scoped invariant validation | 0 | valid JSON; identity, null target, unchanged vector, four undefined mutations, false completion flags, exact change scope, and absent self-test agree |
| scoped `git diff --check` plus per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the exact-statement deliverable did not pass |

The intake checker is a historical receipt checker. Its receipt binds blueprint and execution-DAG
hashes captured in an earlier worker snapshot. The current shared authorities have changed, so the
checker fails closed on freshness before considering this phase's new artifacts. This statement
worker records the limitation rather than rewriting the intake receipt, checker, instance, task
DAG, generated blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before accepting any future
statement transition. Accountable reviewers must lawfully preserve and hash one immutable primary
or authoritative source, select and independently approve one exact proposition, and transcribe
every incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
erratum, and boundary case. They must decide the ambient dimension, ordered cyclic-quadrilateral
encoding, circle or concyclicity predicate, convexity or diagonal-intersection condition,
distinctness policy, side and diagonal convention, and all degenerate cases.

A fresh statement attempt can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
