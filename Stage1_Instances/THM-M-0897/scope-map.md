# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-0897`, the label `设计理论`, the gloss
`组合设计的存在性`, the attribution "many mathematicians," and the twentieth century. Importance
"high" and status `已验证` are catalog metadata, not theorem or proof evidence. No citation,
definition, parameter tuple, or named result accompanies the record.

The wording points toward existence questions in combinatorial design theory. It does not identify
one kind of design or one proposition about that kind.

## Proposition-changing decisions

An approved statement run must freeze all of the following from an immutable, independently
reviewed source:

- the design class: a `t-(v,k,lambda)` design, BIBD, pairwise balanced design, Steiner system,
  group-divisible or resolvable design, Latin-square design, covering/packing, or another object;
- the point carrier and block representation, including finite-set versus finite-type encoding,
  whether blocks are sets or a multiset/list with repetitions, and whether the design must be
  simple;
- parameter domains and ordered binders for `t`, `v`, `k`, `lambda`, replication number, number of
  blocks, allowed block sizes, group sizes, resolution classes, or any source-specific parameters;
- incidence requirements: exactly or at least/at most `lambda` blocks through each `t`-subset,
  whether repeated blocks count with multiplicity, and whether all blocks have fixed cardinality;
- necessary admissibility or divisibility hypotheses, their sufficiency status, exceptional finite
  parameter sets, and all strict inequalities such as `t <= k <= v`;
- the conclusion regime: one explicit construction, exact existence for every admissible tuple,
  existence for all sufficiently large `v`, an if-and-only-if classification, enumeration, or an
  asymptotic estimate; and
- universes, typeclasses, equality conventions, choice/classical principles, computability, and
  every empty, zero, singleton, trivial-block, or vacuous-incidence case.

These choices yield inequivalent theorems. This list is a resolution ledger, not a candidate target.

## Candidate families not credited

- General `t-(v,k,lambda)` design existence under source-selected divisibility and size conditions.
- BIBD or pairwise balanced design existence with source-selected parameter conventions.
- Steiner systems, including Steiner triple systems as a special parameter family.
- Exact, asymptotic, constructive, resolvable, group-divisible, or covering/packing existence
  results.
- Existence and counting of Latin squares or related array designs.

No candidate is canonical at intake. In particular, the catalog does not authorize replacing its
broad gloss with the most familiar theorem in any one family.

## Neighbor-target boundaries

- `THM-M-0898` owns the Kirkman schoolgirl / Steiner triple-system existence target.
- `THM-M-0899` owns the catalog's named Wilson `t`-design existence target.
- `THM-M-0900` owns the catalog's named asymptotic design-existence target.
- `THM-M-0901` owns Latin-square existence and counting.

Those records make plausible readings of `THM-M-0897` explicit elsewhere in the manifest. They do
not supply statement or proof credit here, and this intake does not decide whether the source
intended a disjoint umbrella target or accidentally duplicated one of them.

## Degenerate and boundary cases

The selected source must decide `t = 0`, `lambda = 0`, `k = 0`, `v = 0`, `t > k`, `k > v`, empty
block families, the empty block, full blocks, repeated identical blocks, `k = v`, `t = k`, singleton
point sets, vacuous incidence conditions, zero admissible parameter tuples, and whether isomorphic
designs count as distinct. No case is excluded at intake.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib exposes `Finset.powersetCard`,
`Finset.card_powersetCard`, fixed-size set-family predicates such as `Set.Sized`, and related
counting APIs. The bounded intake search found no exact block-design, combinatorial-design,
`t`-design, BIBD, or Steiner-system declaration in pinned mathlib or repository-local Lean sources.
The checked API probe is substrate evidence only, not a design definition, exact statement,
exhaustive anchor audit, or proof.
