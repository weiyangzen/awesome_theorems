# Proof outline — S5-CLM-00003536

## `PU-ROOT` — Furstenberg's ×2, ×3 density theorem

Hypotheses: a real number `ξ` and the assertion `Irrational ξ`.

Inference: apply Furstenberg's topological recurrence theorem to the commuting
endomorphisms `x ↦ 2x` and `x ↦ 3x` of the circle.  Multiplicative
independence of 2 and 3 rules out a finite common orbit for an irrational
starting point.  The positive-semigroup orbit is therefore dense.  Removing
the finitely many terms with a zero exponent does not change density, and the
remaining orbit is exactly the family represented by positive naturals
`m,n` in the target set-builder.

Output: density of
`{x : AddCircle 1 | ∃ m n : ℕ, 0 < m ∧ 0 < n ∧
x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))}`.

Formal anchor: `Proof.lean`, theorem
`AwesomeTheorems.Stage5.S5_CLM_00003536.furstenberg_two_three_root_application`.

Downstream uses: exact target root `PU-TRANSPORT`, the semantic crosswalk, and
the release decision.

Exceptional cases: rational `ξ` are excluded by hypothesis; zero exponents
are excluded explicitly; casting the natural product through `ℝ` and then
into `AddCircle 1` is part of the frozen statement and is not redefined.

Trust boundary: the supplied Formal Conjectures declaration is statement
authority only because its body contains `sorryAx`.  A release-grade M0 body
must prove this node independently; the typed application lemma merely checks
the exact composition interface.

## `PU-TRANSPORT` — exact-root transport

Hypotheses: the result of `PU-ROOT` for `ξ` and `hξ`.

Inference: definitional identity; the target uses the same `Dense`, set
comprehension, `AddCircle`, exponentiation, multiplication, casts, and
quantifier structure as the frozen declaration.

Output: the exact target proposition.

Formal anchor: `Statement.lean`, theorems `source_to_target_statement` and
`target_to_source_statement`.

Downstream uses: `PU-ROOT-CHECK` and all human/machine release predicates.

Exceptional cases: no local notation, alias, coercion, instance, macro, or
import substitution is allowed to change elaboration.

Trust boundary: the Master must recompute both elaborated expressions and
confirm their equality; text identity alone is insufficient.

## `PU-ROOT-CHECK` — trust-zero reconstruction audit

Hypotheses: `PU-ROOT`, `PU-TRANSPORT`, the pinned provider bytes, and the pinned
Lean toolchain.

Inference: elaborate all claim-owned Lean surfaces at `--trust=0`, enumerate
the root dependencies and axioms, reject `sorryAx`, and replay from a cold
offline source snapshot with semantic-substitution mutations.

Output: an exact-root M0 closure or a fail-closed non-release decision.

Formal anchor: `Audit.lean`, theorem `audit_exact_root_type`.

Downstream uses: machine closure, current validation receipt, strict-dominance
certificate, and provisional release.

Exceptional cases: an elaborating interface lemma does not prove the
mathematical root; a source theorem carrying `sorryAx` is never counted as a
proof dependency.

Trust boundary: the worker records provisional evidence; only the canonical
Master may independently replay and accept it.
