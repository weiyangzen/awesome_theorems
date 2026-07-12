# Scope map

## Catalog scope preserved

- Target identity: `THM-M-1404`, named `测度熵` (measure-theoretic entropy).
- Subject boundary: an entropy invariant associated with measure-preserving dynamics.
- Catalog attribution and date: Andrey Kolmogorov, 1958.
- Literal catalog claim: `保测动力系统的熵`.

This is all the mathematical scope fixed by the repository. In particular, the catalog entry is
not a theorem-grade sentence. The standard finite-partition construction is recorded only as a
candidate vocabulary map, not as the canonical root.

## Decisions required before statement freeze

| Surface | Unresolved decision | Why it changes the proposition |
|---|---|---|
| Root kind | definition, limit-existence theorem, conjugacy invariance, power law, or another property | These have different conclusions and proof obligations |
| Measure space | probability, finite, sigma-finite, or Lebesgue/standard probability space | Finiteness and regularity affect entropy and source hypotheses |
| Dynamics | measurable endomorphism or invertible automorphism; literal or mod-null equality | Inverse-image joins, inverse laws, and conjugacy notions differ |
| Partitions | finite only, countable with finite entropy, or another source class | The supremum domain and approximation theorems differ |
| Information | real or extended-real value, log base, normalization, `0 log 0` convention | These choices change types and exact equalities |
| Rate | limit, limsup, or infimum of normalized finite joins | Limit existence is substantive and cannot be assumed by notation |
| System entropy | supremum construction, original Kolmogorov formulation, or a checked equivalent | The 1958 and later formulations require a source-controlled transport |
| Edge cases | zero-mass atoms, trivial partitions, identity/periodic maps, nonergodicity, infinite entropy | Each must be included or excluded explicitly |

## Explicit exclusions

- Topological entropy (`THM-M-1403`) cannot replace a measure-theoretic invariant.
- The Sinai generator theorem (`THM-M-1405`) cannot replace the invariant it helps compute.
- The separately scheduled Kolmogorov-Sinai entropy entry (`THM-M-1406`) cannot be merged into this
  target without an authoritative deduplication and source decision.
- Bernoulli-shift classification, Shannon-McMillan-Breiman, Pesin's entropy formula, and the
  variational principle are related results, not automatic interpretations of this catalog phrase.
- Binary or finite-distribution Shannon entropy alone is not a theorem about a dynamical system.
- A structure carrying an entropy value or the desired property as an unconstrained field would be
  an assumed conclusion, not a formalization.
- The source label `已验证` supplies neither human-proof nor Lean kernel evidence.

Statement ambiguity blocks obligation-tree construction. No obligation denominator, proof graph,
or formal closure status is frozen by this intake.
