# THM-M-0483 source-statement crosswalk

## Repository source

The target originates in `Docs/researches/math_theorems.md`, lines 3546-3551, introduced at commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The generated Stage0 entry repeats it and explicitly
leaves exact definitions, premises, proof route, equivalent forms, axioms, and machine artifacts
unfilled. The source-status field `已验证` is untrusted metadata, not human-source or machine-proof
evidence.

| Claim component | Supplied repository wording | Immutable candidate or formal cross-reference | Intake assessment |
|---|---|---|---|
| Name | `梅森素数判定` | "Mersenne primality determination/test" | Names a theorem family, not a unique proposition |
| Attribution | Edouard Lucas | Lucas is associated with the historical Mersenne-prime result and Lucas tests | Bibliographic lead only; no work, edition, page, or theorem is cited |
| Date | 1876 | Pinned mathlib archive labels `(mersenne 127).Prime` as `Edouard Lucas (1876)` | Strong disambiguation evidence, but not primary-source acceptance |
| Root wording | `梅森数的素性检验` | Concrete-prime result, historical Lucas criterion, necessary exponent property, and modern Lucas-Lehmer correctness are all plausible | Exact claim remains unresolved |
| Mersenne definition | absent | Pinned `mersenne p := 2 ^ p - 1` | Discovery candidate; natural subtraction and boundary behavior require source approval |
| Quantifiers and domains | absent | Candidates use either fixed `127` or `p : Nat` | Cannot be inferred from the title or year |
| Hypotheses | absent | Modern directions require `1 < p` or `3 <= p`; exponent-prime variants add another premise | No hypothesis may be silently added or removed |
| Conclusion | "primality testing" only | Primality of one number, primality implication, recurrence correctness, or algorithmic decision | Exact conclusion remains unresolved |
| Proof or algorithm | absent | Pinned recurrence definitions and correctness directions | Exact-topic formal anchors, not accepted mapping or proof credit |
| Formalization status | `已验证` | No target-owned legacy file or accepted receipt | Explicitly untrusted under rev-5.6 |

## Human-source candidates

| Source candidate | Version and locator | Material premise/conclusion mapping | Corrections, dependencies, and review | Status |
|---|---|---|---|---|
| An immutable 1876 publication by Edouard Lucas concerning large prime numbers and Mersenne numbers | Exact title, edition/scan, archival identifier, section, and page not yet admitted | Open: must determine whether the result is specifically primality of `2^127 - 1`, a general criterion, or both; must map every definition and premise | Errata/corrections, dependent results, translation, and independent specialist review all open | `H1` source lead only; no `H0` claim |
| Pinned mathlib archive example | `Archive/Examples/MersennePrimes.lean`, immutable mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, lines 64-66 | Labels and checks `(mersenne 127).Prime`; corroborates the year association | Modern formal secondary/discovery artifact, not a primary historical statement or independent source review | `E3/E5` discovery evidence only |
| Pinned mathlib Lucas-Lehmer module | `Mathlib/NumberTheory/LucasLehmer.lean` at the same revision | Defines `mersenne`, residue, and test; sufficiency uses `1 < p`; necessity uses `3 <= p` | Formal provenance, exact target mapping, and cross-target ownership remain unaudited | `E3` exact-topic formal anchor only |

No source row supplies the rev-5.6 `H0` contract: edition/version, stable identifier, exact theorem or
page locator, incorporated definitions, material-premise and conclusion crosswalk, dependent-source
IDs, correction/errata status, and an independent reviewer are still missing.

## Formal candidate crosswalk

| Pinned declaration | Exact role | Relationship to received claim | Credit boundary |
|---|---|---|---|
| `mersenne` | Defines natural Mersenne numbers as `2 ^ p - 1` | Possible notation for every candidate | Definition only; source mapping and boundary cases open |
| `Nat.Prime.of_mersenne` | `(mersenne p).Prime -> Nat.Prime p` | Necessary exponent criterion | Does not determine primality or implement a full test |
| `LucasLehmer.LucasLehmerTest` | Residue-zero predicate | Candidate test predicate | Likely overlaps `THM-M-0484`; definition alone proves nothing |
| `LucasLehmer.lucasLehmerResidue` | Recurrence residue in `ZMod (2 ^ p - 1)` | Candidate computational encoding | Indexing and source relationship unreviewed |
| `lucas_lehmer_sufficiency` | `1 < p -> LucasLehmerTest p -> (mersenne p).Prime` | One correctness direction | No exact target mapping, terminal provenance audit, or receipt |
| `lucas_lehmer_necessity` | `3 <= p -> (mersenne p).Prime -> LucasLehmerTest p` | Converse correctness direction | Lower bound differs; no unqualified iff and no target ownership decision |

`IntakeProbe.lean` elaborates these names and prints their immediate axiom reports in the pinned
environment. This establishes API availability only. It neither chooses a canonical expression nor
inspects the full proof-body, dependency, placeholder, computation, or trust closure.

## Required resolution

The statement gate can reopen after an independent reviewer admits an immutable exact primary or
approved authoritative source, fixes a stable locator and definition chain, maps every premise and
conclusion, audits corrections, and reconciles the boundary with `THM-M-0484`. The selected claim
must then be elaborated with exact binders and boundary cases and compared with each credited formal
candidate through checked transports. Until then the canonical formal target and fingerprints stay
null, and source, statement, tree, proof, and completion credit remain open.
