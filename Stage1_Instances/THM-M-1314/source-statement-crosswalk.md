# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` names Roger Penrose, labels the status "partial proof", and gives
only "bounds on black-hole mass" as the statement. That metadata is too coarse to freeze a theorem:
it supplies neither a formula nor domains, hypotheses, conventions, or a bibliographic citation.

## Candidate primary and theorem sources

- Roger Penrose, "Naked singularities", *Annals of the New York Academy of Sciences* 224 (1973).
  This is a candidate historical source for the cosmic-censorship mass/area inequality. The exact
  page, wording, normalization, and whether it is the intended repository claim require inspection.
- Gerhard Huisken and Tom Ilmanen, "The inverse mean curvature flow and the Riemannian Penrose
  inequality", *Journal of Differential Geometry* 59 (2001). This is a primary proof source for a
  time-symmetric Riemannian branch, not automatically the source or full scope of `THM-M-1314`.
- Hubert Bray, "Proof of the Riemannian Penrose inequality using the positive mass theorem",
  *Journal of Differential Geometry* 59 (2001). This is a second primary proof source for the
  Riemannian branch and likewise cannot silently replace the general claim.

These are discovery anchors only and give no `H0` credit. Exact editions/pages, theorem numbering,
assumptions, definitions, errata, and the relation to sibling `THM-M-1315` need independent review.

## Crosswalk

| Repository phrase | Candidate mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "black hole" | horizon or trapped region in spacetime/initial data | concrete Lorentzian or Riemannian geometric predicate | encoding open |
| "mass" | ADM or other source-selected total mass | asymptotic end and mass definition | notion open |
| "bounds" | candidate lower mass bound from horizon area | ordered real expression with constants | formula open |
| horizon area | area of source-selected cross-section/boundary | measure/volume of a codimension-two object | object open |
| "partial proof" | proved special branches versus unresolved general claim | separate exact declarations and transports | branch audit open |

## Status boundary

The source label "partial proof" is untrusted metadata, not kernel or human-proof closure. Before
`H0`, a reviewer must identify one exact statement and map every assumption and symbol to the Lean
target. Before `M0`, that exact target must elaborate and close without placeholders under the
pinned environment. No such claim is made at intake.
