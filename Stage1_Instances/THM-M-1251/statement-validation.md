# Statement validation record

Item: `S56-M-1251-STATEMENT`  
Base revision: `935f676246c95d817740248fb8588e8cea34c00d`

## Frozen target

`Stage1Instances.THM_M_1251.TemperedDistributionsAreSchwartzDual` fixes the intake claim to
finite-dimensional real normed base spaces and complex-valued distributions. The dual is
mathlib's pointwise-convergence continuous-linear-map type, not a strong dual. The sole direct
import is `Mathlib.Analysis.Distribution.TemperedDistribution`.

The checked `Iff.rfl` transport expands the local dual abbreviation. Structural mutation checks
distinguish removal of finite dimensionality, specialization to Euclidean coordinate spaces, and
a binder-scope change. A kernel-checked boundary theorem confirms that dimension zero remains in
scope.

## Commands and results

All Lean commands ran from `Formalizations/Lean` using the existing pinned `.lake` artifacts.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1251/Statement.lean` | 0 | target, checked expansion, three mutations, and zero-dimensional boundary elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-1251/check_statement.py` | 0 | expression SHA-256 `597f3e4b...a8ab9`; all three structural mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-1251/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `30207d...77cf`, `651c8a...1d2`, and `321626...d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1251` | 0 | rank 171, planned, L0/rework-required, theorem incomplete |

This is statement-only evidence pending master acceptance. The source crosswalk still lacks the
pinpoint primary-source evidence required for `H0`, and later execution nodes remain open.
