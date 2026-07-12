# Scope map

## Included theorem family

- A nonempty carrier equipped with a partial order.
- A chain is a subset whose elements are pairwise comparable under the inherited order.
- Every chain has an upper bound in the carrier. In the relativized subset form, the upper bound
  must also belong to the distinguished subset.
- The conclusion is existence of a maximal element: if `m <= a`, then `a = m`.
- Singleton carriers and carriers with a greatest element remain valid boundary instances.

## Statement decision

The canonical target uses a whole nonempty carrier with `PartialOrder`, requires upper bounds only
for nonempty chains, and concludes `IsMax`. `Statement.lean` fixes the universe and binder order,
elaborates this expression, checks the equality expansion of maximality, and mutation-tests the
empty-carrier, preorder, all-chain, and greatest-element alternatives. General-relation and subset
forms remain uncredited alternate encodings. Exact primary-source wording remains an H-gate rather
than being invented from the repository's incomplete gloss.

## Boundary and mutation obligations

- Removing chain boundedness must not remain equivalent: for example, the integers with their usual
  order are nonempty but have no maximal element.
- Replacing "upper bound" by "greatest member of the chain" strengthens the hypothesis and is not
  the same statement.
- Replacing "maximal" by "greatest" strengthens the conclusion and is invalid in a poset with two
  incomparable maximal elements.
- Allowing an upper bound outside a distinguished subset breaks the subset formulation.
- An empty carrier cannot satisfy the nonempty-poset formulation; conventions involving the empty
  chain must not hide this boundary.

## Explicit exclusions

- Hausdorff's maximal principle (every chain lies in a maximal chain) as a substituted root.
- The well-ordering theorem or axiom of choice as the root, even though these are classically
  equivalent under ordinary foundations.
- The Teichmuller-Tukey finite-character lemma.
- Only `zorn_subset`, only an ideal-existence corollary, or another application of Zorn in place of
  the general order-theoretic claim.
- A preorder conclusion whose `IsMax` predicate does not transport back to the selected partial-order
  statement.

Any equivalence with a choice principle and any general-relation or subset encoding is a bridge
obligation, not automatic proof credit. The dossiers for `THM-M-0772` and `THM-M-0774` are separately
owned and confer no statement or proof credit here.
