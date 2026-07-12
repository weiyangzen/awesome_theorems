# Statement validation record

Item: `S56-M-0498-STATEMENT`  
Base revision: `a73eeda2e13e2eac063df01faf369a96820fa249`

## Frozen target

`Stage1Instances.THM_M_0498.RiemannVonMangoldtTarget` freezes the classical
Chebyshev-psi version of the explicit formula. The domain is `x : Real` with
`1 < x`; prime-power discontinuities are excluded. Nontrivial zeros are those
in the open critical strip, and the zero sum uses a complete injective
enumeration whose positive multiplicities equal zeta's meromorphic orders,
ordered by nondecreasing absolute imaginary part. This makes the limiting
convention part of the type.

The conclusion is
`psi(x) = x - sum_rho x^rho/rho - log(2*pi) - (1/2)*log(1-x^(-2))`,
expressed as convergence of the ordered partial sums.

The direct imports are `Mathlib.NumberTheory.Chebyshev`,
`Mathlib.NumberTheory.LSeries.RiemannZeta`, and
`Mathlib.Analysis.Meromorphic.Order`. The ordinary prime-counting variant is
not silently identified with this root; its normalization and Mobius-inversion
transport remain later obligations.

## Commands and results

All Lean commands ran from `Formalizations/Lean` using the existing pinned Lake
environment. No dependency was fetched or updated.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0498/Statement.lean` | 0 | target, definitions, expanded-form iff, and four mutations elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0498/check_statement.py` | 0 | expression SHA-256 `4de2508b7d4cc86d13c5d51e1b5d6b8c61e43dec6655035224c21e25745af526`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0498/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `ffdaf4...623a`, `651c8a...1d2`, and `321626...2d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0498` | 0 | rank 258, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Mutation boundary

The validator compares the explicitly elaborated root with mutations removing
the lower bound, changing the argument domain, changing binder scope, and
including prime-power discontinuities. Each mutation has a distinct kernel
expression. These checks protect the statement boundary; they do not prove
that any mutated proposition is false and supply no proof credit for the root.

This is statement-only evidence pending master acceptance.
