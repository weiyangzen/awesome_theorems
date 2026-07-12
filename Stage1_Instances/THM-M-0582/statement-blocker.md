# Exact-statement gate: blocked

Item: `S56-M-0582-STATEMENT`  
Theorem: `THM-M-0582`  
Base revision: `7f7539be2690c4075e12d47f531aae8b181f4944`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the accepted intake and repository
source record. The intake freezes a broad intended subject, but expressly leaves the precise
boundary and finite-volume conventions, exceptional cases, canonical source formulation, and
concrete object model open. Its candidate sources have not been inspected to an accepted
theorem/page statement and assumption/errata crosswalk. These unresolved choices change the
proposition, rather than merely its Lean presentation.

In particular, the current material does not decide:

- whether the root quantifies over closed orientable manifolds directly or over their prime
  factors, and exactly how connectedness and boundarylessness are represented;
- whether the conclusion is a prime-plus-JSJ decomposition, a characteristic-submanifold
  formulation, or a thick-thin/Ricci-flow formulation, and which checked implications make these
  formulations equivalent;
- which finiteness, incompressibility, minimality, uniqueness, isotopy, and reconstruction clauses
  belong to the torus decomposition;
- whether each cut piece must carry a complete locally homogeneous metric, a finite-volume
  geometric structure on its interior, or a quotient modeled on one of the eight geometries;
- how spherical, Seifert-fibered, graph-manifold, reducible, and boundary cases are partitioned.

Selecting answers in this phase would invent missing mathematics. A proposition obtained by
introducing abstract predicates or structure fields for those clauses would only elaborate an
interface whose semantics are assumed; it would not elaborate the exact geometrization theorem.
Accordingly no `Statement.lean`, expression fingerprint, alternate-encoding transport, or mutation
suite is emitted, and no statement receipt, proof credit, audit completion, or theorem completion
is claimed. The machine boundary remains `M4` as recorded by the intake.

## Historical Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_128.lean` elaborates in the pinned environment, but
it is not exact-statement evidence for this target. Its `GeometrizationPackage` contains
proposition-valued fields named for prime decomposition, JSJ decomposition, Thurston pieces, and a
Ricci-flow bridge. The terminal field concludes only `True` from those assumed fields, while
`GeometrizationStatementShape` asks for nonemptiness of the package. Thus the module assumes opaque
surrogates for precisely the content that the target must state and cannot establish statement
identity. The file itself labels this construction an abstract statement shape and says that it
does not prove geometrization.

The module's single direct import,
`Mathlib.Geometry.Manifold.PoincareConjecture`, is sufficient to elaborate that historical abstract
surface. This successful check neither identifies a minimal import set for a concrete
geometrization target nor supplies missing APIs for prime decomposition, incompressible tori, JSJ
pieces, the eight model geometries, completeness/finite volume, or reconstruction.

## Required unblock

An accountable source review must select one stable primary formulation and record its exact
edition or immutable version, theorem/section/page location, definitions, ordered hypotheses,
conclusion, conventions, corrections, and errata. The review must resolve every choice listed
above and map each clause to a concrete Lean representation rather than an uninterpreted predicate
standing for the conclusion. If multiple source formulations are retained, it must also specify
the direction of every required transport. A later statement execution can then choose minimal
pinned imports, elaborate and print the canonical expression, hash it, kernel-check the transports,
and mutation-test hypotheses, domains, binder scope, and boundary cases.

## Narrow validation evidence

Commands were run in this worker clone on 2026-07-12. Lean reused the existing symlink to the
canonical pinned `.lake` artifacts; no dependency update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0582` | 0 | rank 624, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_128.lean` | 0 | historical abstract module elaborated and printed its audit checks; not exact-statement evidence |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, matching the repository pin |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/.lake/packages/mathlib/Mathlib/Geometry/Manifold/PoincareConjecture.lean` | 0 | hashes `651c8acc...b1d2`, `321626c8...2d81`, and `4b9c454d...b8cf` |

Known failures are canonical human-claim identity, a concrete Lean object model, minimal imports,
expression fingerprint, checked transports, and meaningful structural mutations. The assigned
deliverable is therefore not self-tested or complete, so no `.stage1-worker-selftest.json` is
emitted. Master acceptance remains outstanding, and this artifact does not modify the generated
blueprint checklist or execution DAG.
