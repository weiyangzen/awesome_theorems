# Scope map

## Included theorem family

- An arbitrary set `A`, with no finiteness, nonemptiness, decidability, or cardinality hypothesis.
- Its full power set `P(A)`, not merely its finite subsets or proper subsets.
- Strict cardinal inequality `|A| < |P(A)|`, including both the injection from `A` into `P(A)`
  and the impossibility of an equivalence in the selected cardinal-order encoding.
- Cantor's diagonal non-surjectivity argument as the central supporting result, subject to an exact
  statement-to-cardinality bridge.

## Decisions required at statement freeze

The statement phase must inspect an immutable primary source and freeze:

- whether the canonical Lean binder is a type `alpha : Type u` or a set `s : Set alpha` represented
  by its subtype;
- whether the conclusion is `#alpha < #(Set alpha)`, `#s < #(Set.powerset s)`, or the normalized
  exponential form `#alpha < 2 ^ #alpha`;
- universe parameters and any lifts needed for a source-faithful comparison;
- the exact meaning of strict cardinal order and the bridge from absence of a surjection;
- the singleton injection witnessing the non-strict direction and the diagonal set witnessing
  non-surjectivity;
- the logical-principle footprint of converting between injection, surjection, equivalence, and
  cardinal-order formulations;
- checked transports among all alternate forms that receive proof credit.

The empty set is not excluded. Its power set is a singleton, so it is an ordinary boundary case
that must survive statement mutation testing. Finite, countably infinite, and uncountable sets are
all covered uniformly.

## Explicit exclusions

- Only the assertion that no function `A -> P(A)` is surjective, without checking that it composes
  to the selected strict-cardinality root.
- Only the assertion that no injection `P(A) -> A` exists, absent the required cardinal bridge.
- The special case `A = Nat`, the uncountability of the reals, or only infinite sets.
- A comparison with the set of finite subsets, lists, multisets, or predicates satisfying an extra
  property instead of the full power set.
- A ZFC universe-level theorem about the class of all sets as a substitute for the polymorphic
  set/type theorem.
- A structure or hypothesis that contains the desired strict inequality as assumed data.
- The repository label `已验证`, a theorem name, or a successful API probe as proof evidence.

No canonical Lean expression is accepted at intake. The downstream statement phase owns exact
elaboration, fingerprints, transports, and mutation tests.
