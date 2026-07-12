# Statement validation record

Item: `S56-M-1566-STATEMENT`  
Base revision: `f17146df4b6c898ac25d181a1cc08d9843b0a710`

## Frozen target

`Stage1Instances.THMM1566.GIPCorollary59Target` freezes Corollary 5.9 of
arXiv:1210.2684v4. It retains the strict parameter ranges, bounded smoothness
index, initial datum, spatial white noise on `T^2`, normalized Schwartz
mollifiers, Lemma 5.8 counterterm, unique limit solution, data-measurable
almost-surely positive stopping time, and convergence in probability in the
stopped `C^alpha` distance.

The pinned libraries do not define the required parabolic Holder-Besov spaces,
white noise on the torus, renormalized PAM equation, or its solution class.
`GIPCorollary59API` types those meanings without including any field that
assumes existence, uniqueness, stopping-time positivity, or convergence. The
legacy `S1_M_182.StatementShape` is therefore not credited as an alternate
encoding.

## Commands and results

Lean commands ran from `Formalizations/Lean` using the existing pinned Lake
environment. No dependency was fetched, updated, or built.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1566/Statement.lean` | 0 | exact target, four mutations, and alpha endpoint boundary elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-1566/check_statement.py` | 0 | expression SHA-256 `70ee4869...e473a`; all four mutations distinguished |
| deletion of the sole import in a temporary copy, then `lake env lean` | 1 | fails immediately on missing filter, real, and measure vocabulary; import is necessary |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Statement.lean lean-toolchain lake-manifest.json` | 0 | `627813...fcd7`, `651c8a...b1d2`, and `321626...2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets consistent |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1566` | 0 | rank 182, planned, legacy artifacts unaccepted, theorem incomplete |
| forbidden-term scan of Lean and validator | 1 | no `sorry`, `axiom`, `admit`, or `placeholder` token found; 1 is ripgrep no-match |
| `git diff --check -- Stage1_Instances/THM-M-1566 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The mutation validator distinguishes the removed white-noise premise, arbitrary
noise/domain weakening, changed mollifier binder scope, and admission of a zero
stopping time. This is statement-only evidence pending master acceptance. It
does not prove Corollary 5.9 and supplies no later-node evidence.
