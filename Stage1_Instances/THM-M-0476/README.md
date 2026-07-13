# THM-M-0476 rev-5.6 statement

This directory is the fail-closed `planned` intake dossier for `THM-M-0476`, Wilson's theorem.
The repository catalog supplies the formula `(p-1)! congruent to -1 (mod p)`, attributes it to
John Wilson in 1770, and labels it verified. Under rev-5.6 those uncited fields are discovery
metadata, not an accepted source statement or proof receipt.

The formula identifies the elementary number-theory theorem family, but it leaves the domain of
`p` and its primality premise implicit. The statement phase freezes the conventional forward scope:
for a natural prime `p`, the factorial of `p - 1`, cast to `ZMod p`, equals `-1`. It does not
silently replace that direction by the stronger primality characterization. This formal selection
does not turn the incomplete catalog wording into an accepted primary-source statement.

Pinned mathlib contains the direct candidate `ZMod.wilsons_lemma` and the stronger related
declaration `Nat.prime_iff_fac_equiv_neg_one` in `Mathlib.NumberTheory.Wilson`.
`IntakeProbe.lean` authenticates their types and representative boundary behavior in the
manifest-pinned environment. `Statement.lean` uses only primitive factorial, prime-definition, and
`ZMod` definition modules; it freezes the explicit-primality target and checks an `Iff` transport
to the `[Fact p.Prime]` form without importing the proof-bearing Wilson module.

`statement.json` records the elaborated expression and environment fingerprints, domains, binders,
hypothesis, conclusion, boundary policy, checked transport, and four structural mutations.
`check_statement.py`, `statement-validation.md`, and `statement-receipt.json` bind the provisional
self-test. `instance.json`, `scope-map.md`, and `source-statement-crosswalk.md` reconcile the earlier
intake projection; `task-dag.json` remains unchanged and open because workers never promote state.

The vector remains `[H1, M3, R4]`. The exact statement is self-tested, but primary-source fidelity,
formal-anchor and terminal-body provenance, proof, trust closure, readable reconstruction, and
release assurance remain open. No H0, M0, R0, accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
