# Source-statement crosswalk

## Candidate primary sources

- Yu. V. Prokhorov, "Convergence of random processes and limit theorems in probability theory,"
  *Theory of Probability and Its Applications* 1 (1956), 157-214. This is the historical-source
  candidate; exact theorem numbering, translated wording, assumptions, and errata remain to be
  inspected against a stable copy.
- Patrick Billingsley, *Convergence of Probability Measures*, second edition, Wiley (1999), the
  tightness and relative compactness chapter. This is a modern exposition candidate, but its exact
  theorem/page and convention crosswalk remain open.

These citations are discovery anchors, not `H0` evidence. Statement work must inspect one stable
edition and record the exact theorem, page, definitions, assumptions, and errata.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "probability measure family" | family/set of Borel probability laws | `Set (ProbabilityMeasure X)` or checked equivalent | included; encoding open |
| "tight" | one compact set works uniformly for the family at each error | `MeasureTheory.IsTightMeasureSet` after coercion audit | included; equivalence open |
| "weak convergence" | convergence against bounded continuous functions / weak laws | topology on `ProbabilityMeasure X` | included; topology audit open |
| "relatively compact" | every net/sequence has a convergent subnet/subsequence, or compact closure | `IsCompact (closure S)` after source equivalence check | included; convention open |
| "Polish space" | separable completely metrizable space with Borel sigma algebra | metric, complete, second-countable, and Borel instances | included; minimal instances open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_260.lean` imports mathlib's tightness,
Levy-Prokhorov, and Prokhorov modules and names candidate wrappers in both directions. It is useful
discovery evidence only: the next phases must check exact declaration types at the pinned revision,
elaborate the canonical target, establish representation transports, and audit every terminal proof
body. The legacy source prose also mentions only "compactness of a probability-measure family" and
does not by itself freeze the full theorem.
