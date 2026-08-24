# Full study: Furstenberg's ×2,×3 density theorem

## FRAG-IDENTITY

**Node PU-00.** Hypotheses: a real number `ξ` and the predicate `Irrational ξ`. Inference: compare the frozen declaration and claim-owned target token by token after elaboration; both quantify positive naturals `m,n`, form the natural product `2^m * 3^n`, cast it into the real multiplication by `ξ`, map the real into `AddCircle (1 : ℝ)`, and assert density of the resulting set. Output: bidirectional identity transports. Formal anchor: `source_to_target_theorem` and `target_to_source_theorem`. Downstream use: fixes the proposition used by every later node. Exceptional case: changing positivity to nonnegativity changes only finitely many orbit points but is still forbidden because the frozen proposition is exact. Trust boundary: source bytes establish the statement only; the provider proof body establishes no closure.

## FRAG-ORBIT

**Node PU-01.** Hypotheses: the exact proposition fixed by PU-00 and an irrational `ξ`. Inference: form the positive semigroup orbit `Oξ = { ↑(ξ * (2^m * 3^n)) | 0<m, 0<n }` in the additive circle and its topological closure `Cξ`. Output: a closed set containing every orbit point. Formal anchor: the set expression in `furstenberg_two_three_m0`. Downstream use: PU-02 proves its invariance and PU-03 proves it infinite. Exceptional case: the use of positive exponents, rather than exponents starting at zero, is preserved throughout. Trust boundary: this is a construction in Mathlib's existing real, power, quotient, set, and topology semantics.

## FRAG-INVARIANCE

**Node PU-02.** Hypotheses: the orbit and closure from PU-01. Inference: multiplication by 2 sends the point indexed by `(m,n)` to the point indexed by `(m+1,n)`; multiplication by 3 sends it to `(m,n+1)`. Both self-maps of the circle are continuous, hence they send limits of orbit nets to limits in the closure. Output: `Cξ` is forward invariant under both ×2 and ×3. Formal anchor: the closed-set portion of `furstenberg_two_three_m0`. Downstream use: one of the two inputs to PU-04. Exceptional case: forward invariance is all that is used; inverse branches are not assumed. Trust boundary: continuity and closure transport are foundation topology facts and must be recomputed by Master.

## FRAG-INFINITE

**Node PU-03.** Hypotheses: `Irrational ξ` and the orbit from PU-01. Inference: unique factorization makes `(m,n) ↦ 2^m3^n` injective. If the circle orbit were finite, two different multipliers `a≠b` would have `↑(ξa)=↑(ξb)`, so `(a-b)ξ` would be an integer. Division by the nonzero integer `a-b` would make `ξ` rational, contradiction. Output: `Oξ`, and therefore `Cξ`, is infinite. Formal anchor: the irrationality branch of `furstenberg_two_three_m0`. Downstream use: the second input to PU-04. Exceptional case: equality of multipliers is excluded using the prime factorizations of 2 and 3. Trust boundary: only integer arithmetic, the AddCircle quotient criterion, and the definition of irrationality are used.

## FRAG-FURSTENBERG

**Node PU-04.** Hypotheses: `Cξ` is closed, infinite, and forward invariant under both ×2 and ×3. Inference: apply Furstenberg's closed-set lemma. Its proof chooses a minimal nonempty invariant subset of the derived set, uses multiplicative independence of 2 and 3 to amplify arbitrarily small return differences at incommensurable scales, obtains arbitrarily fine rational translation invariance, and then uses closedness to obtain invariance under every circle translation. A nonempty subset invariant under all translations is the whole circle. Output: `Cξ = Set.univ`. Formal anchor: the reconstructed closed-set argument consumed by `furstenberg_two_three_m0`. Downstream use: PU-05. Exceptional case: infinitude is indispensable; finite rational orbits are closed and invariant. Trust boundary: this is the substantive theorem-specific argument and cannot be replaced by the provider declaration.

## FRAG-DENSITY

**Node PU-05.** Hypotheses: `Cξ` is the closure of `Oξ` and PU-04 gives `Cξ = Set.univ`. Inference: unfold the topology definition of `Dense`; a set is dense exactly when its closure is the whole carrier. Output: `Dense Oξ`. Formal anchor: the conclusion of `furstenberg_two_three_m0`. Downstream use: PU-06. Exceptional case: no countability, measure, or equidistribution strengthening is claimed. Trust boundary: the conversion is a foundation topology equivalence.

## FRAG-AUDIT

**Node PU-06.** Hypotheses: PU-00's exact identity and PU-05's density conclusion for arbitrary irrational `ξ`. Inference: universally introduce `ξ`, apply the density result, and transport it across the exact source/target identity. Output: the frozen `Bugeaud06.furstenberg_two_three` proposition. Formal anchor: `exact_type_audit` and `terminal_root_audit`. Downstream use: release root. Exceptional case: no statement weakening, alternate growth convention, or source proof is admitted. Trust boundary: worker evidence is provisional; canonical Master alone may recompute and accept the root.
