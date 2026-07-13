# Source-statement crosswalk

## Repository records

`Docs/researches/math_theorems.md:11749-11754` supplies exactly the title `Polar码`, attribution
Erdal Arikan, year 2009, gloss `达到香农限的码`, importance "high," and status `已验证`. Git
history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, channel definition,
formula, theorem locator, code or decoder, quantifier, premise, conclusion, proof boundary,
correction history, reviewer, or formal artifact.

`Docs/researches/cs_theorems.md:635` independently names Arikan's 2009 polar codes and says
`达到容量的Polar码`, but marks them `可验证`. Stage0 projects this row as `THM-C-0386`, outside
Stage1 rev-5.6. It is a useful duplicate-family boundary, not authority to broaden or select the
mathematical root.

`Docs/Stage0_Blueprint.md:43363-43388` repeats the mathematical gloss while explicitly leaving the
formal system, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. Rev-5.6 preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Catalog element | Necessary mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| `Polar码` | one exact construction and performance theorem | one canonical `Prop` plus checked transports | theorem family only |
| "achieves the Shannon limit" | capacity notion, channel class, rate and reliability limit | definitions plus ordered asymptotic binders | all conventions open |
| Erdal Arikan / 2009 | one edition and pinpoint theorem | source ID and node-level provenance | primary paper identified |
| `已验证` | accepted source proof and kernel receipt would be required | separate H and M evidence | no proof credit |

## Inspected primary-source lead

Erdal Arikan, *Channel Polarization: A Method for Constructing Capacity-Achieving Codes for
Symmetric Binary-Input Memoryless Channels*, *IEEE Transactions on Information Theory* 55(7),
July 2009, pages 3051-3073, DOI `10.1109/TIT.2009.2021379`, is the exact author/year/result-family
match. The inspected author-posted arXiv version is `arXiv:0807.3917v5`, dated 20 July 2009; its
metadata says it is the version appearing in the journal. The retrieved 23-page PDF has SHA-256
`36046a14f967b7b8be88a9e7beb4dd1de475a1d689b97dc43a05a3279e1c2f4d`; its layout-text extract
has SHA-256 `9339998e57f042c20c29b6a7b494ba25e88cdc2113fa33b49216e1c8b1163d8d`.

Section I distinguishes five candidate roots. Theorem 1 states channel polarization: for any
B-DMC and fixed `delta` in `(0,1)`, the fractions of synthesized channels with symmetric capacity
near one and near zero converge to `I(W)` and `1-I(W)`. Theorem 2 supplies large information sets
below `I(W)` with Bhattacharyya parameters bounded by `O(N^(-5/4))`. Theorem 3 derives
`P_e(N,R) = O(N^(-1/4))` for fixed `R < I(W)`, where error is averaged over frozen-bit choices.
Theorem 4 gives the corresponding arbitrary-fixed-frozen-vector result for symmetric B-DMCs and
notes that `I(W)` then equals Shannon capacity. Theorem 5 separately establishes `O(N log N)`
encoding and successive-cancellation decoding complexity for `G_N` coset codes.

This source inspection strongly identifies the intended family and supports provisional H1. It
does not establish H0: the repository does not cite or select a theorem, the journal/arXiv identity
and any corrections need accountable review, every incorporated definition and assumption must be
mapped, and no independent source reviewer has approved a canonical root.

## Candidate-root crosswalk

| Candidate root | Relation to catalog gloss | Why not canonical at intake |
|---|---|---|
| Theorem 1 | mechanism behind capacity-achieving codes | proves polarization, not directly a code-error statement |
| Theorem 2 | supplies reliable synthesized channels below symmetric capacity | information-set existence and Bhattacharyya bound, not the complete code theorem |
| Theorem 3 | directly states vanishing block error for polar coding | works for a B-DMC but averages over frozen vectors and targets symmetric capacity |
| Theorem 4 | directly reaches Shannon capacity for symmetric B-DMCs | narrower channel class and fixed-frozen-vector semantics absent from catalog |
| Theorem 5 | supplies low encoder/decoder complexity | no capacity or reliability conclusion and no general low-cost construction claim |
| later refinements | may strengthen exponent, kernel, alphabet, or decoder | later mathematics not identified by the 2009 catalog record |

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe
checks `PMF`, `PMF.bernoulli`, `ProbabilityTheory.Kernel`, `IsMarkovKernel`,
`Kernel.deterministic`, `Real.binEntropy`, `hammingDist`, `Matrix`, `Matrix.kronecker`, and
`Matrix.kroneckerPower`. These are adjacent interfaces only. They do not define mutual information,
symmetric channel capacity, synthesized bit-channels, the Arikan transform, information/frozen
sets, successive-cancellation decoding, or a polar-code error theorem.

A bounded case-insensitive search of pinned mathlib and repository-local Lean found no exact polar-
code or channel-polarization declaration. It also found no mutual-information or channel-capacity
API. No declaration or proof body is credited, and the exhaustive external anchor audit remains a
downstream task.

## Source and statement gate

Before H0 or statement acceptance, accountable reviewers must preserve a lawful immutable source,
select one exact theorem or approved composition, transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, channel/capacity/code/decoder/error convention, proof
boundary, correction and erratum, reconcile `THM-C-0386` and neighboring targets, and approve the
source-to-Lean mapping. The statement phase must then freeze minimal imports, the elaborated
expression and environment fingerprint, checked alternate transports, and all required statement
mutations. Until then the canonical mathematical and Lean targets remain null.
