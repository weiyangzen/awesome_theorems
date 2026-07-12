# Exact-statement gate: blocked

Item: `S56-M-1535-STATEMENT`  
Theorem: `THM-M-1535`  
Base revision: `ef21b67a78defe13c59d95d8eb60a9c05b8afd53`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the frozen intake. The repository
claim is only "AdS/CFT duality" / "duality between gravity and quantum field theory." The intake
deliberately leaves the primary formulation, bulk and boundary models, physical regime, observable
dictionary, renormalization convention, and equality notion open. Those choices are not notation:
they select inequivalent propositions. In particular, the current record does not determine:

- a concrete bulk background, such as type-IIB string theory on `AdS5 x S5`, or whether the bulk
  theory is full string theory, quantum gravity, classical gravity, or a supergravity limit;
- the boundary CFT, spacetime dimension, gauge group, coupling and large-`N` regime;
- the state, field, operator, source, boundary-condition, and observable spaces;
- whether the conclusion is equality of partition/generating functionals, equality of a selected
  correlator sector, an operator/state dictionary, or an equivalence of theories;
- the regulator, holographic-renormalization prescription, approximation status, and boundary or
  degenerate cases.

The cited Maldacena, Gubser-Klebanov-Polyakov, and Witten papers are discovery candidates only in
the intake: no immutable edition plus pinpoint theorem/equation and complete assumption crosswalk
has been selected. Moreover, the full correspondence is presented as a conjectured physical
duality rather than a single established mathematical theorem with repository-ready domains and
hypotheses. Selecting a protected-observable check, a large-`N` or supergravity approximation, or
an abstract dictionary would narrow or replace the named root and is forbidden by the statement
gate.

Therefore there is no canonical human proposition from which to determine minimal imports, ordered
binders and universes, an elaborated expression fingerprint, checked alternate transports, or
meaningful removed-hypothesis/domain/binder-scope/boundary mutations. The first failed gate is the
canonical source-statement identity gate in section 5 of
`Docs/Stage1_Blueprint_rev-5.6.md`.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_177.lean` was inspected and compiled only as
unaccepted discovery input. Its `StatementShape` quantifies over arbitrary abstract bulk and
boundary records and asks for `Nonempty (AdSCFTDuality bulk boundary)` whenever one proposition
field, `bulk.conformalBoundarySpecified`, holds. The records themselves contain unconstrained
stand-ins for geometry, quantum-gravity axioms, holographic renormalization, conformal symmetry,
QFT axioms, locality, and observables. This does not encode a selected physical model or a
source-crosswalked AdS/CFT formulation. The file explicitly calls the declaration a statement-shape
candidate and says that no terminal proof is claimed.

The legacy module elaborates in the pinned environment. That result establishes only syntax and
type correctness of the abstract historical boundary. Its four broad direct imports cannot be
minimal-import evidence for an unidentified exact target, and neither the structure fields nor the
projection lemmas prove the physical correspondence.

## Required unblock

An accountable source review must first select one immutable primary formulation and record its
exact passage/equation, assumptions, caveats, and status. It must freeze the concrete bulk and
boundary models, dimension and regime, observable/source dictionary, boundary conditions,
regularization and renormalization conventions, equality/equivalence relation, and all limiting and
degenerate cases. If the selected root is conjectural, it must remain classified as mathematical
debt; an axiomatized interface may document the conjecture but cannot provide statement or proof
credit for the named correspondence. A later statement worker can then encode the selected claim,
minimize pinned imports, serialize its elaborated expression and environment, and execute all four
required mutation classes.

## Narrow validation evidence

Commands were run from this worker clone on 2026-07-12. Lean used the existing pinned Lake
environment. No `lake update`, build, dependency fetch, or mutation of `.lake` was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1535` | 0 | rank 177, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_177.lean)` | 0 | legacy abstract statement boundary elaborated; no exact-statement credit |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |

Known failures are the exact canonical target, minimal imports, expression/environment fingerprint,
checked transports, and statement mutations. The assigned deliverable is not genuinely self-tested
or complete, so no `.stage1-worker-selftest.json` is emitted. No statement-node acceptance,
downstream-node credit, audit completion, or theorem completion is claimed.
