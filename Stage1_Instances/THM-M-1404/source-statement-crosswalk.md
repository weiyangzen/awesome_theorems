# Source-statement crosswalk

## Repository source record

The source catalog at `Docs/researches/math_theorems.md:10257` records only the name `测度熵`, the
attribution Andrey Kolmogorov, the year 1958, and the phrase `保测动力系统的熵`. The generated
Stage0 entry at `Docs/Stage0_Blueprint.md:38186` repeats those fields while explicitly leaving the
exact definitions, premises, proof path, axioms, and machine artifact open. The rev-5.6 manifest
records rank 903, baseline `L0 / rework_required`, no legacy slot, and treats `已验证` as
`source_status_untrusted`.

The entry therefore identifies a topic but not a proposition. No repository source supplies an
edition, theorem or definition number, page, exact assumptions, conclusion, errata, translation,
or proof artifact.

## Bibliographic discovery candidates

- A. N. Kolmogorov, "A new metric invariant of transient dynamical systems and automorphisms in
  Lebesgue spaces," *Doklady Akademii Nauk SSSR* 119(5) (1958), 861-864, in Russian. This quotes
  Math-Net's English archive title; later English references commonly use "transitive". Stable record:
  `https://www.mathnet.ru/eng/dan22922`; MR0103254; zbMATH 0083.10602.
- A. N. Kolmogorov, "On entropy per unit time as a metric invariant of automorphisms," *Doklady
  Akademii Nauk SSSR* 124(4) (1959), 754-755, in Russian.
- Ya. G. Sinai, "On the notion of entropy of dynamical systems," *Doklady Akademii Nauk SSSR*
  124(4) (1959), 768-771, in Russian.

The 1958 Math-Net record and four-page Russian scan were inspected during intake. The reproducible
retrieval and digest checks are recorded in `validation.md`; the PDF digest is
`abf376fa2e2aefaf1492308a8808d79be3431dae4c821ca546719f35a1d4bf85`. Direct visual inspection
confirms sections 1-4 and numbered Theorems 1-4. The scan visibly introduces `h` in section 2 and
`h(T)` in section 3. Any more specific translation of the theorem statements is deliberately left
open. This primary artifact narrows the historical source family but still does not tell us which
definition or theorem the catalog scheduled as its root. A Russian-language source review, exact
premise and formula transcription, translation review, errata search, and independent approval
remain open.

The 1959 locators were cross-checked through secondary bibliographic indexes only. All three remain
discovery inputs rather than `H0` records for this unselected root. The Encyclopedia of Mathematics
entry also warns that the modern finite-partition presentation is not literally Kolmogorov's
original definition, so any equivalence transport must be source-controlled and checked.

## Claim crosswalk

| Source component | Mathematical information fixed | Prospective Lean surface | Intake result |
|---|---|---|---|
| Name `测度熵` | a measure-theoretic entropy invariant is intended | a future definition plus a selected theorem about it | invariant family only; no proposition |
| `保测动力系统` | some measure-preserving dynamical system | `Measure`, `MeasurableSpace`, `MeasurePreserving`, and a typed self-map | measure class, invertibility, and mod-null conventions absent |
| `熵` | information growth under dynamics | finite measurable partitions, joins of inverse images, `-p log p`, asymptotic rate, and supremum | construction family only; codomain and normalizations absent |
| Kolmogorov / 1958 | historical source family | documentation and source provenance | does not identify which 1958 definition or a theorem conclusion |
| `已验证` | untrusted catalog metadata | inspectable declaration, proof body, and receipt would be required | no source or machine credit |
| Adjacent Sinai/KS entries | the catalog distinguishes related entropy records | separate theorem IDs and checked transports if later related | cannot be folded into this root at intake |

## Lean discovery boundary

The pinned intake probe checks that Lean 4.29.0 with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` exposes measure-preserving maps, ergodicity,
probability-measure structure, finite partitions of measurable sets, iterates, and the scalar
function `Real.negMulLog`. These are ingredients only. The probe defines no entropy object and
asserts no theorem.

A bounded source-name search under pinned `Mathlib/Dynamics` and `Mathlib/MeasureTheory` found no
declaration matching measure-theoretic entropy, Kolmogorov-Sinai entropy, or partition entropy.
Mathlib's topological-entropy modules are a different invariant. This is a narrow intake search,
not a saturated anchor audit and not proof of global absence.

Before statement acceptance, a source reviewer must select one primary passage, record a stable
edition and content digest, transcribe every ordered assumption and conclusion, resolve translation
and correction history, and approve a row-by-row mapping to one elaborated Lean expression.

## Intake classification

The current catalog wording is classified provisionally as `H5`: it is an invariant/topic label,
not a stable truth-valued proposition. This is a target-correction status, not a claim that any
particular entropy theorem is false or mathematically open. Once an exact primary-source proposition
is selected, its human-proof status must be reassessed independently rather than inherited from
this intake classification.
