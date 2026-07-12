# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10355-10360` supplies exactly a Chinese title meaning "SRB
measure," the attribution "Sinai/Ruelle/Bowen," the year 1976, a gloss meaning "physical
measure(s) of dissipative systems," importance "high," and a status labeled "verified." All six
lines were introduced by repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; the record contains no citation or theorem
statement.

`Docs/Stage0_Blueprint.md:38537-38562` repeats the gloss and explicitly leaves exact definitions
and premises, proof process, dependencies, equivalent forms, axioms, machine status, and artifact
links to be supplied. The rev-5.6 manifest carries that status only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

## Candidate sources

Crossref metadata identify David Ruelle, "A Measure Associated with Axiom-A Attractors,"
*American Journal of Mathematics* **98**(3) (1976), starting at p. 619, DOI
`10.2307/2373810`. This aligns with the year and one named contributor, but bibliographic metadata
do not expose the exact theorem, definitions, complete page range, assumptions, proof boundary, or
errata. The repository does not select the paper or one of its results. The JSTOR article endpoint
returned HTTP 403 during intake, so its primary text was not inspected. This is an `E5` discovery
lead, not an accepted primary-source packet.

For scope discovery, the 21-page author-hosted PDF of Lai-Sang Young, "What Are SRB Measures, and
Which Dynamical Systems Have Them?" (published in *Journal of Statistical Physics* **108**(5-6),
733-754 (2002), DOI `10.1023/A:1019762724717`) was inspected with SHA-256
`5de3a2ed19f2f03f0f46cdd1f681419a61589e1a9f8579442e4b842cbc725e42`. Its Section 1,
Theorem 1 summarizes a `C^2` diffeomorphism with an Axiom A attractor and a unique invariant Borel
probability measure through four equivalent characterizations. The introduction and Section 2
also explain that the equivalences change in broader nonuniform settings. This secondary survey
therefore establishes that the catalog wording is materially ambiguous. It is not the catalog's
statement authority, an immutable accepted primary proof source, or `H0` evidence.

## Crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| catalog title | a Sinai-Ruelle-Bowen invariant measure or a family of related definitions/results | one exact `Prop` with a definition bridge | concept named; no proposition |
| "dissipative system" | map, diffeomorphism, or flow on a phase space with an attractor | phase type/structures, dynamics, regularity, invariant set, dissipativity predicate | all open |
| "physical measure" | invariant probability whose empirical statistics govern a positive- or full-volume basin | reference volume, basin predicate, observable class or weak convergence, quantifiers and a.e. scope | definition and conclusion open |
| SRB alternative | absolute continuity of conditionals on unstable manifolds | hyperbolic splitting, unstable leaves, measurable partition/disintegration, leaf volume, absolute continuity | not chosen; key interfaces not identified |
| Sinai/Ruelle/Bowen | a historical body of results for Anosov and Axiom A systems | source provenance and node-by-node premise mapping | no edition, theorem/page, assumptions, proof, errata, or reviewer |
| 1976 | plausible link to Ruelle's Axiom A attractor article | immutable source selection and exact passage | metadata candidate only |
| catalog status | untrusted inventory metadata | inspectable source proof and kernel receipt would be required | no H or M credit |

## Source gate

Before the target can leave `H5`, an accountable reviewer must preserve an immutable primary or
authoritative source, select an exact theorem and page/section, transcribe every definition,
ordered binder, hypothesis, conclusion, equivalence direction, and exceptional case, audit
corrections and errata, and justify why it represents `THM-M-1417` rather than one of the adjacent
hyperbolic-dynamics targets. A second reviewer must approve the mapping.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded search under
`Mathlib` found no occurrence identifying an SRB, Sinai-Ruelle-Bowen, or physical-measure target.
Pinned APIs do include `birkhoffAverage`, `MeasureTheory.MeasurePreserving`,
`MeasureTheory.Ergodic`, and `mfderiv`. They cover only orbit-average, invariant-measure, ergodic,
and derivative substrate; none defines an SRB measure, its physical basin, its unstable
conditionals, or an existence/uniqueness theorem.

The canonical module, declaration or expression, normalized expression hash, checked transports,
and statement mutations remain null. The bounded search is intake discovery, not an exhaustive
formal-anchor audit. No H0, M0, or readable-proof closure is claimed.
