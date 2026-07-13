# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1943-1948` supplies exactly the title `法图引理`, attribution to
Pierre Fatou, year 1906, gloss `积分下极限的不等式`, high importance, and status `已验证`. Git
history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record supplies no bibliography, theorem/page,
formula, definitions, binders, hypotheses, proof boundary, correction history, reviewer, or formal
artifact.

`Docs/Stage0_Blueprint.md:7468-7493` repeats the gloss while explicitly leaving the target formal
system, foundation, exact definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open. Thus the repository record establishes identity
and a theorem family only. The `已验证` field remains untrusted metadata.

## Modern source lead

Sheldon Axler, *Measure, Integration & Real Analysis*, Springer Graduate Texts in Mathematics 282
(2020), current author-hosted open-access PDF dated 12 June 2026, was inspected. In Section 3A,
Exercise 17 on printed page 86:

- `(X, S, mu)` is a measure space;
- `f_1, f_2, ...` is a sequence of nonnegative `S`-measurable functions on `X`;
- `f(x)` is defined as `liminf_{k -> infinity} f_k(x)`;
- part (a) asks for measurability of `f`;
- part (b) asks to prove `integral f dmu <= liminf_{k -> infinity} integral f_k dmu`;
- the following note explicitly calls part (b) Fatou's Lemma and points to the monotone convergence
  theorem as a clean proof route.

The observed PDF SHA-256 is
`7a7ab07fb74f5394c3180da51875ec467a0d89627321c8b2624b6b9b9585fb4e`. The author page identifies
the dated PDF and links an errata page. The errata page says the current PDF incorporates all known
listed print corrections; the bounded search found no Fatou/page-86/Exercise-17 entry. These are
useful source facts, not an accepted correction audit.

This source remains `H1`, not `H0`: the catalog does not cite it; it is a mutable modern edition;
the result is an exercise rather than a supplied complete proof; the exact relationship to Fatou's
1906 work and the catalog's attribution has not been established; incorporated definitions and
integral conventions have not been fully crosswalked; and no independent source reviewer has
approved fidelity. Crossref identifies P. Fatou's 1906 paper *Series trigonometriques et series de
Taylor*, *Acta Mathematica* 30, 335-400, DOI `10.1007/BF02418579`, but no exact lemma passage was
inspected. That paper is also a lead for the distinct radial-limit theorem, so its metadata alone is
not source-statement evidence for this target.

## Clause crosswalk

| Repository or candidate clause | Modern source lead | Pinned Lean candidate | Intake decision |
|---|---|---|---|
| "integrals" | Lebesgue integrals over one measure space | `lintegral` into `ENNReal` | integral and codomain convention remain open |
| sequence | `f_1, f_2, ...` | `f : Nat -> alpha -> ENNReal` | natural indexing aligns, but is not source-frozen |
| nonnegativity | explicit | encoded by `ENNReal` codomain | candidate encoding; real/nonnegative transport open |
| measurability | every `f_k` is measurable | `Measurable` or `AEMeasurable` variant | catalog selects neither; Axler aligns more closely with measurable variant |
| lower limit | pointwise `liminf_{k -> infinity} f_k(x)` | `liminf (fun n => f n a) atTop` | exact filter/pointwise transport open |
| inequality | integral of liminf is at most liminf of integrals | identical inequality shape | strong candidate match, not accepted identity |
| proof route | note suggests monotone convergence | pinned body uses lower-integral supremum/infimum lemmas | full human/formal node and provenance audit remains open |
| `已验证` | no corresponding source claim | no proposition or proof object | no H or M credit |

## Formal candidate crosswalk

The intake probe elaborates `MeasureTheory.lintegral_liminf_le'` and
`MeasureTheory.lintegral_liminf_le` at the pinned revision and prints their axiom reports. Both
reports are `[propext, Classical.choice, Quot.sound]`. The probe also authenticates the adjacent
`lintegral_iSup'`, `Filter.liminf_eq_iSup_iInf_of_nat`, and
`MeasureTheory.le_iInf₂_lintegral` interfaces. This
is scoped discovery evidence only, not the later exhaustive anchor, terminal-body, dependency, or
trust audit.

Before leaving `H1`, accountable reviewers must preserve an immutable approved source edition,
identify an exact result and incorporated definitions, map every binder, premise, conclusion,
integral and liminf convention, audit corrections and historical provenance, and approve fidelity
to `THM-M-0270`. Before statement acceptance, Lean work must freeze minimal imports and the exact
elaborated expression, compile any required transports, and pass removed-hypothesis, changed-domain,
binder-scope, and boundary-case mutations.
