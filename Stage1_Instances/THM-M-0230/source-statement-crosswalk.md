# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1661-1666` supplies exactly the title
`魏尔斯特拉斯分解定理`, attribution to Karl Weierstrass, the year 1876, the gloss
`整函数的无穷乘积表示` ("infinite-product representation of entire functions"), importance
"high," and status `已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, theorem
locator, formula, definitions, ordered binders, hypotheses, proof boundary, correction history,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:6383-6408` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 target manifest preserves `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

## Inspected source leads

Crossref metadata observed on 2026-07-13 identifies Karl Weierstrass,
*Zur Theorie der eindeutigen analytischen Functionen*, in *Functionenlehre* (1900), pages 1-52,
DOI `10.1007/978-3-662-43012-5_1`. Separate metadata identifies an erratum on page 261, DOI
`10.1007/978-3-662-43012-5_8`. The collected-work date does not by itself authenticate the
catalog's 1876 date. Neither primary text nor exact theorem/page, incorporated definitions,
assumptions, proof, relation of the erratum, or edition history was inspected. These are mutable
bibliographic leads, not `E4` or `H0` evidence.

NIST DLMF section 1.10(ix), "Infinite Products," was also observed on 2026-07-13. Its paragraph
labeled "Weierstrass Product," equation 1.10.22, gives a concrete special case: under a summability
condition on nonzero `z_n`, a product with factors `(1 - z/z_n) * exp(z/z_n)` is entire with zeros
`z_n`. The notes point to Titchmarsh (1962), pages 13-19 and 246-250. This supports terminology and
a special construction only. It neither states the catalog's broad given-entire-function
factorization nor resolves arbitrary primary factors, multiplicities, the zero at the origin, the
residual `exp(g)`, or degenerate cases. The live web snapshot is `E5`, not an immutable accepted
source or an independent review.

## Clause crosswalk

| Catalog component | Source decision required | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "entire function" | given nonzero `f : Complex -> Complex`, or constructed function for prescribed zeros | `AnalyticOnNhd Complex f Set.univ`, or a source-checked equivalent | input role, predicate, and zero-function boundary open |
| zeros | sequence or locally finite divisor, multiplicity, enumeration, no finite accumulation | `analyticOrderAt`, a locally finite support object, and exact divisor equality | adjacent order/isolated-zero APIs probed; representation open |
| zero at origin | finite order `m` separated from nonzero zeros | `analyticOrderAt f 0 = m` or source-equivalent data | separation and identically-zero behavior open |
| primary factors | `E_p(w)` and the `p = 0` convention | a future definition using `Complex.exp`, powers, and finite sums | no Weierstrass primary-factor definition credited |
| infinite product | genus sequence and locally uniform convergence on `Complex` | `HasProdLocallyUniformlyOn`, `MultipliableLocallyUniformlyOn`, `tprod` | generic pinned infrastructure only |
| representation | pointwise equality including `z^m`, `exp(g)`, and the canonical product | exact universally quantified equality plus analytic hypotheses on `g` | formula and binder order not selected |
| `已验证` | inspectable human proof and kernel receipt would be required | no proposition or proof object | explicitly rejected as evidence |

## Formal-candidate boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- `analyticOrderAt` and `AnalyticAt.eventually_eq_zero_or_eventually_ne_zero` provide local zero
  order and isolated-zero substrate.
- `Summable.hasProdLocallyUniformlyOn_nat_one_add` and
  `TendstoLocallyUniformlyOn.differentiableOn` provide convergence and holomorphic-limit substrate.
- `MeromorphicOn.extract_zeros_poles` factors a meromorphic function only when its divisor support
  is finite, by a finite product and a zero-free analytic factor.
- `Complex.canonicalFactor` is explicitly a disk/Blaschke factor and is not the Weierstrass primary
  factor `E_p` despite its name.
- `Complex.tendsto_euler_sin_prod` is a checked special-case product for sine.

The intake probe elaborates these declarations and reports only the standard `propext`,
`Classical.choice`, and `Quot.sound` axioms for the printed library theorems. It states no target.
A bounded exact-topic search found no terminal universal Weierstrass factorization declaration;
external discovery and terminal proof-body provenance remain downstream anchor-audit work.

## Source gate

Before statement acceptance or `H0`, accountable reviewers must preserve an immutable primary or
authoritative edition, select one exact root, transcribe all incorporated definitions, ordered
binders, hypotheses, conclusions, and boundary cases, map every material premise and proof
transition, inspect corrections and errata, reconcile the construction/factorization variants, and
approve the source-to-Lean crosswalk. Until then the canonical statement and expression remain
null.
