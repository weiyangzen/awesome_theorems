# THM-M-0483 scope map

## Received scope

The only theorem wording owned by this target is the catalog gloss `梅森数的素性检验`, translated
literally as "primality testing/determination of Mersenne numbers." The same record supplies Lucas,
1876, but no formula, quantifier, premise, conclusion, source edition, or theorem locator. Intake
freezes that received family boundary, not a completed mathematical statement.

## Candidate families

| Candidate | Exact candidate shape | Evidence at intake | Boundary and decision still required |
|---|---|---|---|
| Lucas's 1876 large-prime result | `(mersenne 127).Prime` | Pinned mathlib's archive labels this example `Edouard Lucas (1876)` and checks it through the Lucas-Lehmer implementation | Strongest date match, but the repository never says exponent 127 and the archive is a modern formal discovery source, not the missing primary-source crosswalk |
| Necessary exponent criterion | `forall p, (mersenne p).Prime -> Nat.Prime p` | Pinned `Nat.Prime.of_mersenne` | A general structural property, not by itself a primality test or Lucas's 1876 result |
| General Lucas-Lehmer criterion | for `3 <= p`, `LucasLehmerTest p <-> (mersenne p).Prime` | Pinned sufficiency and necessity directions exist with different lower-bound hypotheses | Presumptively belongs to distinct `THM-M-0484`; no unqualified iff is valid because exponent 2 is exceptional |
| Computational prime certificates | individual propositions such as `(mersenne 127).Prime` discharged by certified recurrence computation | Pinned archive has several examples | One finite instance cannot silently replace a source-defined general criterion, and other exponents cannot be aggregated into the root |
| Historical Lucas criterion | a source-defined recurrence or congruence from an immutable 1876 publication | Catalog attribution and date are a source lead | Exact recurrence, indexing, hypotheses, direction, and relation to the modern Lucas-Lehmer encoding have not been inspected or reviewed |

No row is selected as the canonical target during intake. The first row is the preferred
disambiguation lead because it uniquely matches the supplied year and avoids absorbing the adjacent
1930 test target, but preference is not statement identity.

## Neighbor boundaries

| Neighbor | Relationship | Exclusion from current credit |
|---|---|---|
| `THM-M-0484`, Lucas-Lehmer test | Immediately adjacent catalog target, attributed to Lucas/Lehmer in 1930 and described as a fast Mersenne-prime test | Its recurrence criterion, proof, and future receipts cannot be copied into `THM-M-0483`; any overlap requires explicit reviewed target allocation |
| `THM-M-0405`, Bilu theorem | Existing dossier mentions Lucas-Lehmer only as a nearby non-target while studying primitive divisors | Its searches and artifacts belong to another target and provide no accepted evidence here |
| Mathlib `LucasPrimality` | General multiplicative-order primality certificate, explicitly distinct from the Lucas-Lehmer test | A generic certificate is not a Mersenne-specific canonical statement |

## Open statement choices

- Whether "determination" means one historical prime, a necessary criterion, a decision test, or a
  correctness theorem for a specified algorithm.
- Whether the root quantifies over a natural exponent, requires that exponent to be prime, or fixes
  exponent 127.
- Whether the Mersenne number is exactly natural subtraction `2 ^ p - 1`, and what happens at
  `p = 0`, `p = 1`, and `p = 2`.
- For a recurrence criterion, its initial value, recurrence carrier, modular reduction convention,
  residue index, lower bound, and both logical directions.
- Whether the conclusion is primality, compositeness, decidability, correctness, or a concrete
  certificate.
- Which historical source statement and definition chain the repository intended, and how modern
  notation transports to it.

## Degenerate and mutation boundaries

No degenerate case is excluded before an exact proposition is selected. The statement phase must
test at least removed lower-bound or primality hypotheses, changed exponent/domain types, changed
quantifier scope, and the boundary exponents `0`, `1`, and `2`. For the modern Lucas-Lehmer
candidate, `p = 2` is decisive: `mersenne 2` is prime while `LucasLehmerTest 2` is false, so an
unqualified iff would be a broadened false target.

## Prohibited substitutions

- Do not use only `Nat.Prime.of_mersenne` as proof of a primality-test correctness theorem.
- Do not assign the modern Lucas-Lehmer iff to this target without resolving `THM-M-0484` ownership.
- Do not replace a general theorem with a finite list of checked Mersenne primes.
- Do not treat a definition, `#check`, theorem name, source URL, or the `已验证` metadata label as
  statement or proof evidence.
- Do not assume the desired primality, residue equality, or certificate as a premise.
