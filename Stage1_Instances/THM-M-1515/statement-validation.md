# Statement validation record

Item: `S56-M-1515-STATEMENT`  
Base revision: `b1859cdd6c55344d7a9e8949676f478eb9fee7f0`

## Frozen target

`Stage1Instances.THM_M_1515.NoetherFirstTheoremTarget` selects the forward,
finite-dimensional form of Noether's first theorem. It fixes time, uses a
time-independent Lagrangian on a real normed vector space, permits
quasi-invariance by a configuration-dependent boundary term, and concludes
`HasDerivAt` zero for the resulting charge along regular Euler-Lagrange curves.
The stronger derivative witness avoids treating the fallback value of `deriv`
at a nondifferentiable point as conservation.

The intake left time transformations, signs, and the object model open. This
statement chooses vertical transformations (no time action), the charge
`partial_v L(generator) - boundary`, and an explicit infinitesimal
quasi-invariance equation. Field theory, converse claims, local manifold
domains, and time-dependent Lagrangians remain excluded.

## Commands and results

All commands ran inside this worker clone. Lean commands ran from
`Formalizations/Lean` using the existing pinned Lake environment; no dependency
update or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1515/Statement.lean` | 0 | canonical target, direct expansion, and four structural mutations elaborated; explicit target expression printed |
| `python3 Stage1_Instances/THM-M-1515/check_statement.py` | 0 | expression SHA-256 `91f6f9b51af1889d9f92f9647f41b0c3e23574783ee97517fd0498b67d8e537e`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-1515/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `60b548...9add`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1515` | 0 | rank 184, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Mutation policy

The validator compares explicit elaborated expressions. It distinguishes the
canonical target from strict symmetry only, omission of the Euler-Lagrange
premise, removal of finite dimensionality, and a weaker conclusion stated with
the potentially non-differentiable `deriv` fallback.

This is statement-only evidence pending master acceptance. The human-source
classification remains `H1`; no proof closure or downstream-node completion is
claimed.
