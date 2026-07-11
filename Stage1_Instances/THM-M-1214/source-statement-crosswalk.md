# Source-statement crosswalk

## Candidate primary source

Thierry Cazenave and Fred B. Weissler, "The Cauchy problem for the critical nonlinear Schrodinger
equation in H^s", *Nonlinear Analysis: Theory, Methods & Applications* 14 (1990), 807-836,
DOI `10.1016/0362-546X(90)90023-A` is the primary candidate indicated by the repository phrase
"NLS critical regularity". An authoritative copy still must be inspected to select the exact
theorem, page, hypotheses, notation, and any errata. Bibliographic identification alone is not H0.

The surname label is ambiguous: Cazenave and Weissler published multiple NLS well-posedness
results, and the paper contains multiple conclusions. The statement phase may not silently combine
local well-posedness, maximal continuation, global existence, and scattering from separate results.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "Cazenave-Weissler theorem" | a specific result in the candidate paper | one exact theorem expression | family identified; theorem number open |
| nonlinear Schrodinger equation | source-normalized Cauchy problem | complex-valued time-dependent function, Laplacian, nonlinearity, initial trace | included; conventions open |
| critical regularity | scaling-invariant `H^s`/related data regime | concrete critical space and scaling relation | included; exact index and space open |
| local well-posedness | existence and uniqueness on a nontrivial interval | solution predicate, lifespan, existence and uniqueness quantifiers | included; solution class open |
| stability | continuous dependence asserted by the source | topology and data-to-solution continuity statement | conditional on selected theorem |
| Duhamel formulation | mild solution/fixed-point architecture | propagator, time integral, and equality in a specified space | expected; exact formulation open |

## Evidence boundary

The repository supplies no accepted source excerpt or Lean declaration for this target. Before H0,
an independent reviewer must verify the stable edition, exact theorem/page, definitions referenced
by the theorem, all exponent and endpoint restrictions, and errata, and approve a row-by-row
source-to-Lean mapping. Before M-credit, the exact Lean target must elaborate and later anchor work
must inspect actual declarations and terminal proof bodies at immutable revisions.
