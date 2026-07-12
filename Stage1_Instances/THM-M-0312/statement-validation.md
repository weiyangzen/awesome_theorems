# Statement validation record

Item: `S56-M-0312-STATEMENT`  
Base revision: `fc8e70dc8b3df070bf824de575d4a369542a621f`

## Frozen target

`Stage1Instances.THM_M_0312.UniformBoundednessTarget` freezes the exact intake-selected
normed-space Uniform Boundedness Principle. Its sole direct import is
`Mathlib.Analysis.Normed.Operator.BanachSteinhaus`. The declaration keeps all five type universes,
the two scalar fields, the isometric scalar homomorphism, the complete domain, arbitrary index type,
and the `x -> exists C -> forall i` premise scope explicit.

The checked theorem `uniformBoundednessTarget_iff_iSupTarget` relates the real-bound statement to
the pinned extended-nonnegative-supremum formulation in both directions. The more general
`WithSeminorms.banach_steinhaus` remains excluded as a substitute.

## Commands and results

Commands ran inside this worker clone on 2026-07-12. Lean commands used the existing pinned `.lake`
environment read-only; no update, build, fetch, or clone ran.

| Command | Exit | Result |
|---|---:|---|
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0312/Statement.lean)` | 0 | exact target, pinned-type witness, checked `iff`, four mutations, empty-index boundary, and explicit serialized target elaborated |
| `(cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0312/check_statement.py)` | 0 | expression SHA-256 `8d8de4ab21686d451342fe90b92b7d11d8719ae9ce140609ce8ee6f3abd53725`; all four mutations distinguished |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Stage1_Instances/THM-M-0312/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/BanachSteinhaus.lean` | 0 | hashes `cd5c59...887a`, `651c8a...1d2`, `321626...d81`, `737dd8...c61`, matching `statement.json` |

## Mutation and boundary policy

The validator separately prints and hashes the elaborated canonical expression and four mutations.
It rejects removal of domain completeness, specialization to real continuous linear endomorphisms,
moving the pointwise bound outside the vector binder, and excluding the empty family. The
kernel-checked `emptyIndexBoundary` witnesses that an empty family is genuinely in scope.

This is statement-only worker evidence pending master acceptance. It does not advance anchor audit,
obligation tree, proof, validation, or release, and it does not claim theorem completion.
