# Scope map

## Included topic boundary

- A source-selected diamond principle, including its exact cardinal or ordinal parameter.
- The guessing sequence, with the exact type and restriction condition at each stage.
- The quantified targets to be guessed and the requirement that correct guesses occur on a
  stationary subset of the selected cardinal.
- The source-selected foundation and definitions of club, stationary, regularity, uncountability,
  ordinal initial segments, and powersets.
- If the target is Jensen's relative result, the constructible-universe/model hypothesis and the
  distinction between internal and external ordinals, subsets, and stationarity.
- Checked transports between subset-guessing and function-guessing formulations only in directions
  actually proved.

## Decisions required at statement freeze

1. Identify an exact primary or authoritative source proposition rather than the topic gloss.
2. Decide whether the target is the assertion `Diamond(omega_1)`, a generalized
   `Diamond(kappa)` or `Diamond(S)`, Jensen's theorem inside `L`, an implication from `V = L`, or a
   consequence/equivalence.
3. Freeze the ambient set theory and model semantics, including whether `omega_1`, powersets, club,
   and stationarity are computed internally or externally.
4. Freeze ordered binders for the cardinal, stationary parameter, guessing sequence, arbitrary
   target subset/function, and the stationary set of correct stages.
5. Decide regularity, uncountability, limit-stage, empty-stage, and coding conventions, plus all
   universe lifts required by Lean.

## Explicit exclusions

- The square principle, club principle, weak diamond, or a cardinal-arithmetic consequence as a
  substitute.
- A bare definition of `Diamond` presented as though it were a theorem.
- An unconditional proof of diamond from ZFC; the independence/relative-consistency boundary may
  not be erased.
- Jensen's theorem in the constructible universe without formalized model satisfaction,
  constructibility, and internal stationarity.
- A structure that stores a guessing sequence and its correctness proof as fields, followed by a
  projection theorem.
- Topological closedness or order-theoretic unboundedness alone as a replacement for club and
  stationary subsets of a cardinal.
- The repository label `已验证` or nearby ordinal APIs as human-source or proof evidence.

No canonical Lean proposition is frozen at intake because the repository does not state one.
