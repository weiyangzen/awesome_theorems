# Exact-statement gate: blocked

Item: `S56-M-0193-STATEMENT`

Theorem: `THM-M-0193`

Base revision: `5bc32428da3d17f138ceca67f30fbc2d149da1ba` (tree
`7d2433c3e014a9cc8c4d061bcc1b7d5c637ce33f`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0193-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt is `accepted: false`, is not
content-addressed, and names no accepted receipt. Dependency-ordered preparation can inspect that
packet, but it cannot turn an unaccepted predecessor into an accepted statement transition.

Independently, the exact-statement gate fails closed. The repository record supplies the title
`勾股定理`, the gloss `直角三角形两直角边平方和等于斜边平方`, a Pythagorean-school attribution, an
approximate date, and an untrusted `已验证` label. It supplies no bibliography, exact definition of
triangle or square, ordered vertices, domain, dimension, nondegeneracy policy, proof boundary,
translation, corrections, errata, or reviewer. Stage0 explicitly leaves precise definitions and
premises open.

The intake deliberately leaves the canonical human claim and Lean target null. Its source and
scope records identify proposition-changing decisions that remain unresolved:

- whether the domain is the Euclidean plane, a two-dimensional real affine inner-product space,
  or an arbitrary real inner-product affine torsor;
- which ordered point is the right-angle vertex and which side is the hypotenuse;
- whether a triangle must have three distinct noncollinear vertices, and how repeated points,
  zero-length legs, collinear triples, and low-dimensional ambient spaces are treated;
- whether the squares are Euclid's constructed square areas, powers of real distances, or products
  `d * d`, and which side of the equality is written first; and
- whether the canonical root is only the forward implication or the stronger if-and-only-if
  statement whose converse belongs to Euclid I.48 rather than I.47.

The inspected Casey edition of Euclid I.47 is a strong source lead, but it was not preserved in the
repository and has no accepted definition/assumption/translation/errata mapping or independent
review. Selecting its ordinary nondegenerate plane-triangle convention would therefore invent an
unaccepted source boundary. Selecting mathlib's broad degenerate-compatible affine encoding would
instead silently generalize that source boundary. Neither choice is authorized by the received
target.

Consequently there is no honest canonical declaration whose imports can be certified minimal. No
`Statement.lean`, exact expression, checked transport, or mutation fixture was created. The
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not passed. The provisional root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with the single direct import
`Mathlib.Geometry.Euclidean.Angle.Unoriented.RightAngle`. Its closest affine declaration is
`EuclideanGeometry.dist_sq_eq_dist_sq_add_dist_sq_iff_angle_eq_pi_div_two`, with the angle at the
middle point and a squared-distance equality for the opposite and adjacent sides. The module also
exposes vector-angle and inner-product-zero variants. All six checks pass, and the two printed iff
bodies report only `propext`, `Classical.choice`, and `Quot.sound`.

This is exact-topic discovery evidence, not a frozen target. The affine declaration is an iff over
arbitrary real inner-product affine torsors and explicitly supports degenerate triangles. A forward
projection is plausible, but without an approved domain and boundary transport it is not the exact
catalog root. The probe's import is minimal only for the probe and receives no statement or proof
credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No update, build, clone, fetch, or other
dependency-mutation command was run. The pinned mathlib worktree remained clean.

## Validation Record

Commands ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0193` | 0 | rank 1222; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base revision and tree appear above |
| authority, source, scope, crosswalk, task-DAG, receipt, and intake inspection | 0 | confirmed the provisional dependency, sparse catalog claim, null canonical target, and unresolved source/domain/direction/boundary choices |
| `sha256sum` over authority, source, intake, toolchain, lock, and pinned exact-topic module inputs | 0 | exact digests are recorded in `statement-blocker.json` |
| `git blame -L 1394,1399 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision/tree match the values above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0193/IntakeProbe.lean` | 0 | six exact-topic interfaces elaborated; two iff axiom reports contained only the foundations above; stdout was 1,951 bytes with SHA-256 `4a10c782d686b5c81a4dfc43132ef324dae8429805709fb000d4921e80cf47da`; no canonical root was declared |
| bounded exact-name `rg` search in repo-local Lean outside the intake probe | 0 with unrelated matches | only legacy number-theoretic Pythagorean-triple metadata matched; no separate affine Pythagorean target declaration was found; this is discovery-only, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-0193/check_intake.py` | 1 | historical intake replay fails because its checker expects authoritative intake state `[ ]`, while integration has advanced that item to provisional `[_]`; this statement worker did not rewrite intake evidence |
| prohibited declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0193/statement-blocker.json` and scoped invariant assertions | 0 | valid JSON; identity, null target, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, and absent self-test agree |
| scoped `git diff --check` plus per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the exact-statement deliverable did not pass |

The intake checker validates a historical worker packet. Its embedded expectations predate the
integration-lane update of the authoritative intake state. This statement attempt records the
freshness failure rather than modifying the intake receipt, checker, instance, task DAG, generated
blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before accepting any future
statement transition. Accountable reviewers must lawfully preserve and hash one immutable primary
or authoritative source, independently approve one exact proposition and proof boundary, and map
every incorporated definition, ordered binder, hypothesis, conclusion, translation, correction,
erratum, and boundary case. They must decide the ambient domain and dimension, point order,
right-angle vertex, nondegeneracy, square representation, equality orientation, forward-versus-iff
scope, and all degenerate cases.

A fresh statement attempt can then encode exactly that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
