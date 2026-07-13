# Exact-statement gate: blocked

Item: `S56-M-0214-STATEMENT`

Theorem: `THM-M-0214`

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository record. The statement
item remains `[ ]`. Its prerequisite intake is provisional worker state `[_]`, not master-accepted
state `[x]`; its receipt declares `accepted: false`, is not content-addressed, and deliberately
leaves the canonical mathematical statement and Lean expression null.

More importantly, the complete source wording is only the title `球面几何余弦定理` and the gloss
`球面三角形边与角的关系` ("the relation between the sides and angles of a spherical triangle").
It gives no citation, formula, incorporated definitions, ordered binders, hypotheses, conclusion,
proof boundary, correction history, errata disposition, or reviewer. The catalog's `已验证` field
is untrusted metadata under rev-5.6.

The wording does not choose among materially different claims:

- the side rule `cos a = cos b * cos c + sin b * sin c * cos A`;
- its radius-scaled arc-length form, with trigonometric arguments divided by `R`;
- the dual angle rule `cos A = -cos B * cos C + sin B * sin C * cos a`;
- one cyclic instance, all cyclic instances, or an equivalence between side and angle rules; or
- an extrinsic inner-product identity together with checked intrinsic-side and vertex-angle maps.

It also leaves open the round-sphere model and dimension, radius and curvature normalization,
central angles versus intrinsic arc lengths, minor/major/oriented arc selection and side ranges,
interior versus oriented angle conventions, vertex-side naming, triangle validity, and treatment of
coincident, antipodal, collinear, boundary, and orientation-reversed cases. These choices change
the proposition. Selecting a familiar textbook formula, a unit-radius specialization, or a
convenient nondegenerate encoding would invent, narrow, broaden, or substitute mathematics rather
than elaborate the exact received target.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression fingerprint
hard blockers. With no canonical proposition, there is no honest import set to minimize, no
expression or environment-expression fingerprint, no credited alternate transport, and no
meaningful removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation.
Those statement-gate outputs are undefined, not passed. The root vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with two pinned imports:

```lean
import Mathlib.Geometry.Euclidean.Angle.Sphere
import Mathlib.Geometry.Euclidean.Triangle
```

Ten adjacent API checks pass. They cover an ambient Euclidean sphere, ambient and inner-product
angles, cosine/inner-product identities, the Euclidean law of cosines, and real sine and cosine.
The sphere subtype inherits ambient chord distance; `EuclideanGeometry.law_cos` is Euclidean; and
none of the checked declarations defines intrinsic spherical arc distance or states a spherical
triangle cosine law.

A bounded exact-topic search over pinned mathlib and repository-local Lean matched no spherical-
triangle or spherical-law-of-cosines declaration. This is discovery-only feasibility evidence, not
the downstream immutable anchor audit or a global absence claim. The probe declares no canonical
target, transport, or proof body, so its imports cannot be certified minimal for the absent target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0214` | 0 | rank 1229; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `pwd`; `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | isolated worker clone confirmed; only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 1543,1548 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| repository source, Stage0, intake dossier, and target-boundary inspection | 0 | confirmed that the gloss supplies no truth-valued proposition and that the intake leaves every proposition-changing choice open |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0214/IntakeProbe.lean` | 0 | ten adjacent APIs elaborated; stdout was 1,914 bytes with SHA-256 `b8f75349ad4fd5e2456ecd450a3422f7918edf28566e23326a79841517741e70`; no target declaration or proof body |
| bounded exact-topic search in pinned mathlib and repository-local Lean | 1 | expected no-match result: no spherical-triangle or spherical-law-of-cosines declaration matched |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0214-statement-pycache python3 -B Stage1_Instances/THM-M-0214/check_intake.py` | 1 | historical intake validator fails closed at stale `authoritative_blueprint_sha256` after integration changed the authority snapshot; it is not statement evidence and was not modified |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

The intake checker is bound to intake-time authority hashes and the intake's original artifact
inventory. Integration changed the authoritative blueprint and DAG and recorded intake `[_]`, so
the checker correctly fails closed. This statement attempt records that boundary instead of
rewriting the intake receipt, instance, task DAG, checker, generated blueprint, or authoritative
execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept the prerequisite before accepting a later statement
transition. Accountable source reviewers must lawfully preserve and hash an immutable primary or
authoritative source, select and independently approve one exact side, dual-angle, cyclic-family,
equivalence, or other proposition, and transcribe every incorporated sphere, radius, side, arc,
angle, orientation, triangle-validity, ordered binder, hypothesis, conclusion, proof boundary,
correction, and exceptional case. They must also reconcile the Euclidean cosine law, neighboring
hyperbolic cosine law, and Gauss-Bonnet target boundaries.

A fresh statement run can then encode precisely that approved claim, minimize the pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. No `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, master acceptance, statement fingerprint, or proof credit is
claimed.
