# THM-M-1291 proof execution

Item: `S56-M-1291-PROOF`  
Date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `b1720c87b4674563b995fad5e6dd9828348b7230`

## Verdict

`blocked`. `Proof.lean` adds a genuine placeholder-free proof body for the
frozen `M1291-L-POINTWISE` leaf. From pointwise convergence of `fseq n x`, it
proves convergence of
`|fseq n x|^p - |fseq n x - f x|^p` to `|f x|^p` for every real `p > 0`.
The proof uses continuity of subtraction, norm, and nonnegative real powers.

This does not complete the assigned proof phase. The pinned mathlib tree has
no Brezis-Lieb declaration, and the required truncation, uniform-tail, and
corrected-remainder integral bridge obligations remain open. In particular,
pointwise convergence cannot be promoted by dominated convergence: the frozen
hypothesis supplies only a uniform bound on the integrals, not a common
integrable dominating function. No root declaration or theorem completion is
claimed. `.stage1-worker-selftest.json` is deliberately absent because the
assigned proof deliverable is incomplete.

## Narrow validation evidence

All commands ran in this worker clone and reused the existing pinned Lake
artifacts. No update, build, dependency clone/fetch, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1291` | 0 | rank 462, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-1291/check_obligation_tree.py` | 0 | 17 obligations and 38 typed edges passed; frozen root open `M3` |
| temporary copied `Statement.lean` compiled with `lake env lean -R <tmp> -o <tmp>/Statement.olean`, then `LEAN_PATH=<tmp>:$(lake env printenv LEAN_PATH) lake env lean ../../Stage1_Instances/THM-M-1291/Proof.lean` from `Formalizations/Lean` | 0 | proof elaborated; axiom report exactly `propext`, `Classical.choice`, `Quot.sound` |
| forbidden-token scan of `Proof.lean` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, or `unsafe` |
| `sha256sum Stage1_Instances/THM-M-1291/{Statement.lean,Proof.lean}` | 0 | statement `ef19e70e...dd92f`; proof `95a67ff8...c425d` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git diff --check -- Stage1_Instances/THM-M-1291` | 0 | no whitespace errors |

## Reopen condition

Resume by implementing the frozen truncation and uniform-tail estimates and
their integral composition, or by locating an immutable exact Lean 4
Brezis-Lieb proof whose terminal body and transitive trust closure can be
pinned and checked locally. A dominated-convergence theorem without a proof of
the missing common domination condition does not close this target.
