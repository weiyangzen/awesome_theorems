# Scope map

## Included provisional topic boundary

- A length-omega Gale-Stewart game with perfect information.
- Alternating natural-number moves producing an element of Baire space `Nat -> Nat`.
- A payoff set presented as analytic, with the exact boldface/lightface and parameter convention
  still to be selected from a primary source.
- Determinacy meaning that one of the two players has a winning strategy.
- The precise ambient set theory and every large-cardinal, determinacy, or choice premise used by
  the selected theorem.

This is a candidate normalization of the short repository gloss, not an accepted proposition.

## Decisions required at statement freeze

The source audit must fix the game and strategy definitions, payoff convention, topology and coding
of Baire space, analytic-set representation (continuous image, projection of a Borel/closed set, or
tree projection), parameter policy, and all ordered binders. Most importantly, it must establish
whether the intended result assumes a measurable cardinal, another large-cardinal hypothesis, a
determinacy principle, or is stated in some other explicit base theory. This cannot be inferred from
the old `已验证` label.

## Explicit exclusions

- Borel, open, closed, clopen, finite, or finite-horizon determinacy alone.
- Projective determinacy or the axiom of determinacy as a substituted conclusion.
- Assuming the target game is determined and projecting that assumption.
- Assuming analytic determinacy and proving one of its consequences.
- A theorem only about analytic sets, descriptive trees, or Polish spaces.
- Omitting a root-critical set-theoretic hypothesis to obtain a stronger statement.
- Adding an arbitrary strong hypothesis without a source to make a convenient statement true.
- Treating a citation, metadata status, or successful API probe as proof evidence.

No canonical Lean target is frozen during intake.
