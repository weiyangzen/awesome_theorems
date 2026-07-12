# Scope map

## Included claim

- Two arbitrary sets, encoded extensionally by their element types `alpha : Type u` and
  `beta : Type v`.
- A function `f : alpha -> beta` and a function `g : beta -> alpha`.
- Separate injectivity hypotheses for `f` and `g`.
- Existence of a bijective function `h : alpha -> beta`, hence equipotence.
- Different universes, infinite carriers, finite carriers, and empty carriers.

The theorem is an existence statement. It does not require the resulting bijection to agree with
either injection pointwise, and it does not claim a computable choice of bijection from the input.

## Boundaries for statement freeze

The canonical statement should use raw functions plus `Function.Injective` and conclude existence
of a raw function satisfying `Function.Bijective`, directly reflecting the repository sentence.
The bundled encoding

`(alpha ↪ beta) -> (beta ↪ alpha) -> Nonempty (alpha ≃ beta)`

is expected to be equivalent, but must receive a checked transport rather than silently replacing
the root. A cardinal-equality formulation likewise belongs only as an alternate encoding.

The statement phase must retain universe polymorphism and test mutations that remove either
injectivity hypothesis, replace bijectivity by injectivity or surjectivity alone, add nonemptiness,
or collapse the universes. These mutations must not be credited as the target.

## Explicit exclusions

- Cantor's powerset theorem and any claim about strict cardinal growth.
- The axiom of choice, well-ordering theorem, trichotomy of cardinals, or cardinal arithmetic.
- The stronger relation-preserving `schroeder_bernstein_of_rel` result as the root theorem.
- Bernstein approximation, Bernstein inequalities, or results sharing only a person's name.
- An equivalence supplied as input, or a tautological restatement whose conclusion is assumed.
- The metadata label `已验证` as human-source or machine-proof evidence.

