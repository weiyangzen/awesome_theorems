# Exact-statement gate: blocked

Item: `S56-M-0217-STATEMENT`

Theorem: `THM-M-0217`

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository record. The statement
item remains `[ ]`. Its prerequisite intake is provisional worker state `[_]`, not master-accepted
state `[x]`; its receipt declares `accepted: false`, is not content-addressed, and leaves the
canonical mathematical statement and Lean expression null.

More importantly, the complete source wording is only the title "Klein model" and the gloss "a
projective model of hyperbolic geometry." It gives no citation, definition chain, formula, ordered
binders, hypotheses, conclusion, proof boundary, correction history, or boundary policy. The
catalog's `verified` label is untrusted metadata under rev-5.6.

The wording does not choose among materially different claims, including:

- constructing a projective-conic interior or affine disk/ball with a normalized cross-ratio
  distance;
- proving the metric laws, curvature, completeness, or satisfaction of a synthetic hyperbolic
  axiom system;
- characterizing geodesics as projective-line intersections that appear as Euclidean chords;
- proving that projective transformations preserving the boundary conic act isometrically; or
- constructing an isometry or equivalence with the hyperboloid, Poincare disk, or upper-half-plane
  model.

Carrier, dimension, field, quadratic form, affine chart, cross-ratio order, logarithm convention,
and scale all change the formal target. Metric construction, geodesic characterization, symmetry,
curvature, completeness, model axioms, and inter-model comparison are not interchangeable
conclusions. Selecting a familiar textbook bundle or one convenient component would invent,
narrow, broaden, or substitute mathematics rather than elaborate the received target.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression fingerprint
hard blockers. With no canonical proposition, there is no honest import set to minimize, no
expression or environment-expression fingerprint, no credited alternate transport, and no
meaningful removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation.
Those statement-gate outputs are undefined, not passed. The root vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with these four pinned imports:

```lean
import Mathlib.Analysis.Complex.UnitDisc.Basic
import Mathlib.Analysis.Normed.Module.Convex
import Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Projective
import Mathlib.LinearAlgebra.Projectivization.Action
```

All eleven adjacent API checks pass. They expose an open complex unit-disk subtype, convex balls
and affine segments, vector-space projectivization and its general-linear action, and a projective
general linear group. None selects a real projective conic or ball, defines a Klein distance,
states the required model relation, or supplies a checked inter-model transport.

A bounded exact-topic search found no Klein/Beltrami hyperbolic-model or cross-ratio declaration in
pinned mathlib or repository-local Lean. This is discovery-only feasibility evidence, not the
downstream immutable anchor audit or a global absence claim. The probe is real environment
evidence, but it does not elaborate a canonical target; consequently its imports cannot be
certified minimal for that absent target and receive no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0217` | 0 | rank 1232; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository catalog record, Stage0 projection, and intake dossier inspection | 0 | confirmed that the inspected authoritative records supply only the topic gloss and leave the canonical proposition open |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0217/IntakeProbe.lean` | 0 | eleven adjacent disk, convex-segment, projectivization, action, and projective-group APIs elaborated; no target declaration or proof body |
| `rg -n -i --glob '*.lean' 'beltrami[ _-]?klein\|klein[ _-]?(model\|disk\|disc\|metric)\|hyperbolic.{0,40}(projective\|cross.?ratio)\|projective.{0,40}hyperbolic\|cross.?ratio' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 | expected no-match result; discovery-only search, not an anchor audit or global absence proof |
| `python3 -B Stage1_Instances/THM-M-0217/check_intake.py` | 1 | historical intake-only checker freezes the original authoritative intake state `[ ]`; the integrated DAG now records provisional `[_]`, so this statement run records rather than rewrites historical intake evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0217/statement-blocker.json` | 0 | blocker record is valid JSON |
| scoped blocker invariant assertions and `test ! -e .stage1-worker-selftest.json` | 0 | item/base identity, null target fields, unchanged debt vector, false completion fields, four undefined mutation classes, and required self-test absence agree |
| `git diff --check -- Stage1_Instances/THM-M-0217` plus per-file `git diff --no-index --check /dev/null <blocker>` | 0 / 1 | no whitespace diagnostics; no-index status 1 for each untracked blocker is only the expected new-file difference |

## Retry Condition

The integration lane must master-accept the prerequisite before accepting a later statement
transition. Accountable source reviewers must preserve and hash an immutable primary or
authoritative source, transcribe one exact proposition with every incorporated definition,
normalization, ordered binder, hypothesis, conclusion, proof boundary, correction, and exceptional
case, reconcile the neighboring Klein/disk/upper-half-plane/area target boundaries, and
independently approve the mapping.

A fresh statement run can then encode precisely that claim, minimize the pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and execute
all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change, node receipt, worker `[_]`, or master acceptance
is claimed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json` is emitted.
