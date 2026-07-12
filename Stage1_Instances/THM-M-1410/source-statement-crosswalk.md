# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:10299` through `:10304` is the underlying catalog record. It gives the
title `Rokhlin塔` (`Rokhlin tower`), Vladimir Rokhlin, 1948, and only `遍历理论的工具`
(`an ergodic-theory tool`). It has no domain, quantifiers, hypotheses, conclusion, citation, proof,
or formal artifact. These six lines originate in the initial research-corpus commit and repository
history supplies no deeper version.

`Docs/Stage0_Blueprint.md:38348` through `:38373` repeats the gloss while explicitly leaving the exact
definitions and assumptions, proof route, dependency graph, equivalent formulations, axioms,
machine status, and artifact links open. The rev-5.6 manifest consequently retains `verified` only
as `source_status_untrusted` and starts this theorem at `L0 / rework_required`.

## Inspected discovery sources

Benjamin Weiss, *On the work of V. A. Rokhlin in ergodic theory*, *Ergodic Theory and Dynamical
Systems* **9** (1989), 619-627, DOI `10.1017/S0143385700005253`, was inspected from the publisher
PDF (SHA-256 `ce8ac1bfa65d4b6f924f09eee43246005cf5060a4138749500d6b87935350dcd`).
On p. 620 it formulates Rokhlin's lemma for an aperiodic invertible measurable transformation of
`[0,1]` preserving Lebesgue measure: for every natural height and positive error, a measurable base
has pairwise disjoint forward levels whose union has measure greater than `1 - epsilon`. It defines
aperiodicity as the periodic-point set having measure zero. On pp. 619-620 and in its bibliography,
it relates the lemma to Rokhlin's 1948 paper *A 'general' measure preserving transformation is not
mixing*, *Dokl. Akad. Nauk SSSR* **60**, 349-351, and explicitly says that the short note contains no
proof of the lemma.

S. Bezuglyi, A. H. Dooley, and K. Medynets, *The Rokhlin lemma for homeomorphisms of a Cantor set*,
arXiv:`math/0410505v2`, was inspected from the versioned PDF (SHA-256
`00ed936da36a28df9bf80e0b95fe6fa25b83b0cd4a13a2ff4c8ca8b17e293155`). Its introduction, p. 1,
describes the classical lemma instead for an aperiodic nonsingular automorphism of a standard
measure space, with height at least two. It cites V. A. Rokhlin, *Selected topics from the metric
theory of dynamical systems*, *Uspehi Matem. Nauk* **4** (1949), no. 2, 57-128. Publisher metadata
locates the English translation as AMS Translations Series 2 (1966), pp. 171-240, DOI
`10.1090/trans2/049/09`. That metadata was inspected through the Crossref work record at
`https://api.crossref.org/works/10.1090/trans2/049/09` on 2026-07-12; the response SHA-256 was
`dab32d70b6087fdede3f4bf52c1b6ebaf05b9554c6488ad34a3844ec9ef0269b`.

These inspected sources establish a serious candidate family and the 1948/1949 bibliographic
boundary. They do not make either formulation canonical: neither candidate primary passage was
inspected and accepted, the nonsingular and measure-preserving assumptions differ, no errata or
translation audit was performed, and no independent reviewer approved a mapping. They are
discovery evidence, not `H0` evidence.

## Crosswalk

| Repository or source element | Mathematical component that must be selected | Required Lean component | Intake assessment |
|---|---|---|---|
| `Rokhlin塔` (`Rokhlin tower`) | a finite orbit tower over a measurable base | base set and indexed iterates/images or preimages | theorem family identified; encoding open |
| `遍历理论的工具` (`an ergodic-theory tool`) | no proposition | none can be elaborated from a use-description | explicitly insufficient |
| Vladimir Rokhlin / 1948 | historical locator | documentation and source review only | likely 1948 short note; primary passage not inspected |
| aperiodic | periodic points form a null set, or another source-exact freeness condition | `Function.periodicPts`, measure-zero predicate, and measurability/null-measurability obligations | variants identified; definition open |
| invertible measurable transformation | automorphism of the chosen measure space | measurable equivalence or function plus inverse laws | representation open |
| measure-preserving / nonsingular | exact relationship between transformation and measure | `MeasurePreserving`, `Measure.QuasiMeasurePreserving`, or another checked structure | inspected sources disagree; source choice required |
| standard probability space / `[0,1]` | domain, sigma algebra, measure, atomlessness, normalization | `StandardBorelSpace`, measure typeclasses, or a concrete unit interval | domain open |
| tower height | natural `n`, usually with `n >= 2` in one source | ordered binder and finite index type/range | lower bound and indexing open |
| disjoint levels | literal or modulo-null pairwise disjointness | `Pairwise (Disjoint on ...)` or `Pairwise (AEDisjoint mu on ...)` | relationship must be checked, not normalized textually |
| coverage | union measure greater than `1 - epsilon` | finite union and exact `ENNReal`/real comparison | codomain, normalization, and boundary cases open |
| `已验证` (`verified`) | untrusted catalog status | no statement or proof credit | explicitly rejected as evidence |

## Pinned Lean boundary

A scoped repository and pinned-mathlib search found no declaration named for Rokhlin/Rohlin or a
Rokhlin tower. Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` does provide
adjacent infrastructure: `MeasureTheory.MeasurePreserving` and its iterate theorem,
`Function.periodicPts`, `Ergodic`, `StandardBorelSpace`, `IsProbabilityMeasure`, `NoAtoms`, and
`MeasureTheory.AEDisjoint`. `IntakeProbe.lean` checks those names at the pin, including
`MeasureTheory.Measure.QuasiMeasurePreserving` for the nonsingular candidate vocabulary.

This bounded check is feasibility evidence only. It is not the later immutable anchor audit and
does not establish an aperiodicity measurability theorem, an image/preimage transport, a tower
construction, source identity, or proof closure. The machine classification therefore remains
`M4` for the unselected canonical root.

## First downstream blocker

Select and independently review one immutable primary theorem passage. Reconcile the 1948 and 1949
locators, then transcribe every space assumption, transformation property, aperiodicity convention,
binder, disjointness condition, coverage inequality, and boundary case. Only after that review may
the statement phase choose minimal imports, elaborate and hash the exact expression, check alternate
encodings, and run statement mutations.
