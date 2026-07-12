# Exact-statement gate: blocked

Item: `S56-M-0163-STATEMENT`  
Theorem: `THM-M-0163`  
Base revision: `d7b1a45d1590cdafe55436182144e1f35e6b4194`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository wording,
which says only "geodesic equation" and "the differential equation of shortest curves on a
surface." That description does not select one proposition. In particular, it does not determine
whether the root is the intrinsic definition `nabla_(gamma') gamma' = 0`, its chart-coordinate
characterization, the implication from a regular constant-speed local minimizer, or a local
minimization result for sufficiently short geodesic segments.

These are not interchangeable. They require different hypotheses and objects, and the affine
coordinate equation is not invariant under arbitrary reparameterization. A geodesic also need not
be globally minimizing. The planned intake correctly records these boundaries but proposes a
compound interpretation while leaving the exact source theorem/page, formal domain, conventions,
and every transport unchecked. Choosing one branch now would therefore broaden or substitute the
source claim rather than elaborate its exact statement.

The exact ordered binders, hypotheses, conclusion, expression fingerprint, alternate transports,
and meaningful statement mutations cannot be frozen until that ambiguity is resolved. Machine
state remains `M4`; statement and theorem completion are false. No proxy predicate, axiom,
placeholder, `sorry`, or coordinate equation with an arbitrary function mislabeled as Christoffel
symbols was introduced.

## Pinned Lean boundary

The pinned mathlib revision has real Riemannian metric, covariant derivative, and torsion
infrastructure. `StatementProbe.lean` elaborates checks of
`Bundle.ContMDiffRiemannianMetric`, `CovariantDerivative`, `CovariantDerivative.torsion`, and
`CovariantDerivative.torsion_eq_zero_iff` using two direct imports. Narrow searches found no
geodesic predicate, Christoffel-symbol API, covariant derivative along a curve, Levi-Civita
construction, or theorem connecting local length minimizers to the equation. The probe is only
environment and feasibility evidence; it is not a canonical statement and receives no theorem
credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Existing `.lake` artifacts were read only; no update,
build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0163` | 0 | rank 662, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| repository search for `THM-M-0163`, Chinese/English names, and the source wording | 0 | only metadata, intake material, and neighboring discovery notes; no exact proposition |
| pinned-mathlib search for geodesics, Christoffel symbols, connection along curves, and Levi-Civita declarations | 1 | no matching exact statement API (`rg` exit 1 means no match) |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0163/StatementProbe.lean` | 0 | elaborated and printed only the four nearby pinned substrate declarations named above |
| `python3 -m json.tool Stage1_Instances/THM-M-0163/statement-blocker.json` | 0 | blocker JSON parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0163` | 0 | no whitespace errors |

## Retry condition

An accountable reviewer must preserve and hash an immutable primary-source edition, select and
transcribe one exact result with all incorporated definitions, assumptions, parameterization and
coordinate conventions, dispose of errata, and independently approve the mapping. The required
Lean representation of the Levi-Civita connection along a curve and any coordinate objects must
then be implemented or located in a pinned dependency. A later statement run can use those inputs
to minimize imports, serialize the exact elaborated expression, check transports, and mutation-test
the hypotheses and boundary cases.

This is the first failed gate, not completion of the statement node or a later phase. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
