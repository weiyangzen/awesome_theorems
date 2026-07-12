# Scope map

## Included topic boundary

- Two-player perfect-information games only if confirmed by the exact source.
- The source-selected move alphabet, play length, payoff coding, and winning-strategy convention.
- The precise family of payoff sets over which determinacy is asserted.
- Any foundation-relative formulation and all stated consequences or consistency assumptions.

## Ambiguities to resolve at statement freeze

1. Whether "real games" means plays coding reals (`Nat -> Nat`), moves that are themselves reals,
   or games whose payoff is a set of reals.
2. Whether the claim is full AD for every payoff set, determinacy for a named pointclass, or a
   theorem about a restricted family of games.
3. Whether strategies observe finite histories and players alternate for length omega, including
   who moves first and which payoff belongs to which player.
4. Whether the target is an axiom/schema, a relative consistency assertion, or a consequence of AD.
5. Which ambient set theory and choice principles are intended; full AD is not interchangeable
   with unrestricted choice.

The statement phase must inspect an immutable source and freeze ordered binders, player and payoff
conventions, boundary games, foundation profile, and one exact proposition.

## Explicit exclusions

- Martin's Borel determinacy theorem as a substitute; it is separately listed as `THM-M-0786`.
- Analytic, projective, or other pointclass determinacy without source support.
- Finite backward-induction games or Zermelo determinacy as a substitute for length-omega games.
- A tautology obtained by assuming the desired game's determinacy as a hypothesis.
- Treating the repository label `已验证` as proof, source fidelity, or machine evidence.
- Treating the intake encoding probe as an accepted theorem statement or proof artifact.

No canonical Lean target is frozen at intake because the repository record does not identify one.
