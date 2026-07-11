# Source-statement crosswalk

## Candidate primary sources

- Michael H. Freedman, "The topology of four-dimensional manifolds," *Journal of Differential
  Geometry* 17 (1982), 357-453. This is the primary article candidate for the simply connected
  topological classification branch. Exact theorem numbers, wording, hypotheses, and corrections
  have not yet been inspected.
- Michael H. Freedman and Frank Quinn, *Topology of 4-Manifolds*, Princeton Mathematical Series 39
  (1990). This is a primary monograph candidate for a stable formulation and qualifications. Exact
  chapter/theorem/page and errata remain open.

These are discovery anchors, not `H0` evidence. No theorem wording is inferred from the broad
repository title. The statement phase must inspect a fixed edition and record exact anchors.

## Crosswalk

| Repository phrase | Intended component | Required Lean component | Intake status |
|---|---|---|---|
| "four-dimensional manifolds" | closed oriented simply connected topological 4-manifolds | concrete dimension-4 topological manifold predicate | provisional restriction; exact hypotheses open |
| "classification" | homeomorphism criterion and possibly realization | quantified orientation-preserving homeomorphism/equivalence | conclusion shape open |
| intersection form | integral unimodular symmetric pairing on degree-two homology | canonical `H₂`, pairing, and isometry | included; topology-to-form API open |
| Kirby-Siebenmann obstruction | additional topological/smoothability datum in relevant branch | canonical invariant and equality | included provisionally; role open |
| smooth classification | distinct and substantially stronger problem | diffeomorphism classification | excluded |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_252.lean` is discovery evidence only. It imports
manifold, bordism, singular-homology, bilinear-form, and signature APIs and builds checked local
pairing scaffolding. Its own module header says it lacks terminal Freedman, Donaldson,
Kirby-Siebenmann, intersection-form, transversality, and exotic-four-manifold classification
theorems and "does not prove the classification theorem." Any statement-shaped declaration in
that file must therefore be re-audited rather than credited.

Before `H0`, an independent reviewer must verify the selected source edition, theorem/page, every
assumption and exceptional branch, definitions, errata, and a row-by-row source-to-Lean mapping.
