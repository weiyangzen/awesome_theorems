# THM-M-1171 obligation tree

The frozen proof route is Fourier-multiplier based. Every entry below is an open architecture obligation, not a proof claim.

- **M1171-ROOT** (root): The frozen whole-space Calderon-Zygmund Hessian estimate.
  Output: The exact canonical target.
  - **M1171-T-ASSEMBLE** (composition): Combine component bounds, derivative transports, and finite-dimensional norm assembly.
    Output: The root inequality with a nonnegative constant independent of u.
    - **M1171-S-DEFINITIONS** (definition): Fix Euclidean space, Hessian, Laplacian, exponent, measure, and binder order.
      Output: The exact analytic objects used by the root.
    - **M1171-S-BOUNDARIES** (normalization): Retain n >= 1 and 1 < p < infinity; exclude all endpoint and bounded-domain variants.
      Output: No broadened or substituted theorem enters composition.
    - **M1171-S-FOUNDATION** (certificate): Freeze classical analysis, choice, computation, and TCB policies.
      Output: An accepted foundation profile for all terminal bodies.
    - **M1171-T-COMPONENT** (composition): Compose Fourier identities, the multiplier bound, and zero-frequency removal.
      Output: All n^2 second partial derivatives obey one uniform estimate.
      - **M1171-N-SCHWARTZ** (normalization): Transport a smooth compactly supported real function to the Schwartz/Fourier domain.
        Output: A Fourier-transformable test function with derivative identities.
      - **M1171-N-COMPLEX** (transport): Complexify the scalar function and preserve the relevant Lp norms and derivatives.
        Output: A complex Fourier formulation equivalent to the real component estimates.
      - **M1171-L-FOURIER-DERIV** (core_lemma): Identify Fourier transforms of every second partial derivative and of the Laplacian.
        Output: The multiplier relation away from frequency zero.
      - **M1171-C-MULTIPLIER** (construction): Define m_ij(xi) = xi_i xi_j / |xi|^2 off zero and choose its value at zero.
        Output: A total measurable multiplier with the correct punctured-space symbol.
      - **M1171-L-MIHLIN** (bridge): Prove uniform derivative bounds for m_ij and apply strong Lp multiplier boundedness for 1 < p < infinity.
        Output: A constant depending only on n and p for every component multiplier.
      - **M1171-L-ZERO-FREQ** (lemma): Show the arbitrary value of m_ij at frequency zero does not alter the Lp identity.
        Output: A valid global multiplier identity from the punctured identity.
    - **M1171-L-FDERIV-PARTIAL** (transport): Identify Hessian evaluations on standard basis vectors with second partial derivatives.
      Output: Component estimates for the dossier's Frechet Hessian.
    - **M1171-L-TRACE** (transport): Identify the dossier's trace definition of laplacian with the Fourier-side Laplacian.
      Output: The exact right-hand side used by the root.
    - **M1171-L-OPNORM** (core_lemma): Bound the finite-dimensional bilinear operator norm by the sum of standard-basis components.
      Output: A dimension-only pointwise Hessian norm bound.
    - **M1171-L-LP-ASSEMBLY** (core_lemma): Lift the finite component sum and scalar constants through eLpNorm.
      Output: A single Hessian eLpNorm estimate with a finite-dimensional constant.

## Node ledgers

### M1171-ROOT

The frozen whole-space Calderon-Zygmund Hessian estimate.

Formal target: `Stage1Instances.THM_M_1171.CalderonZygmundEstimateTarget`

Output: The exact canonical target.

Semantic ledger:
1. Consume every required incoming proof edge.
2. Derive: The exact canonical target.
3. Record an exact child-to-parent composition certificate.

### M1171-S-DEFINITIONS

Fix Euclidean space, Hessian, Laplacian, exponent, measure, and binder order.

Formal target: `Statement.lean definitions and ExpandedTarget`

Output: The exact analytic objects used by the root.

Semantic ledger:
1. Freeze the exact hypotheses and named input interfaces.
2. Establish the stated transition: Fix Euclidean space, Hessian, Laplacian, exponent, measure, and binder order.
3. Derive the declared output: The exact analytic objects used by the root.
4. Pass that output to the parent edge without strengthening or changing the target.

### M1171-S-BOUNDARIES

Retain n >= 1 and 1 < p < infinity; exclude all endpoint and bounded-domain variants.

Formal target: `Boundary package for the canonical target`

Output: No broadened or substituted theorem enters composition.

Semantic ledger:
1. Freeze the exact hypotheses and named input interfaces.
2. Establish the stated transition: Retain n >= 1 and 1 < p < infinity; exclude all endpoint and bounded-domain variants.
3. Derive the declared output: No broadened or substituted theorem enters composition.
4. Pass that output to the parent edge without strengthening or changing the target.

### M1171-S-FOUNDATION

Freeze classical analysis, choice, computation, and TCB policies.

Formal target: `Foundation and trust certificate`

Output: An accepted foundation profile for all terminal bodies.

Semantic ledger:
1. Freeze the exact hypotheses and named input interfaces.
2. Establish the stated transition: Freeze classical analysis, choice, computation, and TCB policies.
3. Derive the declared output: An accepted foundation profile for all terminal bodies.
4. Pass that output to the parent edge without strengthening or changing the target.

### M1171-N-SCHWARTZ

Transport a smooth compactly supported real function to the Schwartz/Fourier domain.

Formal target: `ContDiff plus HasCompactSupport implies the required Schwartz regularity`

Output: A Fourier-transformable test function with derivative identities.

Semantic ledger:
1. Freeze the exact hypotheses and named input interfaces.
2. Establish the stated transition: Transport a smooth compactly supported real function to the Schwartz/Fourier domain.
3. Derive the declared output: A Fourier-transformable test function with derivative identities.
4. Pass that output to the parent edge without strengthening or changing the target.

### M1171-N-COMPLEX

Complexify the scalar function and preserve the relevant Lp norms and derivatives.

Formal target: `Real-to-complex Fourier transport`

Output: A complex Fourier formulation equivalent to the real component estimates.

Semantic ledger:
1. Freeze the exact hypotheses and named input interfaces.
2. Establish the stated transition: Complexify the scalar function and preserve the relevant Lp norms and derivatives.
3. Derive the declared output: A complex Fourier formulation equivalent to the real component estimates.
4. Pass that output to the parent edge without strengthening or changing the target.

### M1171-L-FOURIER-DERIV

Identify Fourier transforms of every second partial derivative and of the Laplacian.

Formal target: `F(partial_i partial_j u) and F(laplacian u) identities`

Output: The multiplier relation away from frequency zero.

Semantic ledger:
1. Freeze the exact hypotheses and named input interfaces.
2. Establish the stated transition: Identify Fourier transforms of every second partial derivative and of the Laplacian.
3. Derive the declared output: The multiplier relation away from frequency zero.
4. Pass that output to the parent edge without strengthening or changing the target.

### M1171-C-MULTIPLIER

Define m_ij(xi) = xi_i xi_j / |xi|^2 off zero and choose its value at zero.

Formal target: `Measurable homogeneous multiplier family m_ij`

Output: A total measurable multiplier with the correct punctured-space symbol.

Semantic ledger:
1. Freeze the exact hypotheses and named input interfaces.
2. Establish the stated transition: Define m_ij(xi) = xi_i xi_j / |xi|^2 off zero and choose its value at zero.
3. Derive the declared output: A total measurable multiplier with the correct punctured-space symbol.
4. Pass that output to the parent edge without strengthening or changing the target.

### M1171-L-MIHLIN

Prove uniform derivative bounds for m_ij and apply strong Lp multiplier boundedness for 1 < p < infinity.

Formal target: `LpBounded (fourierMultiplier m_ij) p`

Output: A constant depending only on n and p for every component multiplier.

Semantic ledger:
1. Freeze the exact hypotheses and named input interfaces.
2. Establish the stated transition: Prove uniform derivative bounds for m_ij and apply strong Lp multiplier boundedness for 1 < p < infinity.
3. Derive the declared output: A constant depending only on n and p for every component multiplier.
4. Pass that output to the parent edge without strengthening or changing the target.

### M1171-L-ZERO-FREQ

Show the arbitrary value of m_ij at frequency zero does not alter the Lp identity.

Formal target: `Almost-everywhere zero-frequency removal`

Output: A valid global multiplier identity from the punctured identity.

Semantic ledger:
1. Freeze the exact hypotheses and named input interfaces.
2. Establish the stated transition: Show the arbitrary value of m_ij at frequency zero does not alter the Lp identity.
3. Derive the declared output: A valid global multiplier identity from the punctured identity.
4. Pass that output to the parent edge without strengthening or changing the target.

### M1171-T-COMPONENT

Compose Fourier identities, the multiplier bound, and zero-frequency removal.

Formal target: `eLpNorm (partial_i partial_j u) p <= C * eLpNorm (laplacian u) p`

Output: All n^2 second partial derivatives obey one uniform estimate.

Semantic ledger:
1. Consume every required incoming proof edge.
2. Derive: All n^2 second partial derivatives obey one uniform estimate.
3. Record an exact child-to-parent composition certificate.

### M1171-L-FDERIV-PARTIAL

Identify Hessian evaluations on standard basis vectors with second partial derivatives.

Formal target: `hessian u x e_i e_j = partial_i partial_j u x`

Output: Component estimates for the dossier's Frechet Hessian.

Semantic ledger:
1. Freeze the exact hypotheses and named input interfaces.
2. Establish the stated transition: Identify Hessian evaluations on standard basis vectors with second partial derivatives.
3. Derive the declared output: Component estimates for the dossier's Frechet Hessian.
4. Pass that output to the parent edge without strengthening or changing the target.

### M1171-L-TRACE

Identify the dossier's trace definition of laplacian with the Fourier-side Laplacian.

Formal target: `laplacian u = sum_i partial_i partial_i u`

Output: The exact right-hand side used by the root.

Semantic ledger:
1. Freeze the exact hypotheses and named input interfaces.
2. Establish the stated transition: Identify the dossier's trace definition of laplacian with the Fourier-side Laplacian.
3. Derive the declared output: The exact right-hand side used by the root.
4. Pass that output to the parent edge without strengthening or changing the target.

### M1171-L-OPNORM

Bound the finite-dimensional bilinear operator norm by the sum of standard-basis components.

Formal target: `norm A <= K(n) * sum_i sum_j norm (A e_i e_j)`

Output: A dimension-only pointwise Hessian norm bound.

Semantic ledger:
1. Freeze the exact hypotheses and named input interfaces.
2. Establish the stated transition: Bound the finite-dimensional bilinear operator norm by the sum of standard-basis components.
3. Derive the declared output: A dimension-only pointwise Hessian norm bound.
4. Pass that output to the parent edge without strengthening or changing the target.

### M1171-L-LP-ASSEMBLY

Lift the finite component sum and scalar constants through eLpNorm.

Formal target: `eLpNorm of Hessian norm controlled by component eLpNorms`

Output: A single Hessian eLpNorm estimate with a finite-dimensional constant.

Semantic ledger:
1. Freeze the exact hypotheses and named input interfaces.
2. Establish the stated transition: Lift the finite component sum and scalar constants through eLpNorm.
3. Derive the declared output: A single Hessian eLpNorm estimate with a finite-dimensional constant.
4. Pass that output to the parent edge without strengthening or changing the target.

### M1171-T-ASSEMBLE

Combine component bounds, derivative transports, and finite-dimensional norm assembly.

Formal target: `Canonical inequality for fixed n p u`

Output: The root inequality with a nonnegative constant independent of u.

Semantic ledger:
1. Consume every required incoming proof edge.
2. Derive: The root inequality with a nonnegative constant independent of u.
3. Record an exact child-to-parent composition certificate.

### M1171-X-SOURCE

Pinpoint primary and modern sources for each analytic bridge and check assumptions and errata.

Formal target: `Reviewed node-specific source crosswalk`

Output: H-state evidence without machine-proof credit.

Semantic ledger:
1. Freeze the exact hypotheses and named input interfaces.
2. Establish the stated transition: Pinpoint primary and modern sources for each analytic bridge and check assumptions and errata.
3. Derive the declared output: H-state evidence without machine-proof credit.
4. Pass that output to the parent edge without strengthening or changing the target.

### M1171-X-PROVENANCE

Resolve terminal declarations, bodies, revisions, licenses, axioms, and transitive TCB.

Formal target: `Transitive provenance and trust closure`

Output: No anchor-only candidate is mistaken for a proof body.

Semantic ledger:
1. Freeze the exact hypotheses and named input interfaces.
2. Establish the stated transition: Resolve terminal declarations, bodies, revisions, licenses, axioms, and transitive TCB.
3. Derive the declared output: No anchor-only candidate is mistaken for a proof body.
4. Pass that output to the parent edge without strengthening or changing the target.

## Typed overlays

`X-SOURCE` and `X-PROVENANCE` cover source and terminal-body boundaries. They are informational overlays and cannot close a proof node or increase a machine denominator.

## Closure boundary

All 16 semantic machine obligations are open. The first critical cut contains `M1171-L-MIHLIN`, `M1171-L-FOURIER-DERIV`, and `M1171-L-LP-ASSEMBLY`. No composition certificate, proof body, H0/R0 review, or theorem completion is claimed.
