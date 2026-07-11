# Scope map

## Included claim family

- Functions on Euclidean space (or a source-authorized Euclidean domain) with weak derivatives.
- Integers `0 <= j < m` and a bound of the schematic form
  `||D^j u||_Lp <= C * ||D^m u||_Lr^a * ||u||_Lq^(1-a)`.
- The scaling relation between `p`, `q`, `r`, `a`, `j`, `m`, and ambient dimension `n`.
- All endpoint exclusions, additive lower-order terms, density/completion conditions, and constant
  dependencies stated by the selected source theorem.

## Decisions deferred to statement

The statement phase must select one exact theorem rather than combine variants. It must freeze
whether derivatives are individual multi-index derivatives or a Sobolev seminorm, whether the
domain is `R^n`, a bounded extension domain, or another region, the scalar field, measurability and
weak differentiability hypotheses, finite/infinite exponents, the admissible interval for `a`, and
exceptional endpoints. Binder order, universes, norm conventions, and degenerate cases (`j = 0`,
zero function, `q = infinity`, `r = infinity`) must then be recorded explicitly.

## Explicit exclusions

- A one-dimensional elementary interpolation inequality substituted for the general result.
- A Sobolev embedding, Nash inequality, or logarithmic Gagliardo-Nirenberg inequality presented as
  though it were the scoped classical theorem.
- A bounded-domain result with an omitted additive term or extension-domain hypothesis.
- A definition or structure that assumes the desired estimate as a field.
- Any convenient mathlib inequality whose exponents do not exactly transport to the frozen source.
