# THM-M-0282 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalogue entry named
Chebyshev's inequality. The repository source says that the result gives an upper bound on the
probability that a random variable deviates from its expectation. Its category is real analysis,
but the wording is explicitly probabilistic. The `已验证` label is untrusted metadata under
rev-5.6 and grants no source, statement, or proof credit.

The gloss identifies the classical probability-tail theorem family, but it does not state a
formula or fix a probability space, codomain, measurability and moment assumptions, threshold,
strict versus closed event, expectation and variance conventions, or boundary cases. The catalogue
also contains `THM-M-0992`, an almost verbatim probability Chebyshev record. That target's existing
dossier calls this target the deterministic similarly-sorted finite-sum inequality, but the claim
conflicts with the authoritative `THM-M-0282` source row. Intake therefore preserves the
probability scope and records the duplicate-ID conflict; it does not silently reallocate this ID.

The NUMDAM/Gallica scan of the historical paper *Des valeurs moyennes* (1867) was inspected. Its
opening theorem, proof, average-value form, weak-law statement, and Bernoulli corollary confirm the
probabilistic family. A complete modern translation, incorporated-definition and assumption map,
correction or errata disposition, and independent review are still open, so this is an H1 lead, not
H0. Pinned mathlib contains the strong exact-topic candidate
`ProbabilityTheory.meas_ge_le_variance_div_sq`, and `IntakeProbe.lean` authenticates that interface
and its extended-variance companion. These declarations are candidates, not an accepted mapping to
an unfrozen source proposition.

The provisional root vector is `[H1, M3, R4]`: a published human theorem and source lead are known
but source fidelity is unaudited; usable pinned formal candidates exist but no canonical target or
checked source transport is frozen; and no source-faithful readable reconstruction exists. All six
downstream phases remain open in `task-dag.json`.

No canonical proposition, H0, M0, R0, accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
