# THM-M-0476 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0476`, Wilson's theorem.
The repository catalog supplies the formula `(p-1)! congruent to -1 (mod p)`, attributes it to
John Wilson in 1770, and labels it verified. Under rev-5.6 those uncited fields are discovery
metadata, not an accepted source statement or proof receipt.

The formula identifies the elementary number-theory theorem family, but it leaves the domain of
`p` and its primality premise implicit. Intake preserves the conventional forward scope: for a
natural prime `p`, the factorial of `p - 1` is congruent to `-1` modulo `p`. It does not silently
replace that direction by the stronger primality characterization, and it does not yet freeze a
canonical Lean expression or a source-approved encoding of congruence.

Pinned mathlib contains the direct candidate `ZMod.wilsons_lemma` and the stronger related
declaration `Nat.prime_iff_fac_equiv_neg_one` in `Mathlib.NumberTheory.Wilson`.
`IntakeProbe.lean` authenticates their types, the explicit-primality wrapper, and representative
boundary behavior in the manifest-pinned environment. This is discovery evidence only: proof-body
provenance, exact statement identity, trust closure, and anchor acceptance remain downstream.

`instance.json` is the structured scope authority. `scope-map.md` records proposition-changing
choices and exclusions, `source-statement-crosswalk.md` maps the catalog formula to source and Lean
components, and `task-dag.json` leaves all six dependent phases open.

The provisional vector is `[H1, M3, R4]`. No H0, M0, R0, accepted execution state, audit
completion, theorem completion, or master acceptance is claimed.
