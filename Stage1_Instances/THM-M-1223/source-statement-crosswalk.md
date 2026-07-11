# Source-statement crosswalk

## Primary source candidate

Jalal Shatah and Michael Struwe, "Regularity results for nonlinear wave equations", *Annals of
Mathematics*, Second Series 138(3) (1993), 503-518, DOI `10.2307/2946554` is the identified
historical primary paper. The bibliographic identification is an intake anchor only: an exact
theorem number/page, verbatim hypotheses, notation, corrections, and errata have not yet been
inspected and therefore this is not `H0` evidence.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| `临界NLW` | energy-critical semilinear wave equation | concrete wave operator, critical nonlinearity, dimension | included; exact formula open |
| `整体` | solution exists over the full time axis | global time-domain solution object | included |
| `适定性` | existence, uniqueness, and source-supported stability | initial-value predicate and uniqueness/continuity class | included; exact clauses open |
| finite energy | critical Sobolev energy data and propagated regularity | Sobolev spaces, traces, energy functional | included; conventions open |
| Shatah-Struwe | regularity/global theory proved in the cited paper | row-level theorem/source mapping | primary paper identified, theorem anchor open |

## Statement fidelity boundary

The generic phrase "Shatah-Struwe theorem" is not a unique formal proposition. The statement phase
must inspect the paper and choose one exact theorem, record its page and all assumptions, and show
how its equation and function spaces map to Lean definitions. It must not silently import later
dimension-general formulations or conflate regularity, global existence, and scattering.

No repo-local Lean declaration or pinned external Lean 4 proof has been identified or credited at
intake. Before `H0`, a separate reviewer must check the edition, theorem/page, assumptions and
errata. Before machine credit, the anchor audit must inspect exact declarations and proof-body
provenance at immutable revisions.
