# Scope map

## Included topic boundary

- A source-named recursively axiomatized formal theory, including its syntax, derivability, and
  chosen metatheory.
- A source-named ordinal or recursive notation system and its well-founded ordering.
- An exact relation between the theory's proof strength and that ordinal, such as a soundness,
  consistency, reflection, termination, upper-bound, lower-bound, or equality statement.
- Every hypothesis needed for the calibration and the direction in which it is proved.

## Ambiguities to resolve at statement freeze

The repository record does not decide among materially different propositions:

1. A Gentzen-style consistency theorem for Peano arithmetic from transfinite induction up to
   epsilon zero.
2. A theorem identifying epsilon zero as the proof-theoretic ordinal of PA, which requires a
   precise definition and both upper- and lower-bound directions.
3. A general definition or metatheorem assigning proof-theoretic ordinals to formal theories.
4. An ordinal analysis of a theory other than PA, potentially using ordinals far beyond epsilon
   zero and a different notation system.

The statement phase must inspect an immutable source and freeze one proposition, ordered binders,
object theory, metatheory, proof coding, ordinal presentation, calibration relation, hypotheses,
and conclusion. It must distinguish actual ordinals from recursive notations and distinguish a
consistency upper bound from an exact proof-theoretic-ordinal characterization.

## Explicit exclusions

- `Ordinal.epsilon_zero_eq_nfp` or another pure ordinal-arithmetic theorem as a substitute for an
  ordinal-analysis result about formal theories.
- Gentzen's consistency theorem, transfinite induction, or ordinal notation as an automatic synonym
  for this separately indexed repository item.
- A definition that merely assumes a theory's ordinal measure as data and projects it back.
- A finite termination experiment, unverified notation comparison, or informal proof-strength
  slogan as proof of a universal metatheorem.
- The repository label `已验证` as evidence of a human proof or machine closure.

No canonical Lean target is frozen at intake because the source record does not identify one.
