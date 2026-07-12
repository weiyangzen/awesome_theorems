# Statement validation record

Item: `S56-M-1091-STATEMENT`  
Theorem: `THM-M-1091`  
Base revision: `af3ab2139ee7b58a502efdf255f659aff45a2f9b`  
Validation date: 2026-07-12 (Asia/Shanghai)

## Frozen target

`Stage1Instances.THM_M_1091.ChapmanKolmogorovTarget` fixes the repository's "semigroup
property of transition probabilities" gloss to the homogeneous discrete-time Markov-kernel
form. It quantifies over an arbitrary measurable state space, a Markov endokernel, and natural
step counts `m` and `n`. The equation is `K^(m+n) = K^n composed after K^m`, so `m` steps act
first. Its sole direct import is `Mathlib.Probability.Kernel.Composition.Comp`.

`target_iff_integralTarget` kernel-checks equivalence to the conventional measurable-set form
`K^(m+n)(x,A) = integral K^n(y,A) d(K^m(x))`. The alternate includes the necessary
`MeasurableSet A` premise. The declaration does not claim a general inhomogeneous three-time
family or a continuous-time transition semigroup; those need a different indexed-kernel model
and a source-fidelity bridge.

## Commands and results

All commands ran in this worker clone. Lean used the existing pinned Lake artifacts; no update,
build, clone, fetch, or other `.lake` mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard valid: 15 groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest valid: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1091` | 0 | Rank 533; planned; hard mathlib anchor/wrapper lane; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1091/Statement.lean` | 0 | Exact target, setwise integral encoding, checked iff, four mutations, and both zero-step boundaries elaborated; explicit target printed |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-1091/check_statement.py` | 0 | Expression SHA-256 `c40da0506d47094c906bdcab758ccd3bc8b91beb3f7bcd0465052d77d8115f45`; all four mutations distinguished |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-1091/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | Hashes `64e794...5ded`, `651c8a...b1d2`, and `321626...2d81`, matching `statement.json` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `jq -e . Stage1_Instances/THM-M-1091/statement.json` | 0 | Structured statement record parses |
| `git diff --check -- Stage1_Instances/THM-M-1091 .stage1-worker-selftest.json` | 0 | No whitespace errors |

## Mutation and boundary policy

The validator serializes explicit elaborated expressions and distinguishes removal of the Markov
premise, restriction to finite state spaces, changed binder/addition/composition order, and the
positive-step-only mutation. Kernel-checked lemmas exercise `m=0` and `n=0`; empty state types are
not excluded. The expression comparison establishes that the mutations differ structurally. It
does not purport to decide logical equivalence, and no proof evidence was inspected for credit.

## Status boundary

This is self-tested statement evidence pending master acceptance. It does not prove the
Chapman-Kolmogorov theorem, establish `H0`, audit the pinned mathlib proof body, or advance any
dependent node. The automation-provided untracked `Formalizations/Lean/.lake` link was not created
or modified here, so this remains nonrelease worker evidence.
