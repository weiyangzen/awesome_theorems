# Scope map

## Preserved theorem family

The intake preserves the Borel-Cantelli theorem family named by the catalog, concerning whether a
point belongs to infinitely many events in a countable sequence. It does not silently choose one
of the customary directions:

- first direction: finite total event measure implies that the limsup event has measure zero;
- second direction: for mutually independent measurable events in a probability space, divergent
  total event measure implies that the limsup event has measure one.

These descriptions locate the family only. Neither is the frozen canonical proposition, and the
target is not assumed to be their conjunction.

## Decisions required at statement freeze

An exact, independently reviewed source statement must decide all of the following:

1. Whether the target is the first lemma, the second lemma, a paired two-part theorem, or an exact
   named generalization.
2. Whether the ambient object is a measure, probability measure, outer measure, or another
   source-specified measure-like object, and which finiteness assumptions apply.
3. Whether the events must be measurable and, for the second direction, the exact mutual,
   pairwise, or conditional independence predicate.
4. Whether convergence is stated as `sum < infinity`, `tsum != infinity`, summability in another
   codomain, or a source-specific series formulation; likewise for divergence.
5. Whether infinitely-often occurrence is expressed by set limsup, a frequently predicate,
   almost-everywhere finite membership, or another encoding, with checked transports for every
   credited alternate form.
6. Whether the conclusion is measure zero/one, probability zero/one, almost-sure eventual
   nonmembership, or an equivalence, and whether the source includes any converse.
7. The ordered binders, universes, typeclasses, foundation and TCB profiles, exact conclusion, and
   all exclusions and boundary cases.

Each choice can alter the proposition or proof boundary. Intake freezes the ambiguity rather than
inventing an answer.

## Degenerate and boundary cases

Source review must explicitly cover an empty sample type; the zero measure; finite versus
probability measures; empty, universal, or constantly repeated events; eventually empty or
eventually universal sequences; zero terms; finite support; a total measure exactly finite or
infinite in `ENNReal`; nonmeasurable sets in the first outer-measure formulation; measurable-set
requirements for the second direction; independent versus merely pairwise independent sequences;
and the meaning of full measure when the ambient measure is not normalized.

No case is excluded at intake because no exact proposition has been selected.

## Excluded substitutions

- The first Borel-Cantelli lemma cannot stand in for the second, or conversely.
- A conjunction of both customary directions cannot be created merely because the family name is
  plural in some expositions.
- Levy's generalized conditional-expectation theorem is related and stronger in one direction, but
  it is not the catalog target without a checked source selection and transport.
- The Erdos-Renyi or Kochen-Stone extensions, independence zero-one laws, strong laws, convergence
  in measure, and other applications are distinct theorems.
- Pairwise independence cannot replace mutual independence without a source and proof showing that
  the selected conclusion remains valid.
- A finite-union bound, tail estimate, special sequence, or finite probability-space example is
  not the infinite-event theorem family.
- A structure or hypothesis that stores the desired null/full-measure conclusion supplies no
  proof.
- A theorem name, `#check`, metadata label, secondary summary, or passing adjacent API probe gives
  no H0 or M0 credit.

## Neighbor and ownership boundaries

`THM-M-0284` owns Kolmogorov's zero-one law and `THM-M-0286` owns Egorov's theorem. The later
catalog target `THM-M-1009` owns the Erdos-Renyi second lemma, described there as a Borel-Cantelli
generalization. Repo-local Lean artifacts for that other target are read-only discovery inputs and
grant no statement or proof credit to `THM-M-0285`.

## Formal boundary

No canonical Lean expression is frozen at intake. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe checks the first and second standard
endpoints, an almost-everywhere first-lemma variant, and Levy's generalized endpoint. This is
bounded discovery evidence, not the later immutable anchor audit, a source-to-statement transport,
or a theorem proof.
