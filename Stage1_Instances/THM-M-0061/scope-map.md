# Scope map

## Preserved catalog claim

The repository fixes the title `拉格朗日定理`, attribution Joseph-Louis Lagrange, year 1771, and
the sentence `有限群G的子群H的阶整除G的阶`: the order of a subgroup `H` of a finite group `G`
divides the order of `G`. Intake preserves that complete mathematical sentence rather than a
broader theorem associated with Lagrange's name.

The intended mathematical binders are an arbitrary finite multiplicative group `G` and an
arbitrary subgroup `H <= G`. The conclusion is divisibility in the natural numbers. No normality,
properness, nontriviality, commutativity, cyclicity, or chosen coset-representative hypothesis is
part of the claim.

## Lean encoding decisions reserved for statement

The likely faithful Lean shape is `{G : Type u} [Group G] [Finite G] (H : Subgroup G)` with
conclusion `Nat.card H ∣ Nat.card G`. The statement phase must nevertheless freeze and test:

- the universe and exact ordered binders;
- `Finite G` versus `Fintype G`, including any noncomputable instance conversion;
- `Nat.card` versus `Fintype.card` and checked transports between them;
- whether the root is a named proposition, theorem declaration, or both;
- the minimal import and normalized expression/environment fingerprints;
- whether the additive theorem is merely excluded or recorded as a checked alternate encoding;
- removed-finiteness, changed-domain, changed-binder-scope, and boundary mutations.

These are encoding choices, not permission to weaken or broaden the source claim.

## Boundary cases included

- the trivial group;
- the bottom subgroup, of order one;
- the top subgroup, whose order equals the ambient group order;
- arbitrary finite nonabelian groups;
- subgroups that are normal, nonnormal, proper, or equal to the whole group.

The group carrier is inhabited by the identity, and finiteness of a subgroup follows from ambient
finiteness. No additional nonemptiness or subgroup-finiteness premise may be added merely for API
convenience.

## Explicit exclusions

- the stronger arbitrary-group `Nat.card` declaration used as literal statement identity without
  preserving the catalog's finite-group premise;
- the additive-group analogue;
- the quotient-cardinality product identity or an index formula substituted for divisibility
  without a checked implication to the selected root;
- element-order divisibility, cyclic-subgroup corollaries, Cauchy's theorem, or Sylow theorems;
- only normal subgroups, only proper subgroups, only abelian groups, or a fixed concrete group;
- a structure or hypothesis that assumes the divisibility conclusion;
- the catalog's `已验证` label, a theorem name, or a successful API probe used as source or proof
  acceptance.

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.GroupTheory.Coset.Card` documents and proves `Subgroup.card_subgroup_dvd_card`. Its exposed
type has only `[Group G]`; for an infinite carrier `Nat.card G = 0`, so the declaration is a genuine
generalization of the finite catalog claim. The probe demonstrates that it can discharge a
finite-scope example. It does not establish normalized statement identity, source fidelity,
accepted wrapper ownership, proof-body provenance, or M0.
