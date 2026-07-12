# Exact-statement gate: blocked

Item: `S56-M-1540-STATEMENT`  
Base revision: `6d7db94bb24d91df72f83fd7a393db356a7bb93b`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entire mathematical wording supplied for this target is `时空的扭量描述` ("a twistor description
of spacetime"), under the broad label "Penrose twistor theory" and a 1967 attribution. This names
a theory and a correspondence slogan, not one proposition. In particular, it does not determine:

- affine complexified Minkowski space or its conformal compactification;
- complex spacetime or a real slice and its reality structure;
- the spinor and homogeneous-coordinate conventions in the incidence equation;
- whether the target is the point-to-projective-line direction, its converse, a bijection, or a
  statement about null geodesics;
- the admissibility and nondegeneracy conditions on projective lines and homogeneous coordinates;
- treatment of `pi = 0`, zero twistors, projective scaling, and conformal infinity; or
- whether the Penrose transform, conformal reconstruction, or field equations are conclusions.

These choices give inequivalent theorems. The intake deliberately leaves the exact primary
theorem/page, direction, conventions, and boundary cases open. Its scoped intention to formalize a
classical incidence correspondence is not itself authority to choose those missing details. The
bibliographic candidate Penrose, "Twistor Algebra" (1967), has not been crosswalked to an exact
numbered result and surrounding definitions. Selecting a convenient projective-geometry lemma or
inventing an incidence model would therefore broaden or substitute the claim.

Consequently this phase fails at the canonical source-statement identity gate, before a canonical
Lean declaration, minimal pinned imports, expression fingerprint, checked transports, or meaningful
hypothesis/domain/binder/boundary mutations can be established. Machine status remains `M4`. No
statement acceptance, theorem proof, audit completion, or theorem completion is claimed.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_201.lean` was inspected and elaborated only as
legacy discovery input. Its `StatementShape` quantifies over an arbitrary `TwistorModelData` whose
geometric and field-theoretic conclusions are unconstrained `Prop` fields. It also includes the
Penrose transform and field-equation predicates, although the intake explicitly limits the intended
scope to the classical incidence correspondence. The file itself says that it is an abstract typed
boundary and not a terminal theorem.

The legacy file elaborates in the existing pinned environment, but that result proves only that its
abstract interface and adjacent projectivization lemmas typecheck. It does not crosswalk an exact
source theorem and cannot establish minimal imports or the exact target requested by this node.

## Required unblock

An accountable source reviewer must select a stable primary edition and exact theorem/page, quote
the result and its definitions, and freeze the spacetime model, real/complex locus, spinor and sign
conventions, projective quotients, direction and strength of correspondence, admissibility
hypotheses, and all degenerate and infinity cases. A later statement worker can then encode that
claim without substitution, minimize its pinned imports, print and hash the elaborated expression,
and run the required structural mutations.

## Narrow validation evidence

Commands were run from this worker clone on 2026-07-12. No `lake update`, build, dependency fetch,
or mutation of `.lake` was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1540` | exit 0; rank 201, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_201.lean)` | exit 0; legacy abstract boundary and projectivization probes elaborated; this is not exact-statement evidence |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_201.lean` | exit 0; `651c8acc...b1d2`, `321626c8...2d81`, and `9ba2cff4...be2` |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression fingerprint, checked transports, and mutation tests. The
assigned phase is therefore not self-tested or complete, and no `.stage1-worker-selftest.json` is
emitted.
