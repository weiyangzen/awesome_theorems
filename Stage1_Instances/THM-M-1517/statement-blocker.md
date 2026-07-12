# Exact-statement gate: blocked

Item: `S56-M-1517-STATEMENT`  
Base revision: `98e63368ae23fcc5338261550116996c11891fc1`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entire mathematical wording is `经典力学的拉格朗日形式` ("the Lagrangian formulation of classical
mechanics"). This names a theory or formalism, not a uniquely quantified theorem. It does not
determine:

- whether the root is Hamilton's stationary-action principle, the forward Euler-Lagrange
  implication, its converse, or a coordinate/manifold equation of motion;
- the configuration space, time domain, scalar field, path and variation spaces, or differentiability
  classes;
- the action integral and derivative convention, admissibility predicate, fixed/free endpoint
  policy, or treatment of constraints;
- whether the Lagrangian is regular or singular and whether forces, time dependence, or generalized
  coordinates are included; or
- the exact quantified conclusion and its boundary or degenerate cases.

These choices give inequivalent propositions. The accepted intake therefore records only a
candidate forward Euler-Lagrange reading, with `canonical_statement: null`, an empty binder and
hypothesis list, and a formal-target state of
`blocked_pending_source_disambiguation_and_statement_phase`. Choosing that candidate as canonical
in this phase would substitute newly invented mathematics for the source label. The metadata value
`已验证` is untrusted scheduling input and supplies neither a source pinpoint nor kernel evidence.

Consequently this phase fails at canonical human-claim identity, before minimal imports, an exact
elaborated expression and fingerprint, checked alternate transports, or meaningful removed-
hypothesis/domain/binder-scope/boundary mutations can be established. Machine status remains `M4`.
No theorem completion or downstream-node credit is claimed.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_186.lean` was inspected and elaborated only as
legacy discovery input. Its `ClassicalLagrangianData` makes the desired
`eulerLagrangeEquation : Path -> Prop` and the crucial
`firstVariationImpliesEulerLagrange` implication fields of the input data. Its `StatementShape`
then proves that supplied implication after using mathlib's local-minimum derivative theorem. This
is a valid abstract wrapper, but it does not define a concrete Euler-Lagrange equation, action
integral, endpoint variation, or regularity theorem and cannot identify the missing source claim.

The legacy file elaborates with four broad direct imports in the existing pinned environment. That
check establishes only that the old abstract interface is type-correct. It neither makes those
imports minimal for an exact target nor supplies a rev-5.6 statement fingerprint. A scoped search
of the pinned mathlib source found no terminal Euler-Lagrange/Lagrangian-mechanics declaration; this
negative discovery result is not an anchor-audit claim.

## Required unblock

An accountable source reviewer must select a stable primary or authoritative source and record its
edition, theorem/page, exact wording, and errata status. The selected claim must freeze the direction
of implication, configuration and time models, ordered binders, regularity assumptions, action and
variation definitions, endpoint policy, coordinate conventions, and all boundary/degenerate cases.
A later statement worker can then encode that exact claim, minimize its pinned imports, serialize
and hash its elaborated expression, compile any credited transports, and run all four structural
mutation classes.

## Narrow validation evidence

Commands ran from this worker clone on 2026-07-12 using only the existing canonical pinned `.lake`
artifacts. No update, build, dependency fetch, or mutation of `.lake` was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1517` | 0 | rank 186, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_186.lean)` | 0 | legacy abstract wrapper elaborated and printed its checked declarations; no exact physical target was established |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_186.lean` | 0 | hashes `651c8acc...b1d2`, `321626c8...2d81`, and `9e78d375...11b6` |
| `rg -n -i 'Euler[- ]?Lagrange\|Lagrangian mechanics\|stationary action\|least action\|Hamilton.?s principle' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching terminal declaration in the pinned mathlib source |

First failed gate: exact source-statement identity. Known failures are canonical-target selection,
minimal-import determination, expression serialization/fingerprint, checked transports, and the
required mutation tests. The assigned phase is therefore not self-tested to its completion gate,
so no `.stage1-worker-selftest.json` is emitted.
