# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:11651-11656` supplies exactly the title
`香农无噪声编码定理`, Claude Shannon, 1948, the gloss `数据压缩的极限`, importance `high`, and
status `已验证`. Git history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:42985-43010` repeats the metadata while explicitly leaving the formal
system and foundation, precise definitions and premises, proof route, dependencies, equivalent
forms, axioms, machine status, and artifact links open. The rev-5.6 manifest preserves `已验证`
only as `source_status_untrusted` and resets the target to `L0 / rework_required`.

The repository record contains no source or channel definition, entropy formula, code class,
encoder or decoder, length or rate criterion, binder, hypothesis, conclusion, bibliography,
incorporated definition, proof boundary, correction history, or reviewer. It therefore does not
identify an exact proposition.

## Inspected primary-source lead

Claude E. Shannon, *A Mathematical Theory of Communication*, *Bell System Technical Journal* 27
(1948), Part I, pages 379-423, DOI `10.1002/j.1538-7305.1948.tb01338.x`, and Part II, pages
623-656, DOI `10.1002/j.1538-7305.1948.tb00917.x`, is the exact author/year/result-family match.
The consolidated 55-page PDF inspected on 2026-07-13 has SHA-256
`6e4e3411984f3edf99dbfe8b941cb5e8a321379ff0cae6ae5c1f592ad8882ca8`.

Part I, Section 9, `The Fundamental Theorem for a Noiseless Channel`, Theorem 9 (consolidated
PDF page 16) says: for a source with entropy `H` bits per symbol and a channel with capacity `C`
bits per second, the source can be encoded for average transmission rate `C / H - epsilon` source
symbols per second for arbitrarily small epsilon, and no average rate greater than `C / H` is
possible. The converse uses nonsingularity of the transmitter and the capacity bound on channel
input entropy. The direct proof uses long source sequences and then gives a second arithmetic/Fano
style construction.

The statement incorporates earlier paper context. Sections 2-4 define discrete sources, entropy,
ergodic finite-state sources, and entropy rate. Sections 1, 7, and 8 define discrete noiseless
channels with symbol constraints or durations and capacity as asymptotic signal-count growth.
Sections 9-10 discuss transducer matching, average rate, arbitrarily close efficiency, and delay.
Those definitions and assumptions cannot be silently replaced by a modern finite iid prefix-code
model.

This inspection identifies a strong source candidate and justifies provisional `H1`. It does not
show that the catalog intended this exact historical proposition, provide an independent source
review, or authorize `H0`.

## Component crosswalk

| Repository element | Primary-source component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `香农无噪声编码定理` | Part I, Section 9 fundamental theorem | one source-reviewed canonical `Prop` | strong family match; exact root open |
| `数据压缩的极限` | entropy determines the capacity needed by efficient coding | source/process, entropy, code/channel, rate and converse | gloss omits all operative semantics |
| Claude Shannon / 1948 | two-part Bell System paper | immutable edition and source identity | bibliographic identity established; independent admission open |
| `已验证` | untrusted inventory label | reviewed source and kernel receipts would be required | no H0 or M credit |

## Candidate-root crosswalk

| Candidate root | Material content | Why not canonical at intake |
|---|---|---|
| Shannon Theorem 9 | asymptotically optimal matching of an ergodic source to a constrained noiseless channel, direct and converse | requires the paper's source, channel, duration, transducer, entropy-rate, and nonsingularity model |
| Expected-length inequality | finite distribution and `D`-ary prefix or uniquely decodable code with entropy lower bound and usually a `< H + 1` construction | narrower modern objects; may package converse and construction differently |
| Lossless block source coding | asymptotic rate threshold at entropy for iid or stationary ergodic sources | source class, fixed/variable length, exact lossless policy, and quantifiers are absent |
| Typical-set almost-lossless coding | rates above entropy admit vanishing error and rates below entropy do not | introduces an error criterion absent from the title and gloss |

## Repository boundary records

`Docs/researches/math_theorems.md:11623-11656` separately lists information theory, Shannon
entropy, channel capacity, noisy-channel coding, and this noiseless theorem. The target must not
absorb those roots merely because the historical statement depends on entropy and capacity.

`Docs/researches/cs_theorems.md:599` separately lists a source coding theorem with gloss
`无损压缩的熵下界`. It is a Stage0 discovery record outside the 1546-ID target set. Its wording
is useful for duplicate-boundary review but supplies no accepted statement or proof credit.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`PMF`, `Real.binEntropy`, `Real.qaryEntropy`, `InformationTheory.UniquelyDecodable`, its basic
consequences, and `InformationTheory.kraft_mcmillan_inequality`. The latter proves that a finite
uniquely decodable code over a finite nonempty alphabet has Kraft sum at most one.

A bounded exact-topic search found no source-entropy, expected-code-length, source-coding,
noiseless-channel, or Shannon-noiseless theorem declaration in pinned mathlib or repository-local
Lean. Kraft-McMillan is a possible converse ingredient only. The canonical module, declaration or
expression, elaborated-expression hash, checked transports, and statement mutations remain null.
The probe and search are not the exhaustive downstream candidate audit or a proof of global absence.

## Source and statement gate

Before ordinary theorem-proof execution, accountable reviewers must select or correct one stable
truth-valued proposition, preserve and hash an immutable primary or authoritative edition,
transcribe every incorporated definition, ordered binder, hypothesis, conclusion, source and code
model, rate or length convention, direct/converse boundary, proof boundary, correction and erratum,
reconcile the Stage0 source-coding record and neighboring targets, and independently approve the
mapping. The statement phase must then freeze minimal imports, the elaborated expression and
environment fingerprint, checked alternate transports, and removed-hypothesis, changed-domain,
binder-scope, and boundary mutations.

Until then, `H1` records a pinpoint primary-source candidate without an accepted exact mapping.
The canonical mathematical and Lean targets remain null, and the downstream anchor audit remains
open.
