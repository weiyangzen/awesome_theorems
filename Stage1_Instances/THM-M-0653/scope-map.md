# Scope map

## Included claim

- A one-sorted first-order base language `L` and its expansion by one distinguished relation symbol
  `R` of a fixed finite arity `n`.
- A theory `T` in the expanded language.
- Implicit definability: two `T`-models on the same carrier whose `L`-reducts agree cannot assign
  different relations to `R`.
- Explicit definability: a single parameter-free `L`-formula `phi` of arity `n` agrees with `R` in
  every model of `T`.
- The theorem implication from implicit definability to explicit definability. The reverse
  implication is elementary but belongs to the repository's stated "equivalence" and must be
  included or connected by a checked wrapper in the canonical root.

## Statement-phase decisions

The statement phase must freeze the representation of the one-symbol language extension, relation
arity and tuple convention, ordered binders and universes, equality versus definitional equality of
reduct structures, and semantic consequence over all carriers. It must decide from a reviewed
source whether inconsistent `T`, nullary `R`, empty carriers, equality symbols, and parameterized
variants are included. The formula must be in the old language; merely defining `R` with an
expanded-language formula is circular.

The same-carrier uniqueness formulation is the intake root because it states uniqueness of an
expansion directly. A formulation using isomorphic reducts may be credited only after a checked
transport. Mutation tests must remove the model hypothesis, weaken equality of reducts, change the
formula language, move the existential formula inside the model quantifier, and exercise nullary
and inconsistent-theory boundaries.

## Explicit exclusions

- Svenonius-style definability via automorphism invariance as a substitute without its additional
  hypotheses and a checked equivalence.
- Definability of a set in one fixed structure rather than uniform definability modulo `T`.
- A formula allowed to mention the distinguished relation `R`.
- A separate defining formula chosen for each model instead of one uniform formula.
- Craig interpolation alone, compactness alone, or completeness alone as the root theorem.
- A structure or proposition that assumes the desired defining formula as input.
- The repository label `已验证` or the intake probe as proof evidence.
