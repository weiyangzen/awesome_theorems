# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names `T1 theorem`, attributes it to Guy David and Jean-Lin
Journe, dates it to 1984, and supplies only `L2 boundedness of singular integral operators`.
Stage0 repeats this record while explicitly leaving definitions, assumptions, proof route,
dependencies, axioms, and machine artifacts open. The rev-5.6 manifest retains `verified` only as
an untrusted source-status label.

## Bibliographic identification

The official Annals metadata page identifies Guy David and Jean-Lin Journe, *A boundedness
criterion for generalized Calderon-Zygmund operators*, Annals of Mathematics, volume 120 (1984),
pages 371-397, DOI `10.2307/2006946`, MR `0763911`. This establishes a credible intended work and
corrects no mathematical omission in the repository gloss. The page exposes metadata but no
abstract or theorem text. No theorem number, page-level theorem passage, edition/snapshot, proof
boundary, assumptions, or errata was accepted during intake, so this is not H0 evidence.

## Crosswalk

| Repository/source component | Required mathematical detail | Required Lean component | Intake status |
|---|---|---|---|
| "singular integral operator" | operator/form domain and off-diagonal kernel representation | measure spaces, test functions, operator/form and kernel predicates | absent; generic APIs only probed |
| "generalized Calderon-Zygmund" | exact size and regularity estimates and constants | structured kernel hypotheses | absent from repository and no matching local abstraction located |
| `T(1)` and `T*(1)` | distributional definitions and adjoint conventions | duality/distribution encoding plus BMO membership | absent from repository gloss |
| weak boundedness | source's test functions, scaling, and uniform constant | quantified predicate | absent |
| BMO | cubes/balls, averages, quotient by constants, scalar convention | BMO definition and membership | absent; no name-level pinned mathlib API found in bounded intake search |
| L2 boundedness | extension domain/codomain, uniqueness, and norm estimate | `MemLp`/Lp spaces and continuous linear operator | conclusion-level gloss only |
| `verified` | untrusted inventory label | no proposition or proof credit | explicitly rejected |

## Source-statement boundary

A familiar textbook formulation often describes L2 boundedness by weak boundedness together with
`T(1), T*(1) in BMO`, but adopting that slogan as the canonical statement would still invent all
the suppressed definitions and could change the original generalized-operator criterion. The next
phase must inspect an immutable primary theorem passage, record its exact page/theorem locator and
assumptions, check errata, and obtain independent source review before elaborating Lean.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks generic measure, `MemLp`, Lp-space, and continuous-linear-map APIs. These are encoding
ingredients only. The bounded name search found no local `T(1)` theorem, generalized
Calderon-Zygmund operator abstraction, weak-boundedness predicate, or BMO definition; this negative
intake observation is not the later immutable anchor audit.
