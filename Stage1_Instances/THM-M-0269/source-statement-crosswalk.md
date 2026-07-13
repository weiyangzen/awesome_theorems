# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:1936-1941` supplies exactly the Chinese title
`勒贝格单调收敛定理`, Henri Lebesgue, 1902, the Chinese gloss `单调函数列的积分极限`, high
importance, and status `已验证`. The English renderings used in this dossier are translations. All
six uncited lines originate at
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no formula, bibliography,
definitions, hypotheses, proof boundary, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:7441-7466` repeats the gloss and explicitly leaves the formal system,
precise definitions and premises, proof route, dependencies, equivalent formulations, axioms,
machine state, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Modern proof source candidate

Sheldon Axler, *Measure, Integration & Real Analysis*, Springer Graduate Texts in Mathematics
(2020), open-access author PDF dated 12 June 2026, Theorem 3.11 with its complete proof on printed
page 78, was inspected. The theorem assumes an arbitrary measure space and an
increasing sequence of nonnegative extended-real measurable functions. It defines the pointwise
limit and concludes that the limit of the integrals equals the integral of that limit.

The author's errata page says the current PDF incorporates all listed corrections. It contains a
page-79 correction, already incorporated in the inspected copy, concerning the following lemma;
no listed item names Theorem 3.11 or changes its statement or proof. This is strong E4 discovery
and an H1 source candidate, not H0: the repository never cited this modern formulation, the
historical identity and attribution remain open, and no independent source reviewer has accepted
the full source-to-Lean map.

## Historical source lead

Crossref and Zenodo identify H. Lebesgue, *Integrale, Longueur, Aire*, *Annali di Matematica Pura
ed Applicata* (Serie III) 7(1) (1902), pages 231-359, DOI `10.1007/BF02420592`. A public-domain
129-page scan was inspected in a bounded search. Material around printed pages 257-260 concerns
limit measurability and a dominated-convergence-like result, but the modern monotone convergence
proposition was not pinpointed. The work corroborates a historical date only; it supplies no
theorem/page, statement, premise, or proof crosswalk here. Mathlib calls monotone convergence the
"Beppo Levi lemma," so the catalog's exclusive Lebesgue attribution requires historical review.

## Literal crosswalk

| Repository phrase | Axler 3.11 component | Candidate Lean component | Intake status |
|---|---|---|---|
| `单调函数列` | increasing sequence `0 <= f_1 <= f_2 <= ...` | `f : Nat -> alpha -> ENNReal`; `Monotone f`, or an AE variant | family mapped; exact convention open |
| functions | measurable maps from `X` to `[0, infinity]` | `Measurable`, `AEMeasurable`, `ENNReal`, `Measure alpha` | domain/codomain and AE choice open |
| limit of functions | `f(x) = lim_k f_k(x)` pointwise | `fun x => iSup fun n => f n x`, or explicit `F` plus `Tendsto` | alternate encoding transport open |
| `积分极限` | `lim_k integral f_k dmu = integral f dmu` | `lintegral_iSup` or `lintegral_tendsto_of_tendsto_of_monotone` | direct candidate, no root credit |
| Henri Lebesgue, 1902 | historical work located but exact MCT passage not located | no formal component | attribution audit open |
| `已验证` | untrusted catalog label | accepted H/M receipts would be required | no H0 or M credit |

## Lean candidate boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.MeasureTheory.Integral.Lebesgue.Add` explicitly describes the theorem and provides:

- `MeasureTheory.lintegral_iSup`, the pointwise measurable/monotone supremum equality;
- `MeasureTheory.lintegral_iSup'`, the almost-everywhere measurable/monotone equality;
- `MeasureTheory.lintegral_tendsto_of_tendsto_of_monotone`, the explicit-limit form; and
- `MeasureTheory.lintegral_iSup_ae`, with measurable functions and successive AE inequalities.

`MeasureTheory.integral_tendsto_of_tendsto_of_monotone` is a related real-valued Bochner-integral
variant that assumes integrability of every term and the limit. Pinned documentation also lists
monotone convergence declarations. These are discovery interfaces only. No canonical expression,
checked source equivalence, proof-body provenance, trust closure, or M0 receipt follows.

## Source gate

Before H0 or statement acceptance, accountable reviewers must admit an immutable source edition;
confirm which monotone convergence formulation the catalog owns; pinpoint and review the complete
proof and incorporated definitions; reconcile Lebesgue and Beppo Levi attribution; map every
domain, binder, hypothesis, limit convention, conclusion, and boundary case; inspect corrections
and errata; compile checked alternate transports; and independently approve the source-to-Lean
crosswalk. Until then only the literal non-propositional catalog wording is frozen; the exact
proposition and elaborated expression remain open.
