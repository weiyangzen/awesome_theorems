# Exact-statement gate: blocked

Item: `S56-M-0197-STATEMENT`

Theorem: `THM-M-0197`

Base revision: `f23ca64267b6746e12a641dcc66cc4dbaf1e2191` (tree
`d1872d3251ef6a9c395116467608691849d80496`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0197-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`; the intake receipt says `accepted: false` and has no
accepted receipt ID. Rev-5.6 section 10.2 permits this dependency-ordered statement attempt, but
the statement node cannot be master-accepted before its prerequisite.

Independently, the exact-statement gate fails. The repository supplies only the title `费马点定理`
(Fermat point theorem) and the gloss `三角形内到三顶点距离之和最小的点`: a point inside a
triangle for which the sum of the distances to its three vertices is minimal. It supplies no
bibliography, definition of triangle or inside, ordered binder, hypothesis, conclusion, proof
boundary, correction history, or boundary convention. Its `已验证` label is untrusted metadata.

The intake's inspected modern source lead, Mordukhovich and Nam, arXiv `1302.5244v4`, confirms that
the omissions are proposition-changing. It distinguishes a global minimization problem, existence
and uniqueness results, an interior 120-degree branch when every triangle angle is below 120
degrees, and a vertex-minimizer branch when an angle is at least 120 degrees. The catalog does not
cite or select this source, and the source has not received independent approval for the root.
In particular, an unrestricted strict-interior reading of the catalog gloss conflicts with the
at-least-120-degree branch, whose minimizer is a vertex rather than an interior point.

An exact proposition must still freeze:

- the ambient two-dimensional affine or vector space, and the exact nondegenerate-triangle
  predicate;
- strict interior, closed convex hull, or the entire plane as the candidate and comparison domain;
- existence, uniqueness, a universal minimizing inequality, or a geometric characterization as
  the conclusion;
- whether the complete theorem contains both angle branches, with equality at exactly 120 degrees
  assigned explicitly;
- the three 120-degree equalities and both directions of any interior characterization; and
- repeated, collinear, empty-interior, higher-dimensional, and whole-plane boundary cases.

Silently adding the hypothesis that all angles are below 120 degrees, broadening strict interior to
the closed triangle or plane, or substituting the full two-branch Fermat-Torricelli theorem would
narrow, broaden, or replace the received claim. Sections 5 and 5.1 make this ambiguity and the
resulting missing expression fingerprint hard blockers.

Consequently there is no honest canonical declaration whose imports can be certified minimal. No
`Statement.lean`, exact expression, checked transport, or mutation suite was created. The required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not passed. The provisional vector remains `[H5, M4, R4]`: `H5` classifies the catalog wording as
not yet a stable proposition; it does not say that a correctly stated Fermat-Torricelli theorem is
false or open.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned environment. Its four direct imports
expose `dist`, `convexHull`, finite convex-hull compactness, Euclidean angle, `IsMinOn`, compact
minimum existence, and convexity of distance. All eight checks pass. The probe declares no
triangle contract, objective, canonical target, transport, or proof body, and its own header marks
the imports as not certified minimal for the absent target. It receives no statement or proof
credit.

A bounded exact-name search over pinned mathlib and repository-local Lean found no Fermat-point,
Fermat-Torricelli, Torricelli-point, or geometric-median declaration under the recorded terms. This
is discovery-only feasibility evidence, not the downstream immutable anchor audit or a global
absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused without running an update, build, clone, fetch, or
other dependency-mutation command. The pinned mathlib Git worktree was clean after validation; no
claim of filesystem-level immutability for the full shared `.lake` tree is made.

## Validation Record

Commands ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0197` | 0 | rank 1015; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base revision and tree appear above |
| repository authority, source crosswalk, scope map, task DAG, and intake inspection | 0 | confirmed the sparse catalog wording, provisional dependency, null target, domain conflict, and lack of an approved proposition |
| `sha256sum` over authority, intake, source, probe, toolchain, dependency lock, and imported mathlib sources | 0 | exact digests are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned mathlib revision and tree match the values above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0197/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout was 1,458 bytes with SHA-256 `efa606638cf391b8d21c257ab17ffd9fa5133e2e9b02b79dfed27fc0d25da5f2`; no target declaration or proof body |
| bounded exact-name `rg` search in pinned mathlib and repository-local Lean | 1 (expected no match) | no target-specific declaration matched the recorded terms |
| `python3 -B Stage1_Instances/THM-M-0197/check_intake.py` | 1 | historical intake replay stops at its stale frozen blueprint input hash; current shared authority no longer matches the hash captured by the earlier intake worker, and this statement worker did not rewrite intake evidence |
| prohibited declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0197/statement-blocker.json` and scoped blocker-invariant validation | 0 | identity, base, null target, unchanged vector, four undefined mutations, false completion fields, exact changed paths, and absent self-test agree |
| scoped `git diff --check` plus per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the exact-statement deliverable did not pass |

The intake checker is a historical receipt checker. Its receipt binds blueprint and execution-DAG
hashes captured in an earlier worker snapshot and the original intake-only inventory. The current
shared authorities no longer match those captured hashes, and this phase adds artifacts beyond that
inventory. This attempt records the exact limitation rather than rewriting the intake receipt,
checker, instance, target task DAG, generated blueprint, or authoritative execution DAG to
manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before a future statement can be
accepted. Accountable reviewers must preserve and hash one lawful immutable primary or
authoritative source, select and independently approve one exact proposition and proof boundary,
and transcribe every incorporated definition, ordered binder, hypothesis, conclusion, correction,
erratum, and boundary case. The decision must resolve the interior/closed/whole-plane domain and
the less-than-120 versus at-least-120 degree branches without silently changing the catalog claim.

A fresh statement attempt can then encode precisely that approved claim, minimize pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
