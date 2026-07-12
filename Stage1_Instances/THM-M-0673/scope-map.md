# Scope map

## Included claim

- A one-sorted first-order language `L` and an arbitrary family of `L`-structures `M i`.
- A nonempty carrier for every factor and an ultrafilter `U` on the index type.
- The model-theoretic ultraproduct, implemented as the filter product quotient with its induced
  `L`-structure.
- For every sentence `phi`, a biconditional between truth of `phi` in the ultraproduct and truth in
  `U`-almost every factor.
- Principal and nonprincipal ultrafilters, empty languages, nullary symbols, and quantified
  sentences. No finiteness assumption on the language, index type, or factors is introduced.

## Boundary decisions for the statement phase

The canonical public root is the sentence form because it exactly expresses elementary theory
transfer and matches the repository phrase. The statement phase must decide whether the stronger
formula-with-assignments result is a separately modeled supporting obligation or a checked alternate
encoding. It must preserve the order of the language, family, structure/nonempty instances,
ultrafilter, and sentence binders, and record how `Filter.Product` represents the quotient.

The phrase "elementary equivalence" must not be broadened into the false claim that an arbitrary
factor is elementarily equivalent to its ultraproduct. It means agreement between the ultraproduct's
theory and the ultrafilter-almost-everywhere truth predicate. A common-theory preservation theorem
is only a one-way corollary.

## Explicit exclusions

- A direct product theorem with no ultrafilter quotient.
- Preservation only of atomic, quantifier-free, or first-order universal formulas.
- The one-way statement that if every factor models a sentence then the ultraproduct does.
- Compactness, saturation, transfer to hyperreals, or the Los-Vaught test as substitute roots.
- A proposition that assumes the desired satisfaction equivalence as structure data.
- The repository label `已验证`, a declaration name, or `#check` output as proof acceptance.

## Degenerate cases

Each carrier is required to be nonempty by mathlib's semantics and by the quantifier step of the
standard theorem. Principal ultrafilters remain valid and reduce to evaluation at their principal
index up to the quotient. Any empty-index behavior is governed by existence of `Ultrafilter I`, not
by an invented extra hypothesis. These cases must be mutation-tested during the statement phase.
