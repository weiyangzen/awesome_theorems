# Exact-statement gate: blocked

Item: `S56-M-0218-STATEMENT`

Theorem: `THM-M-0218`

Base revision: `a07fc18923e20fd2876d04809a15d5b31e55512f` (tree
`1268491c8f2677e1c8e38754fa93dd190892e69e`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository record. The statement
item remains `[ ]`. Its prerequisite intake is provisional worker state `[_]`, not master-accepted
state `[x]`; its receipt declares `accepted: false`, is not content-addressed, and leaves the
canonical mathematical statement and Lean expression null.

More importantly, the complete source wording is only the title "Poincare disk model" and the gloss
"a conformal model of hyperbolic geometry." It gives no citation, definition chain, formula,
ordered binders, hypotheses, conclusion, proof boundary, correction history, or boundary policy.
The catalog's `verified` label is untrusted metadata under rev-5.6.

The wording does not choose among materially different claims, including:

- defining a normalized hyperbolic distance or Riemannian metric on the open unit disk;
- proving that such a metric is conformal to the Euclidean metric and fixing the orientation policy;
- proving constant curvature, completeness, a distance formula, or the Euclidean description of
  geodesics;
- constructing an isometry with the Poincare upper-half-plane model; or
- proving that the disk construction satisfies a selected synthetic axiom system.

Even the common line-element normalizations differ by a constant factor, changing distance and
curvature. Conformality, curvature, completeness, geodesic classification, analytic-model
isometry, and satisfaction of synthetic axioms are not interchangeable conclusions. Selecting a
familiar textbook bundle or any one convenient component would invent, narrow, broaden, or
substitute mathematics rather than elaborate the received target.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression fingerprint
hard blockers. With no canonical proposition, there is no honest import set to minimize, no
expression or environment-expression fingerprint, no credited alternate transport, and no
meaningful removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation.
Those statement-gate outputs are undefined, not passed. The root vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with these three pinned imports:

```lean
import Mathlib.Analysis.Complex.Conformal
import Mathlib.Analysis.Complex.UnitDisc.Basic
import Mathlib.Analysis.Complex.UpperHalfPlane.Metric
```

All nine adjacent API checks pass. This is real environment evidence but not target elaboration.
`Complex.UnitDisc` is the Euclidean open-disk subtype and the checked basic module does not install
a `Dist` instance on it. Generic `ConformalAt` is a function-level local conformality predicate,
not a disk hyperbolic metric theorem. `UpperHalfPlane.dist_eq` and
`UpperHalfPlane.isometry_vertical_line` concern the separately cataloged upper-half-plane type; no
disk metric or checked inter-model transport follows from them.

A bounded exact-topic search found no pinned mathlib declaration for a hyperbolic unit-disk metric
or Poincare-disk model theorem. This is discovery-only feasibility evidence, not the downstream
immutable anchor audit or a global absence claim. Therefore the probe's imports cannot be certified
minimal for an absent canonical target and receive no statement or proof credit.

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
| `python3 scripts/stage1_target.py show THM-M-0218` | 0 | rank 1011; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository source, Stage0, intake dossier, and exact-topic inspection | 0 | confirmed that the gloss supplies no truth-valued proposition and that no other repository source selects one |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0218/IntakeProbe.lean` | 0 | nine adjacent unit-disk, metric-ball, conformality, and upper-half-plane APIs elaborated; no target declaration or proof body |
| temporary `UnitDisc.Basic` probe with `#check_failure` for `Dist Complex.UnitDisc` and `MetricSpace Complex.UnitDisc` | 0 | the topological-space instance elaborated; both expected instance failures were confirmed, so the basic unit-disk API is not a disk hyperbolic metric |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 1/0 | no matching pinned mathlib target; repo-local matches were the blocker text or unrelated Poincare-conjecture strings only |
| `python3 -B Stage1_Instances/THM-M-0218/check_intake.py` | 1 | historical intake-only checker requires its now-absent intake worker self-test and freezes its original nine-file inventory; this statement run records rather than rewrites historical intake evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

## Retry Condition

The integration lane must master-accept the prerequisite before accepting a later statement
transition. Accountable source reviewers must preserve and hash an immutable primary or
authoritative source, transcribe one exact proposition with every incorporated definition,
normalization, ordered binder, hypothesis, conclusion, proof boundary, correction, and exceptional
case, reconcile the neighboring disk/upper-half-plane/Klein target boundaries, and independently
approve the mapping.

A fresh statement run can then encode precisely that claim, minimize the pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and execute
all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change, node receipt, worker `[_]`, or master acceptance
is claimed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json` is emitted.
