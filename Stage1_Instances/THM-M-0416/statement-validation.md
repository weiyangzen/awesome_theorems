# Statement validation record

Item: `S56-M-0416-STATEMENT`  
Base revision: `1371ca5a74c6cbc303b18e97c518ffe32b24e9ef`

## Frozen target

`Stage1Instances.THM_M_0416.DirichletUnitTheoremTarget` is the intake-selected finite-free quotient,
unit-rank, and unique-decomposition formulation. Its only direct import is
`Mathlib.NumberTheory.NumberField.Units.DirichletTheorem`. The checked transport to the direct
local restatement of the historical `StatementShape` is definitional identity.

## Commands and results

Commands ran in this worker clone. Lean ran from `Formalizations/Lean` using the existing pinned
Lake environment; no dependency or `.lake` mutation command was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0416/Statement.lean` | 0 | target, checked historical-shape identity, mutation declarations, and rational boundary elaborated; explicit target expression printed |
| `python3 Stage1_Instances/THM-M-0416/check_statement.py` | 0 | expression SHA-256 `06bf575f99a9885ece0264066a051c4e066fb5058395b51fb5b4a8e3b18318d1`; removed-hypothesis mutation failed elaboration and three expression mutations differed |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-0416/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `0d98e8...0f4d`, `651c8a...1d2`, and `321626...2d81`, matching `statement.json` |

## Mutation and boundary policy

The validator removes `NumberField K` and requires the mutated source to fail elaboration. It also
distinguishes specialization to `Rat`, universal-to-existential binder relocation, and addition of
a positive-rank premise from the explicit canonical expression. `RationalBoundaryTarget`
elaborates the rank-zero/empty-product specialization; the canonical proposition adds no
positive-rank or exceptional-field premise.

This is statement-only evidence pending master acceptance. It does not prove Dirichlet's unit
theorem or advance anchor-audit, obligation-tree, proof, validation, or release nodes.
