# Exact-statement gate: blocked

Item: `S56-M-0219-STATEMENT`

Theorem: `THM-M-0219`

Base revision: `f23ca64267b6746e12a641dcc66cc4dbaf1e2191` (tree
`d1872d3251ef6a9c395116467608691849d80496`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository record. The statement
item remains `[ ]`. Its prerequisite intake is provisional worker state `[_]`, not master-accepted
state `[x]`; its receipt declares `accepted: false`, is not content-addressed, and leaves the
canonical mathematical statement and Lean expression null.

More importantly, the complete source wording is only the title "Poincare half-plane model" and
the gloss "another model of hyperbolic geometry." It gives no citation, definition chain, formula,
ordered binders, hypotheses, conclusion, proof boundary, correction history, or boundary policy.
The catalog's `verified` label is untrusted metadata under rev-5.6.

The wording does not choose among materially different claims, including:

- constructing the open upper-half-plane carrier with a normalized hyperbolic distance or
  Riemannian metric;
- proving the metric laws, conformality, completeness, simple connectedness, or constant curvature
  `-1`;
- classifying geodesics as vertical lines and circles orthogonal to the real boundary;
- proving that a named real fractional-linear group acts isometrically;
- constructing an isometry with the separately cataloged Poincare disk model; or
- proving that the construction satisfies a selected synthetic axiom system for hyperbolic
  geometry.

Even standard line-element scalings change distance and curvature. Metric construction,
completeness, curvature, geodesic classification, transformation invariance, model equivalence,
and satisfaction of synthetic axioms are not interchangeable conclusions. Selecting a familiar
textbook bundle or any convenient checked mathlib component would invent, narrow, broaden, or
substitute mathematics rather than elaborate the received target.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression fingerprint
hard blockers. With no canonical proposition, there is no honest import set to minimize, no
expression or environment-expression fingerprint, no credited alternate transport, and no
meaningful removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation.
Those statement-gate outputs are undefined, not passed. The root vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with these two pinned imports:

```lean
import Mathlib.Analysis.Complex.UpperHalfPlane.Metric
import Mathlib.Analysis.Complex.UnitDisc.Basic
```

All nine adjacent API checks pass. `UpperHalfPlane` is a genuine complex upper-half-plane carrier;
`UpperHalfPlane.dist_eq` exposes its Poincare distance formula; the pinned library installs
`MetricSpace` and `ProperSpace`; and `SL(2,R)` acts isometrically through the fractional-linear
action. `Complex.UnitDisc` is available for the neighboring disk-model boundary. These are real
environment and feasibility facts, not elaboration of one source-selected model theorem.

A bounded exact-topic search found the pinned upper-half-plane metric and isometric-action APIs but
no checked Cayley isometry or repository-local proposition that resolves the catalog ambiguity.
This is discovery-only evidence, not the downstream immutable anchor audit or a global absence
claim. Therefore the probe's imports cannot be certified minimal for an absent canonical target and
receive no statement or proof credit.

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
| `python3 scripts/stage1_target.py show THM-M-0219` | 0 | rank 1012; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository source, Stage0, intake dossier, and exact-topic inspection | 0 | confirmed that the gloss supplies no truth-valued proposition and that no other repository source selects one |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0219/IntakeProbe.lean` | 0 | nine adjacent carrier, Poincare-distance, fractional-linear, unit-disk, metric, properness, and isometric-action APIs elaborated; no target declaration or proof body |
| bounded exact-topic search in pinned mathlib and repository-local Lean | 0 | found adjacent upper-half-plane metric/isometry APIs but no checked source-selected model proposition or Cayley disk equivalence; discovery-only search |
| `python3 -B Stage1_Instances/THM-M-0219/check_intake.py` | 1 | historical intake-only checker freezes the original authoritative intake state `[ ]`; the integrated DAG now records provisional `[_]`, so this statement run records rather than rewrites historical intake evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

## Retry Condition

The integration lane must master-accept the prerequisite before accepting a later statement
transition. Accountable source reviewers must preserve and hash an immutable primary or
authoritative source, transcribe one exact proposition with every incorporated definition,
normalization, ordered binder, hypothesis, conclusion, proof boundary, correction, and exceptional
case, reconcile the neighboring half-plane/disk/Klein/area target boundaries, and independently
approve the mapping.

A fresh statement run can then encode precisely that claim, minimize the pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and execute
all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change, node receipt, worker `[_]`, or master acceptance
is claimed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json` is emitted.
