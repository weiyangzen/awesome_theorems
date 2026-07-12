# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records `Rubio de Francia外推定理`, Jose Rubio de Francia, 1984,
and only `加权不等式的外推` ("extrapolation of weighted inequalities"). Stage0 repeats this gloss
while leaving exact definitions, assumptions, proof route, equivalent forms, axioms, and formal
artifacts open. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted`.

The repository record therefore identifies a theorem family and historical attribution, not an
exact proposition. In particular it supplies no initial exponent, family or operator, base space,
weight convention, quantified constants, endpoint policy, theorem/page, proof source, or errata
record.

## Primary-source locator, not accepted crosswalk

A high-priority locator for the source audit is Jose L. Rubio de Francia, *Factorization theory and
`A_p` weights*, American Journal of Mathematics 106 (1984), 533-547. Its author, date, and subject
align with the metadata. This intake did not independently inspect an immutable scan and pinpoint
the exact theorem passage, assumptions, proof boundary, or errata. The citation is therefore a
discovery lead, not `H0` evidence and not authority to transcribe a Lean target.

## Crosswalk

| Repository phrase | Possible mathematical component | Lean representation candidate | Intake status |
|---|---|---|---|
| "weighted inequality" | integral or `L^p(w)` inequality for a pair `(f,g)` or an operator | `Measure.withDensity`, `lintegral`, `eLpNorm`, measurability predicates | APIs probed; exact inequality absent |
| "extrapolation" | implication from a fixed-exponent estimate to estimates across exponents | nested quantifiers over exponents, weights, pairs, and constants | direction plausible; exact binders open |
| weight class | Muckenhoupt `A_p` under a specified averaging convention | a source-exact predicate using averages/integrals over cubes or balls | no accepted mathlib encoding located at intake |
| Jose Rubio de Francia / 1984 | historical locator | no Lean term or proof credit | pinpoint passage and independent review open |
| `已验证` | untrusted inventory label | no proposition or proof term | explicitly rejected as evidence |

## Required source audit

The next source pass must retain an immutable source or digest; record edition, theorem and pages;
transcribe every premise and conclusion; check definitions, later corrections, and errata; and map
each clause to a canonical human statement and ordered Lean binder. An independent reviewer must
approve that crosswalk before `H0` or exact-statement acceptance.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe checks weighted measures, `L^p` seminorms and membership, nonnegative integrals, and measure
restriction. These are representation ingredients only. A bounded name/text search found no
Rubio de Francia or Muckenhoupt `A_p` declaration in pinned mathlib; this is not the later immutable
anchor audit and receives no machine-proof credit.
