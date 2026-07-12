# Scope map

## Included provisional claim

- A Gale-Stewart game of length `omega` with perfect information.
- Player I and Player II alternately choose natural numbers, producing a play in Baire space
  `Nat -> Nat`.
- A payoff set `A` is Borel in the product topology on Baire space.
- Player I wins a play exactly when it lies in `A`; Player II wins otherwise.
- Determinacy means that Player I has a strategy winning against every Player II strategy, or
  Player II has a strategy winning against every Player I strategy.

This scope is a source-faithful normalization of the repository phrase, not an accepted exact
statement. The statement phase must compare every choice against Martin's inspected definitions.

## Decisions deferred to the statement phase

The source audit must freeze the representation of finite positions, whose turn is determined by
position length, total strategies versus strategies indexed only by the acting player's positions,
strategy compatibility and the induced unique play, and the exact definition of winning. It must
also freeze the topology on `Nat -> Nat`, the Borel-set predicate, any coding of the source's game
notation, the payoff/complement convention, and all foundation assumptions.

The theorem's proof architecture is intentionally not asserted from memory. In particular, the
Borel hierarchy, ranks, auxiliary games, transfinite induction, and closure steps listed as likely
source boundaries in the dossier remain audit questions, not accepted proof nodes.

## Explicit exclusions

- Open, closed, clopen, finite-horizon, or finite-action determinacy alone.
- The axiom of determinacy, projective determinacy, analytic determinacy, measurable determinacy,
  or determinacy derived from large cardinals.
- A theorem saying a game is determined after taking determinacy as a hypothesis or structure
  field.
- A finite backward-induction theorem or a strategy-stealing result.
- Replacing arbitrary Borel sets by a convenient subclass or replacing Baire space by a finite
  sample space without checked transports.
- Treating the manifest's `已验证` label or the paper citation as machine evidence.

Boundary cases such as the empty or universal payoff, constant strategies, and payoff complements
must eventually be mutation probes, but they cannot establish the arbitrary-Borel root.
