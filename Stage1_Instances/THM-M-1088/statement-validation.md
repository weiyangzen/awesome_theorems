# Statement validation record

Item: `S56-M-1088-STATEMENT`  
Base revision: `2c9a031dc32c54d7f41663314d181605e7bf2398`

## Frozen target

`Stage1Instances.THM_M_1088.BorellTISTarget` selects the standard one-sided upper-tail form for a
nonempty countable real Gaussian process. Countability is the formal separability convention. The
target quantifies over an explicit measurable real representative `S` of the pointwise supremum,
requires pointwise boundedness and `Integrable S P`, and requires centered coordinates.

The variance parameter `σ2` is strictly positive and equals
`sSup (range (fun t => variance (X t) P))`. Thus the exponent is exactly
`-u^2 / (2*σ2)`, while the degenerate zero-variance extension is deliberately outside this target.
The event uses the strict form `u < S - E S` for every `u >= 0`. Empty index types are excluded.

The sole direct import is
`Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Def`.
`target_iff_expandedSourceShape` kernel-checks the direct expansion. Four separately elaborated
mutations expose prohibited removal of Gaussian/centering/variance hypotheses, restriction to a
finite domain, changed `u` binder boundary, and admission of zero variance.

## Commands and results

Commands ran against the existing pinned `.lake` environment; dependency state was not changed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1088/Statement.lean` | 0 | target, direct expansion, checked equivalence, and four boundary mutations elaborated; explicit target printed |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Stage1_Instances/THM-M-1088/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | statement `907c7a...e1c7` before final documentation-only edits; toolchain `651c8a...b1d2`; manifest `321626...2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1088` | 0 | rank 530; L0/rework-required; planned; theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1088 .stage1-worker-selftest.json` | 0 | no output |

## Status boundary

This is self-tested statement evidence pending master acceptance. It selects a precise canonical
formalization but does not upgrade the discovery citations to `H0`: exact primary-source theorem
and page inspection remains anchor-audit work. No Borell-TIS proof, `M0`, audit completion, or
theorem completion is claimed.
