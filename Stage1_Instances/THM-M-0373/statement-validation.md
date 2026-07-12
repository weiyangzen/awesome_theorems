# Statement validation record

Item: `S56-M-0373-STATEMENT`  
Base revision: `6f601f70dc531aafc2c0e73ea51db67cebeb3ad9`

## Frozen target

`Stage1Instances.THM_M_0373.CoronaTheoremTarget` formalizes the intake-selected classical
finite-generator Bezout formulation on `Metric.ball (0 : ℂ) 1`. The generator index is an arbitrary
nonempty finite type. Membership in `H∞` is represented by `AnalyticOnNhd ℂ` on that open ball and
`Bornology.IsBounded` for the restricted image. The lower bound is an explicit `δ : ℝ`, with
`0 < δ` and `δ <= sum_i ‖f_i(z)‖`. The conclusion asserts bounded analytic coefficients and the
pointwise identity `sum_i f_i(z) * g_i(z) = 1`; it asserts no quantitative coefficient bound.

The direct imports are the three pinned modules in `statement.json`. The unit-disc import is needed
for the complex analytic and normed structure instances; removing it makes the target fail to
elaborate. `coronaTheoremTarget_iff_expanded` kernel-checks the unfolding of the local disc and
`H∞` predicates.

## Commands and results

All commands ran in this worker clone. Lean commands ran from `Formalizations/Lean` using the
existing pinned `.lake` artifacts read-only. No update, build, clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0373/Statement.lean` | 0 | canonical target, direct-expansion iff, and four mutations elaborated; explicit canonical expression printed |
| `python3 ../../Stage1_Instances/THM-M-0373/check_statement.py` | 0 | expression SHA-256 `682732528e7459a7e3cd1be98c6a0bc35ce0d80a7b7be1011b0bade5073d69cf`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0373/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `548f86...abe`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets pass |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0373` | 0 | rank 865, planned, legacy artifacts unaccepted, theorem incomplete |

## Boundary and status policy

The mutation checker rejects omission of `Nonempty ι`, omission of `0 < δ`, replacement of the sum
of norms by squared norms, and replacement of the open disc by the closed disc. Singleton and
constant families remain admitted. An empty family, nonpositive delta, the boundary circle,
several-variable variants, and maximal-ideal-space density are not silently substituted.

This is statement-only evidence pending master acceptance. The exact primary-source passage and
independent H review remain open, as do anchor audit, obligation tree, proof, validation, and
release. No theorem-completion claim is made.
