# Source-statement crosswalk

## Candidate primary sources

- William Feller, *An Introduction to Probability Theory and Its Applications*, volume II,
  second edition, Wiley (1971), the Markov-process/semigroup treatment. The exact theorem and page
  have not been inspected.
- Stewart N. Ethier and Thomas G. Kurtz, *Markov Processes: Characterization and Convergence*,
  Wiley (1986), Chapter 4. This is a modern theorem-source candidate; the exact theorem number,
  assumptions, edition wording, and errata remain unverified.

These are discovery anchors, not `H0` evidence. A stable edition must be inspected and independently
reviewed before any exact-source claim.

## Crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Feller process" | Markov process induced by a Feller semigroup | concrete process, filtration, laws, and Markov predicate | included; encoding open |
| "Feller semigroup" | positive conservative strongly continuous semigroup preserving the chosen continuous-function space | kernels or operators plus checked laws | included; `C₀` versus bounded-continuous open |
| transition laws | conditional transition probabilities agree with the semigroup | finite-dimensional/conditional-law equality | included; exact equality open |
| path regularity | right-continuous or cadlag modification where justified | topology on paths and one-sided limit predicates | source-dependent; not yet claimed |
| state space | topological measurable space satisfying source hypotheses | explicit typeclasses and Borel compatibility | included; hypotheses open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_233.lean` is discovery evidence only. It defines
kernel-based `FellerSemigroupData` and checks adjacent mathlib APIs. Its
`FellerProcessRealization` stores `transition_law_matches_semigroup_holds` and
`markov_property_holds` as fields, so `StatementShape` asks for a package containing the terminal
facts rather than constructing them. The module's earlier search notes and build results must be
re-audited against the pinned revision and do not establish M0.

Before `H0`, an independent reviewer must verify edition, theorem/page, definitions, every
assumption, conclusion, edge cases, and errata, then approve the row-by-row source-to-Lean mapping.
