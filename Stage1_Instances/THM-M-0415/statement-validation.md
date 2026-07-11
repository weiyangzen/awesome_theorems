# Statement validation record

Item: `S56-M-0415-STATEMENT`  
Base revision: `4fe349b4364c7aee03dbe67f21b7a631e12042da`

## Frozen target

`Stage1Instances.THM_M_0415.IdealClassGroupFiniteTarget` quantifies over an arbitrary universe,
field `K`, and `NumberField K` instance, and concludes
`Finite (ClassGroup (NumberField.RingOfIntegers K))`. Its sole direct import is
`Mathlib.NumberTheory.NumberField.ClassNumber`. The checked iff with `FintypePresentation`
keeps the stronger data-bearing encoding separate from the source-level proposition.

## Commands and results

Commands ran inside this worker clone. Lean ran from `Formalizations/Lean` with the existing pinned
Lake environment; no dependency update or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0415/Statement.lean` | 0 | target, Finite/Fintype iff, four mutations, and rational boundary elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0415/check_statement.py` | 0 | expression SHA-256 `7597a79fb775bc7ecf0830020941f6962e64c6d3251d114f780b32e4c25d1590`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0415/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `3dc07d...8eda`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |

## Mutation and boundary policy

The validator compares explicit elaborated expressions and rejects removal of the number-field
structure, specialization from arbitrary `K` to `Rat`, changing the typeclass binder to an
implication, and restriction to class number one. The kernel-checked rational example confirms
that the degree-one boundary is included. No nontriviality, class-number, degree, signature, or
effectiveness condition is silently introduced.

This is statement-only evidence pending master acceptance. It does not inspect or credit the
mathlib terminal proof body and does not advance later nodes.
