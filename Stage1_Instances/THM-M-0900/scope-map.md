# Scope map

## Preserved repository scope

The repository fixes only the title `Keighery定理`, the gloss `设计的渐近存在性` ("asymptotic
existence of designs"), a collective attribution, the twentieth century, and an untrusted verified
label. Intake preserves those strings exactly. It does not normalize `Keighery` to `Keevash`, infer
a bibliographic source, or choose one mathematical meaning of "design" or "asymptotic existence."

## Identity decision required

An accountable source correction must first decide whether `Keighery` is:

- a misspelling or mistransliteration of Peter Keevash;
- another person, named result, or source not located by the bounded intake search;
- an unattributed theorem-family label rather than a person's name; or
- a corrupted merger of Wilson's theorem, the Erdos-Hanani/Rodl approximate-design result,
  Keevash's exact existence theorem, or another design result.

The candidate Keevash correction is plausible but uncredited. The catalog says "many
mathematicians" and "twentieth century," whereas Keevash's first arXiv version appeared in 2014.
Those discrepancies must be adjudicated from source provenance rather than repaired by similarity.

## Proposition-changing decisions

After identity correction, the statement phase must obtain an immutable source and freeze:

- the meaning of a design: a simple block set or a block multiset, a Steiner system, a
  `(v,k,t,lambda)` design, a pairwise balanced design, a graph or hypergraph decomposition, a
  resolvable design, or another incidence structure;
- the ground object and finiteness model, including labeled versus unlabeled points and whether
  repeated blocks are allowed;
- every integer parameter, its range and ordering, and which parameters are fixed while the point
  count tends to infinity;
- the exact incidence multiplicity requirement and whether every `r`-subset is covered exactly,
  at least, or asymptotically `lambda` times;
- the complete natural divisibility or congruence conditions and whether they are assumed to be
  necessary and sufficient;
- the order and dependency of the threshold and universal quantifiers, including strict versus
  non-strict comparison with the threshold;
- exact existence versus approximate packing/covering, an asymptotic density statement, an
  enumeration formula, or an algorithmic construction;
- all boundary cases, such as `r = 0`, `r = 1`, `q = r`, `q > n`, `lambda = 0`, empty ground sets,
  zero thresholds, duplicated blocks, and vacuous divisibility; and
- one truth-valued conclusion, all incorporated definitions, alternate encodings, and the
  foundation, trust, and computation profiles.

These choices produce inequivalent propositions. They are a resolution checklist, not a canonical
claim.

## Candidate families not credited

- Keevash's general exact existence result for fixed `q > r >= 1` and constant multiplicity,
  conditional on the natural divisibility constraints for all sufficiently large `n`.
- Wilson's asymptotic existence result for the `r = 2` balanced incomplete block-design case.
- The Erdos-Hanani conjecture and Rodl's approximate packing result, which cover asymptotically all
  `r`-subsets but do not give the same exact design conclusion.
- Exact Steiner-system existence (`lambda = 1`) versus general constant-multiplicity designs.
- Hypergraph clique-decomposition, typicality, extendability, or robust fractional-decomposition
  theorems that imply design existence only after checked specialization.
- Results allowing parameters to grow with `n`, large multiplicity, resolvability, enumeration, or
  randomized construction guarantees.

No family in this list is selected or credited at intake.

## Neighbor and substitution exclusions

The immediately preceding targets separately own Kirkman's schoolgirl problem (`THM-M-0898`) and
Wilson's theorem (`THM-M-0899`). The following target owns Latin-square existence and counting
(`THM-M-0901`). Their statements, sources, formal artifacts, and proof credit cannot be transferred
to this target. A Steiner triple system, finite projective plane, strongly regular graph, Latin
square, or one explicitly constructed small design is only a special object, not the unspecified
asymptotic root.

A structure containing blocks together with a field that asserts the required coverage is data
assuming the desired design, not a proof that such a design exists. Likewise, a random generator,
search result, numerical density, or unchecked certificate cannot close an exact existence claim.

## Formal boundary

No canonical Lean target or minimal import set is frozen. Pinned mathlib provides finite-set
`powersetCard`, membership, cardinality, and `Nat.choose` infrastructure, but the bounded exact-topic
search found no block-design, Steiner-system, or `t`-design declaration. `IntakeProbe.lean`
authenticates only that adjacent substrate. It does not define a design, select a source statement,
or supply statement or proof credit.
