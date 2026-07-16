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

This fresh revalidation is bound to base revision
`f545339546bf410d5110d7fe44e70bdcf5d8b48e`. The unique scheduler-owned proof
validator exists at that base with Git blob
`fb97725b7b6dbccfd44d3f05c661f072bfd6f6bd`, but it hard-codes the earlier worker
base, graph digest, open task state, ledger digest, and changed-path set. Its exact
required argv therefore emits a typed `repair_required` result at the current base.
The worker did not modify, replace, rename, or add a validator candidate. Scheduler
repair and a fresh exact replay are required; neither the stale-validator failure nor
the checked countermodel can promote `[_]` to master-accepted `[x]`.

Repair requires reopening the statement phase and replacing the unconstrained numerical
stand-ins with intrinsic definitions or sufficient noncircular laws tied to the
projective klt pair. The exact expression fingerprint and every downstream frozen
artifact must then be regenerated and accepted before proof work resumes. Assuming the
conclusion or its output package would be circular and is not an admissible repair.
