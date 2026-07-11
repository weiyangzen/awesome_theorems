# Source-statement crosswalk

| Claim component | Human source anchor | Lean surface | Intake assessment |
|---|---|---|---|
| A probability distribution on `Real` is uniquely determined by its characteristic function | E. Lukacs, *Characteristic Functions*, 2nd ed., Griffin, 1970, Chapter 2 (uniqueness theorem); discovery bibliographic anchor | Canonical measure-level expression recorded in `intake.json` | Standard source family identified, but exact theorem/page, assumptions, edition scan hash, and errata have not been accepted: `H1` |
| Characteristic function is the Fourier-Stieltjes transform `t \mapsto \int exp(i t x) d\mu(x)` | Same monograph, introductory definition and uniqueness chapter | mathlib Fourier/measure integration APIs require audit | Sign convention does not affect uniqueness, but any transport between conventions must be checked |
| Equal characteristic functions of random variables imply equal distributions | P. Billingsley, *Probability and Measure*, 3rd ed., Wiley, 1995, characteristic-functions chapter; discovery anchor | Pushforward measures `Measure.map X P` and `Measure.map Y P` | Candidate corollary; measurability and probability-space hypotheses must be explicit |
| Stronger uniqueness of Fourier transforms of finite measures | Classical Fourier analysis route underlying the probability result | Search pinned mathlib for an exact finite-measure Fourier uniqueness theorem | Candidate dependency only; no declaration name or proof credit is asserted |

## Scope decisions

The Stage0 statement is `特征函数唯一确定分布` (a characteristic function uniquely determines
the distribution). The canonical root therefore uses real Borel probability measures and equality
at every real frequency. It does not silently broaden to arbitrary locally compact groups, nor
weaken to distributions possessing densities or all moments. The random-variable wording is an
alternate encoding because a random variable's distribution is its pushforward law.

The statement phase must choose the actual pinned mathlib representation, elaborate it, record its
normalized expression and environment, and check any bridge from a general Fourier-transform
uniqueness result. It must mutation-test removal of probability hypotheses, restriction of the
frequency domain, added density/moment hypotheses, and the atomic/Dirac cases.

These references are discovery anchors rather than immutable H0 evidence. A later source audit must
pin scans or editions, provide exact theorem/page and assumption-to-binder mapping, check errata,
and obtain independent review. No public Lean theorem was located or credited during intake.
