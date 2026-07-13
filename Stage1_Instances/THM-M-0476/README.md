# THM-M-0476 rev-5.6 dossier

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
intake projection; `task-dag.json` remains open and mirrors only prerequisite worker states because
workers never promote authoritative state.

`obligation-registry.json` freezes 26 semantic obligations across the statement, normalization,
branch, construction, core-lemma, external, and terminal layers. `typed-graphs.json` separates
proof, refinement, provenance, evidence, trust, documentation, and workflow edges, while
also freezing a static seven-task workflow graph. `validation-specs.json` keeps conditional
interface checks distinct from proof-closure credit.
`ObligationTree.lean` checks factorial-to-product, residue-to-unit, inverse-pairing, unit-product,
Fact-transport, and exact-root compositions without invoking the audited Wilson theorem.
`build_obligation_artifacts.py`, `check_obligation_tree.py`, `obligation-tree.md`,
`obligation-tree-validation.md`, and `obligation-tree-receipt.json` bind the deterministic freeze
and provisional node self-test.

`Proof.lean` installs `ZMod.wilsons_lemma` at the exact frozen root and independently supplies every
leaf of the frozen factorial-to-units graph. Its expanded route composes the interval factorial,
representative-to-unit bijection, inverse pairing, unit product, `Fact` transport, and exact root.
`check_proof.sh`, `check_proof.py`, `proof-validation.md`, and `proof-receipt.json` bind this
placeholder-free proof proposal to the pinned sources and allowlisted axiom closure.

The accepted vector remains `[H1, M3, R4]`. The proof phase proposes `M0-W`, but only the integration
lane may accept it; accepted proof state is still empty. Primary-source H0, full provenance and
trust closure, readable R0, hermetic and independent validation, release assurance, and master
acceptance remain open. No accepted M0, accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
