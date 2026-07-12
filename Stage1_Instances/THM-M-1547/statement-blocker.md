# THM-M-1547 exact-statement blocker

Item: `S56-M-1547-STATEMENT`  
Base revision: `07528e773ee08308d0b56d7d25d934d4839c658f`

## Decision

The exact Lean 4 target cannot yet be truthfully frozen or elaborated. The repository source gives
only the topic phrase `完全可积的哈密顿系统` ("completely integrable Hamiltonian systems"), attributes
it to many mathematicians in the twentieth century, and leaves its definitions, assumptions,
proof, and source location unspecified. The accepted intake narrows the intended family to the
Liouville-Arnold theorem, but deliberately leaves the following proposition-changing choices open:

- the primary-source edition, theorem/page, exact wording, and errata decision;
- the symplectic-manifold and smoothness conventions and whether Hamiltonian flows must be complete;
- the meaning and locus of independence of the first-integral differentials;
- whether compactness and connectedness apply to a fiber, one component, or every selected fiber;
- whether the conclusion is only a torus diffeomorphism, linearized flow on that torus, a saturated
  neighborhood with action-angle coordinates, or a Hamiltonian normal form; and
- the behavior at dimension zero, empty or singular levels, noncompact fibers, boundaries, and
  globally obstructed action-angle coordinates.

These choices yield inequivalent theorems. Neither the historical Liouville citation nor the
uninspected Arnold textbook section in the intake supplies a reviewed theorem transcription and
assumption crosswalk. Choosing one modern formulation now would invent missing mathematics rather
than elaborate the exact assigned target.

Consequently the first failed gate is rev-5.6 exact source-statement identity, before canonical
Lean elaboration. There is no canonical declaration or expression fingerprint, no meaningful
minimal-import result, no checked transport to alternate encodings, and no valid mutation suite for
removed hypotheses, changed domains, binder scope, or boundary cases. Machine status remains `M4`.
No statement acceptance, proof credit, audit completion, or theorem completion is claimed.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_206.lean` was inspected and elaborated only as
legacy discovery input. Its `CompletelyIntegrableSystem` stores `invariantLagrangianTori` and
`actionAngleCoordinates` as unconstrained `Prop` fields, and its `CompleteIntegrabilityConclusion`
merely projects those fields. It uses a finite-coordinate function-space surrogate rather than a
smooth symplectic manifold and stores several absent analytic and geometric bridges as proposition
fields. Thus its `StatementShape` is an abstract interface whose desired conclusion is already
carried by the input structure, not an exact Liouville-Arnold statement selected from a source.
Copying or accepting it would violate the intake's explicit exclusion of that substitution.

The legacy module elaborates with four broad imports in the pinned environment. That establishes
only that the old interface and its adjacent substrate lemmas typecheck. Since the exact target is
unknown, this run cannot establish an exact-target import set or prove those imports minimal.

## Required unblock

An accountable source review must select a stable primary edition and exact theorem/page, quote the
result and governing definitions, map every hypothesis and conclusion, check errata, and decide all
regularity, compactness, completeness, locality, and degenerate-case choices above. A later
statement worker can then encode precisely that claim, minimize its pinned imports, print and hash
the elaborated expression, check transports, and run the four mutation classes.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12. The Lean command reused the existing canonical
`.lake` artifacts. No `lake update`, build, fetch, clone, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Passed: 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1547` | 0 | Rank 206, planned, `hard_mathlib_anchor_and_wrapper`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_206.lean)` | 0 | Legacy abstract boundary elaborated and printed its audit probes; this is not exact-statement evidence |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_206.lean` | 0 | SHA-256: `651c8acc...b1d2`, `321626c8...2d81`, and `70849eb4...15b6` |
| repo-local `rg` search for Liouville-Arnold, complete integrability, and action-angle terms, excluding `.lake` and this dossier | 0 | Only terse research/blueprint records and legacy boundary modules were found; no reviewed exact source statement exists locally |

The assigned phase is blocked rather than genuinely self-tested, so no
`.stage1-worker-selftest.json` is emitted.
