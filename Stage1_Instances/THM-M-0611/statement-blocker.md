# Exact-statement gate: blocked

Item: `S56-M-0611-STATEMENT`  
Theorem: `THM-M-0611`  
Base revision: `6930a74babf81271621795a2d247c6a48f1c432e`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is "Lagrangian intersection Floer homology" / "intersection theory of
Lagrangian submanifolds". This names a theory and family of results, not one proposition. The
accepted intake correctly leaves both the primary-source pinpoint and theorem variant unselected.

A familiar formulation cannot be chosen silently. The label could denote construction of the
Floer complex and homology, the proof that the strip-count differential squares to zero,
continuation and Hamiltonian-isotopy invariance, comparison with ordinary homology, the resulting
total-Betti-number intersection lower bound, or the distinct cup-length estimate. These roots have
different ambient, compactness, bubbling, transversality, relative-homotopy, Maslov, orientation,
coefficient, grading, quantifier, and conclusion data. Substituting any one of them would invent
missing mathematics.

The intake's three Floer papers are discovery anchors only. None has been accepted at the
granularity of an immutable edition, exact theorem and page, incorporated definitions, assumptions,
conventions, errata, and independent source review. Consequently there is no canonical human claim
from which to derive minimal imports, an elaborated expression fingerprint, checked transports, or
meaningful removed-hypothesis, changed-domain, binder-scope, and boundary mutations. No assumed
Floer interface, axiom, placeholder, weakened finite model, or broadened Arnold-conjecture target was
introduced. Machine state remains `M4`; statement and theorem completion are false.

## Pinned Lean boundary

`StatementProbe.lean` imports only `Mathlib.LinearAlgebra.SymplecticGroup` and checks its matrix
`J`, `symplecticGroup`, membership characterization, and determinant-unit result. This is the
closest name-specific substrate found in the pinned environment, but it is finite-dimensional
linear algebra rather than symplectic-manifold or Floer infrastructure. Narrow searches found no
symplectic-manifold, Lagrangian-submanifold, Hamiltonian-isotopy, pseudoholomorphic-curve,
Floer-complex, or Floer-homology API. The probe is feasibility evidence only and receives no
statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The existing canonical `.lake` artifacts were read
only; no update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0611` | 0 | rank 648, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| repository `rg` search for the theorem ID, Chinese/English names, and cited paper titles | 0 | only underspecified metadata, intake discovery material, and a related target; no exact proposition |
| pinned-mathlib `rg` search for Lagrangian Floer, pseudoholomorphic, symplectic manifold, Lagrangian submanifold, Hamiltonian isotopy, and Maslov | 1 | no matching symplectic-topology or Floer API (`rg` exit 1 means no match) |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0611/StatementProbe.lean` | 0 | elaborated four finite-dimensional symplectic-group substrate checks |
| `python3 -m json.tool Stage1_Instances/THM-M-0611/statement-blocker.json` | 0 | blocker JSON is syntactically valid |
| `git diff --check -- Stage1_Instances/THM-M-0611` | 0 | no whitespace errors |

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary-source edition, select
and transcribe one exact theorem with all incorporated definitions and assumptions, dispose of
errata, and independently approve the mapping. A later statement worker can then encode that same
claim with real Lean definitions, minimize pinned imports, serialize and hash the elaborated
expression, check alternate transports, and run all four statement mutations.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
