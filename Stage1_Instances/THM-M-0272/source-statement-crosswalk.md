# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1957-1962` supplies exactly the title `托内利定理`, attribution
to Leonida Tonelli, 1909, the gloss `非负函数的重积分`, importance "high," and status
`已验证`. Git blame places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, stable source ID,
edition, theorem or page locator, formula, definition, ordered binder, hypothesis, conclusion,
proof boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:7522-7547` repeats the gloss while explicitly leaving exact definitions
and premises, the proof process, dependencies, alternate formulations, axioms, machine status, and
artifact links open. Its generic planning text is not mathematical evidence. The rev-5.6 manifest
retains `已验证` only as `source_status_untrusted` and resets the target to
`L0 / rework_required`.

## Human-source boundary

The attribution, name, and familiar content establish a published classical theorem family, which
supports a provisional H1 classification. No immutable primary Tonelli text or authoritative modern
proof edition, exact theorem passage, incorporated definitions, premise and conclusion map, proof
boundary, translation, correction or errata audit, or independent review is admitted in this
intake. The catalog's year therefore remains provenance metadata rather than a pinpoint proof
citation. H0 is unavailable.

Secondary web discovery shows another result also called a "Tonelli theorem" about surface area,
and the repository itself has `THM-M-1266` for variational existence. These homonyms reinforce the
need for statement content and source locators; neither is evidence for this target.

## Literal crosswalk

| Repository element | Necessary mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| `非负函数` | codomain, measurability, equality modulo null sets, infinity convention | `ENNReal`-valued function plus `Measurable` or `AEMeasurable`, or a checked alternate encoding | open |
| multiple integral | product measurable space, product measure, whole-space or restricted integral | `Measure.prod` and one exact `lintegral` expression | open |
| iterated form implicit in the theorem name | order, equality orientation, measurability of inner integral | nested `lintegral` and any required measurability theorem | open |
| measure spaces | finiteness and completion hypotheses | measurable-space data and `SFinite`, `SigmaFinite`, or other instances | absent |
| Tonelli / 1909 | source provenance | immutable source locator, translation, proof and errata crosswalk | absent |
| `已验证` | untrusted inventory field | accepted human-source and kernel receipts | no credit |

The gloss is not a quantified proposition. Choosing a standard formulation would still add domains,
premises, a codomain, and a conclusion that the repository does not state.

## Formal-candidate crosswalk

All candidates below are from pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.MeasureTheory.Measure.Prod`. `IntakeProbe.lean` checks their interfaces and representative
axiom reports only.

| Declaration | Candidate role | Identity boundary |
|---|---|---|
| `MeasureTheory.lintegral_prod` | product integral equals one iterated integral for an `ENNReal`-valued a.e.-measurable function | direct named candidate, but its one-sided s-finiteness and exact order are not source-selected |
| `MeasureTheory.lintegral_prod_symm` | product integral equals the reverse iterated integral | needs s-finiteness of both measures in the surrounding context; not automatically part of the root |
| `MeasureTheory.lintegral_lintegral` | curried form with reverse equality orientation | representation transport and source identity are unchecked |
| `MeasureTheory.lintegral_lintegral_swap` | equality of the two iterated integrals | plausible familiar conclusion, but it is not identical by syntax or assumptions to `lintegral_prod` |
| `MeasureTheory.setLIntegral_prod` | Tonelli on a product of measurable sets | restricted variant not stated by the catalog |
| `Measurable.lintegral_prod_right'` | measurability of the inner integral | supporting interface, not the whole integration equality |

Pinned mathlib's own module documentation names `lintegral_prod` as Tonelli's theorem and explains
the curried and symmetric naming variants. This is strong formal discovery evidence, not a source-
statement crosswalk, expression fingerprint, proof-body audit, or M0 receipt.

## Duplicate and legacy boundary

`THM-M-1266` has the English title `Tonelli定理`, date 1920, and gloss `变分问题的存在性`
(existence for variational problems). It is a distinct target in differential equations and must
not receive source, statement, task, or proof credit from `THM-M-0272`, or vice versa.

The filename `S1_M_272.lean` is also misleading for this intake: its header explicitly maps the
legacy slot to `THM-M-0992` and its declarations formalize Chebyshev's inequality. Rev-5.6 rejects
legacy slot identity as target identity, so that file is not a candidate artifact for Tonelli.

## Open gates

Before H0, reviewers must admit an immutable primary or authoritative proof source, pinpoint its
exact result and incorporated definitions, map all premises, conclusions, integration orders and
proof transitions, audit translation and errata, and independently approve the mapping. Before
statement acceptance, Lean work must freeze the exact binders and minimal imports, serialize the
elaborated expression and environment fingerprint, compile each credited transport, and pass the
required mutations. Exhaustive anchor and terminal-body provenance work remains the later
anchor-audit phase.
