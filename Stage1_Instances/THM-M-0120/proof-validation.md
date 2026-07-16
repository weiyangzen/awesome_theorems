# THM-M-0120 proof-phase validation

The current frozen Lean proposition cannot receive a truthful positive proof body. The
target-owned declaration
`Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget` has exact type
`Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})` and replays at
trust level zero using only `propext`, `Classical.choice`, and `Quot.sound`.

The countermodel uses the identity morphism on the spectrum of an algebraic closure of
the rationals, makes every geometric premise true, takes the numerical space to be
`Real`, the asserted Mori cone to be `{-1}`, and the rational-curve carrier to be empty.
Any claimed decomposition of `-1` then forces the nonnegative summand to equal `-1`, a
contradiction. This refutes only the disconnected abstract encoding, not the mathematical
Mori cone theorem.

The declared direct and transitive parent closure is empty. The refreshed schema-1.1
dependency ledger records that exact empty inspection order and consumes no provider
body, receipt, checkbox state, acceptance, or proof credit.

`check_proof.py` validates the current authority hashes, claim order, empty dependency
context, frozen statement and 25-obligation denominator, absence of terminal proof
bodies and prohibited constructs, pinned Lean/mathlib identities, the trust-zero
countermodel replay, the node receipt, and the worker handoff. Its sole stdout value is
a `stage1-validator-semantic-result/1.0` JSON object with `status: blocked`,
`phase_accepted: false`, and `theorem_complete: false`.

Repair requires reopening the statement phase and replacing the unconstrained numerical
stand-ins with intrinsic definitions or sufficient noncircular laws tied to the
projective klt pair. The exact expression fingerprint and every downstream frozen
artifact must then be regenerated and accepted before proof work resumes. Assuming the
conclusion or its output package would be circular and is not an admissible repair.
