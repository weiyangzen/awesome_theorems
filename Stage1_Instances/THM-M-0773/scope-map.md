# Scope map

## Included mathematical claim

- An arbitrary type `alpha` and a family `F` of subsets of `alpha`.
- Finite character in the biconditional sense: `X` belongs to `F` exactly when every finite subset
  of `X` belongs to `F`.
- A nonempty-family premise, represented either directly or by a selected seed `x` in `F`.
- Existence of an `m` in `F` that is maximal under subset inclusion.
- The stronger pointed conclusion that every selected `x` in `F` extends to such an `m`.

The empty family is the decisive boundary case. With the standard definition it has finite
character, since both sides of the defining biconditional are false for every `X`: the empty set is
a finite subset of `X` but is not a member of the empty family. It nevertheless has no maximal
member. Thus the repository gloss is only true with nonemptiness, or equivalently in the pointed
form beginning from `x in F`.

## Statement choices frozen for downstream checking

`Maximal (fun y => y in F) m` is relative maximality: `m` belongs to `F` and any member of `F`
containing `m` equals `m`. It does not assert that `m` contains every member of `F`. The order is
ordinary subset inclusion, not strict inclusion or reverse inclusion. No finiteness condition is
placed on `m`; finite character is a closure/detection property of the family.

The pointed and unpointed nonempty forms are intended as equivalent encodings of the same root.
The statement phase must implement and kernel-check both transports rather than relying on prose.

## Explicit exclusions

- The Kuratowski-Zorn lemma for arbitrary partially ordered sets as a substitute root.
- Hausdorff's maximal principle or the axiom of choice as a substitute, despite known equivalences.
- A greatest member of `F`; maximal and greatest are materially different conclusions.
- Families of finite sets, finite families, finite-character predicates in matroid theory, or
  finite-character model-theoretic properties unless transported to the frozen set-family claim.
- Dropping nonemptiness, changing the biconditional definition to one implication, or restricting
  the finite subsets to nonempty finite subsets.
- Treating the repository's `已验证` label or a successful API probe as proof acceptance.

## Profiles and open downstream work

The canonical backend is Lean 4 with pinned mathlib. The candidate implementation invokes a Zorn
lemma; exact classical logic, choice, dependency, terminal-body, and TCB closure remain for the
statement and anchor-audit phases. Primary-source fidelity, historical attribution, obligation
decomposition, readable reconstruction, reproducibility, and independent review remain open.
