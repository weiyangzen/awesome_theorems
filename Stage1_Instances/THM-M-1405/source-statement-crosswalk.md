# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records `Sinai定理`, attributes it to Yakov Sinai, dates it to
1959, and gives only `测度熵的生成子` (approximately "a generator for measure-theoretic entropy").
`Docs/Stage0_Blueprint.md` repeats those fields while leaving exact definitions, premises, proof
route, equivalent statements, axioms, and formal artifacts open. The rev-5.6 manifest retains
`已验证` only as `source_status_untrusted`. These records identify a theorem family, not an exact
proposition.

## Source candidates

The historical primary-source candidate is Ya. G. Sinai, *On the Notion of Entropy of a Dynamical
System*, *Dokl. Akad. Nauk SSSR* 124(4) (1959), 768-771. A later candidate reprint is the chapter
of the same English title in *Selecta* (2010), pages 3-10, DOI
`10.1007/978-0-387-87870-6_1`. Intake has not accepted an immutable scan, the original Russian
wording, a translation relationship, an exact theorem passage, assumptions, corrections, or
errata. Both citations are discovery locators, not `H0` receipts.

Yakov Sinai's author-written Scholarpedia article *Kolmogorov-Sinai entropy*, 4(3):2034 (2009),
DOI `10.4249/scholarpedia.2034`, gives a precise secondary anchor at fixed revision `91407`
(`http://www.scholarpedia.org/w/index.php?title=Kolmogorov-Sinai_entropy&oldid=91407`). Its
Definition 2 calls a finite partition generating when the smallest sigma-algebra containing all
integer translates of its atoms is the ambient sigma-algebra. Its Theorem 1 states that a
generating partition satisfies `h(T) = h(T, xi)` and attributes the general proof to the 1959
source. This makes the generator equality the leading interpretation, but a secondary statement
does not settle the exact 1959 scope or provide the required source review.

## Component crosswalk

| Repository/source component | Candidate mathematical object | Required Lean surface | Intake status |
|---|---|---|---|
| "measure entropy" | Kolmogorov-Sinai entropy of a probability-preserving transformation | a source-matched partition entropy and system entropy API | likely meaning; exact definition and codomain open |
| "generator" | a measurable partition whose orbit generates the ambient sigma-algebra | partition atoms, iterated preimages/translates, generated measurable space, completion/mod-null relation | likely meaning; finite/countable and null conventions open |
| dynamical system | probability space with a measure-preserving transformation | `Measure`, `IsProbabilityMeasure`, `MeasurePreserving`, and possibly a measurable equivalence | adjacent pinned APIs exist; exact system class open |
| `h(T, xi)` | entropy rate of iterated partition joins | joins/refinements, Shannon entropy, limit or infimum characterization | no target-specific pinned API located during intake |
| `h(T)` | supremum over the source's permitted partitions | extended-real supremum under one normalization | no target-specific pinned API located during intake |
| generator theorem | `h(T) = h(T, xi)` for a generating `xi` | exact typed equality plus checked transports for alternate encodings | leading candidate only; no canonical expression |
| `已验证` | untrusted catalogue status | no proposition or declaration | explicitly rejected as evidence |

## Human-source boundary

The provisional human status is `H1`, not `H0`: a named published proof source and a precise
author-written statement candidate exist, but the exact primary text and its premise-by-premise
mapping have not been audited. Before `H0`, an independent reviewer must inspect and hash an
immutable edition, identify the exact statement and definitions, map every system/partition/null
set/entropy convention and boundary case, check translation fidelity and errata, and approve the
source-to-Lean crosswalk.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks only adjacent definitions for measure preservation, ergodicity, probability measures,
generated measurable spaces, and finite partitions. A bounded theorem-name search found no
Sinai, Kolmogorov-Sinai, measure-theoretic-entropy, or generating-partition declaration. That
bounded result is intake evidence only, not the required immutable anchor audit and not proof that
no differently named formalization exists.
