# Source-statement crosswalk

## Repository records

`Docs/researches/math_theorems.md:11721-11726` supplies exactly the title `BCH码`, attribution
`Bose/Chaudhuri/Hocquenghem`, year 1959, gloss `能纠正多个错误的码`, importance "high," and status
`已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, theorem locator,
formula, definitions, binders, hypotheses, correction history, proof boundary, reviewer, or formal
artifact.

`Docs/Stage0_Blueprint.md:43255-43280` repeats the gloss while explicitly leaving the exact
definitions and premises, proof process, dependencies, alternate forms, axioms, machine status,
and artifact links open. The rev-5.6 target manifest keeps `已验证` only as untrusted metadata and
resets the target to `L0 / rework_required`.

`Docs/researches/cs_theorems.md:627-631` has a parallel BCH row attributed to Bose,
Ray-Chaudhuri, and Hocquenghem in 1959-60 with the gloss `循环纠错码`. Its Stage0 projection is
THM-C-0382. That item is outside the rev-5.6 target manifest, so it is useful only for duplicate and
scope discovery; it cannot choose this target's theorem or supply evidence.

## Inspected 1959 primary report

The NCSU Libraries repository scan of R. C. Bose and D. K. Ray-Chaudhuri, *On a Class of Error
Correcting Binary Group Codes*, University of North Carolina Institute of Statistics Mimeograph
Series No. 240, September 1959, was inspected. Its stable resolver is
`http://www.lib.ncsu.edu/resolver/1840.4/2137`; the observed 15-page, 556,750-byte PDF SHA-256 is
`b3beca1aa6fb6f5d47ab94eded5d0119a794b6761de866964a80aece8a3980d8`.

The report contains several distinct candidate statements:

- Lemma 1, printed page 3, characterizes a binary group code as `t`-error correcting exactly when
  every nonnull codeword has weight at least `2t + 1`.
- Theorem 1, printed page 6, gives an equivalent rank-`n-k` binary rank-matrix criterion in which
  every set of `2t` rows is independent. Calling it a parity-check-matrix formulation requires a
  later checked transport.
- Lemma 2, printed pages 9-10, supplies the finite-field power-sum independence used by the
  construction.
- Theorem 3, printed page 11, constructs a `t`-error-correcting binary `(n,k)` group code for
  `n = 2^m - 1`, with `k = 2^m - 1 - R(m,t) >= 2^m - 1 - mt`.

Theorem 3 is a strong candidate for the catalog's year and gloss, but intake does not silently make
it canonical. The same report offers the general correction criterion and matrix criterion; the
catalog also names Hocquenghem; exact parameter ranges and endpoint conventions still require
transcription; and no correction audit, complete source-to-node mapping, lawful preservation
decision, or independent review is accepted. The report is an inspected primary human proof source
of `E4` kind, not an accepted `E4`/`H0` packet; it supports only provisional `H1`.

The report's construction uses a binary rank/check matrix built from finite-field powers. It does
not use the name `BCH` or fix the modern parity-check orientation, and it does not state the modern
consecutive-root generator-polynomial designed-distance bound verbatim. Treating those formulations
as identical requires a checked historical and mathematical transport in a later phase.

## Authenticated journal bibliographic leads

Crossref metadata was inspected for two primary articles:

- R. C. Bose and D. K. Ray-Chaudhuri, "On a class of error correcting binary group codes,"
  *Information and Control* 3(1), March 1960, pages 68-79,
  DOI `10.1016/S0019-9958(60)90287-4`.
- R. C. Bose and D. K. Ray-Chaudhuri, "Further results on error correcting binary group codes,"
  *Information and Control* 3(3), September 1960, pages 279-290,
  DOI `10.1016/S0019-9958(60)90870-6`.

These journal records are authenticated bibliographic leads, not inspected journal proof sources.
Their textual relationship to the 1959 mimeograph, editorial changes, corrections, and exact
catalog mapping remain unaudited. They add provenance context but no status beyond `H1`.

The catalog also names Hocquenghem. The commonly cited lead is A. Hocquenghem, "Codes correcteurs
d'erreurs," *Chiffres* 2 (1959), often listed at pages 147-156. No authoritative primary or
bibliographic record for that paper was authenticated during this intake. Its edition, page range,
statement, proof, corrections, translation, and relationship to the Bose-Ray-Chaudhuri papers all
remain open and receive no source credit.

## Clause crosswalk

| Catalog component | Possible source-level meaning | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `BCH码` | inspected 1959 report: binary group-code rank/check-matrix construction; modern alternative: cyclic codes defined through consecutive zeros | future binary matrix code or cyclic polynomial code with checked transport | source encoding, matrix orientation, code model, field, length, generator, and transport open |
| `多个错误` (multiple errors) | a parameter `t`, often related to designed distance by `delta >= 2t + 1` | natural-number radius plus exact inequalities | no value, range, floor, or quantifier order supplied |
| `能纠正` (can correct) | disjoint radius-`t` balls, uniqueness of a nearby codeword, existence of a bounded-distance decoder, or correctness of an algebraic decoder | metric uniqueness, decoder function/specification, or an equivalent checked encoding | decoding notion and checked equivalence open |
| algebraic construction | report Theorem 3: finite-field power rows and a binary rank matrix; modern alternative: primitive element/root interval and generator polynomial | matrices/submodules or polynomial ideals plus checked transports | no construction statement selected |
| distance/correction route | report Lemma 1 plus Theorem 1 and Theorem 3; modern alternative: consecutive-root BCH bound | nonzero-codeword Hamming weight, parity-check independence, or minimum distance | exact root and checked transports open |
| cyclicity/linearity | structural properties of the constructed code | closure and cyclic-shift predicates | ingredients only; not the correction conclusion |

The table deliberately does not choose a row as canonical. The catalog gloss is too weak to decide
whether error correction is the root theorem, a corollary of the BCH bound, or merely motivation
for a construction statement.

## Formal discovery boundary

The bounded search covered repo-local Lean and pinned mathlib text for BCH names, Bose,
Ray-Chaudhuri, Hocquenghem, cyclic/linear code, coding theory, minimum distance, and error
correction. It found no exact-topic formal declaration. Pinned mathlib does provide generic
`hammingDist`, `hammingNorm`, `FiniteField.card`, `FiniteField.pow_card`, `Polynomial.IsRoot`, and
`IsPrimitiveRoot` infrastructure, which `IntakeProbe.lean` checks. Those declarations neither
define a BCH code nor state its designed-distance or decoding theorem.

This bounded intake discovery is not the later precommitted exhaustive anchor audit. It cannot
justify `M0`, `M1`, `M2`, or `M3`; the truthful provisional machine status is `M4`.

## Missing source-to-statement obligations

Before a canonical statement can be frozen, downstream work must:

1. select one exact theorem/proposition from the inspected report, its journal version, an
   authenticated Hocquenghem source, or another immutable primary edition;
2. verify its definitions, full premise context, parameter endpoints, proof boundary, and
   correction/errata status with an independent reviewer;
3. reconcile the 1959 versus 1959-60 dates and Hocquenghem versus Bose-Ray-Chaudhuri formulations;
4. decide construction, distance, dimension, and decoding ownership rather than conflate them;
5. map field, extension, length, roots, designed/actual distance, radius, code, and decoder clauses;
6. resolve every degenerate case and alternate encoding in the scope map; and
7. elaborate the exact Lean target with minimal pinned imports, a serialized expression and
   environment fingerprint, checked transports, and statement mutation tests.

Until those obligations close, the source crosswalk is intentionally incomplete and all downstream
tasks remain open.
