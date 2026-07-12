# THM-M-1333 obligation tree

The frozen route is delayed Euler approximation followed by finite-dimensional Arzela-Ascoli, passage to the integral equation, and the fundamental theorem of calculus. Every mathematical node below is open unless explicitly described as an interface check; no proof of Peano existence is claimed.

## Proof flow

### M1333-ROOT

Kind: `root`. Risk: `critical`. Step budget: `8`.

The exact finite-dimensional local Peano existence target.

Formal target: `Stage1Instances.THM_M_1333.PeanoExistenceTarget`

Output: The canonical proposition.

Semantic ledger:
1. Bind the exact statement fingerprints of every declared proof child.
2. Consume every declared child output without adding an undeclared premise.
3. Derive the declared output: The canonical proposition.
4. Record a kernel-checked child-to-parent composition declaration before closure.

Frozen interface only; the listed mathematical result and root closure remain open.

### M1333-S-STATEMENT

Kind: `definition`. Risk: `critical`. Step budget: `10`.

Preserve the open domain, joint continuity, positive symmetric interval, graph membership, and derivative-within encoding.

Formal target: `Stage1Instances.THM_M_1333.{PeanoExistenceTarget,IsSolutionWithin}`

Output: The exact input and output interfaces used by composition.

Semantic ledger:
1. Freeze the exact local context and named premises.
2. Establish the transition: Preserve the open domain, joint continuity, positive symmetric interval, graph membership, and derivative-within encoding.
3. Derive the declared output: The exact input and output interfaces used by composition.
4. Pass only that output through the declared proof edge; retain all boundary conditions.

Frozen interface only; the listed mathematical result and root closure remain open.

### M1333-S-BOUNDARIES

Kind: `normalization`. Risk: `high`. Step budget: `12`.

Handle n = 0, positive radius, endpoint derivatives, and exclude uniqueness and global continuation.

Formal target: `Boundary package for PeanoExistenceTarget`

Output: No degenerate or neighboring theorem is silently substituted.

Semantic ledger:
1. Freeze the exact local context and named premises.
2. Establish the transition: Handle n = 0, positive radius, endpoint derivatives, and exclude uniqueness and global continuation.
3. Derive the declared output: No degenerate or neighboring theorem is silently substituted.
4. Pass only that output through the declared proof edge; retain all boundary conditions.

Frozen interface only; the listed mathematical result and root closure remain open.

### M1333-S-FOUNDATION

Kind: `certificate`. Risk: `critical`. Step budget: `12`.

Audit finite-dimensional compactness, integration, classical subsequence extraction, and the transitive trust boundary.

Formal target: `Foundation and TCB certificate for every terminal body`

Output: An accepted foundation profile covering all proof dependencies.

Semantic ledger:
1. Freeze the exact local context and named premises.
2. Establish the transition: Audit finite-dimensional compactness, integration, classical subsequence extraction, and the transitive trust boundary.
3. Derive the declared output: An accepted foundation profile covering all proof dependencies.
4. Pass only that output through the declared proof edge; retain all boundary conditions.

Frozen interface only; the listed mathematical result and root closure remain open.

### M1333-N-RECTANGLE

Kind: `normalization`. Risk: `critical`. Step budget: `24`.

From openness and membership, choose a compact time-state box inside U and a positive uniform bound for f on it.

Formal target: `Planned Lean signature: exists_compact_rectangle_and_bound`

Output: Positive radii a,b and M with the rectangle in U and norm (f t x) <= M.

Semantic ledger:
1. Freeze the exact local context and named premises.
2. Establish the transition: From openness and membership, choose a compact time-state box inside U and a positive uniform bound for f on it.
3. Derive the declared output: Positive radii a,b and M with the rectangle in U and norm (f t x) <= M.
4. Pass only that output through the declared proof edge; retain all boundary conditions.

Frozen interface only; the listed mathematical result and root closure remain open.

### M1333-C-EULER

Kind: `construction`. Risk: `critical`. Step budget: `38`.

Construct delayed Euler polygonal approximants on a common positive interval.

Formal target: `Planned Lean signature: exists_delayedEulerApproximation`

Output: A sequence of continuous polygonal curves with explicit mesh and integral-delay equation.

Semantic ledger:
1. Freeze the exact local context and named premises.
2. Establish the transition: Construct delayed Euler polygonal approximants on a common positive interval.
3. Derive the declared output: A sequence of continuous polygonal curves with explicit mesh and integral-delay equation.
4. Pass only that output through the declared proof edge; retain all boundary conditions.

Frozen interface only; the listed mathematical result and root closure remain open.

### M1333-C-INVARIANTS

Kind: `construction`. Risk: `critical`. Step budget: `34`.

Prove every approximant remains in the rectangle and is uniformly bounded and equicontinuous.

Formal target: `Planned Lean signature: delayedEuler_invariants`

Output: Common-domain containment and a uniform Lipschitz modulus for the approximants.

Semantic ledger:
1. Freeze the exact local context and named premises.
2. Establish the transition: Prove every approximant remains in the rectangle and is uniformly bounded and equicontinuous.
3. Derive the declared output: Common-domain containment and a uniform Lipschitz modulus for the approximants.
4. Pass only that output through the declared proof edge; retain all boundary conditions.

Frozen interface only; the listed mathematical result and root closure remain open.

### M1333-L-COMPACT

Kind: `bridge`. Risk: `critical`. Step budget: `32`.

Apply finite-dimensional Arzela-Ascoli to extract a uniformly convergent subsequence.

Formal target: `Planned Lean signature: exists_uniformlyConvergent_subsequence`

Output: A continuous limit curve and uniform convergence on the selected interval.

Semantic ledger:
1. Freeze the exact local context and named premises.
2. Establish the transition: Apply finite-dimensional Arzela-Ascoli to extract a uniformly convergent subsequence.
3. Derive the declared output: A continuous limit curve and uniform convergence on the selected interval.
4. Pass only that output through the declared proof edge; retain all boundary conditions.

Frozen interface only; the listed mathematical result and root closure remain open.

### M1333-L-INTEGRAL

Kind: `core_lemma`. Risk: `critical`. Step budget: `42`.

Use uniform continuity of f on the compact box to pass the delayed integral equations to the limit.

Formal target: `Planned Lean signature: limit_satisfies_integralEquation`

Output: The limit satisfies x t = x0 + integral over t0..t of f s (x s).

Semantic ledger:
1. Freeze the exact local context and named premises.
2. Establish the transition: Use uniform continuity of f on the compact box to pass the delayed integral equations to the limit.
3. Derive the declared output: The limit satisfies x t = x0 + integral over t0..t of f s (x s).
4. Pass only that output through the declared proof edge; retain all boundary conditions.

Frozen interface only; the listed mathematical result and root closure remain open.

### M1333-L-DERIV

Kind: `bridge`. Risk: `critical`. Step budget: `28`.

Apply the interval fundamental theorem of calculus to recover HasDerivWithinAt, including endpoints.

Formal target: `Planned Lean signature: integralEquation_hasDerivWithinAt`

Output: The limit curve has derivative f t (x t) within the closed interval.

Semantic ledger:
1. Freeze the exact local context and named premises.
2. Establish the transition: Apply the interval fundamental theorem of calculus to recover HasDerivWithinAt, including endpoints.
3. Derive the declared output: The limit curve has derivative f t (x t) within the closed interval.
4. Pass only that output through the declared proof edge; retain all boundary conditions.

Frozen interface only; the listed mathematical result and root closure remain open.

### M1333-L-ZERO-DIM

Kind: `lemma`. Risk: `high`. Step budget: `20`.

Close the n = 0 branch with the unique constant state curve while retaining a positive interval inside U.

Formal target: `Planned Lean signature: peanoExistence_fin_zero`

Output: PeanoExistenceTarget specialized to n = 0.

Semantic ledger:
1. Freeze the exact local context and named premises.
2. Establish the transition: Close the n = 0 branch with the unique constant state curve while retaining a positive interval inside U.
3. Derive the declared output: PeanoExistenceTarget specialized to n = 0.
4. Pass only that output through the declared proof edge; retain all boundary conditions.

Frozen interface only; the listed mathematical result and root closure remain open.

### M1333-B-DIM

Kind: `branch`. Risk: `high`. Step budget: `14`.

Split n = 0 from n > 0 and recompose the exhaustive dimension cases.

Formal target: `Planned Lean signature: peanoExistence_of_zero_and_positive_dimension`

Output: Existence for every natural dimension.

Semantic ledger:
1. Bind the exact statement fingerprints of every declared proof child.
2. Consume every declared child output without adding an undeclared premise.
3. Derive the declared output: Existence for every natural dimension.
4. Record a kernel-checked child-to-parent composition declaration before closure.

Frozen interface only; the listed mathematical result and root closure remain open.

### M1333-T-SOLUTION

Kind: `transport`. Risk: `high`. Step budget: `16`.

Package the positive-dimensional limit curve, initial value, graph containment, and derivative result as IsSolutionWithin.

Formal target: `Stage1Instances.THM_M_1333.isSolutionWithin_of_components`

Output: The exact IsSolutionWithin conjunct required by the target.

Semantic ledger:
1. Bind the exact statement fingerprints of every declared proof child.
2. Consume every declared child output without adding an undeclared premise.
3. Derive the declared output: The exact IsSolutionWithin conjunct required by the target.
4. Record a kernel-checked child-to-parent composition declaration before closure.

Frozen interface only; the listed mathematical result and root closure remain open.

### M1333-T-ASSEMBLE

Kind: `transport`. Risk: `critical`. Step budget: `18`.

Quantify the selected radius and curve and discharge the exact canonical target from both dimension branches.

Formal target: `Planned Lean signature: peanoExistenceTarget_of_dimension_branches`

Output: Stage1Instances.THM_M_1333.PeanoExistenceTarget.

Semantic ledger:
1. Bind the exact statement fingerprints of every declared proof child.
2. Consume every declared child output without adding an undeclared premise.
3. Derive the declared output: Stage1Instances.THM_M_1333.PeanoExistenceTarget.
4. Record a kernel-checked child-to-parent composition declaration before closure.

Frozen interface only; the listed mathematical result and root closure remain open.

### M1333-X-SOURCE

Kind: `certificate`. Risk: `critical`. Step budget: `18`.

Pinpoint primary and modern sources for every compactness, approximation, limit, and differentiation node.

Formal target: `Reviewed node-specific source crosswalk`

Output: Human-source evidence without machine-proof credit.

Semantic ledger:
1. Freeze the exact local context and named premises.
2. Establish the transition: Pinpoint primary and modern sources for every compactness, approximation, limit, and differentiation node.
3. Derive the declared output: Human-source evidence without machine-proof credit.
4. Pass only that output through the declared proof edge; retain all boundary conditions.

Frozen interface only; the listed mathematical result and root closure remain open.

### M1333-X-PROVENANCE

Kind: `certificate`. Risk: `critical`. Step budget: `20`.

Resolve every terminal declaration, body, revision, license, placeholder scan, dependency, and axiom report.

Formal target: `Transitive terminal-body provenance and trust closure`

Output: No anchor-only candidate or wrapper is credited as a proof body.

Semantic ledger:
1. Freeze the exact local context and named premises.
2. Establish the transition: Resolve every terminal declaration, body, revision, license, placeholder scan, dependency, and axiom report.
3. Derive the declared output: No anchor-only candidate or wrapper is credited as a proof body.
4. Pass only that output through the declared proof edge; retain all boundary conditions.

Frozen interface only; the listed mathematical result and root closure remain open.

## Typed overlays

The JSON bundle separates proof, refinement, provenance, evidence, trust, documentation, and workflow edges. Source and provenance overlays cannot close machine obligations or add proof-body credit.

## Closure boundary

All fourteen machine-required obligations are open. The first critical root cut is `M1333-C-EULER`, `M1333-L-COMPACT`, `M1333-L-INTEGRAL`, and `M1333-L-DERIV`. Primary-source node review, terminal provenance, readable reconstruction, composition bodies, and release validation also remain open.
