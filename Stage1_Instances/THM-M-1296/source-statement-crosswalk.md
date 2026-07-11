# Source-statement crosswalk

## Available record and candidate sources

The repository inventory supplies only the label "profile decomposition", the phrase "decomposition
of bounded sequences", a twentieth-century date, and no named author or citation. Its `已验证`
marker is untrusted under rev-5.6 and does not identify a unique theorem.

Two historically relevant discovery candidates are Sergio Solimini, *A note on compactness-type
properties with respect to Lorentz norms of bounded subsets of a Sobolev space*, Annales de
l'Institut Henri Poincare C 12 (1995), and Patrick Gerard, *Description du defaut de compacite de
l'injection de Sobolev*, ESAIM: Control, Optimisation and Calculus of Variations 3 (1998). Neither
paper's exact theorem, page, hypotheses, definitions, corrections, or errata has been independently
inspected for this intake. They are candidate locators, not `H0` evidence.

## Crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "bounded sequences" | bounded sequence in a source-defined function space | normed function space, sequence, boundedness | ambient space open |
| "profile" | weak limits after recentering/rescaling | profile sequence and symmetry action | exact encoding open |
| "decomposition" | finite partial sum plus remainder along a subsequence | subsequence, sums, equality | included provisionally |
| parameter orthogonality | distinct profiles separate asymptotically | metric/scale divergence predicate | source formula open |
| decoupling | asymptotic splitting of norm or energy | limit statement and norm powers | exact strength open |
| negligible remainder | smallness in a weaker or critical target norm | iterated limit and target norm | norm and limit order open |

## Source and machine boundary

No theorem-specific Lean declaration is credited at intake. The later anchor audit must search the
pinned mathlib and credible external Lean 4 projects at immutable revisions, record exact types and
terminal proof bodies, and distinguish generic weak compactness from the full profile theorem.

Before `H0`, an independent reviewer must select and inspect one edition, approve theorem/page,
definitions, every hypothesis and conclusion, proof boundaries, and errata. Before statement
credit, every approved component must map row by row to an elaborated canonical Lean expression.
