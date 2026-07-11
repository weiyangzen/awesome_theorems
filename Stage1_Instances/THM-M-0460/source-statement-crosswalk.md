# Source-statement crosswalk

## Available record and candidate source

The repository inventory gives only the Chinese title, attribution to Shou-Wu Zhang, year 1995,
and the phrase "equidistribution of points of small height". Its `已验证` status is explicitly
untrusted under rev-5.6.

A strong primary-source candidate is Shou-Wu Zhang, *Small points and adelic metrics*, Journal of
Algebraic Geometry 4 (1995). It is recorded here only as a discovery candidate. The actual paper,
theorem number/page, exact wording, definitions, corrections, and errata have not been independently
inspected in this intake, so this is not `H0` evidence and no exact source claim is asserted.

## Crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "small height" | normalized heights approach a source-defined minimum | height function, normalization, convergence | included provisionally; conventions open |
| "points" | algebraic points and their conjugates on an arithmetic variety | variety, closed/geometric points, Galois orbit | domain open |
| "equidistribution" | weak convergence of orbit measures | probability measures, pushforward/empirical measure, weak convergence | conclusion family identified; exact form open |
| canonical limit | local measure from an adelically metrized line bundle | analytification and canonical measure construction | source and API open |
| generic sequence | avoidance of proper closed subvarieties or source equivalent | quantified sequence and genericity predicate | exact definition open |
| 1995 / Zhang | bibliographic locator | no proof credit | candidate paper identified only |

## Source and machine boundary

No theorem-specific Lean file or accepted external Lean declaration was found by the repository-wide
name search performed at intake. That negative local search is not a full anchor audit. The later
anchor phase must search pinned mathlib and credible external Lean 4 projects at immutable revisions,
record exact types and terminal bodies, and classify any missing arithmetic-geometry infrastructure.

Before `H0`, an independent reviewer must inspect the selected edition and approve theorem/page,
definitions, every hypothesis, normalization, proof boundaries, and errata. Before statement credit,
each approved source component must map row by row to an elaborated canonical Lean expression.
