# Statement validation record

Item: `S56-M-1003-STATEMENT`  
Base revision: `656a1be3548d492354ef99a755ef0bbcab9bd22b`

## Frozen target

`Stage1Instances.THM_M_1003.LpMartingaleConvergenceTarget` freezes the intake-selected,
real-valued discrete-time claim. The strict range `1 < p < infinity`, martingality, and uniform
`L^p` bound are fields of `LpBoundedMartingale`; the existential limit must simultaneously be in
`L^p`, be the almost-everywhere pointwise limit, and be the `L^p`-norm limit. The sole direct import
is `Mathlib.Probability.Martingale.Convergence`.

The target uses a finite measure rather than probability normalization because the conventional
claim and mathlib API do not require total mass one. It does not add the legacy candidate's
independent `L^1` bound. It existentially quantifies the common limit instead of prematurely
selecting `Filtration.limitProcess`; equivalence with that selected limit is later proof/anchor
work, not an assumed statement transport.

## Commands and results

All commands ran in this worker clone. Lean commands ran from `Formalizations/Lean` against the
existing pinned Lake artifacts; no dependency operation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1003/Statement.lean` | 0 | exact target, expanded-form iff, four mutations, and endpoint-exclusion lemmas elaborated; explicit expressions printed |
| `python3 ../../Stage1_Instances/THM-M-1003/check_statement.py` | 0 | statement expression SHA-256 `ead768...b8e9f`; statement file SHA-256 `338885...60ed`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard and 1546-target projection passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, all uniform L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1003` | 0 | rank 283, planned, L0/rework-required, theorem incomplete |

## Mutation and boundary policy

The checker compares the explicit elaborated expressions and distinguishes removal of the
martingale/convergence content, removal of the `L^p` bound, admission of the `p = 1` endpoint, and
removal of almost-sure convergence. Kernel-checked lemmas derive `p != 1` and `p != infinity` from
the strict stored inequalities. The zero-measure case is retained rather than silently adding a
probability-space hypothesis.

This is statement-only evidence pending master acceptance. It does not prove the theorem or advance
anchor-audit, obligation-tree, proof, validation, or release nodes.
