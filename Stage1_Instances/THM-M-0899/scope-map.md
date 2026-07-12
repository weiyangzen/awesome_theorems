# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0899`, the title `Wilson定理`, Richard Wilson, the year 1972,
and the gloss `t-设计的存在性`. Importance `高` and status `已验证` are catalog metadata, not
source or kernel evidence. No citation, theorem number, definition, parameters, hypotheses, or
conclusion accompanies the record.

The title and gloss point toward combinatorial design existence, but do not identify one exact
claim. The unrelated factorial/primality Wilson theorem present in pinned mathlib is excluded by
the catalog's category, attribution, date, and design gloss.

## Candidate readings requiring a source decision

1. **Pairwise balanced designs.** A Wilson existence theorem for PBDs with an allowed block-size
   set and sufficiently large admissible point count. Wilson's 1972 paper titles are discovery
   evidence for this family, but the catalog does not give the definition, admissibility invariants,
   quantifier order, threshold, or selected theorem in the series.
2. **Balanced incomplete block designs.** An eventual existence theorem for a fixed
   `2-(v,k,lambda)` parameter family under the necessary divisibility conditions. This may be a
   specialization or corollary of PBD theory, but no such specialization is selected by the record.
3. **General `t`-designs.** Eventual existence of a `t-(v,k,lambda)` design under natural
   divisibility conditions for fixed parameters. This matches the literal gloss more closely, but
   it cannot be attributed to the located 1972 paper titles without a source and checked historical
   crosswalk; silently replacing Wilson with a later theorem would substitute mathematics.
4. **A fixed finite construction or exact classification.** The gloss does not rule this out, but
   supplies no order, parameter tuple, exceptional set, or if-and-only-if conclusion.

No candidate is canonical or receives proof credit during intake.

## Statement-phase decisions

An immutable, independently reviewed source must freeze:

- the design class and representation: `t`-design, BIBD, PBD, simple block family, or blocks counted
  with multiplicity;
- the point carrier, block carrier, universes, finiteness and decidable-equality assumptions, and
  whether equality is literal or up to isomorphism;
- all parameter domains and ordered binders, including `t`, `v`, `k`, `lambda`, an allowed
  block-size set, replication number, or source-specific gcd invariants;
- the incidence law, exact multiplicity convention, block cardinality restrictions, and every
  inequality such as `t <= k <= v`;
- every necessary congruence or divisibility hypothesis and whether it is also sufficient only
  beyond a threshold;
- which parameters are fixed before the threshold and which may vary, the exact threshold
  dependency, strict versus non-strict comparison, and any exceptional orders;
- whether the conclusion is an explicit construction, existential witness, nonempty structure,
  eventual existence statement, or iff characterization;
- source edition, theorem/page locator, incorporated definitions, proof boundary, corrections or
  errata, and the relationship among the 1972 parts I/II and 1975 part III; and
- minimal Lean imports, canonical expression/environment fingerprints, checked alternate
  encodings, foundation/TCB policy, and mutations for deleted divisibility assumptions, changed
  domains, moved binders, and boundary cases.

## Degenerate and boundary cases

The selected source must decide `t = 0`, `lambda = 0`, `k = 0`, `v = 0`, `t > k`, `k > v`,
`t = k`, `k = v`, the empty allowed-size set, empty or repeated blocks, vacuous incidence,
singleton carriers, zero thresholds, point count equal to the threshold, and whether repeated
blocks contribute separately. No case is excluded at intake.

## Explicit exclusions

- Substituting the factorial/primality Wilson theorem because it has the same English name.
- Treating a PBD, BIBD, arbitrary `t`-design, Steiner system, or graph-decomposition theorem as
  canonical without an accepted source identity and checked specialization.
- Presenting necessary counting/divisibility conditions as sufficient existence.
- Replacing eventual existence by one explicit finite example, or conversely.
- Defining a structure or hypothesis that already stores the required design witness and then
  projecting it as an existence proof.
- Using generic `Finset`, powerset, cardinality, or binomial APIs as a design theorem.
- Using search, random generation, a database, numerical evidence, or an unchecked certificate as
  proof.
- Using the catalog's `已验证` label as human-source or machine evidence.

## Neighbor-target boundary

- `THM-M-0897` is the broader underspecified design-theory target.
- `THM-M-0898` is the Kirkman schoolgirl / Steiner-triple-system target.
- `THM-M-0900` separately owns the catalog's asymptotic design-existence label.
- `THM-M-0901` owns Latin-square existence and counting.

These records do not supply statement or proof credit here. In particular, the overlap between a
plausible eventual Wilson theorem and `THM-M-0900` must be resolved rather than silently duplicated.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib exposes fixed-cardinality finite subsets and
binomial coefficients, while the bounded intake search found no exact design declaration under the
names `BlockDesign`, `BalancedIncompleteBlockDesign`, `PairwiseBalancedDesign`, `SteinerSystem`, or
`TDesign`. This is discovery-only evidence, not an exhaustive anchor audit or a global absence
claim. The existing `Mathlib.NumberTheory.Wilson` module proves the unrelated number-theoretic
theorem and is not a candidate.
