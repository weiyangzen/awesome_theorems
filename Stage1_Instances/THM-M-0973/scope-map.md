# Scope map

## Preserved catalog scope

The repository fixes `THM-M-0973`, the title `Kim-Vu不等式`, year 2000, and the gloss
`多项式集中不等式`. It records `Jeong Han Han/Van Vu`, while publisher metadata for the likely
paper records Jeong Han Kim and Van H. Vu; this dossier preserves the former as catalog text and
records the latter only as a bibliographic correction candidate. Importance "high" and status
`已验证` are untrusted metadata.

The likely 2000 bibliographic lead is *Concentration of Multivariate Polynomials and Its
Applications*. Its accessible abstract identifies independent zero-one random variables and a
multivariable polynomial with positive coefficients. This identifies a result family, but it does
not select an exact theorem, constants, or tail form.

## Candidate family, not credited

The familiar Kim-Vu family controls the deviation of a positive-coefficient polynomial of
independent Bernoulli variables using expectations of suitable partial derivatives. Different
sources and later reformulations package those controls, auxiliary parameters, constants, and tail
probabilities differently. This description is a search and resolution lead only. It is not the
canonical statement, an elaborated Lean expression, or proof evidence.

## Proposition-changing decisions

The statement phase must freeze all of the following from an admitted immutable source:

1. The exact source result: theorem number/page, original main theorem versus a corollary or later
   reformulation, and whether the target is one-sided, two-sided, or a finite conjunction.
2. The finite or countable variable index, underlying probability space and measure, zero-one or
   general bounded independent variables, and common versus coordinate-dependent Bernoulli laws.
3. Whether the input is a formal polynomial, a multilinear polynomial/function on the Boolean
   cube, a hypergraph counting polynomial, or an equivalent representation with a checked map.
4. The coefficient domain, nonnegativity versus strict positivity, finite support, total degree,
   maximum monomial degree, and treatment of repeated powers before zero-one evaluation.
5. The exact derivative family: subsets, ordered tuples, iterated partial derivatives, or another
   source-defined operator, including the order-zero derivative and empty set.
6. The controlling expectations and extrema: which derivatives are evaluated, whether maxima range
   over derivative order or index sets, and how zero or undefined maxima are normalized.
7. Every numerical constant, exponential/logarithmic factor, auxiliary parameter and admissible
   range, integrality or positivity restriction, and asymptotic versus literal inequality.
8. The exact event and conclusion: deviation from expectation, upper or lower tail, absolute value,
   threshold scaling, strict versus weak inequality, and probability codomain/coercions.
9. Ordered binders, universes, measurability and integrability assumptions, classical principles,
   representation transports, and all boundary or degenerate cases.
10. Proof locator, incorporated definitions and preceding lemmas, correction and errata status,
    translation fidelity, and independent source review.

## Boundary and degenerate cases

No case is excluded at intake. Source review must decide an empty variable family; zero and constant
polynomials; degree zero; all-zero coefficients; zero expectation; vanishing first or higher
derivative parameters; deterministic Bernoulli coordinates; empty maxima; auxiliary parameter at
its endpoints; and thresholds equal to zero. The encoding must not gain accidental strength or
vacuity from conventions for powers, maxima, logarithms, or division by zero.

## Neighbor and substitution exclusions

- `THM-M-0972` Janson inequality, `THM-M-0974` Talagrand concentration, and later Azuma-Hoeffding,
  McDiarmid, Chernoff, Hoeffding, Bernstein, or Bennett targets are distinct concentration results.
  A generic tail inequality or special consequence cannot replace the Kim-Vu root.
- A theorem about algebraic multivariate polynomials without random evaluation does not establish
  concentration; a probability theorem without the source derivative controls does not establish
  the Kim-Vu inequality.
- One hypergraph-counting application, a fixed degree, identical Bernoulli parameter, multilinear
  special case, asymptotic big-O form, or numerical experiment cannot be substituted silently.
- A structure or hypothesis storing the desired tail bound, derivative estimates, or concentration
  conclusion supplies no proof.
- The catalog's `已验证` label, a DOI, an abstract, an API probe, or a bounded no-match search gives
  no H0 or M proof credit.

## Downstream boundary

No canonical human or Lean proposition is frozen at intake. The statement phase must first admit
and independently review the exact primary statement and definitions, resolve the catalog author
error and variant selection, and freeze every choice above. Only then may it select minimal imports,
elaborate and fingerprint one expression, add checked transports, and run the required statement
mutations. Anchor audit, obligation architecture, proof, validation, and release remain separate
open tasks.
