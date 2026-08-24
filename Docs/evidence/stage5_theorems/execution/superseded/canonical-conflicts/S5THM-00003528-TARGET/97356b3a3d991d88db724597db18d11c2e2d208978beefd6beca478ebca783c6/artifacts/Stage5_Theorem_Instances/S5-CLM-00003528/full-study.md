# Full study — Borwein sine series

## R-STATEMENT

**Hypotheses.** The frozen record identifies `FormalConjectures.Books.BorweinSineSeries`, revision `2270d31e8dd611521f979de6d86da364930b7669`, and `BorweinSineSeries.borwein_sine_series`. Its type is `answer(True) ↔ Summable` of the displayed positive-natural-indexed real sequence. The workset binds the current Stage6 alias.

**Inference.** Read every source symbol in its pinned environment. The claim-owned surface writes the left proposition as `True`, while retaining the exact real coefficients, `Real.sin`, positive-natural index, natural exponent, real division, and `Summable`. Bidirectional equality is subject to Master recomputation of the elaborated expression; text similarity alone is not used.

**Output.** The exact target proposition and its source/target transport declarations.

**Formal anchor.** `A-STATEMENT`, declaration `source_to_target_statement` in `Statement.lean`.

**Downstream uses.** Nodes PU-002 through PU-005 depend on this identity, and the release binds `S6-CLM-00003985`.

**Exceptional cases.** The provider's `answer` wrapper may only be normalized after elaborated equality is confirmed. Its theorem body contains `sorryAx`, so the body supplies no proof authority.

**Trust boundary.** Frozen provider bytes authenticate the statement. Canonical Master authenticates semantic equality and the claim-owned proof.

## R-ANALYTIC

**Hypotheses.** The obligation is summability of exactly `((2/3 + (1/3) * sin n)^n) / n` over positive naturals, interpreted in the reals.

**Inference.** Establish the `Summable` conclusion without appealing to the provider theorem body. The sine values lie in the real interval `[-1,1]`, but the base can approach one along integers; therefore a mere pointwise bound by the harmonic series, a claimed uniform geometric ratio, or a numerical partial-sum calculation is insufficient. The exact analytic closure must remain visible to trust-zero replay and its pinned dependencies.

**Output.** The exact summability fact used by the logical reconstruction.

**Formal anchor.** `A-FORWARD`, declaration `borwein_sine_series_forward` in `Proof.lean`, records the exact analytic conclusion carried by the root proposition.

**Downstream uses.** PU-003 reconstructs the biconditional and PU-005 audits root closure.

**Exceptional cases.** No conditional irrationality-measure hypothesis, changed index domain, absolute-value surrogate, bounded-partial-sum proxy, or approximate sum is accepted as the unconditional output.

**Trust boundary.** Canonical Master must verify a claim-owned analytic body and its complete transitive dependency/axiom census; the source `sorryAx` is excluded.

## R-RECONSTRUCT

**Hypotheses.** The exact series is summable, and the left side of the normalized claim is `True`.

**Inference.** For the forward direction, ignore the inhabitant of `True` and return the established summability proof. For the reverse direction, ignore the summability proof and return the unique logical fact needed, namely `True`.

**Output.** `True ↔ Summable` for the exact frozen sequence.

**Formal anchor.** `A-RECONSTRUCT`, declaration `borwein_sine_series_reconstruct` in `Proof.lean`.

**Downstream uses.** PU-004 transports the rebuilt proposition and PU-005 audits it.

**Exceptional cases.** The reconstruction never deletes the analytic obligation and never treats the reflexive shape of an audit theorem as a proof of summability.

**Trust boundary.** This logical shell uses only explicit local theorem bodies and kernel primitives; its analytic premise remains separately auditable.

## R-TRANSPORT

**Hypotheses.** Master-recomputed source and target expressions agree, PU-003 supplies the exact target proposition, and the local environment contains no source-symbol shadowing.

**Inference.** Carry the proposition from source identity to target identity and back. In canonical Lake files the unavailable Formal Conjectures module path is retained as an exact provenance comment, while the executable import is `Mathlib`; this does not authorize a substituted mathematical meaning.

**Output.** A bidirectional semantic crosswalk naming both transport declarations.

**Formal anchor.** `A-TRANSPORT`, declaration `audit_bidirectional_transport` in `Audit.lean`.

**Downstream uses.** PU-005 and the Stage6 alias consume the transported proposition.

**Exceptional cases.** Local definitions, abbrevs, notation, syntax, macros, coercions, instances, namespace aliases, and changed imports are rejected even when the printed theorem header is identical.

**Trust boundary.** Source theorem name and bytes are provenance. Only the claim-owned body and pinned Mathlib dependencies may enter the accepted closure.

## R-AUDIT

**Hypotheses.** Nodes PU-001 through PU-004, all formal and human anchors, empty H/M/R cut sets, the exact source snapshot, and the structured machine/readability records are present.

**Inference.** Rebuild from source offline, compile at trust zero, recompute the exact root and transitive constant environment, enumerate declaration bodies and axioms, verify node/fragment bijection, and run semantic-substitution plus deletion mutations. Compare the result to every applicable THM-M-0387 evidence-shape predicate and require strict additions in semantic binding and adversarial replay.

**Output.** A provisional release candidate whose `master_accepted` field remains false until canonical Master independently succeeds.

**Formal anchor.** `A-AUDIT`, declaration `audit_exact_surface_expression` in `Audit.lean`.

**Downstream uses.** Canonical Stage5 acceptance and current alias `S6-CLM-00003985`.

**Exceptional cases.** Worker `--no-lean` validation, polished prose, self-attested hashes, a successful source theorem reference, or a terminal worker goal cannot establish canonical theorem completion.

**Trust boundary.** This worker proposes bytes and evidence. Canonical Master alone validates integrated bytes, sets `master_accepted=true`, and advances underscore to x.
