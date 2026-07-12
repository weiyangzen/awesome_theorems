# Statement validation record

Item: `S56-M-1080-STATEMENT`  
Base revision: `ec625affaba626d33138848b34fb76da0bf247cf`

## Frozen target

`Stage1Instances.THM_M_1080.Statement` freezes the one-sided upper-tail Azuma inequality selected
at intake. It quantifies over a real discrete-time martingale on a probability space, a varying
family `c : Nat -> NNReal`, and an inclusive horizon `0,...,n`. The a.e. hypothesis covers exactly
the `n` increments `X (k+1) - X k` for `k < n`; the denominator is the corresponding sum of
`c (k+1)^2`. The conclusion bounds the real-valued probability of `t <= X n - X 0` for `t >= 0`.

The declaration retains `n = 0`, `t = 0`, and zero total squared bound. Thus it does not silently
add a positive-variance hypothesis; real division has Lean's totalized zero-denominator semantics.
The lower-tail and two-sided forms remain downstream transports rather than substitutes for this
root. `statement_iff_expandedSourceShape` kernel-checks the direct expansion.

The sole direct import is `Mathlib.Probability.Martingale.Basic`; it provides the
martingale/filtration and measure surface and transitively the real exponential used by the
expression. Removing this import makes the target fail to elaborate.

## Commands and results

All Lean commands used the existing pinned Lake environment. No dependency state was fetched,
updated, built, or otherwise changed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1080/Statement.lean` | 0 | target, checked expansion, and four structural mutations elaborated and printed |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-1080/check_statement.py` | 0 | expression SHA-256 `af69d1d8...d0d350`; expansion checked; all mutations distinguished |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && git -C .lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 -m json.tool Stage1_Instances/THM-M-1080/statement.json` | 0 | structured statement artifact valid |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1080` | 0 | rank 522; planned; L0/rework-required; theorem incomplete |
| forbidden-term scan over executable statement/validator content | 1 | expected no-match exit; no `sorry`, `admit`, `axiom`, or `sorryAx` |
| `git diff --check -- Stage1_Instances/THM-M-1080 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This is self-tested statement evidence pending master acceptance. It proves only that the selected
exact target and its boundary mutations elaborate in the pinned environment. Primary-source
pinpointing, anchor/provenance audit, the obligation graph, proof, hermetic replay, and independent
review remain open. No `H0`, `M0`, audit completion, or theorem completion is claimed.
