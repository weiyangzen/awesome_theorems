# THM-M-0045 statement validation

Item: `S56-M-0045-STATEMENT`. Base revision:
`540472523b6c0717ed925193071191f81f62d6eb`; base tree:
`64b0c81418ef2c97b0250188444c672b9ae885d0`.

## Frozen Target

`Stage1Instances.THM_M_0045.SchurTriangularizationTarget` quantifies over a natural number `n`
and arbitrary `A : Matrix (Fin n) (Fin n) Complex`. It returns a matrix `U` that belongs to
`Matrix.unitaryGroup (Fin n) Complex` and makes `star U * A * U` satisfy
`Matrix.BlockTriangular _ id`. By the pinned predicate definition this is upper triangular: entries
whose column index is strictly less than their row index vanish.

The target selects the finite complex matrix specialization of Axler's upper-triangular
operator/orthonormal-basis Schur theorem. Dimensions zero and one are included and kernel-checked
with the identity witness. The source PDF was inspected, but immutable preservation, corrections,
definition transport, catalog identity, and independent H0 review remain open. Thus source status
stays H1. Schur's original real-or-complex lower-triangular convention is an uncredited alternate,
not silently conflated with the selected target.

## Commands And Results

All commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). The automation-provided
canonical `.lake` symlink was reused read-only. No update, build, dependency clone/fetch, or `.lake`
mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0045` | 0 | rank 1085; planned; no legacy slot; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e3...`; Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0045/Statement.lean` | 0 | target, four expected mutation identity rejections, and fully explicit expression elaborated; output SHA-256 `9ecf65c5...b985` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0045/BoundaryProbe.lean` | 0 | zero- and one-dimensional witnesses and selected upper-triangular/unitary conventions kernel-checked; empty output |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0045/check_statement.py` | 0 | expression/source/output hashes, three deletion probes, four mutation fingerprints, boundaries, authority identity, structured artifacts, packet, and pins agree |
| import deletion probe without `Mathlib.Data.Complex.Basic` | 1 expected | `Complex` is unknown |
| import deletion probe without `Mathlib.LinearAlgebra.Matrix.Block` | 1 expected | `Matrix.BlockTriangular` is unknown |
| import deletion probe without `Mathlib.LinearAlgebra.UnitaryGroup` | 1 expected | `Matrix.unitaryGroup` is unknown |
| `python3 -m json.tool` over structured statement artifacts and worker packet | 0 | all structured artifacts parse |
| prohibited-construct scan over target-owned `.lean` files | 1 expected no match | no `sorry`, `admit`, `sorryAx`, custom `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0045 .stage1-worker-selftest.json` and new-file no-index checks | 0 | no whitespace diagnostics |

The historical `check_intake.py` is bound to intake-time authority hashes, its old nine-file
inventory, and the pre-integration intake state. It now fails closed and is neither modified nor
cited as current statement evidence.

## Mutations And Boundaries

The validator serializes the root and four mutations with `pp.universes=true` and
`pp.explicit=true`, requires pairwise-distinct SHA-256 fingerprints, and checks the expected Lean
identity failures. The mutations remove unitarity, replace complex matrices by rational matrices,
change the universally quantified matrix to an existential one, or exclude dimension zero.

The three direct imports are individually necessary. No eigenspace, Gram-Schmidt,
triangularizable-endomorphism, spectrum, or proof-bearing Schur module is imported. No alternate
encoding is credited because no equality, iff, or directional transport has yet been checked.

## Status Boundary

This is statement-only worker evidence pending master acceptance. It defines a proposition but no
inhabitant and neither audits nor credits a formal proof candidate. Source acceptance, checked
transports, anchor audit, obligation registry, proof, composition, trust closure, readable
reconstruction, hermetic validation, independent verification, audit completion, and theorem
completion remain open.
