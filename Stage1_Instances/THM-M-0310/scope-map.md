# Scope map

## Provisional included claim

- A measure space `(X, μ)` and scalar field selected by the exact source.
- Exponents `p` and `q` satisfying the source's conjugacy convention.
- The canonical map sending `g` in `L^q(μ)` to the continuous linear functional
  `f ↦ ∫ x, f x * g x ∂μ`, with the appropriate real or complex conjugation convention.
- Isometry of that map, and surjectivity onto the continuous dual of `L^p(μ)`, under every
  measure-theoretic hypothesis actually needed by the selected theorem.

## Decisions required at statement freeze

The statement phase must select and inspect one exact source theorem and freeze: real versus
complex scalars; the concrete `L^p` model and equality-a.e. quotient; whether exponents are real,
extended nonnegative real, or another encoding; the range `1 < p < infinity` versus endpoints;
the definition of conjugacy; completeness, sigma-finiteness, semifiniteness, or localizability
assumptions on the measure; the bilinear or sesquilinear pairing; which argument is conjugated;
the norm equality; and the direction and uniqueness of the representing element. It must handle
the zero measure, null spaces, infinite measure, `p = 1`, and `p = infinity` explicitly.

## Explicit exclusions

- The product-integral Holder inequality alone; that is separately represented by `THM-M-0279`.
- The finite-sum Holder inequality or duality of finite-dimensional `ell^p` spaces.
- Only the bounded embedding `L^q -> (L^p)'` without the source theorem's surjectivity conclusion.
- Hilbert-space Riesz representation restricted to `p = 2`.
- A structure that contains the desired isomorphism or representation theorem as an assumed field.
- The metadata label `已验证` as human-source or kernel evidence.

No Lean target is frozen during intake. A later encoding must use concrete measure-theoretic
`L^p`, continuous-dual, integration, and norm interfaces and may not hide the conclusion in data.
