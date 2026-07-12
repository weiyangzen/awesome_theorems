# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `里斯-费耶尔定理`, attributes it to
Marcel Riesz and Lipot Fejer, gives 1923, and states only `傅里叶级数的收敛性` ("convergence of
Fourier series"). Stage0 repeats only the title. The rev-5.6 manifest preserves `已验证` solely as
`source_status_untrusted`. No theorem, definition, hypotheses, proof citation, edition, page,
errata record, or formal artifact is supplied.

These fields locate a harmonic-analysis topic but do not establish an exact proposition. In
particular, neither the paired name nor the gloss resolves the conflict between a Fourier
convergence theorem and Fejer-Riesz factorization. Intake found no repository-local source capable
of resolving that conflict.

## Candidate source work

The source audit must first locate a primary or authoritative use of the exact paired name and
inspect an immutable edition. It must record the theorem/section/page, terminology, assumptions,
proof boundary, date and attribution, corrections, and an independent review. Bibliographic search
is deliberately left to the later anchor/source audit; no uninspected citation is promoted to H0.

## Crosswalk

| Repository component | Possible mathematical meaning | Required Lean component | Intake status |
|---|---|---|---|
| "Fourier series" | coefficients and partial sums on a specified periodic domain | additive circle, Fourier coefficients, finite sums | APIs probed; conventions open |
| "convergence" | ordinary, Cesaro, uniform, pointwise, a.e., or `L^p` convergence | an exact filter/topology/norm statement | absent from source record |
| Riesz-Fejer | a convergence or summability theorem | source-specific hypotheses and conclusion | unresolved |
| Fejer-Riesz | nonnegative trigonometric polynomial factorization | Laurent/trigonometric polynomial and squared-modulus factor | competing theorem family only |
| 1923 / named authors | historical provenance | no Lean proposition or proof credit | unverified metadata |
| `已验证` | untrusted inventory label | no formal counterpart | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded probe
imports Fourier analysis on the additive circle, the general Cesaro convergence lemma, and Laurent
polynomials. It checks representative definitions and theorems only. Pinned mathlib also contains
Fourier density, `L^2` convergence, and polynomial Parseval results, but none may be credited before
the source-faithful proposition is selected and exact types are audited.

The next phase is blocked on an independently reviewed exact source. Only then may it freeze ordered
binders, hypotheses, conclusion, alternate encodings, mutations, and an elaborated expression hash.
