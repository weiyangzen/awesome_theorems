# Exact-statement gate: blocked

Item: `S56-M-0196-STATEMENT`

Theorem: `THM-M-0196`

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0196-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt has `accepted: false`, is explicitly
non-content-addressed, and provides no accepted receipt ID. Rev-5.6 permits dependency-ordered
preparation from provisional work, but master closure remains dependency ordered.

Independently, the exact-statement gate fails. The repository record supplies only the title
`九点圆定理`, the gloss `三角形九点共圆` (the nine points of a triangle are concyclic), Feuerbach
attribution, and the year 1822. It supplies no bibliography, definition of the nine points,
triangle or ambient-space boundary, ordered binders, hypotheses, circle or concyclicity encoding,
indexing, cardinality semantics, proof boundary, correction history, or reviewer. Its `已验证`
label is untrusted metadata.

The intake correctly leaves the canonical human statement and Lean target null. Its scope map
records proposition-changing choices that remain unresolved:

- whether the triangle is an affine-independent simplex or another nondegenerate triple, and
  whether the ambient space is exactly a Euclidean plane or a higher-dimensional affine space;
- whether the nine points are the three side midpoints, three vertex-orthocenter midpoints, and
  three altitude feet, with an exact vertex/opposite-side indexing convention;
- whether the root exhibits an arbitrary circle, asserts membership in mathlib's constructed
  `ninePointCircle`, identifies the medial triangle's circumcircle, or uses abstract concyclicity;
- whether the result is one conjunction, a set-containment statement, or a claim about nine
  distinct points; and
- how right, isosceles, equilateral, repeated-point, collinear, and other boundary cases are treated.

These formulations are not definitionally interchangeable. In particular, special nondegenerate
triangles can have coincidences among the conventional constructed points, so incidence in one
circle does not imply a cardinality-sensitive claim about nine distinct points. Mathlib's
`Affine.Triangle` also fixes affine independence while allowing an arbitrary real inner-product
affine ambient space; adopting it without source approval would add domain and boundary choices.

Selecting the conventional three-family conjunction from mathematical familiarity would invent
missing source decisions. Selecting a single existing membership theorem would be only partial
coverage. Substituting Feuerbach's incircle/excircle tangency theorem or the higher-dimensional
`3(n+1)`-point sphere would change the theorem. Rev-5.6 makes statement ambiguity and a missing
expression fingerprint hard blockers, so none of these substitutions is permitted.

Consequently there is no honest canonical declaration whose import can be certified minimal. No
`Statement.lean`, exact expression, checked transport, or mutation fixture was created. The
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are
undefined, not passed. The provisional root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with the single direct import
`Mathlib.Geometry.Euclidean.NinePointCircle`. It checks the constructed sphere, the side-midpoint
and Euler-point membership families, the midpoint bridge, the altitude-foot membership family, and
the medial-circumsphere identity. All checks pass. The three printed membership bodies report only
`propext`, `Classical.choice`, and `Quot.sound`.

This exact-topic API is strong discovery evidence and a promising later wrapper route, but the
probe declares no canonical root, source transport, or proof body. The import is minimal only for
the probe; it cannot be certified minimal for an absent target. The mathlib module's own reference
is to a higher-dimensional Monge-point/`3(n+1)`-point-sphere paper, not an independently approved
source identity for the repository's sparse Feuerbach catalog record.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No update, build, clone, fetch, or other
dependency-mutation command was run. The pinned mathlib Git worktree was clean after validation.

## Validation Record

Commands ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0196` | 0 | rank 1225; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base revision and tree appear above |
| authority, source, scope, crosswalk, task DAG, receipt, and intake inspection | 0 | confirmed provisional dependency, sparse catalog claim, null canonical target, and unresolved source/domain/packaging/boundary choices |
| `sha256sum` over authority, source, intake, toolchain, lock, and pinned exact-topic module inputs | 0 | exact digests are recorded in `statement-blocker.json` |
| `git blame -L 1415,1420 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision/tree match the values above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0196/IntakeProbe.lean` | 0 | six exact-topic interfaces elaborated; three membership bodies reported only the accepted standard axioms above; stdout was 2,010 bytes with SHA-256 `2ad86c6d8573b2a8135dd50361a5fb27fd1017219e6a95db4e417a18a663355d`; no canonical root was declared |
| bounded exact-name `rg` search in repo-local Lean outside the intake probe | 1 (expected no match) | no separate repo-local nine-point-circle target declaration matched; this is discovery-only, not a downstream anchor audit |
| `python3 -B Stage1_Instances/THM-M-0196/check_intake.py` | 1 | historical intake replay stops at stale receipt input hash `Docs/Stage1_Blueprint_rev-5.6.md`; this statement phase did not rewrite historical intake evidence |
| prohibited declaration scan over owned Lean files | 0 wrapper / expected inner no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0196/statement-blocker.json` and scoped invariant validation | 0 | valid JSON; identity, null target, unchanged vector, four undefined mutations, false completion flags, exact change scope, and absent self-test agree |
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
erratum, and boundary case. They must decide the triangle and ambient space, the three point
families and indexing, circle/concyclicity packaging, cardinality semantics, special cases, and any
credited alternate formulations.

A fresh statement attempt can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
