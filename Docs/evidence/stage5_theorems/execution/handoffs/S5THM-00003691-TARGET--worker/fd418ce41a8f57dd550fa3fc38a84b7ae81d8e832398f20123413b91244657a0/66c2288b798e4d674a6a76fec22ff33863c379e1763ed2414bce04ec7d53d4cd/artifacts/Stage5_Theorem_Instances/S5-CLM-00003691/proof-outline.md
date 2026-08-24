# Proof outline — Erdős 1105(ii) transport

Let `P(k,n)` be the frozen right-hand equality after assigning
`ℓ = (k - 1) / 2` and `ε = 1` for odd `k`, `2` otherwise. Let `N(k,n)` be the
same equality with those two names expanded in place.

1. Bind the frozen statement, bounds, graph input, arithmetic branches, and
   Stage6 alias. Treat the provider as statement authority only because its
   proof closes with `sorryAx`.
2. Observe that `P(k,n)` and `N(k,n)` are definitionally equal: reducing the
   two `let` binders changes no mathematical term.
3. For the forward direction, assume the exact formula for every `k,n` with
   `5 ≤ k ≤ n`. Introduce bounded `k,n`, specialize the premise, and use the
   definitional equality from step 2.
4. For the reverse direction, assume the normalized formula under the same
   bounds. Introduce the variables and return that evidence under the two let
   binders.
5. Pair steps 3 and 4 to obtain a biconditional, establishing the crosswalk in
   both directions.
6. Audit substitution by introducing an arbitrary alternative graph invariant
   but retaining the exact invariant in both the premise and conclusion.

No hypothesis, inference, output, formal anchor, downstream use, exceptional
case, or trust boundary is implicit: the structured inventory in
`proof-units.json` carries those fields for each node.
