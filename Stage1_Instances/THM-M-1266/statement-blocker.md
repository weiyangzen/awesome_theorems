# Exact-statement gate: blocked

Item: `S56-M-1266-STATEMENT`  
Theorem: `THM-M-1266`  
Base revision: `9b754a21a3b3cd70ee15517f1b114d8c32500ff0`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entire mathematical wording is `变分问题的存在性` ("existence for variational problems"), under
the label "Tonelli theorem". This identifies a theorem family, but it does not fix a single
proposition. In particular, the record does not determine:

- the interval, endpoint data, and admissible class of curves;
- the classical, absolutely-continuous, or Sobolev solution space and representative convention;
- whether the Lagrangian is autonomous or time-dependent and its exact regularity assumptions;
- the convexity, strict-convexity, or quasiconvexity condition in the velocity variable;
- the coercive or superlinear growth inequality, exponent range, and constants;
- the real-valued or extended-real action and its measurability/integrability policy;
- the topology or convergence mode used for compactness and lower semicontinuity;
- the precise existence, regularity, or uniqueness conclusion and all boundary cases.

These choices yield inequivalent Tonelli existence theorems. Selecting one without a pinpointed
primary-source theorem would invent missing mathematics, while replacing the claim with generic
compact-set minimization would prove only a stronger-premise direct-method subcase. The intake
record explicitly leaves the same choices unresolved and does not authorize the statement worker
to choose among them. Thus the canonical human-claim identity gate fails before a minimal import
set, serialized elaborated expression, checked alternate transport, or meaningful mutation suite
can be produced.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_162.lean` was inspected and elaborated only as
legacy discovery input. Its `StatementShape` quantifies over an abstract
`TonelliVariationalProblem`. The record stores `coercive_growth`, `boundary_conditions_closed`,
and `compactness_or_weakCompactness` as unconstrained `Prop` fields, while also assuming action
lower semicontinuity directly. Consequently it neither states concrete coercivity or compactness
implications nor fixes the admissible function space, boundary trace, or convergence topology.
Its checked compact lower-semicontinuity wrapper is a valid subcase but is not the source theorem.

The legacy module elaborates in the pinned environment and contains no `sorry`, `admit`, `axiom`,
or `sorryAx`. That establishes only that the historical abstract boundary is type-correct. It does
not establish exact source fidelity or minimal imports, and the rev-5.6 baseline expressly gives
legacy artifacts no statement or proof credit.

## Required unblock

An accountable source reviewer must select an immutable primary edition and identify an exact
theorem by volume/page/theorem, including surrounding definitions and any errata. The resulting
crosswalk must freeze the interval and endpoint policy, admissible curve space, Lagrangian domain,
regularity, convexity and growth hypotheses, action codomain, compactness/lower-semicontinuity
mode, conclusion, and degenerate cases. A later statement worker can then encode that claim,
minimize its pinned imports, print and hash the elaborated expression, check transports, and test
removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations.

## Narrow validation evidence

Commands ran from this worker clone on 2026-07-12. Lean used the existing canonical pinned `.lake`
artifact; no update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1266` | 0 | rank 162, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_162.lean)` | 0 | legacy declarations and target shapes elaborated; this is not canonical-statement evidence |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_162.lean` | 0 | `651c8acc...b1d2`, `321626c8...2d81`, and `d1114fc4...106` |
| `rg -n '\\b(sorry\|admit\|axiom)\\b\|sorryAx' Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_162.lean` | 1 | no forbidden proof construct found |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression fingerprint, checked transports, and the four required
mutation classes. The assigned phase is not self-tested or complete, so no
`.stage1-worker-selftest.json` is emitted. No statement acceptance, downstream-node credit, audit
completion, or theorem completion is claimed.
