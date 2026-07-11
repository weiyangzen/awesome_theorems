# Exact-statement gate: blocked

Item: `S56-M-1311-STATEMENT`  
Base revision: `4d48a3c5fbec6d005a64a99338e40c001656264c`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the accepted intake record. The
repository discovery wording is only "Einstein equations have local existence." The intake
deliberately leaves unresolved the precise theorem/page statement in the 1952 source and all of
the choices needed to identify one proposition:

- the vacuum or matter-coupled equation regime and sign conventions;
- spatial and spacetime dimensions, topology, and the regularity class of the initial data;
- the concrete Riemannian metric and symmetric second-fundamental-form objects;
- the Hamiltonian and momentum constraint equations;
- the gauge or coordinate conditions and their quantifier scope;
- the solution/development notion, the nonzero local-time condition, and realization of the data;
- whether uniqueness, geometric equivalence, or continuous dependence belongs to this target.

These choices produce inequivalent theorems. Selecting a smooth modern vacuum-development
formulation, a Sobolev formulation, a harmonic-gauge reduced PDE statement, or a theorem with
uniqueness would invent mathematics not fixed by the intake. Omitting those choices would broaden
the claim into an arbitrary abstract existence proposition. The neighboring maximal globally
hyperbolic development theorem `THM-M-1312` must also remain excluded.

The intake therefore remains at `[H1, M4, R3]` with a null module, declaration, expression hash,
and environment fingerprint. Its source crosswalk explicitly requires a source-text hash,
theorem-level pinpoint, exact assumptions, and an errata review before this phase can freeze a
target. The first failed gate is canonical human-claim identity, before minimal imports,
expression serialization, checked transports, or meaningful hypothesis/domain/binder/boundary
mutations can be established.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_167.lean` was inspected and kernel-checked only as
legacy discovery input. Its `EinsteinInitialData` stores the metric and second fundamental form in
arbitrary carrier types and represents the constraint equations, gauge, and regularity as
uninterpreted `Prop` fields. `LocalEinsteinDevelopment` similarly stores Lorentzian signature,
the vacuum equations, realization, gauge compatibility, and uniqueness as proposition fields
paired with assumed inhabitants. Consequently its `StatementShape` asks for a package already
containing the desired facts; it is not an encoding of the Einstein equations or an exact
crosswalk to an identified source theorem. The file itself calls this a statement-shape boundary.

That legacy module elaborates with six broad imports. The check establishes syntax and types only;
it cannot establish exactness or minimal imports for an exact target. A case-insensitive search of
the pinned mathlib source found no Lorentzian-metric, Ricci-curvature, Einstein-tensor, vacuum-
Einstein-equation, or terminal Einstein-equation API. Introducing local uninterpreted substitutes
would repeat the legacy abstraction and is rejected rather than credited as statement completion.

## Required unblock

An accountable source reviewer must pin an immutable copy of the primary source and identify the
edition, theorem and page, exact wording, assumptions, and errata status. The reviewer must freeze
the equation regime, dimensions, data and constraint objects, topology and regularity, gauge
scope, local interval, development/realization notion, uniqueness/equivalence content, and all
degenerate cases. A later statement worker can then implement the necessary geometric/PDE object
model (or pin a compatible external implementation), minimize imports, elaborate and serialize the
exact expression, add checked transports, and run the four required structural mutations.

## Narrow validation evidence

Commands were run from this worker clone on 2026-07-12. The clone's `.lake` is the existing
canonical symlink; no update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1311` | 0 | rank 167, planned, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_167.lean)` | 0 | legacy abstract module elaborated and printed its declarations; this is not exact-statement credit |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |
| `rg -n -i 'lorentzian|ricci curvature|einstein tensor|vacuum einstein|einstein equation' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching pinned-mathlib API source found; exit 1 means no match |

The assigned statement phase is blocked, not self-tested complete. No
`.stage1-worker-selftest.json` is emitted. This record gives no theorem proof or downstream-node
credit and makes no theorem-completion claim.
