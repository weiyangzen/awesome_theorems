# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:11644-11649` supplies exactly the title
`香农噪声信道编码定理`, Claude Shannon, 1948, the gloss `信道编码的存在性`, importance `high`, and
status `已验证`. Git history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:42958-42983` repeats the metadata while explicitly leaving the formal
system and foundation, precise definitions and premises, proof route, dependencies, equivalent
forms, axioms, machine status, and artifact links open. The rev-5.6 manifest preserves `已验证`
only as `source_status_untrusted` and resets the target to `L0 / rework_required`.

The repository record contains no channel or source definition, formula for capacity, code or
decoder, reliability criterion, binder, hypothesis, conclusion, bibliography, incorporated
definition, proof boundary, correction history, or reviewer. It therefore does not identify an
exact proposition.

## Inspected primary-source lead

Claude E. Shannon, *A Mathematical Theory of Communication*, *Bell System Technical Journal* 27
(1948), Part I, pages 379-423, DOI `10.1002/j.1538-7305.1948.tb01338.x`, and Part II, pages
623-656, DOI `10.1002/j.1538-7305.1948.tb00917.x`, is the exact author/year/result-family match.
The consolidated 55-page PDF retrieved on 2026-07-13 has SHA-256
`6e4e3411984f3edf99dbfe8b941cb5e8a321379ff0cae6ae5c1f592ad8882ca8`.

Section 5 says sources are assumed ergodic unless stated otherwise. Section 11 models the most
general noisy discrete channel considered there by finitely many states and probabilities of the
next state and received symbol conditional on current state and transmitted symbol; a one-state
channel with independently perturbed symbols is a special case. Section 12 defines information
rate as input entropy less equivocation and capacity as the maximum over possible input sources.

Section 13, Theorem 11 (consolidated pages 22-24) states that for a discrete channel of capacity
`C` and discrete source entropy rate `H`, if `H <= C` a coding system can make error frequency or
equivocation arbitrarily small; if `H > C`, equivocation can be made less than `H - C + epsilon`,
and no encoding makes it less than `H - C`. Its existence argument averages error over random
message-to-channel-input associations. Materially, the displayed proof later assumes a transmitted
rate `R < C`. Equality at capacity therefore cannot be silently preserved or changed without an
accountable source review.

The same section's Theorem 12 defines `N(T,q)` using equal-probability selected signals and
most-probable-cause decoding with error at most `q`, and asserts that
`log N(T,q) / T` tends to `C` for `q` neither zero nor one. It is a distinct operational
formulation, not an automatic restatement of whichever theorem the repository intends.

This inspection strongly identifies the family and exposes its choices. It does not authorize this
worker to select a root, clear `H0`, or assert that the historical argument already meets a modern
proof standard.

## Component crosswalk

| Repository element | Primary-source component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `香农噪声信道编码定理` | Section 13 fundamental theorem for a discrete channel with noise | one exact canonical `Prop` plus source-defined objects | strong family match; exact root open |
| `信道编码的存在性` | Theorem 11 random-coding existence below capacity | encoder/decoder existence with exact rate/error quantifiers | gloss omits channel, source, and reliability semantics |
| Claude Shannon / 1948 | two-part Bell System paper | immutable edition and source identity | bibliographic identity established; independent admission open |
| `已验证` | untrusted inventory label | reviewed human source and kernel receipt would be required | no H or M credit |

## Candidate-root crosswalk

| Candidate root | Material content | Why not canonical at intake |
|---|---|---|
| Shannon Theorem 11 in full | below-capacity coding existence plus above-capacity equivocation bound and converse for source/channel processes | broader than the catalog's existence gloss and needs the paper's full definitions |
| Theorem 11 direct clause | reliable transmission of a discrete source over a capacity-sufficient noisy channel | printed non-strict boundary conflicts with the proof's strict inequality and error/equivocation are alternatives |
| Shannon Theorem 12 | operational limit of reliably distinguishable signal-set cardinality | channel-only formulation with a fixed decoder/error convention rather than the stated source-coding existence |
| Modern finite-DMC achievability | finite alphabets, memoryless transition law, `R < C`, block encoder/decoder, vanishing average or maximal error | narrower channel class and modern definitions absent from the catalog and historical statement |
| Direct plus converse or separation package | reliable coding below capacity and impossibility above it, possibly with source coding | manufactures a conjunction and overlaps separately listed converse/joint-coding records |

## Repository boundary records

`Docs/researches/math_theorems.md:11623-11656` separately lists information theory, Shannon
entropy, channel capacity, this noisy-channel theorem, and the noiseless coding theorem. The target
must not absorb those separate roots merely because its proof depends on their definitions.

`Docs/researches/cs_theorems.md:599-605` separately lists a source coding theorem, channel coding
theorem, noisy-channel coding theorem, capacity converse, and joint source-channel coding. These
are Stage0 discovery records rather than rev-5.6 targets, but their separation confirms that
achievability, converse, and separation must not be merged by default.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`PMF`, `ProbabilityTheory.Kernel`, `IsMarkovKernel`, `Real.binEntropy`,
`InformationTheory.klDiv`, its composition-product chain rule,
`InformationTheory.UniquelyDecodable`, and `hammingDist`. A bounded exact-topic search found no
channel-capacity, mutual-information, noisy-channel, or channel-coding declaration in pinned
mathlib or repository-local Lean.

These are supporting interfaces only. The canonical module, declaration/expression, elaborated
expression hash, checked transports, and statement mutations remain null. The probe and search do
not constitute the exhaustive downstream candidate audit or proof of global absence.

## Source and statement gate

Before ordinary theorem-proof execution, accountable reviewers must select or correct one stable
truth-valued proposition, preserve an immutable primary or authoritative edition, transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, channel/source/code/error
convention, proof boundary, correction, and erratum, resolve the capacity-boundary discrepancy,
reconcile neighboring records, and independently approve the mapping. The statement phase must
then freeze minimal imports, the elaborated expression and environment fingerprint, checked
alternate transports, and removed-hypothesis, changed-domain, binder-scope, and boundary
mutations.

Until then, `H5` records that the received catalog wording is not one stable proposition. It does
not refute Shannon's theorem. The canonical mathematical and Lean targets remain null, and the
downstream anchor audit remains open.
