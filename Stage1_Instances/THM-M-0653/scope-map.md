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

## Frozen statement decisions

`Statement.lean` uses `L.sum (OneRel n)`, where `OneRel n` has no function symbols and relation
symbols `PLift (k = n)`. Tuples are `Fin n -> M`. Binders are ordered `L`, `n`, `T`; each semantic
side then ranges over `M : Type w`, a `Nonempty M` witness, structures, model hypotheses, and tuples.
Reducts are compared by equality of the `Language.Structure M` values obtained from `LHom.sumInl`.
The formula is `L.Formula (Fin n)` and its existential binder precedes every carrier/model binder.

The target includes `n = 0`, the empty theory, inconsistent theories (both sides are vacuous in the
expected way), equality atoms supplied by first-order logic, and all nonempty carriers. It excludes
parameters and empty carriers. These choices match mathlib's `Theory.Model` semantic boundary and
the standard parameter-free, one-new-relation formulation frozen at intake.

The same-carrier uniqueness formulation is canonical because it states uniqueness of expansion
directly. Isomorphic-reduct and two-copy syntactic formulations still require checked transports.
Statement review rejected the four weakening mutations: removing either model hypothesis permits
non-model structures; weakening reduct equality changes implicit definability; using an expanded-
language formula permits the circular atom itself; and moving `exists phi` under the model binder
loses uniformity. Nullary relations and inconsistent theories were retained rather than mutated
away.

## Explicit exclusions

- Svenonius-style definability via automorphism invariance as a substitute without its additional
  hypotheses and a checked equivalence.
- Definability of a set in one fixed structure rather than uniform definability modulo `T`.
- A formula allowed to mention the distinguished relation `R`.
- A separate defining formula chosen for each model instead of one uniform formula.
- Craig interpolation alone, compactness alone, or completeness alone as the root theorem.
- A structure or proposition that assumes the desired defining formula as input.
- The repository label `已验证` or the intake probe as proof evidence.
