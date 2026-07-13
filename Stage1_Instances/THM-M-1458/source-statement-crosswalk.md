# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10644-10649` supplies exactly the title
`快速傅里叶变换`, attribution to James Cooley and John Tukey, the year 1965, the gloss
`DFT的快速算法`, importance `high`, and status `已验证`. All six uncited lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, DFT formula,
algorithm, permitted length, ordered binder, premise, correctness theorem, complexity model,
proof, erratum, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:39649-39674` repeats the metadata while explicitly leaving exact
definitions and premises, proof route, dependencies, alternate statements, axiom policy,
machine-checked status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

## Bibliographic source lead

Crossref and OpenAlex DOI records observed on 2026-07-13 identify James W. Cooley and John W.
Tukey, *An Algorithm for the Machine Calculation of Complex Fourier Series*, *Mathematics of
Computation* volume 19, issue 90 (1965), pages 297-301, DOI
`10.1090/S0025-5718-1965-0178586-1`. The Crossref response was used only to confirm bibliographic
identity. The publisher classifies the article as closed access; no full text was added here.

This locator strongly explains the catalog metadata, but a DOI record contains no admitted
theorem text or proof. The catalog does not cite it, and the worker has not preserved a lawful
immutable edition, selected an exact passage, mapped assumptions and proof nodes, audited
corrections or historical scope, or obtained independent review. It supplies no `H0` credit.

## Literal crosswalk

| Repository component | Material interpretations | Required Lean component | Intake result |
|---|---|---|---|
| `DFT` | positive/negative exponential, normalized/unnormalized, forward/inverse, `Fin N`/`ZMod N` | exact carrier, index type, root/sign/normalization, dense reference definition | unspecified |
| `算法` | algebraic factorization, recursive pure function, array program, or machine implementation | executable or relational algorithm plus termination and semantics | unspecified |
| `快速` | fewer operations than direct DFT, exact recurrence, `O(N log N)`, or measured runtime | explicit cost function, operation set, input-size and asymptotic filter | unspecified |
| Cooley/Tukey 1965 | composite-factor FFT family and historical article | admitted source passage and node crosswalk | bibliographic lead only |
| `已验证` | untrusted screening label | accepted source and kernel receipts | no credit |

These choices are proposition-changing. An algebraic equality can be correct without an executable
program or cost theorem; a correct radix-2 program does not apply to every positive length; and a
finite benchmark cannot establish asymptotic complexity.

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.Fourier.ZMod` defines `ZMod.dft : (ZMod N -> E) ≃ₗ[ℂ] (ZMod N -> E)` through a
dense sum. `ZMod.dft_apply` and `ZMod.dft_def` expose the formula, while `ZMod.dft_dft` proves
discrete inversion. `Mathlib.Analysis.Fourier.FiniteAbelian.PontryaginDuality` supplies the
character equivalence `AddChar.zmodAddEquiv` and the finite complex character basis
`AddChar.complexBasis`.

These declarations provide a plausible mathematical reference semantics. They do not state a
Cooley-Tukey factorization, implement an FFT, prove equality between an algorithm and `ZMod.dft`,
or define an operation count. A bounded case-insensitive search found no FFT-named source file or
declaration in pinned mathlib or tracked repo-local Lean. That observation is discovery only, not
the downstream exhaustive anchor audit.

## Source gate and retry condition

An accountable correction must preserve a lawful immutable edition, select one exact FFT
correctness and/or complexity theorem, map every definition, binder, factorization premise,
permutation, conclusion, cost clause, proof node, and boundary case, audit corrections and
historical attribution, and receive independent review. Only then may the statement phase freeze
and mutation-test the exact Lean expression. Until that correction, the canonical mathematical
and Lean targets remain null and the catalog-target source classification is `H5`.
