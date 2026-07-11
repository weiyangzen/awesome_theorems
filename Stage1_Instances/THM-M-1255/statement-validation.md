# Statement validation record

Item: `S56-M-1255-STATEMENT`  
Base revision: `9b754a21a3b3cd70ee15517f1b114d8c32500ff0`

## Frozen target

`Stage1Instances.THM_M_1255.MalgrangeEhrenpreisTarget` quantifies over every finite coordinate
type, existentially packages the polynomial differential action, and asserts a tempered
fundamental solution for every nonzero complex polynomial symbol. The action contract requires
`X i` to act as the checked mathlib distributional derivative in coordinate direction `i`.
Existential packaging is essential: merely quantifying over an arbitrary supplied action would
strengthen the theorem and assume away construction of the polynomial calculus.

The direct imports are the minimal pair found by deletion testing. Removing
`Mathlib.Analysis.Distribution.TemperedDistribution` removes the distribution objects, while
removing `Mathlib.RingTheory.MvPolynomial.Basic` removes the polynomial object and algebra map.

## Commands and results

All commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean` against the
existing pinned `.lake` symlink; no dependency update, fetch, clone, or build was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1255/Statement.lean` | 0 | exact target, object model, packaging iff, and four mutations elaborated; explicit root expression printed |
| `python3 ../../Stage1_Instances/THM-M-1255/check_statement.py` | 0 | expression SHA-256 `0ea54a...d3cf`; all four mutations distinguished; mathlib revision `8a178386...a95` |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-1255/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `06e76a...e94f`, `651c8a...1d2`, and `321626...2d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1255` | 0 | rank 160, planned, L0/rework-required, theorem incomplete |
| forbidden-term scan of `Statement.lean` and `check_statement.py` | 1 | no `sorry`, `admit`, or `axiom` occurrence; 1 is ripgrep's no-match exit |

## Scope boundary

The mutation validator distinguishes removal of `P != 0`, real rather than complex polynomial
coefficients, universal rather than existential action packaging, and restriction to dimension one.
Zero-dimensional spaces and nonzero constant symbols remain within the target.

This is statement-only evidence pending master acceptance. The classical theorem is often phrased
for general distributions; proving or sourcing equivalence with the frozen tempered formulation is
still an explicit human-source and proof obligation. No theorem completion is claimed.
