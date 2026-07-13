# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1780-1785` names `柯尔莫哥洛夫定理`, attributes it to Andrey
Kolmogorov, gives 1925, and glosses the statement as `共轭函数的弱型估计` ("weak-type estimate for
conjugate functions"). `Docs/Stage0_Blueprint.md:6842-6863` repeats the gloss while explicitly
leaving exact definitions and hypotheses open. Git blame traces the six catalog fields to corpus
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted`. It supplies no proposition,
source locator, human proof review, formal declaration, or proof credit.

## Primary source inspected

A. Kolmogoroff, "Sur les fonctions harmoniques conjuguees et les series de Fourier,"
*Fundamenta Mathematicae* **7** (1925), 24-29, DOI `10.4064/fm-7-1-24-29`. The publisher scan
downloaded on 2026-07-13 has SHA-256
`b0567754c1c50a5549f664effcc2e29163b4409de1e4fcc228895e19e803a73b` and six pages. The dynamic
publisher landing page is retained only as a DOI-resolved locator, not as hashed evidence.

Printed page 24 fixes the context: a summable `f(theta)` on an angular period, its Poisson integral
in the disk, and the almost-everywhere nontangential boundary value `g(theta)` of the harmonic
conjugate, represented by a circular principal-value integral with kernel `-1/tan(alpha/2)` and
factor `1/(2*pi)`. Printed page 25, Theorem I, then states that if
`E = {theta | |g(theta)| > R}`, then

```text
Mes(E) * R < C * integral_{-pi}^{pi} |f(theta)| d theta,
```

where `C` is an absolute constant. This source pinpoint matches the repository gloss. It is intake
source evidence, not `H0`: the scan has not been independently reviewed, its cited Privaloff
boundary theorem and full proof-premise map have not been audited, and no errata record is yet
accepted.

## Crosswalk

| Source component | Mathematical meaning | Required Lean component | Intake state |
|---|---|---|---|
| `f(theta)` summable | periodic `L^1` input on one angular period | `Integrable f mu` or `Lp _ 1 mu`, plus representative bridge | source located; encoding open |
| Poisson extension and conjugate harmonic function | selects the boundary conjugate, including additive normalization | construction plus a.e. nontangential boundary theorem, or checked equivalent operator | absent from target |
| principal-value formula on p. 24 | circular Hilbert/conjugate transform with source sign and factor | exact principal-value definition and equivalence witness | absent from pinned probe |
| `E = {|g| > R}` | strict superlevel set; source calls `R` arbitrary without an explicit sign condition | measurable set, measure expression, and reviewed threshold domain | carrier API available; exact target open |
| `Mes(E) * R` | weak `(1,1)` distribution-function quantity | angular measure or checked normalized-Haar scaling | normalization bridge open |
| absolute `C` | one constant independent of `f` and `R` | existential constant outside both binders | binder order to freeze |
| integral of `|f|` | source `L^1` size | integral norm or checked `L^1` norm identity | API available |
| strict `<` | printed conclusion | exact strict form or reviewed implication to `<=` | direction not yet selected |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks `AddCircle`, probability-normalized `AddCircle.haarAddCircle`, integrability and `Lp`,
`eLpNorm`, Fourier coefficients, real-valued measure, and generic Chebyshev-Markov inequalities.
A bounded repo-local and pinned-mathlib search for Hilbert/conjugate-transform and weak-type names
found no terminal theorem for this target. Generic Markov inequalities do not construct the
conjugate and cannot establish its endpoint estimate. This is intake discovery only, not the later
immutable anchor audit and not a global absence claim.

The statement phase must elaborate the source-selected proposition, record its expression and
environment fingerprints, check any measure/operator transports, and perform all four mutation
classes before proof evidence is inspected.
