# Full study

## inputs

- Node: `N1-INPUTS`
- Hypotheses: ξ is real; p is natural and prime; the minimal polynomial of ξ over ℚ has natural degree two.
- Inference: Bind the universally quantified variables and hypotheses hp and hξ.
- Output: The quadratic-real and prime-p hypotheses are available.
- Formal anchor: `Statement.lean:statement`
- Downstream uses: N2-SOURCE, N3-ROOT
- Exceptional cases: No inference is made if hp or hξ is absent.
- Trust boundary: Input hypotheses are trusted only as explicit theorem binders.

## source-binding

- Node: `N2-SOURCE`
- Hypotheses: The frozen provider record and exact qualified declaration are fixed by content hashes.
- Inference: Match its binders and proposition to the target surface without aliases or substitutions.
- Output: A bidirectional syntactic transport obligation is recorded.
- Formal anchor: `Audit.lean:source_to_target`
- Downstream uses: N3-ROOT
- Exceptional cases: The source declaration itself contains sorryAx and therefore is not proof authority.
- Trust boundary: Source bytes establish statement identity, not theorem truth.

## mathematical-root

- Node: `N3-ROOT`
- Hypotheses: The N1 hypotheses and the quadratic p-adic Littlewood theorem of de Mathan and Teulié.
- Inference: Apply the unavailable sorry-free mathematical theorem to the exact infimum formulation.
- Output: The infimum of q |q|_p ||qξ|| over positive naturals is zero.
- Formal anchor: `Proof.lean:proof`
- Downstream uses: N4-RELEASE
- Exceptional cases: The pinned environment supplies no sorry-free body; this is the open machine cut.
- Trust boundary: A proof must be kernel-replayed without sorryAx, axioms, or bodyless oracles.

## release-conjunction

- Node: `N4-RELEASE`
- Hypotheses: Exact semantic identity, a closed N3 root, R0 reconstruction, empty H/M/R cuts, and current validation.
- Inference: Conjoin every completion predicate and compare against THM-M-0387.
- Output: The theorem may be released only if every predicate holds simultaneously.
- Formal anchor: `Audit.lean:target_to_source`
- Downstream uses: terminal release decision
- Exceptional cases: This node is blocked whenever N3 or validation is incomplete.
- Trust boundary: Only the canonical Master may set master_accepted and advance the checklist.
