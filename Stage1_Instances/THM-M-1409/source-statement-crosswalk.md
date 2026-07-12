# Source-statement crosswalk

## Authoritative repository record

`Docs/researches/math_theorems.md:10292`-`:10297`, introduced by commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`, is the complete research-corpus record. It gives:

- title: `Kakutani塔`;
- proposer: Shizuo Kakutani;
- date: 1943;
- statement: `诱导变换的构造` ("construction of an induced transformation");
- importance: high;
- formalization status: `已验证`.

`Docs/Stage0_Blueprint.md:38321`-`:38346` repeats the metadata and explicitly leaves precise
definitions and premises, proof path, equivalent formulations, axioms, machine status, and artifact
links open. The rev-5.6 manifest carries `已验证` only as `source_status_untrusted` and resets the
target to `L0 / rework_required`. These are secondary inventory records, not a theorem statement,
primary proof source, or kernel receipt.

## Bibliographic candidate

The attribution and year align with Shizuo Kakutani, "131. Induced Measure Preserving
Transformations," *Proceedings of the Imperial Academy* **19**(10) (1943), 635-641, DOI
`10.3792/pia/1195573248`. The J-STAGE article metadata identifies the author, title, year, volume,
issue, page range, and DOI. Its seven-page primary PDF (717145 bytes) had SHA-256
`054e0d2296324bec6f0b319bcb9aea5044a72b941f3dd83b75b788968320b16b` when inspected on
2026-07-12. Stable retrieval locators used for this discovery check were:

- article metadata: `https://www.jstage.jst.go.jp/article/pjab1912/19/10/19_10_635/_article/-char/en`;
- primary PDF: `https://www.jstage.jst.go.jp/article/pjab1912/19/10/19_10_635/_pdf/-char/en`.

Section 3, pp. 636-637, is a strong candidate for the catalog gloss. Given an ergodic
measure-preserving transformation in Kakutani's "strong sense" and a measurable subset of positive
measure, Lemma 1 removes a null subset and gives infinitely many positive and negative returns.
For each remaining point it then chooses the least positive return time and defines the induced
map by that iterate. Lemma 2 says the resulting map is an ergodic measure-preserving transformation
in the strong sense of the induced measure space onto itself. A footnote says the starting
transformation need not be assumed ergodic when the ambient total measure is finite. The following
paragraph passes from the strong representative to the weak-sense induced transformation on the
original subset.

The source fixes more context than the catalog gloss: Section 2 requires positive total measure
and a countable cover by finite-measure measurable sets when the total measure is infinite. Its
induced measure is the unnormalized restriction to the subset. A "strong" m.p.t. is a bijection
onto the target space for which images and inverse images of measurable sets are measurable and
measure preserving; it must not be translated as only mathlib's one-way `MeasurePreserving`
predicate. The paper itself calls the object an induced transformation, not a tower or skyscraper.

Section 1 also says the note gives only definitions and fundamental results and leaves detailed
discussion to another occasion; the inspected Lemmas 1-2 are stated without proofs. Thus this PDF
is strong statement/provenance evidence but is not, by itself, a complete human-proof source. The
finite-total-measure footnote also needs careful review: it removes the starting ergodicity
assumption at the recurrence setup, but must not be read as proving that an induced map of every
nonergodic finite measure-preserving automorphism is ergodic.

This inspection resolves the likely source family, but it is not an accepted `H0` crosswalk. An
independent reviewer has not decided whether the target is Lemma 1 plus the definition, Lemma 2,
the weak-sense consequence, or a combined construction theorem; nor have the paper's strong/weak
definitions, sigma-algebra restrictions, null-set representative, finite-measure footnote, full
proof boundary, and errata been formally mapped. The intake therefore keeps the canonical claim
open rather than silently choosing one of these materially different scopes.

## Crosswalk

| Repository element | Possible source component | Required Lean component | Intake result |
|---|---|---|---|
| `Kakutani塔` | first-return tower, skyscraper, or representation family | one exact proposition or construction interface | topic identified; theorem absent |
| Shizuo Kakutani; 1943 | Section 3, pp. 636-637 of the located primary paper | pinned source snapshot and reviewed passage | primary PDF inspected; independent review open |
| "induced transformation" | first-return map on a measurable base | space/measure, `T`, base `A`, return-time function, iterate | all binders and conventions open |
| "construction" | Lemma 1 return existence, least-positive-return definition, Lemma 2 preservation/ergodicity, or their weak-sense consequence | exact output and laws, not assumed structure fields | likely source nodes found; root selection open |
| return | pointwise or almost-everywhere recurrence | finite-return domain and exceptional-set convention | open |
| tower | orbit levels over the base | level sets, disjointness, carrier, and coverage theorem | open |
| measure preservation | strong-sense automorphism assumption and conclusion in the source candidate | bijective/bimeasurable measure equivalence on the unnormalized restricted measure, not merely `MeasurePreserving` | source-specific facts located; root acceptance open |
| `已验证` | untrusted inventory classification | accepted source review or kernel evidence | explicitly rejected as credit |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded search over
`Mathlib/Dynamics` and `Mathlib/MeasureTheory` found no `Kakutani`, ergodic `firstReturn`, or
`induced transformation` declaration. It did find adjacent infrastructure:

- `MeasureTheory.MeasurePreserving` and `.iterate` express preservation by a self-map and its
  iterates.
- `MeasureTheory.MeasurePreserving.conservative` derives conservativity for a finite
  measure-preserving system.
- `MeasureTheory.Conservative.ae_mem_imp_frequently_image_mem` states almost-everywhere repeated
  return to a null-measurable set.
- `MeasureTheory.Conservative.inter_frequently_image_mem_ae_eq` identifies the recurrent part of a
  set modulo null sets.
- `MeasureTheory.Conservative.measure_inter_frequently_image_mem_eq` records equality of its
  measure with the base measure.

`IntakeProbe.lean` checks these exact pinned interfaces. They are recurrence ingredients, not an
induced map, first-return-time definition, tower construction, or exact source anchor. Mathlib also
contains `PFun.fix`, documented as a first-return operator for a generic partial function
`alpha ->. beta Sum alpha`; its type is not a measure-theoretic Kakutani-tower target and it is
explicitly excluded from root credit.

## First downstream blocker

Archive the lawfully retrieved primary PDF with its recorded digest and have an independent
reviewer select and transcribe one exact proposition or construction with page/theorem locator,
ordered assumptions, conclusion, conventions, proof boundary, and errata; alternatively obtain an
authoritative source correction if the catalog intended a different result. Only then may the
statement task choose minimal imports, elaborate and fingerprint a canonical Lean expression,
check transports, and perform the required domain/hypothesis/scope/boundary mutation tests.
