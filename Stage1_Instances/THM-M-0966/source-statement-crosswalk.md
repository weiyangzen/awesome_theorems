# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:7057-7062` is the complete received record: the
Kruskal-Katona name, Kruskal/Katona attribution, year 1963, and the gloss `阴影的最小大小`
(minimum size of the shadow). Git history places these uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:26335-26360` repeats the
gloss while leaving exact definitions, hypotheses, proof route, dependencies, alternate forms,
axioms, machine state, and artifact links open. Rev-5.6 retains `已验证` only as untrusted metadata
and resets the target to `L0 / rework_required`.

## Primary-source leads

The catalog year matches Joseph B. Kruskal, *The Number of Simplices in a Complex*, in
*Mathematical Optimization Techniques* (1963), pp. 251-278, DOI
`10.1525/9780520319875-014`. A bounded Crossref query confirmed author, title, container, year,
pages, and DOI. The independently attributed Katona route is commonly associated with G. Katona,
*A Theorem of Finite Sets*; Crossref exposes a 2009 reprint in *Classic Papers in Combinatorics*,
pp. 381-401, DOI `10.1007/978-0-8176-4842-8_27`.

These are bibliographic leads, not admitted `E4` evidence. This intake did not obtain and inspect a
complete original Kruskal or Katona text, pin an exact theorem/page passage, audit incorporated
definitions and premises, dispose of errata, map the proof boundary, or obtain independent review.
It therefore does not claim that the usual modern colex or cascade wording is literally the
catalog's source statement. Human status remains `H1`.

## Component crosswalk

| Catalog/source component | Unresolved source meaning | Pinned Lean candidate | Intake assessment |
|---|---|---|---|
| shadow | lower, iterated, inclusive, or another complex face operation is unstated | `Finset.shadow` deletes one element from each member and deduplicates | credible one-step lower-shadow encoding; source identity open |
| family | ambient complex or uniform finite set family is unstated | `Finset (Finset (Fin n))` | finite simple family on `Fin n`; alternate ground sets need transports |
| uniformity | rank and any nonuniform reduction are unstated | `(A : Set _).Sized r` | exact-size premise is explicit in the candidate |
| comparator | the catalog does not name colex | `Finset.Colex.IsInitSeg C r` | candidate uses an `r`-uniform colex down-set |
| family size | exact versus no-greater comparator is unstated | `C.card <= A.card` | weaker comparator premise includes exact equality; existence of exact-size `C` is not concluded |
| minimum | inequality, attainment, numerical value, or minimizer classification is unstated | `C.shadow.card <= A.shadow.card` | proves a conditional comparison, not a standalone existence or equality characterization |
| cascade value | no representation convention is supplied | absent from the basic declaration; module TODO says to add the `k`-cascade version | cannot be inferred or credited |
| iteration | one-step versus repeated shadow is unstated | `Finset.iterated_kk`; `Finset.kruskal_katona_lovasz_form` | separate, proposition-changing candidates |
| equality cases | catalog does not specify classification | module TODO says to characterize equality | absent; no credit |
| `已验证` | untrusted catalog label | no accepted receipt | no H or M credit |

## Pinned Lean candidate boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Combinatorics.SetFamily.KruskalKatona` declares:

```text
Finset.kruskal_katona
  {A C : Finset (Finset (Fin n))}
  (hAr : (A : Set (Finset (Fin n))).Sized r)
  (hCA : C.card <= A.card)
  (hC : Finset.Colex.IsInitSeg C r) :
  C.shadow.card <= A.shadow.card
```

The module entered mathlib in commit `bf434437a5dbaff9d9bad9107c87447348b1af2f`
(`feat: The Kruskal-Katona theorem`, 2024-08-24). The pinned source is a real proof body, but intake
does not perform the downstream terminal-provenance, dependency, placeholder, trust, or exact-root
audit. `IntakeProbe.lean` elaborates the declaration and reports
`[propext, Classical.choice, Quot.sound]`. It also exposes the iterated and Lovasz forms. These facts
support only discovery status `M3`; they do not select the canonical root or establish `M0-W`.

The basic theorem is conditional on a supplied `C`; it does not conclude that an initial segment of
any requested cardinality exists. The implication from the candidate to an exact-cardinality
minimum statement therefore needs an explicit realization lemma and checked composition. The
numeric binomial/cascade form needs further representation and evaluation results. Conversely, a
source theorem in cascade form cannot be identified with this declaration by matching names or
informal equivalence alone.

## Required source admission

Before leaving `H1`, accountable reviewers must admit a complete immutable primary edition, select
the exact proposition, record theorem/page and proof boundaries, map every binder, premise,
definition, conclusion, and degenerate case, audit corrections and errata, and independently review
the translation. The statement phase must then freeze a kernel expression and compile every
required colex/cascade/ground-set transport rather than infer it from the eponym.
