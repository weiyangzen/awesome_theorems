# Scope map

## Candidate source family

The inspected 1950 paper supports this candidate family for later statement selection:

- A finite collection of players, with one strategy chosen per player. The source's `n-person`
  wording supports finiteness; whether `n > 0` is an explicit formal hypothesis remains open.
- A finite pure-strategy set for every player. The formal nonemptiness convention needed to form
  mixed strategies remains a statement-phase decision rather than an unqualified source quote.
- A real-valued payoff for every player at every pure-strategy profile.
- A mixed strategy for a player is a probability distribution over that player's pure strategies;
  a mixed profile is one such distribution for every player.
- Expected payoff is the finite multilinear extension of the pure payoff table.
- A player best-responds when no unilateral replacement of that player's mixed strategy improves
  expected payoff while the other players' strategies remain fixed.
- The conclusion is existence of a mixed profile at which every player best-responds, equivalently
  a self-countering profile in Nash's terminology.

This is a source candidate, not the frozen repository statement. The statement phase must make an
accountable source-selection decision and map every clause to one elaborated Lean expression.

## Decisions required at statement freeze

1. Whether players are represented by an arbitrary finite nonempty type, `Fin n` with `0 < n`, or
   another finite index, and whether the zero-player case is excluded.
2. Whether each pure-strategy carrier is a finite nonempty type or an explicitly finite nonempty
   set, and how empty or singleton strategy spaces are treated.
3. Whether payoffs are real-valued, rational-valued, or live in another ordered field, and whether
   the source-real formulation is the canonical root.
4. Whether mixed strategies use `stdSimplex Real`, `PMF`, finitely supported measures, or another
   encoding; every credited alternate form needs a checked transport.
5. The exact expected-payoff finite sum, product-profile encoding, coercions, binder order, and
   convention for a unilateral strategy update.
6. Whether best responses quantify over pure deviations, mixed deviations, or both, and the checked
   lemma relating those formulations under finite multilinear expected payoff.
7. Whether equilibrium is expressed as all-player best response, membership in a best-response
   correspondence, or Nash's self-countering relation, with checked equivalences.
8. Whether equality ties, constant payoffs, dominated actions, zero-sum games, identical interests,
   and nonunique equilibria require special clauses or fall under the general statement.
9. The exact source edition, printed theorem locator, definitions incorporated by reference,
   translation policy, corrections or errata, and independent source reviewer.

## Proof-route boundary

The 1950 proof route constructs the product of finite probability simplices, the countering or
best-response correspondence, its nonempty convex values, and its closed graph, then applies
Kakutani's fixed-point theorem. These are prospective obligation-tree nodes only. They are not
frozen obligations and receive no closure credit at intake. Kakutani is a dependency, not a
substitute for the Nash theorem.

## Explicit exclusions

- A pure-strategy equilibrium theorem, since finite games need not have pure equilibria.
- The two-player zero-sum minimax theorem or saddle-point existence used as the general root.
- The 1951 compact-convex continuous-game generalization, or games with infinite action spaces,
  unless an approved source decision redirects the target and records the semantic delta.
- Correlated, trembling-hand perfect, subgame-perfect, Bayesian, evolutionary, or approximate
  equilibrium substituted for ordinary mixed-strategy Nash equilibrium.
- A fixed point for an arbitrary continuous function, the Banach fixed-point theorem, or
  Kakutani's correspondence theorem alone.
- Assuming equilibrium, a fixed point, or a nonempty best-response intersection as a structure
  field or hypothesis and projecting it as the conclusion.
- A finite enumeration, numerical solver, learning simulation, or computed equilibrium for one
  game presented as the general existence theorem.
- Reusing the separate `THM-M-1511` target (`纳什均衡`) or any of its future evidence without an
  accepted identity and scope decision.
- Treating the catalog label `已验证`, a citation, or the discovery-only Lean probe as proof.
