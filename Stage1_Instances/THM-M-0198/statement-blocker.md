# Exact-statement gate: blocked

Item: `S56-M-0198-STATEMENT`

Theorem: `THM-M-0198`

Base revision: `f023dbc3411d83201065d1a1156d7406b81135d4` (tree
`3b3a73ec19293a2a9b8d9c7e67f0d25da2a511b4`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0198-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt has `accepted: false`, is explicitly
non-content-addressed, and supplies no accepted receipt ID. Rev-5.6 permits dependency-ordered
preparation from provisional work, but master closure remains dependency ordered.

Independently, the exact-statement gate fails before target elaboration. The repository supplies
only the title `西姆松线定理` (Simson line theorem), Robert Simson attribution, the year 1756, and
the gloss `三角形外接圆上一点在三边的投影共线` (the projections of a point on a triangle's
circumcircle onto its three sides are collinear). It supplies no bibliography, immutable edition,
exact proposition, definitions, ordered binders, hypotheses, proof boundary, corrections, errata,
or independent reviewer. Its `已验证` label is untrusted inventory metadata.

The intake therefore correctly leaves the canonical human statement and Lean target null. Its
scope map records proposition-changing choices that remain unresolved:

- whether the ambient object is exactly a Euclidean plane or an arbitrary real inner-product
  affine space with an explicit coplanarity condition;
- whether the triangle is an affine-independent `Affine.Triangle` or another ordered,
  nondegenerate triple, and how vertices and opposite sides are indexed;
- whether the circumcircle is a planar circle, mathlib's simplex `circumsphere`, an equidistance
  predicate, or an existential circle, especially in ambient dimension greater than two;
- whether the circle point may equal a vertex and which repeated-foot boundary cases are included;
- whether each side means its full supporting affine line or its closed segment;
- whether a perpendicular foot is an orthogonal projection, an incidence/perpendicular witness,
  or a coordinate construction; and
- whether collinearity is packaged as `Collinear Real` on a range or finite set, affine dependence,
  membership in an existential line, or a determinant identity.

These are not merely notational choices. In a higher-dimensional ambient space, membership in a
sphere through the triangle's vertices does not by itself impose the planar circle-point boundary.
Projection onto a closed segment differs from projection onto a supporting line when a foot lies
on a side extension. Set and range encodings also need checked transports and an exact indexing
decision. Selecting the convenient pinned APIs without a source-approved proposition would add or
change scope. Adding the converse or an if-and-only-if Wallace-Simson theorem would broaden the
repository's forward-only gloss.

Rev-5.6 treats statement ambiguity and a missing expression fingerprint as hard blockers.
Consequently there is no honest canonical declaration whose imports can be certified minimal. No
`Statement.lean`, canonical expression, checked alternate transport, expression fingerprint, or
mutation suite was created. The required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined rather than passed. The
provisional root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned environment. Its three direct
imports expose `Affine.Triangle`, `Affine.Simplex.faceOpposite`, `circumsphere`,
`orthogonalProjectionSpan`, `EuclideanGeometry.orthogonalProjection_mem`, `Concyclic`, and
`Collinear`. All eight interface checks pass. The probe declares no target, transport, or proof
body; its imports are only discovery inputs and cannot be certified minimal for the absent
canonical target.

A bounded exact-topic search over repository-local Lean and pinned mathlib found no separately
named Simson, Wallace-Simson, or pedal-line declaration. This is discovery-only evidence, not the
downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No update, build, clone, fetch, or other
dependency-mutation command was run, and the pinned mathlib worktree remained clean.

## Validation Record

Commands ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0198` | 0 | rank 1530; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` before edits | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base revision and tree appear above |
| authority, source, scope, crosswalk, task-DAG, receipt, and intake inspection | 0 | confirmed the provisional dependency, sparse forward gloss, null canonical target, and unresolved source/domain/projection/boundary choices |
| `sha256sum` over authority, source, intake, toolchain, lock, probe, and pinned API inputs | 0 | current input digests are recorded in `statement-blocker.json` |
| `git blame -L 1429,1434 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision/tree match the values above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0198/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout was 1,864 bytes with SHA-256 `e93d8f2e41131d15910bfc7262bac71eedd9d604cb791aeb5d0772f75833aea9`; stderr was empty; no target or proof body was declared |
| bounded exact-topic `rg` search in repository-local and pinned Lean | 1 (expected no match) | no separately named Simson, Wallace-Simson, or pedal-line declaration matched; discovery only |
| `python3 -B Stage1_Instances/THM-M-0198/check_intake.py` | 1 | the historical intake checker expects the pre-integration authoritative intake state `[ ]`, while the current execution DAG records provisional `[_]`; shared authority hashes also postdate that receipt; this phase did not rewrite historical evidence |
| prohibited declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0198/statement-blocker.json` and scoped invariant validation | 0 | valid JSON; identity, null target, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, and absent self-test agree |
| scoped `git diff --check` plus per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; each raw no-index exit 1 is only the expected new-file difference status |
| `test ! -e .stage1-worker-selftest.json` | 0 | the self-test manifest is absent because the exact-statement deliverable did not pass |

The intake checker validates a historical provisional receipt and an intake-only inventory. The
master has since integrated that intake and changed the authoritative DAG projection. This worker
records the resulting freshness/state mismatch rather than rewriting the intake receipt, checker,
instance, target task DAG, generated blueprint, or authoritative execution DAG to manufacture
agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before accepting a future
statement transition. Accountable reviewers must lawfully preserve and hash one immutable primary
or authoritative source, select and independently approve one exact forward proposition and proof
boundary, and transcribe every incorporated definition, ordered binder, hypothesis, conclusion,
correction, erratum, and boundary case. They must decide the ambient plane and dimension, triangle
representation and indexing, circle and coplanarity predicates, vertex-point policy, supporting
lines versus segments, projection-foot construction, collinearity packaging, and all degenerate
cases.

A fresh statement attempt can then encode precisely that approved claim, minimize pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
