# Source-statement crosswalk

## Repository provenance

`Docs/researches/math_theorems.md:2062-2067` is the entire original catalog record:

- title: `卢津定理`;
- attribution: Nikolai Luzin;
- year: 1912;
- gloss: `可测函数与连续函数的关系`;
- importance: high;
- untrusted formalization label: `已验证`.

All six lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no
citation, formula, theorem number, page, definition, assumption, conclusion, or artifact link.
`Docs/Stage0_Blueprint.md:7927-7952` repeats it while leaving exact definitions, premises, proof,
equivalent forms, axioms, machine status, and artifacts open. These records identify a theorem
family only and give no H0 or machine-proof credit.

## Primary-source lead

The Bibliotheque nationale de France's public-domain Gallica scan supplies a matching source:

> N. Lusin, "Sur les proprietes des fonctions mesurables," *Comptes rendus hebdomadaires des
> seances de l'Academie des sciences*, volume 154, seance of 17 June 1912, pages 1688-1690.
> Stable volume ARK: `ark:/12148/bpt6k31070`; article begins at image `f1788`.

Printed page 1689 was visually inspected. Its general theorem says, in substance: if `f(x)` is a
measurable function on the interval `0 <= x <= 1`, then for arbitrarily small `epsilon > 0` there
exists a perfect nowhere-dense set `P` in that interval such that `f` is continuous on `P`
relative to `P` and `measure(P) > 1 - epsilon`. The note calls this the `C-propriete` and sketches
its derivation from Baire-class functions and Egorov's theorem.

This is a strong `H1` lead, not H0. The repository does not cite this article or select this
particular theorem among the note's several results. The interval, real-valuedness convention,
definition of measurable function, perfect/nowhere-dense requirement, relative-continuity notion,
Lebesgue measure normalization, epsilon quantification, preceding definitions and proof boundary,
translation, later corrections or errata, and independent review have not been fully admitted.
The three inspected page-image SHA-256 values and access boundary are recorded in `instance.json`.

## Clause crosswalk

| Repository phrase or source clause | Historical source lead | Lean target | Intake decision |
|---|---|---|---|
| "measurable function" | measurable `f(x)` on `0 <= x <= 1` | no expression frozen | codomain and measurability notion remain open |
| "continuous function relationship" | restriction of the same `f` is relatively continuous on `P` | candidate `ContinuousOn f P` only | do not replace relative continuity without a checked mapping |
| large set | `P` perfect and nowhere dense | closed/compact candidates only | topological requirements are source-bearing, not decoration |
| exceptional size | `measure(P) > 1 - epsilon` for arbitrarily small positive epsilon | complement/difference inequality not selected | binder order, ENNReal translation, and strictness remain open |
| domain and measure | unit interval with normalized length | possible subtype/set and volume encodings | no modern general domain may be substituted |
| `已验证` | catalog metadata only | no proposition or proof object | explicitly rejected as H/M evidence |

## Pinned formal crosswalk

| Declaration | Candidate role | Boundary |
|---|---|---|
| `ContinuousOn` | language for relative continuity | generic predicate only; no target existence theorem |
| `Continuous.measurable` | continuous implies measurable | reverse direction only |
| `MeasurableSet.exists_isCompact_diff_lt` | produces a large compact subset of a finite-measure measurable set | no continuity claim |
| `Measurable.exists_continuous` | makes a measurable map continuous under a finer Polish topology | changes topology rather than removing a small set |
| `ContinuousMap.toAEEqFun` | embeds continuous maps into an a.e.-measurable function space | no density, representative, or large-set theorem |

The same pinned Polish module also contains Lusin separation and Lusin-Souslin results. Their name
overlap does not make them candidates for this real-analysis target. A bounded search over
repo-local Lean and pinned mathlib located no usual large-measure continuous-restriction theorem;
this is intake discovery, not an exhaustive anchor audit or proof of global absence.

## Retry condition

An accountable source reviewer must select the exact immutable source proposition, transcribe its
full ordered statement and incorporated definitions, map every assumption and conclusion, audit
translation and corrections or errata, reconcile historical and modern variants, and obtain
independent approval. A later statement worker must then freeze minimal imports, universes,
binders, expression and environment fingerprints, checked transports, and all four required
statement mutation classes.
