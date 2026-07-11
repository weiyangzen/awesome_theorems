# Scope map

## Included subject boundary

- Affine Kac-Moody Lie algebras, their integrable highest-weight modules, and formal characters.
- The affine weight lattice, affine Weyl group, Weyl vector, roots and multiplicities, and the
  completed formal-series ring needed to state an infinite character identity.
- If the primary-source statement is the modular result: normalized affine characters, level,
  theta functions, modular parameter, and the `SL(2,Z)` transformation law.
- Degenerate and boundary cases to freeze later include level zero versus positive level, twisted
  versus untwisted affine type, convergence versus formal equality, and singular weights.

## Required source decision

The repository gives only the Chinese title, the gloss "characters of affine Lie algebras", and an
untrusted `已验证` label. That does not distinguish these materially different roots:

1. the Weyl-Kac alternating-sum/product character identity for an integrable highest-weight module;
2. Kac-Peterson modular transformation formulae for normalized affine characters and string
   functions;
3. a specialized numerical character or denominator formula.

The statement node must select one exact theorem from a stable primary-source edition and record
its ordered hypotheses and conclusion before a Lean proposition is authored. It must not combine
the alternatives into a broader theorem.

## Explicit exclusions

- The repo-local loop-algebra and Hahn-series wrappers as a substitute for a character formula.
- Finite-dimensional Weyl character formulae, denominator identities alone, or merely defining a
  formal character.
- A theorem with abstract predicates whose conclusion is supplied as an assumption.
- Legacy `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_053.lean` as accepted rev-5.6 evidence.

The later statement phase must freeze universes, coefficient ring, completion/order, affine type,
imports, declaration type, environment fingerprint, transports, and hypothesis mutations.
