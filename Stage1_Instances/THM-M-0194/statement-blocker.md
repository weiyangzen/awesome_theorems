# Exact-statement gate: blocked

Item: `S56-M-0194-STATEMENT`

Theorem: `THM-M-0194`

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0194-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`; its receipt says `accepted: false` and contains no
accepted receipt ID. Dependency-ordered preparation does not waive master acceptance.

Independently, the exact-statement gate fails. The repository supplies only the title `泰勒斯定理`
(Thales' theorem) and the gloss `圆周角等于圆心角的一半`: an inscribed angle is half the central
angle. It gives no bibliography, binder-complete proposition, definitions, proof boundary,
correction history, or independently approved source crosswalk. Its `已验证` label is untrusted
metadata under rev-5.6.

The intake's matching source lead, Euclid's *Elements* III.20 in David E. Joyce's English edition,
says that the angle at the center is double the angle at the circumference when both have the same
circumference as base. That lead has not been independently reviewed as the root, and its
incorporated definitions, diagrammatic cases, translation history, attribution, corrections, and
errata remain open. The catalogue and source lead do not yet fix:

- one common circle and the exact same-chord, selected-arc, or side relation;
- ordinary angles in `[0, pi]`, directed angles, or oriented angles modulo `2 * pi`;
- a minor or reflex central angle and the side of the chord containing the circumference point;
- `inscribed = central / 2`, `central = 2 * inscribed`, or a congruence as the conclusion;
- the Euclidean plane, a two-dimensional oriented affine space, or a higher-dimensional setting;
- point distinctness, zero-radius circles, coincident endpoints, endpoint vertices, antipodal
  endpoints, straight or zero angles, and arc-boundary cases; or
- whether the separately named semicircle/right-angle theorem is excluded, included as a
  corollary, or intended instead of the general inscribed-angle theorem.

These choices change the proposition. In particular, division by two is not automatically the
inverse of doubling in `Real.Angle`. Selecting the convenient pinned oriented declaration would
silently impose a two-dimensional orientation and modulo-`2 * pi` equality. Selecting mathlib's
declaration named `thales_theorem` would instead substitute the semicircle/right-angle theorem.
Both actions violate the intake boundary and the rev-5.6 prohibition on invented or substituted
mathematics.

Consequently there is no honest canonical declaration whose imports can be certified minimal. No
`Statement.lean`, exact expression fingerprint, checked transport, or mutation suite was created.
The required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
are undefined rather than passed. The lifecycle remains `planned`, and the provisional root vector
remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned environment using the direct module
`Mathlib.Geometry.Euclidean.Angle.Sphere`. It checks six exact-topic and semicircle interfaces. The
closest exact-topic candidate is
`EuclideanGeometry.Sphere.oangle_center_eq_two_zsmul_oangle`: three points lie on one sphere in a
two-dimensional oriented real inner-product affine torsor, the circumference vertex differs from
both chord endpoints, and the oriented central angle equals twice the oriented circumference
angle. Its diagnostic axiom report is `[propext, Classical.choice, Quot.sound]`.

The probe also confirms that `EuclideanGeometry.Sphere.thales_theorem` has the distinct type
"the ordinary angle is `pi / 2` if and only if the apex lies on a sphere with the other points as
diameter endpoints." Its axiom report is the same. Successful elaboration authenticates pinned API
availability only. The probe declares no canonical target, source transport, mutation fixture, or
proof body and receives no statement or proof credit. The complete output is 2,483 bytes with
SHA-256 `bd47379182d6ed664001745c31bf5912b1e47d192e85fe809272c6c581ead899`.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused without running an update, build, clone, fetch, or
other dependency-mutation command. The pinned mathlib Git worktree was clean after validation.

## Validation Record

Commands ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0194` | 0 | rank 1223; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base revision and tree appear above |
| repository authority, source crosswalk, scope map, task DAG, receipt, and intake inspection | 0 | confirmed provisional intake, null target, exact-source ambiguity, candidate restrictions, and six open downstream tasks |
| `sha256sum` over authority, intake, toolchain, dependency lock, and pinned candidate source | 0 | exact digests are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned mathlib revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0194/IntakeProbe.lean` | 0 | six APIs elaborated; both diagnostic axiom reports were `[propext, Classical.choice, Quot.sound]`; output size and hash recorded above |
| bounded source and repository search for the exact-topic and named Thales declarations | 0 | located the central/circumference oriented theorem and the distinct semicircle alias in the pinned defining module; no source-approved canonical target was found |
| `python3 -B Stage1_Instances/THM-M-0194/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]`, while current authority records provisional `[_]`; this statement worker did not rewrite historical intake evidence |
| prohibited declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0194/statement-blocker.json` and scoped invariant validation | 0 | finalized structured blocker parsed and its identity, base, null target, unchanged vector, four undefined mutations, false completion fields, changed paths, and absent self-test agreed |
| scoped `git diff --check` plus per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the exact-statement deliverable did not pass |

The historical intake checker was written for its intake-time authoritative state. Its assertion
that the intake item is `[ ]` is stale after integration recorded provisional `[_]`; this statement
phase records that limitation instead of editing the historical checker, intake receipt, instance,
target task DAG, generated blueprint, or authoritative execution DAG.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before accepting a future
statement transition. Accountable reviewers must preserve and hash one lawful immutable primary or
authoritative source, select and independently approve its exact proposition and proof boundary,
and transcribe every incorporated definition, ordered binder, premise, conclusion, diagrammatic
case, correction, erratum, and boundary case. They must explicitly settle the circle/chord/arc
relation, angle codomain and orientation, minor/reflex convention, conclusion direction, dimension,
distinctness, degeneracies, and relationship to the semicircle theorem.

A fresh statement attempt can then encode precisely that approved claim, minimize pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. Because the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, or master acceptance is claimed.
