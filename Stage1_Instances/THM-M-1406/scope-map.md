# Scope map

## Catalog scope preserved

- Target identity: `THM-M-1406`, named `Kolmogorov-Sinai熵`.
- Subject boundary: entropy associated with a measure-preserving dynamical system.
- Catalog attribution and date: Kolmogorov/Sinai, 1958.
- Literal catalog claim: `动力系统的熵`.

This is all the mathematical scope fixed by the repository. The name conventionally denotes the
modern measure-theoretic entropy invariant, but neither the name nor the gloss supplies a
truth-valued root. The finite-partition construction below is only a vocabulary map for later
source selection.

## Decisions required before statement freeze

| Surface | Unresolved decision | Why it changes the proposition |
|---|---|---|
| Root kind | definition, entropy-rate existence, isomorphism invariance, iterate law, historical equivalence, or a computation theorem | These have different conclusions and proof obligations |
| Historical scope | Kolmogorov's quasi-regular systems, Sinai's general finite-partition invariant, or a reviewed equivalence between them | The 1958 and modern invariants do not have identical literal definitions or domains |
| Measure space | probability, finite, sigma-finite, or Lebesgue/standard probability space | Finiteness and regularity affect entropy and source hypotheses |
| Dynamics | measurable endomorphism or invertible automorphism; literal or mod-null equality; discrete or continuous time | Inverse-image joins, two-sided translates, conjugacy, and scaling laws differ |
| Partitions | finite only, countable with finite entropy, or another source class | The supremum domain and approximation theorems differ |
| Information | real or extended-real value, logarithm base, normalization, and `0 log 0` convention | These choices change types and exact equalities |
| Rate | limit, limsup, or infimum of normalized finite joins | Limit existence is substantive and cannot be assumed by notation |
| System entropy | supremum over partitions, an original conditional-entropy formulation, or a checked equivalent | A transport between historical and modern definitions needs its own statement and evidence |
| Edge cases | zero-mass atoms, trivial systems, identity/periodic maps, nonergodicity, and infinite entropy | Each must be included or excluded explicitly |

## Explicit exclusions

- Topological entropy (`THM-M-1403`) cannot replace a measure-theoretic invariant.
- The separately scheduled generic measure-theoretic entropy record (`THM-M-1404`) cannot be
  silently merged with this target. Their catalog glosses overlap and require an authoritative
  identity or deduplication decision.
- The Sinai generator theorem (`THM-M-1405`) is a computation theorem for a generating partition,
  not automatically the definition or another unspecified theorem about KS entropy.
- Bernoulli-shift entropy, Ornstein classification, Shannon-McMillan-Breiman, Pesin's formula,
  Abramov's formula, Kushnirenko finiteness, and the variational principle are related results, not
  automatic readings of this catalog phrase.
- Shannon entropy of one finite distribution alone is not a theorem about a dynamical system.
- A structure carrying an entropy value, limit existence, invariance, or the desired equality as
  an unconstrained field would assume rather than prove the missing result.
- The source label `已验证` supplies neither a human-proof crosswalk nor Lean kernel evidence.

Statement ambiguity blocks obligation-tree construction. No canonical expression, obligation
denominator, proof graph, or formal closure status is frozen by this intake.
