# Source-statement crosswalk

## Repository records

`Docs/researches/math_theorems.md:11693-11698` supplies exactly the title `Singleton界`, Richard
Singleton, year 1964, the gloss `MDS码的界`, importance "high," and status `已验证`. Git
history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, theorem locator,
formula, alphabet, code definition, parameter ranges, proof, correction history, reviewer, or
formal artifact.

`Docs/researches/cs_theorems.md:615` separately repeats the title, author, year, importance, and
untrusted status with the gloss `MDS码的Singleton界`. Stage0 projects this row as
`THM-C-0371`, outside Stage1 rev-5.6. Its extra word `Singleton` does not select a mathematical
formula or resolve whether the target is a general bound or an MDS equality characterization.

`Docs/Stage0_Blueprint.md:43147-43172` repeats the mathematical gloss while explicitly leaving the
formal system, exact definitions and premises, proof history, dependencies, equivalent forms,
axioms, machine status, and artifact links open. Its generic claim that a closed result is known is
planning metadata, not source evidence. Rev-5.6 preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Catalog element | Necessary mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| `Singleton界` | one exact size/dimension-distance inequality | one exact `Prop` with checked transports | family only; variant open |
| "MDS code" | equality case of a selected Singleton inequality | a predicate defined from the selected code model and equality | definition and direction open |
| "bound" | size or dimension upper bound, with exact exponent/range | finite cardinalities, powers, and inequalities | formula absent |
| Richard Singleton / 1964 | historical source identity | immutable source ID and node provenance | bibliography identified; theorem text unavailable |
| `已验证` | untrusted inventory field | source proof and kernel receipt would be required | no H or M credit |

## Primary bibliographic identity

Crossref and DBLP identify Richard C. Singleton, *Maximum distance q-nary codes*, **IEEE
Transactions on Information Theory** 10(2), April 1964, pages 116-118, DOI
`10.1109/TIT.1964.1053661`; DBLP key `journals/tit/Singleton64`. Crossref supplies the title,
author, journal, volume, issue, date, pages, DOI, and publisher metadata. Unpaywall reports the work
closed with no open repository copy, and an IEEE download attempt did not yield the paper in this
worker environment.

This exact bibliography strongly identifies the published result family and supports provisional
H1 rather than H0. The repository does not cite the paper; its text was not inspected or preserved;
no theorem/page-level transcription, assumption and proof mapping, errata decision, or independent
source review exists. The paper title alone does not authorize importing the familiar modern
formula as though it were the received statement.

## Secondary scope discriminator

The Error Correction Zoo data repository at immutable revision
`1fcaa85f447bff9c77a6c33595ee4c72548d5d85`, file
`codes/classical/q-ary_digits/distributed_storage/mds.yml`, cites the Singleton DOI and says a
linear `[n,k,d]_q` code is MDS when `d <= n-k+1` is equality. It separately notes that a general
nonlinear or unrestricted q-ary bound can be formulated. The inspected file SHA-256 is recorded in
`instance.json` and the provisional receipt.

This is useful family-discrimination evidence, not primary proof evidence and not target
authority. It confirms why the catalog gloss is ambiguous between the general inequality, the
linear specialization, and equality defining MDS. It cannot close H0 or select the root.

## Candidate-root crosswalk

| Candidate root | Material content | Why not canonical at intake |
|---|---|---|
| unrestricted finite q-ary bound | a code of length `n`, size `M`, and minimum distance `d` satisfies a source-specific form of `M <= q^(n-d+1)` | alphabet, code object, distance convention, ranges, and subtraction are absent |
| linear specialization | an `[n,k,d]_q` linear code satisfies `d <= n-k+1` or `k <= n-d+1` | finite-field and dimension assumptions are absent from the catalog |
| MDS equality characterization | a selected linear code is MDS exactly when equality holds | this defines or characterizes MDS rather than merely stating the general bound |
| puncturing form | deleting `d-1` coordinates yields an injection into shorter words and hence a cardinality bound | deletion carrier, distance hypothesis, injection proof, and cardinal transport are not frozen |
| MDS existence/length claim | existence or maximum length of equality-achieving codes | a different theorem and potentially an open/conjectural family, not licensed by "bound" |

## Source gate

Before H0 or statement acceptance, accountable reviewers must obtain and preserve a lawful
immutable primary edition, identify the exact theorem/page and corrections, select one root,
transcribe every incorporated definition, ordered binder, hypothesis, conclusion, equality and
boundary convention, reconcile `THM-C-0371`, map all material premises and proof steps, and approve
the source-to-Lean crosswalk. Until then the canonical mathematical statement and formal expression
remain null.

## Lean discovery boundary

The pinned probe checks `hammingDist`, `hammingDist_eq_zero`,
`hammingDist_le_card_fintype`, `hammingDist_comp_le_hammingDist`, `Fintype.card_fun`,
`Fintype.card_le_of_injective`, `Fintype.card_congr`, and `Finite.of_injective`. These authenticate
useful Hamming, puncturing-adjacent, and finite-cardinality substrate, not a code object,
minimum-distance definition, puncturing theorem, Singleton bound, or MDS equality result. No
declaration or proof body is credited.
