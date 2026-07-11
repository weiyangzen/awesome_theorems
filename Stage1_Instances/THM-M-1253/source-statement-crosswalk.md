# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` attributes the item to Laurent Schwartz (1950) and gives only
the phrase `分布的卷积运算` ("the convolution operation for distributions"). It supplies no domain,
hypotheses, conclusion, bibliographic citation, or proof. It is discovery metadata, not H0 evidence.

## Candidate primary sources

- Laurent Schwartz, *Theorie des distributions*, first edition, Hermann, Paris (1950-1951), is the
  historical primary monograph candidate. The exact volume, chapter, section, theorem/page,
  wording, edition differences, and errata have not yet been inspected.
- Lars Hormander, *The Analysis of Linear Partial Differential Operators I: Distribution Theory
  and Fourier Analysis*, Springer, is a modern authoritative candidate for a precise convolution
  theorem. Exact edition, theorem/page, assumptions, and errata remain to be inspected.

These citations are candidates only. They convey no H0 or proof credit.

## Crosswalk

| Repository phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| distribution | continuous functional on test functions | concrete test-function space and continuous dual | included; API open |
| convolution operation | iterated pairing after addition/pullback | addition map, translation/pullback, iterated continuous functional | included; encoding open |
| existence | pairing again defines a distribution | well-definedness and continuity theorem | intended; exact conclusion open |
| support condition | compact support of one factor or source-specific alternative | compact support predicate and quantified disjunction | compact-support branch included |
| laws | commutativity, associativity, support, differentiation | separate typed propositions | only if present in selected theorem |

Before H0, an independent reviewer must verify an immutable edition, theorem/page, definitions,
every hypothesis and conclusion, and errata, then approve a row-by-row source-to-Lean crosswalk.

