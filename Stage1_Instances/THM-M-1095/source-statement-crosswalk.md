# Source-statement crosswalk

| Catalog/source component | Source lead | Lean surface | Intake assessment |
|---|---|---|---|
| `扩散过程` / diffusion processes | Repository research record `Docs/researches/math_theorems.md`, entry headed `扩散过程` | No canonical declaration | The record names a field and says only "the theory of diffusion processes"; it is insufficient to identify a proposition |
| Martingale-problem approach | D. W. Stroock and S. R. S. Varadhan, *Multidimensional Diffusion Processes*, Springer, 1979 | Repo-local discovery artifact `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_242.lean`; no accepted terminal declaration | A credible primary monograph lead, but no theorem/section/page has been selected and this route overlaps distinct target `THM-M-1049` |
| Classical diffusion/SDE treatment | K. Itô and H. P. McKean, Jr., *Diffusion Processes and Their Sample Paths*, Springer, 1965 | General mathlib probability/process substrate only | A primary monograph lead, not evidence for one exact unnamed root; edition, theorem locator, assumptions, and corrections remain unaudited |
| Existing Lean substrate | Pinned local mathlib directories under `Mathlib/Probability/Process`, `Mathlib/Probability/Martingale`, and `Mathlib/Probability/Kernel` | Filtrations, processes, martingales, and kernels | Supporting APIs do not select or close a diffusion theorem |
| Historical `已验证` status | Generated source metadata | None | Explicitly untrusted under rev-5.6 and gives no H/M/R credit |

## Crosswalk verdict

There is no source statement to crosswalk premise by premise. The two books are discovery leads for
different formulations, not interchangeable citations and not immutable evidence receipts. No
`H0` or `H1` claim is made: exact edition, stable locator, verbatim assumptions/conclusion,
correction/errata status, source artifact hash, and independent review are all absent.

The source audit must first decide whether this entry is intended to assert an existence theorem,
a characterization theorem, or a semigroup/generator theorem. It must also show why the choice is
not merely a duplicate of a neighboring named catalog target. Only then can a Lean expression and
source-statement fingerprint be truthfully frozen.
