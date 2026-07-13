# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6700-6705` supplies exactly:

- title: `欧拉五边形数定理`;
- attribution: Leonhard Euler;
- year: 1750;
- gloss: `整数分拆的生成函数恒等式`;
- importance: high;
- formalization label: `已验证`.

Git blame places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no displayed equation,
edition, theorem/page, definitions, binders, assumptions, conclusion, proof, correction history,
reviewer, or formal declaration. `Docs/Stage0_Blueprint.md:24985-25010` repeats the gloss while
explicitly leaving precise definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Mathematical component to freeze | Prospective Lean component | Intake result |
|---|---|---|---|
| `欧拉五边形数定理` | a source-identified generalized-pentagonal identity | exact equality, convergence claim, or recurrence | recognizable family; root form open |
| `整数分拆` | partitions of natural numbers and their count `p(n)` | `Nat.Partition n` and `Fintype.card` after source transport | adjacent pinned representation only |
| `生成函数` | formal series or analytic q-series and its coefficient domain | `PowerSeries`, `HasProd`, `HasSum`, or source-selected analytic objects | semantics and assumptions open |
| `恒等式` | product-series, reciprocal-partition, or coefficient identity | one exact proposition plus checked transports | materially ambiguous |
| Euler / 1750 | historical provenance | immutable edition and pinpoint source ledger | secondary history identifies 1750 as first-proof date; independent review open |
| `已验证` | untrusted inventory metadata | no proposition or proof term | explicitly rejected as H or M evidence |

## Primary-source lead

Euler's *Demonstratio theorematis circa ordinem in summis divisorum observatum*, *Novi
Commentarii Academiae scientiarum Imperialis Petropolitanae* 5 (1760), pages 75-83, Enestrom E244,
is a matching primary work. Jordan Bell's immutable English translation, arXiv
`math/0507201v2`, is an 88,041-byte, eight-page PDF with SHA-256
`0900718052a4085b7b9b2067fd2710b323223a90f4b8683a0bbe7795f177770e`.

Translation pages 1-2 display the product and signed expansion. Proposition 3 on translation pages
3-5 states and proves the product expansion, then identifies the generalized-pentagonal exponent
pattern. This is strong primary-text evidence, not `H0`: the Latin-to-English translation, exact
historical semantics of infinite expressions, complete proof-node map, correction history, source
admission, and independent review remain open.

Jordan Bell, *Euler and the pentagonal number theorem*, arXiv `math/0510054v2`, is a 220,767-byte
historical study with SHA-256
`28623ab30a2a9b025d3c5946f1426366195578b715bffdc53e4874f316f3bcf4`. It reports the formula in
Euler's 1748 *Introductio*, a proof in Euler's letter to Goldbach of 9 June 1750, and the fuller E244
publication in 1760. This makes the catalog date plausible as the first-proof date, but the secondary
history has not been independently reviewed and is not itself primary proof evidence.

## Authoritative modern statement lead

NIST DLMF section 27.14(ii), equations 27.14.2-27.14.5, separates the relevant claims. Equation E2
defines `f(x)` as the product for real `|x| < 1`; E3 gives the reciprocal partition generating
function with `p(0) = 1`; E4 explicitly names and states Euler's paired-index pentagonal number
theorem; and E5 defines its two generalized-pentagonal exponents. Stable root locators are
`https://dlmf.nist.gov/27.14.E4` and `https://dlmf.nist.gov/27.14.E5`.

The observed TeX SHA-256 values for E2 through E5 are respectively
`678ece35634aba3460abd71fab710f833ba619fc42986733827e0e1759738331`,
`5ccf9eb943d8fa75eb0c3ba5bd74acd66063ee626c8d0a440280e3854664157b`,
`a5f9de98289d8d6872f4b17d1726972d5ba5ed673117c0d586a6321629859191`, and
`2e184a4385ee799a583614fa11872cbd6b5d8ff51428ee706f7f7d0e9b2294f5`.
DLMF is an authoritative statement lead rather than a complete proof source. Its analytic domain,
errata, relationship to E244, and transport to any formal-power-series root remain to be reviewed.

## Candidate mathematical crosswalk

The familiar formulas below are resolution candidates only and are intentionally not canonical:

```text
product_(m >= 1) (1 - X^m)
  = sum_(k in Z) (-1)^k X^(k(3k-1)/2)

  = 1 + sum_(k >= 1) (-1)^k
      (X^(k(3k-1)/2) + X^(k(3k+1)/2)).
```

A partition-generating-function form identifies the reciprocal product with
`sum_(n >= 0) p(n) X^n`; coefficient extraction then yields a signed recurrence for `p(n)`. A
reviewed source must choose which equality is the root and which forms are consequences or
alternates. In Lean, integer exponent arithmetic, natural reindexing, infinite products, inversion,
coefficient extraction, and formal-versus-analytic transport all require checked witnesses.

## Formal-source crosswalk

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` provides adjacent
partition and power-series interfaces:

| Candidate component | Pinned declaration | Relationship | Credit boundary |
|---|---|---|---|
| partitions of `n` | `Nat.Partition n` | finite multiset representation of positive parts summing to `n` | representation candidate only |
| weighted generating series | `Nat.Partition.genFun` | coefficient is a weighted sum over partitions | generic definition, not ordinary `p(n)` theorem |
| coefficient equation | `Nat.Partition.coeff_genFun` | unfolds the generic coefficient | interface only |
| generic product formula | `Nat.Partition.hasProd_genFun` | product of per-part weighted series converges to `genFun` | adjacent bridge, no pentagonal series |
| product equality | `Nat.Partition.genFun_eq_tprod` | equality to the same generic infinite product | adjacent bridge, no pentagonal expansion |
| odd versus distinct parts | `Nat.Partition.card_odds_eq_card_distincts` | Glaisher/Euler partition theorem | different theorem, explicitly excluded |

The `GenFun.lean` module documentation explicitly marks the weight-one specialization to the
ordinary partition function TODO. A bounded case-insensitive search over pinned mathlib and
repo-local Lean found no `pentagonal` declaration. `IntakeProbe.lean` merely confirms that the
listed generic APIs elaborate in the pinned environment; it creates no declaration and supplies no
statement or proof credit.

## H0 and downstream gates

Before `H0`, reviewers must admit a versioned primary proof source, locate the exact formula and all
incorporated definitions, map every premise and material proof transition, resolve the catalog date,
audit corrections and errata, and independently approve the crosswalk. Before statement acceptance,
Lean work must freeze exact binders and minimal imports, preserve expression and environment
fingerprints, compile checked alternate-form transports, and pass all semantic mutations. Formal
candidate provenance, obligation decomposition, proof, trust, and release checks remain downstream.
