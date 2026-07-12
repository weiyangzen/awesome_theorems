# THM-M-1070 obligation tree

This is the frozen architecture for the exact real-valued Levy-process predicate. Checked conjunction transport does not establish any open process clause.

## Proof route

- **M1070-ROOT** (root): Establish the exact frozen Levy-process predicate for the given process.
  Output: The exact canonical proposition.
  - **M1070-T-COMPOSE** (transport): Conjoin the six exact clauses and transport the package definitionally to IsLevyProcess.
    Output: The exact root conditional on every clause.
    - **M1070-L-PROBABILITY** (terminal): Show that P is a probability measure.
      Output: The probability-space clause.
    - **M1070-L-MEASURABLE** (terminal): Show every time marginal X t is P-almost-everywhere measurable.
      Output: Measurable random variables at every time.
    - **M1070-L-ZERO** (terminal): Show that the process starts at zero P-almost everywhere.
      Output: The exact initial-value clause.
    - **M1070-L-INDEPENDENT** (bridge): Prove joint independence for every finite ordered family of consecutive increments.
      Output: The full joint independent-increment clause.
    - **M1070-L-STATIONARY** (bridge): Prove every increment X(s+t)-X(s) has the same law as X(t).
      Output: Stationarity of all increment laws.
    - **M1070-L-STOCH-CONT** (bridge): Prove convergence in P-measure of X along every neighborhood filter in time.
      Output: Stochastic continuity at every nonnegative time.

## Node ledgers

### M1070-ROOT

Establish the exact frozen Levy-process predicate for the given process.

Formal target: `Stage1Instances.THM_M_1070.IsLevyProcess P X`

Output: The exact canonical proposition.

Semantic ledger:
1. Consume every exact incoming proof_requires child.
2. Derive the declared output: The exact canonical proposition.
3. Use the registered reciprocal composition edge without any undeclared premise.

### M1070-S-DEFINITIONS

Fix nonnegative-real time, real state space, the measurable sample space, measure, and process binder order.

Formal target: `Statement.lean definitions and ExpandedSourceShape`

Output: The exact objects and quantifier scopes used below.

Semantic ledger:
1. Freeze the exact formal context and named premises.
2. Establish: Fix nonnegative-real time, real state space, the measurable sample space, measure, and process binder order.
3. Derive: The exact objects and quantifier scopes used below.
4. Pass only that output through the registered typed edge.

### M1070-S-BOUNDARY

Preserve zero and repeated endpoints, almost-everywhere initial value, joint rather than pairwise independence, and exclusion of cadlag regularity.

Formal target: `Canonical statement boundary package`

Output: No discrete-time, pairwise-only, pointwise-zero, continuous-path, or cadlag substitution.

Semantic ledger:
1. Freeze the exact formal context and named premises.
2. Establish: Preserve zero and repeated endpoints, almost-everywhere initial value, joint rather than pairwise independence, and exclusion of cadlag regularity.
3. Derive: No discrete-time, pairwise-only, pointwise-zero, continuous-path, or cadlag substitution.
4. Pass only that output through the registered typed edge.

### M1070-S-FOUNDATION

Freeze classical measure theory, quotient/extensionality, kernel, and no-oracle policies.

Formal target: `Foundation and transitive trust certificate`

Output: An audited trust boundary for eventual terminal bodies.

Semantic ledger:
1. Freeze the exact formal context and named premises.
2. Establish: Freeze classical measure theory, quotient/extensionality, kernel, and no-oracle policies.
3. Derive: An audited trust boundary for eventual terminal bodies.
4. Pass only that output through the registered typed edge.

### M1070-L-PROBABILITY

Show that P is a probability measure.

Formal target: `IsProbabilityMeasure P`

Output: The probability-space clause.

Semantic ledger:
1. Freeze the exact formal context and named premises.
2. Establish: Show that P is a probability measure.
3. Derive: The probability-space clause.
4. Pass only that output through the registered typed edge.

### M1070-L-MEASURABLE

Show every time marginal X t is P-almost-everywhere measurable.

Formal target: `forall t, AEMeasurable (X t) P`

Output: Measurable random variables at every time.

Semantic ledger:
1. Freeze the exact formal context and named premises.
2. Establish: Show every time marginal X t is P-almost-everywhere measurable.
3. Derive: Measurable random variables at every time.
4. Pass only that output through the registered typed edge.

### M1070-L-ZERO

Show that the process starts at zero P-almost everywhere.

Formal target: `X 0 =m[P] 0`

Output: The exact initial-value clause.

Semantic ledger:
1. Freeze the exact formal context and named premises.
2. Establish: Show that the process starts at zero P-almost everywhere.
3. Derive: The exact initial-value clause.
4. Pass only that output through the registered typed edge.

### M1070-L-INDEPENDENT

Prove joint independence for every finite ordered family of consecutive increments.

Formal target: `ProbabilityTheory.HasIndepIncrements X P`

Output: The full joint independent-increment clause.

Semantic ledger:
1. Freeze the exact formal context and named premises.
2. Establish: Prove joint independence for every finite ordered family of consecutive increments.
3. Derive: The full joint independent-increment clause.
4. Pass only that output through the registered typed edge.

### M1070-L-STATIONARY

Prove every increment X(s+t)-X(s) has the same law as X(t).

Formal target: `forall s t, IdentDistrib (X (s + t) - X s) (X t) P P`

Output: Stationarity of all increment laws.

Semantic ledger:
1. Freeze the exact formal context and named premises.
2. Establish: Prove every increment X(s+t)-X(s) has the same law as X(t).
3. Derive: Stationarity of all increment laws.
4. Pass only that output through the registered typed edge.

### M1070-L-STOCH-CONT

Prove convergence in P-measure of X along every neighborhood filter in time.

Formal target: `forall t, TendstoInMeasure P X (nhds t) (X t)`

Output: Stochastic continuity at every nonnegative time.

Semantic ledger:
1. Freeze the exact formal context and named premises.
2. Establish: Prove convergence in P-measure of X along every neighborhood filter in time.
3. Derive: Stochastic continuity at every nonnegative time.
4. Pass only that output through the registered typed edge.

### M1070-T-COMPOSE

Conjoin the six exact clauses and transport the package definitionally to IsLevyProcess.

Formal target: `Stage1Instances.THM_M_1070.isLevyProcess_of_components`

Output: The exact root conditional on every clause.

Semantic ledger:
1. Consume every exact incoming proof_requires child.
2. Derive the declared output: The exact root conditional on every clause.
3. Use the registered reciprocal composition edge without any undeclared premise.

### M1070-X-SOURCE

Pinpoint primary definitions and regularization results for every convention and material bridge.

Formal target: `Reviewed node-specific human-source crosswalk`

Output: Human-source evidence without machine-proof credit.

Semantic ledger:
1. Freeze the exact formal context and named premises.
2. Establish: Pinpoint primary definitions and regularization results for every convention and material bridge.
3. Derive: Human-source evidence without machine-proof credit.
4. Pass only that output through the registered typed edge.

### M1070-X-PROVENANCE

Resolve all terminal bodies, revisions, wrappers, licenses, axioms, and transitive trust dependencies.

Formal target: `Transitive provenance and trust closure`

Output: No component API or near-match is mistaken for a root proof body.

Semantic ledger:
1. Freeze the exact formal context and named premises.
2. Establish: Resolve all terminal bodies, revisions, wrappers, licenses, axioms, and transitive trust dependencies.
3. Derive: No component API or near-match is mistaken for a root proof body.
4. Pass only that output through the registered typed edge.

## Typed overlays

`M1070-X-SOURCE` and `M1070-X-PROVENANCE` cover human-source and terminal-body boundaries. They cannot supply semantic proof credit.

## Closure boundary

The conditional conjunction transport is locally checked, but the six semantic clause premises remain open. The first critical cut is independent increments, stationary increment laws, and stochastic continuity. No arbitrary process is proved Levy, no cadlag regularization theorem is asserted, and audit/theorem completion remain false.
