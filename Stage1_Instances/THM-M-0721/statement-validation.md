# Statement validation record

Item: `S56-M-0721-STATEMENT`  
Base revision: `33db6c6fe92d3a3ab683d2fbc8ab03cd68505e8e`

## Frozen target

`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage` is the exact intake-selected existential
claim over binary strings. `InNP` uses polynomial-time deterministic verification with a
polynomially bounded existential certificate. `NPComplete` conjoins membership with hardness under
polynomial-time many-one reductions. The sole direct import is
`Mathlib.Computability.TuringMachine.Computable`, the smallest pinned mathlib module exposing the
used `Turing.TM2ComputableInPolyTime` interface.

The encoding of a verifier input pair is fixed locally and is self-delimiting. The target does not
name SAT: SAT is an intended future witness, while this theorem asserts only existence. The checked
`existsNPCompleteLanguage_iff_expandedTarget` wrapper expands the named completeness and reduction
predicates without weakening the claim.

## Commands and results

Commands ran in this worker clone. Lean commands ran from `Formalizations/Lean` using the existing
pinned Lake environment; no dependency operation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0721/Statement.lean` | 0 | target, expanded-target iff, four mutations, and three boundary checks elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-0721/check_statement.py` | 0 | expression SHA-256 `758b1033903c92b231a24ae3fb5e01e0bbb0d6fdb0bc41f809c062deb7b4b204`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0721/Statement.lean lean-toolchain lake-manifest.json` | 0 | statement hash recorded in `statement.json`; toolchain `651c8a...b1d2`, manifest `321626...2d81` |

## Mutation and boundary policy

The validator compares serialized explicit elaborated expressions and rejects an unchecked
verifier, a one-symbol input domain, an incorrectly scoped universal reduction, and hardness
without target membership in NP. Kernel-checked boundary declarations cover two distinct alphabet
symbols, pairing two empty words, and the empty certificate. Empty inputs and certificates are in
scope; no nonempty-language assumption is silently added.

This is statement-only evidence pending master acceptance. It does not prove the existential
target or advance anchor-audit, obligation-tree, proof, validation, or release nodes.
