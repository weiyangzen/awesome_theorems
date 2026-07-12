# Scope map

## Included topic boundary

- A source-specified operator or uniformly controlled family of operators.
- Exact scalar or Banach-valued input and output function spaces over specified measure spaces.
- The source's vector aggregation, such as a finite or countable `ell^q` norm, square function, or
  norm in a named Banach space.
- Exact outer and inner exponents, endpoint exclusions, measurability assumptions, operator
  hypotheses, and the quantitative bound including the dependencies of its constant.

## Ambiguities to resolve at statement freeze

The repository record does not decide among these non-interchangeable targets:

1. **Fefferman-Stein maximal inequality:** an `L^p(ell^q)` bound for a sequence of
   Hardy-Littlewood maximal functions, with a specified exponent range and measure geometry.
2. **Marcinkiewicz-Zygmund inequality:** a scalar bounded linear operator extended to sequences,
   commonly with an `ell^2` aggregation, under specified `L^p` hypotheses.
3. **Square-function or Littlewood-Paley estimate:** a vector of frequency-localized operators is
   controlled by, or controls, a scalar function norm.
4. **Banach-valued operator bound:** one operator acts directly on Bochner-measurable functions;
   validity can depend on geometry of the target space.
5. **Strong versus weak type:** an ordinary `L^p` norm conclusion and a distribution-function or
   weak-`L^p` conclusion are distinct propositions.

The statement phase must inspect an immutable source and freeze the operator definition, ordered
binders, domains, index set, scalar and sequence exponents, all hypotheses, norm conventions,
constant quantification, and conclusion. It must decide endpoint and degenerate cases explicitly.

## Explicit exclusions

- The adjacent Hardy-Littlewood maximal-function theorem or generic scalar `L^p` boundedness as a
  substitute for the vector-valued conclusion.
- Weighted inequalities, Rubio de Francia extrapolation, Fefferman-Stein Hardy-space
  characterizations, or unrelated Banach-valued integration facts as substitutes.
- Assuming the desired vector-valued boundedness in the definition of the operator and projecting
  it back as a tautology.
- A finite-dimensional special case unless the selected source statement is exactly finite.
- Any convenient `Lp`, convolution, or continuous-linear-map theorem absent a checked source
  crosswalk.
- The inventory label `已验证` as evidence of a human proof or machine closure.

No canonical Lean target is frozen at intake because the source record does not identify one.
