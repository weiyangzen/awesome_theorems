# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-1592`, the title `Reed-Solomon码`, the literal gloss `MDS码`, the
attribution to Reed and Solomon, and the year 1960. The importance and `已验证` fields are catalog
metadata, not source-fidelity or Lean evidence. `MDS码` names a code property or family; it is not a
truth-valued statement with fixed parameters and hypotheses.

The separate computer-science record `THM-C-0381` says `MDS码的构造`. Stage0's exact-deduplication
rule retained it as a distinct item, and it is outside the 1546-target Lean manifest. It may inform
duplicate review but cannot broaden or substitute this mathematics target.

## Candidate result families not credited

The Reed-Solomon name and the primary bibliographic lead make several distinct roots plausible.
None is selected or credited by this intake:

1. Define a polynomial evaluation code over a finite field at a list or finite family of distinct
   evaluation points.
2. Prove that evaluation is injective below a degree bound and derive the code dimension or
   cardinality.
3. Prove that two distinct message polynomials yield words differing in at least `n-k+1`
   coordinates, using the bound on the number of roots of a nonzero polynomial.
4. Combine the lower bound with a source-selected Singleton bound to prove exact minimum distance
   `n-k+1`, hence the MDS property.
5. Derive a unique-decoding or error-correction radius from that distance, with an exact rounding
   convention and decoder specification.
6. State an extended, generalized, shortened, punctured, cyclic, or projective Reed-Solomon result,
   rather than the ordinary evaluation-code theorem.
7. Formalize a result bundle or an algorithm from the 1960 paper instead of a single MDS theorem.

These claims are related but not interchangeable. In particular, a definition is not a theorem;
injectivity alone does not establish the minimum distance; a lower distance bound alone is not
equality in the Singleton bound; and an MDS property does not by itself prove a decoder correct.

## Proposition-changing decisions

An approved statement phase must freeze all of the following from one immutable source passage:

- the selected edition and theorem/equation/page locator, incorporated definitions, exact proof
  boundary, errata decision, translation decisions, and independent review;
- ordinary versus generalized/extended/shortened/punctured/projective Reed-Solomon codes and
  whether the target is a construction, parameter, distance, MDS, correction, or decoding claim;
- the finite field, its cardinality `q`, word length `n`, message dimension or degree cutoff `k`,
  and the exact constraints among `q`, `n`, and `k`;
- ordered evaluation points versus a finite set, injectivity/distinctness, inclusion of zero or an
  infinity coordinate, and any column multipliers or normalization;
- message representation as coefficient vectors or polynomials, strict `natDegree < k` versus a
  degree bound, treatment of the zero polynomial, and the evaluation map's codomain/index type;
- code representation as a set, submodule, range of a linear map, generator matrix, or quotient,
  together with the definition of length, dimension/cardinality, Hamming distance, and minimum
  distance;
- whether `MDS` means equality in the Singleton bound, the explicit parameter identity
  `d = n-k+1`, a generator-matrix minor condition, or another equivalent formulation, and which
  transports must be checked in which directions;
- absolute versus relative distance, pairwise-codeword versus nonzero-word weight conventions,
  minimum over an empty set, natural-number subtraction, and all strict/non-strict inequalities;
- any claimed error radius, floor/ceiling convention, erasure/error mix, decoder, tie behavior,
  failure result, and algorithmic termination or complexity claim; and
- whether finite computation is proof-producing with a checked certificate or merely an example,
  search, experiment, or unchecked oracle.

## Boundary cases to resolve

- empty or singleton fields are impossible for a field but the exact finite-field/nontriviality
  assumptions and universe/typeclass instances must still be explicit;
- `n = 0`, `k = 0`, `k = 1`, `k = n`, `k > n`, and `n > q`, including whether empty or constant
  codes are admitted and whether an infinity coordinate permits `n = q + 1`;
- repeated evaluation points, zero multipliers, empty point families, reordered points, and whether
  code equality is definitional or only up to coordinate equivalence;
- the zero polynomial, zero word, equal codeword pair, zero-dimensional code, and whether minimum
  distance ranges over distinct pairs or nonzero codewords;
- natural subtraction at parameter endpoints, exact versus at-least distance, and whether the
  Singleton bound is imported as a separate root-critical obligation; and
- error radius zero, half-distance rounding, errors plus erasures, decoder ties, malformed received
  words, algorithm failure, and claims about correction versus detection.

## Excluded substitutions

- A definition of a polynomial evaluation code presented as the requested theorem.
- Generic polynomial evaluation, root-count, Hamming-distance, or Vandermonde lemmas presented as
  an exact Reed-Solomon or MDS result.
- A toy code over one chosen small field or a finite enumeration used for the general family.
- The Singleton bound alone, an arbitrary MDS-code existence theorem, or a different algebraic code
  family used as the Reed-Solomon root.
- A lower minimum-distance bound used as exact MDS equality without the necessary upper bound and
  source-selected parameter definitions.
- A decoder, structure field, input hypothesis, oracle, simulation, or example that assumes the
  target property.
- The separate `THM-C-0381` gloss used to change the claim, formal system, status, or evidence of
  this target.
- The catalog label `已验证` used as a primary source, formal proof, or validation receipt.

## Lean and trust boundary

Pinned mathlib provides Hamming distance/weight, polynomial evaluation and root-cardinality bounds,
and square Vandermonde matrices with determinant and injectivity results. Those APIs could support
a future finite-field evaluation-code encoding. They do not define a Reed-Solomon code, its
dimension or minimum distance, an MDS predicate, a Singleton-bound bridge, or a decoder theorem.
Exact imports, expression and environment fingerprints, alternate transports, mutation tests,
foundation and axiom policies, obligation registry, discovery inventory, proof architecture, and
release evidence remain downstream work.
