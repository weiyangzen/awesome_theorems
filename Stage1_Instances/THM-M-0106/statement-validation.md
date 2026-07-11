# Statement validation record

Item: `S56-M-0106-STATEMENT`  
Base revision: `8f566755a28459bda22aa05071d96cc391ef0db6`

## Frozen target

`Stage1Instances.THM_M_0106.NoetherNormalizationTarget` is the exact claim selected from the intake
scope. It retains both the coordinate-ring normalization data and the public affine-space
conclusion. The binders range over a field `k` and a nonzero finite-type commutative `k`-algebra
`R`. The conclusion provides an injective finite map from `MvPolynomial (Fin s) k`, together with
the induced finite morphism from `Spec R` to affine space and its checked coordinate-ring identity.

The sole direct import is `Mathlib.AlgebraicGeometry.AffineSpace`. A trial direct import of
`Mathlib.AlgebraicGeometry.Morphisms.Finite` was redundant and was removed before final validation.
`target_iff_pinnedAffineSpecCandidateShape` checks both directions between this target and the
historical affine-Spec encoding. This is statement-identity evidence only, not root proof credit.

## Commands and results

All commands ran in this worker clone. Lean commands ran from `Formalizations/Lean` against the
existing canonical `.lake` symlink; no dependency update, fetch, clone, or build was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0106/Statement.lean` | 0 | exact target, affine-Spec transport, four mutations, and the zero-variable boundary elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0106/check_statement.py` | 0 | expression SHA-256 `4980834b63da78609158f944b53234d72089e2bfaacb348461de2651aa671209`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0106/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `cdcc10...d291`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0106` | 0 | rank 30, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0106` | 0 | no whitespace errors |

## Mutation and boundary policy

The validator compares explicit elaborated expressions and rejects removal of `Nontrivial R`,
specialization of the arbitrary field to `Rat`, relocation of the polynomial-variable count, and
loss of the finite affine-space morphism. The natural variable count includes `s = 0`; the module
checks that an empty `Fin 0` family is inhabited as a function. The target deliberately adds no
reducedness, irreducibility, algebraic-closedness, or positive-dimension hypothesis.

This is statement-only evidence pending master acceptance. It does not prove Noether normalization
or advance anchor-audit, obligation-tree, proof, validation, or release nodes.
