# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0940`, the label `加法组合学基本定理`, collective attribution,
the twentieth century, and the gloss `加法组合的核心结果`. These strings identify a subject-area
umbrella, not a standard uniquely named theorem or binder-complete claim. Intake preserves the
literal record and does not expand "fundamental" or "core" into a conjunction of favored results.

No source publication, theorem number, page, definition, premise, proof boundary, correction,
erratum, or formal declaration accompanies the record. An accountable target correction must
identify one exact source proposition before ordinary theorem execution can begin.

## Proposition-changing decisions

After target identity is corrected, the statement phase must freeze all of the following:

- whether the carrier is a finite cyclic group, an arbitrary finite or infinite abelian group, a
  noncommutative group, a torsion-free group, the integers, a vector space, or another structure;
- whether inputs are finite sets, multisets, functions, measures, or positive-density subsets, and
  which nonemptiness, finiteness, measurability, or generating assumptions apply;
- the exact operation: sumset, difference set, iterated sum, restricted sumset, convolution,
  additive energy, doubling, or another additive relation;
- whether the result is direct, inverse, structural, extremal, covering, counting, or
  local-to-global, and whether it is an inequality, existence statement, classification, or
  equivalence;
- every cardinality, density, stabilizer, subgroup, progression, Freiman-homomorphism, rank,
  dimension, exponent, and constant convention;
- the ordered quantifiers, typeclass assumptions, side conditions, strict versus non-strict
  inequalities, conclusion strength, and direction of every alternate encoding; and
- the exact source edition, theorem locator, incorporated definitions, proof boundary,
  corrections, errata, and independent review.

These choices are inequivalent. They are a resolution checklist, not a proposed theorem.

## Candidate families not selected

- A lower bound for a sumset, including the Cauchy-Davenport, Kneser, or Kemperman families.
- An inverse theorem for small doubling, including Freiman-type structure results.
- Ruzsa's covering lemma or a Ruzsa triangle inequality.
- The Plunnecke or Plunnecke-Ruzsa inequalities for iterated sumsets and difference sets.
- The Balog-Szemeredi-Gowers theorem relating additive energy to small doubling.
- Density or progression results such as Roth, Szemeredi, or Green-Tao.
- A package or conjunction of several "core" results chosen by the worker.

The catalog provides no discriminator among these families. None is canonical or credited at
intake.

## Degenerate and boundary cases

Source review must resolve empty and singleton input sets; the trivial group; zero-cardinality and
zero-density cases; repeated summands; zero-fold sums; torsion versus torsion-free carriers;
finite versus infinite cardinality; improper or whole-group stabilizers; constants below one;
division by the cardinality of an empty set; exponents zero and one; strict versus non-strict small
doubling; and whether multiplicities are discarded by set addition. No case is silently excluded.

## Neighbor target boundaries

The surrounding manifest separately owns `THM-M-0936` Cauchy-Davenport, `THM-M-0938` Kneser,
`THM-M-0939` Kemperman, `THM-M-0941` Freiman, `THM-M-0942` Ruzsa covering,
`THM-M-0943` Plunnecke-Ruzsa, `THM-M-0944` Balog-Szemeredi-Gowers, and `THM-M-0945` Green-Tao.
Their names make the generic row especially unsafe to interpret by proximity. No neighbor supplies
inherited statement identity, source status, receipt, or proof credit.

## Formal and trust boundary

Pinned mathlib provides precise, mutually different declarations for several neighboring
families. `IntakeProbe.lean` authenticates representative signatures only. No canonical Lean
expression, minimal import set, statement fingerprint, transport, mutation suite, discovery
protocol, obligation registry, proof body, or axiom/TCB closure is frozen. Numerical experiments,
search results, citations, and the catalog's `已验证` value are explicitly excluded as theorem
evidence.
