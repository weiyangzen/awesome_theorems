# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records `Corona定理`, attributes it to Lennart Carleson, dates it
to 1962, and gives only the gloss `H^infinity的Corona问题`. Stage0 repeats this text and leaves exact
definitions, assumptions, proof route, axioms, and artifacts open. The manifest deliberately carries
the old `已验证` label as `source_status_untrusted`; it supplies no proof credit.

## Primary-source candidate

Lennart Carleson, "Interpolations by bounded analytic functions and the corona problem", *Annals of
Mathematics*, second series, volume 76 (1962), pages 547-559, is the original-paper candidate. This
bibliographic identification is discovery evidence only. An immutable copy, exact theorem/page,
notation, premise and conclusion mapping, corrections/errata check, and independent source review
remain required before `H0`.

## Crosswalk

| Repository/source component | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| `H^infinity` | bounded analytic complex functions on the open unit disc | analyticity plus bounded range/function predicate | scope frozen; exact representation open |
| corona condition | generators uniformly bounded away from a common zero | `0 < delta` and pointwise finite sum of norms bounded below | scope frozen; norm variant open |
| solution | bounded analytic Bezout coefficients `g_i` | existential finite function family with analytic and bounded predicates | scope frozen; quantitative bound open |
| Bezout identity | `sum f_i g_i = 1` pointwise | `Finset.univ.sum` equality for every disc point | intended conclusion |
| maximal ideal formulation | disc evaluations dense in the maximal ideal space | Banach-algebra spectrum and checked equivalence | alternate only; no credit |
| `已验证` | legacy inventory assertion | no Lean proposition or kernel evidence | explicitly rejected |

## Lean statement boundary

The statement gate selects `Stage1Instances.THM_M_0373.CoronaTheoremTarget`: a nonempty finite index
type, ambient functions on `ℂ` restricted to the open unit ball, analyticity plus bounded restricted
image, an explicit positive lower bound on the sum of norms, and bounded analytic Bezout
coefficients. Its direct expanded form is connected by a kernel-checked iff. This formal freeze does
not upgrade source status: the original paper's exact passage, notation, conclusion, errata, and
independent review remain open H gates.

## Intake Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports the unit-disc and analytic APIs and checks `Complex.UnitDisc`, `AnalyticOnNhd`,
`Bornology.IsBounded`, `Finset.sum`, and the unit-disc norm lemma. These are encoding ingredients,
not a corona theorem or proof. No formal anchor search is credited at intake; that belongs to the
downstream immutable anchor-audit node after the exact statement is frozen.
