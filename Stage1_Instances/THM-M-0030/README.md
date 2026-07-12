# THM-M-0030 rev-5.6 intake

`THM-M-0030` is the repository's Krull intersection theorem item. The catalog describes it only
as an ideal-intersection property in a Noetherian local ring, attributes it to Wolfgang Krull in
1938, and labels it verified. That label is untrusted metadata, not human-source or kernel evidence.

## Planned scope

This intake selects the conventional ideal specialization for later source ratification: if `R`
is a commutative Noetherian local ring and `I` is a proper ideal of `R`, then the intersection of
all natural powers `I ^ n` is the zero ideal. The more general finite-module theorem is an
authoritative source form and a pinned Lean candidate, but it is not silently substituted for the
catalog's ideal-only root.

Stacks Project Lemma 10.51.4 (tag `00IP`) was inspected at an immutable revision as an authoritative
modern source lead. It states the finite-module form and proves it using Artin-Rees and Nakayama.
This supports an `H1` lead only: historical source fidelity, corrections, complete premise mapping,
and independent review remain open.

## Formal boundary

Pinned mathlib module `Mathlib.RingTheory.Filtration` contains the close candidate
`Ideal.iInf_pow_eq_bot_of_isLocalRing` and the finite-module declaration
`Ideal.iInf_pow_smul_eq_bot_of_isLocalRing`. `IntakeProbe.lean` authenticates their types with the
pinned toolchain. Intake does not freeze a canonical Lean declaration or expression fingerprint,
audit a terminal proof body or transitive trust closure, or credit machine completion.

The planned vector is `[H1, M3, R3]`: a stable conventional claim and modern proof source lead are
identified, exact formal interfaces are located but unaccepted, and the dossier maps scope without
reconstructing the proof. All six dependent phases remain open. No H0, M0, R0, accepted execution
state, audit completion, theorem completion, or master acceptance is claimed.
