# Source-statement crosswalk

## Repository record

| Catalog component | Repository evidence | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Target identity | `Docs/researches/math_theorems.md:11784-11789`: `零知识证明` | Future namespace and declaration | Stable UID and subject only |
| Attribution/date | Goldwasser/Micali/Rackoff, 1985 | Provenance metadata | Strongly identifies the GMR source family, not one root |
| Literal claim | `不泄露信息的证明` | No expression | Intuitive slogan, not a binder-complete proposition |
| Source status | `已验证` | No receipt | Explicitly untrusted; supplies no H or M credit |
| Exact premises/result | `待补充` in Stage0 | Ordered binders, hypotheses, conclusion | Absent; canonical statement remains null |
| Formal artifact | `待补充` in Stage0 | Proof body, wrapper, or pinned import | Absent |

The same repository separately lists `THM-C-0181` (the GMR zero-knowledge definition),
`THM-C-0182` (the GMW theorem), and `THM-C-0183` (3-color zero knowledge). Those records confirm
that definition and existence claims are distinct. They are Stage0 computer-science neighbors, not
scope or evidence authority for this Stage1 mathematical target.

## Inspected primary-source lead

Shafi Goldwasser, Silvio Micali, and Charles Rackoff, "The Knowledge Complexity of Interactive Proof
Systems," *SIAM Journal on Computing* 18(1), 1989, pages 186-208, DOI `10.1137/0218012`. The
article notes receipt on 1985-08-26 and a preliminary FOCS 1986 version. An author-hosted 23-page
scan was inspected for source-family discrimination; observed SHA-256:
`17b24f25b180ba64559a089efb443337c61c916078f73be4c496bf8d27410222`.

This is primary discovery evidence, not `H0`. The repository does not cite this edition or select a
root; no complete definition-chain, premise, proof-dependency, correction/errata, or translation
crosswalk has been accepted; and no independent reviewer is assigned.

## Primary source to candidate target

| Source locator | Source content | Prospective formal surface | Intake boundary |
|---|---|---|---|
| Abstract, p. 186 | Defines ZK proofs intuitively as conveying no additional knowledge beyond correctness; announces QR and QNR examples | High-level canonical-name discriminator | Not a proposition or proof receipt |
| Section 2.2, p. 190 | Defines interactive proof systems using completeness and soundness negligible faster than every inverse polynomial | Language, protocol, acceptance probability, adversarial prover | Required dependency if a GMR proof-system theorem is selected |
| Sections 3.1-3.2, pp. 191-193 | Defines perfect/statistical/computational indistinguishability and approximability by expected-PPT sampling | Distribution families, distinguishers, simulator | Multiple inequivalent security notions |
| Section 3.3, pp. 193-194 | Defines a protocol as perfect/statistical/computational ZK for every PPT verifier with polynomial auxiliary input; defines ZK proof systems | Protocol/view/simulator predicate and proof-system conjunction | Definition candidate, not an existence theorem |
| Section 5, Theorem 1, p. 199 | The displayed protocol is a perfectly zero-knowledge proof system for `QR` | Exact QR protocol correctness plus perfect simulation | Concrete theorem candidate, not selected by catalog |
| Section 6, Theorem 2, p. 203 | The displayed protocol is a statistically zero-knowledge proof system for `QNR` | Exact QNR protocol correctness plus statistical simulation | Different concrete theorem candidate, not selected |

The journal text calls computational zero knowledge the most general of its three notions and then
uses "zero knowledge" unqualified for that notion. A future statement cannot treat the three
notions as synonyms or infer a general existence statement from the definition.

## Neighbor and non-substitution boundary

| Neighbor | Distinction |
|---|---|
| `THM-M-0727` interactive proofs | Names the broader protocol/proof-system model; it supplies no ZK property or theorem credit |
| `THM-C-0181` GMR definition | A definition target, not automatically the theorem requested here |
| `THM-C-0182` GMW theorem | A later all-NP existence result; its exact assumptions require its own source audit |
| `THM-C-0183` 3-color ZK | A specific later protocol/language theorem |
| `THM-C-0185` Fiat-Shamir | Interactive-to-noninteractive heuristic/transform under different models |
| `THM-C-0186` through `THM-C-0190` | SNARK, STARK, Bulletproof, Sigma, and concurrent-ZK targets use different setup, interaction, security, or composition contracts |

## Pinned Lean discovery surface

| Pinned module/declaration | Possible role | Credited status |
|---|---|---|
| `Mathlib.Computability.Language`: `Language` | Bit-string language substrate | API availability only |
| `Mathlib.Computability.TuringMachine.Computable`: `Turing.TM2ComputableInPolyTime` | Deterministic polynomial-time computation interface | Does not model probabilistic interactive parties |
| `Mathlib.Probability.ProbabilityMassFunction.Monad`: `PMF`, `PMF.pure`, `PMF.bind` | Discrete distribution and sampler composition | No protocol, view, or indistinguishability theorem |
| `Mathlib.Analysis.Asymptotics.SuperpolynomialDecay`: `Asymptotics.SuperpolynomialDecay` | Candidate negligible-function substrate | Generic asymptotic predicate only |

A bounded lexical search of pinned mathlib and repo-local Lean found no zero-knowledge, knowledge-
complexity, interactive-protocol, or computational-indistinguishability declaration. That is a
discovery observation, not an exhaustive anchor audit or a global nonexistence claim.

## Required source acceptance

Before statement elaboration, an accountable source decision must select one truth-valued root and
record an immutable edition, exact definition/theorem/page locators, all incorporated definitions,
ordered binders, assumptions, conclusion, proof dependencies, errata/correction status, translation
decisions, and independent review. It must map every machine, probability, auxiliary-input,
simulator, view, indistinguishability, complexity, completeness, soundness, language, and boundary
choice into the Lean target. Until then `H5` applies to the literal unstable catalog wording, the
canonical statement and expression fingerprint remain null, and no proof credit is legal.
