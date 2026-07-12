# THM-M-1200 obligation tree

The frozen route uses one nonzero smooth compactly supported interface trace to cancel the scalar jump coefficient. Nodes remain open unless explicitly kernel-backed; this architecture is not a proof claim.

- **M1200-ROOT** (root): The exact frozen scalar Rankine-Hugoniot equivalence.
  Output: The canonical target.
  - **M1200-T-ASSEMBLE** (transport): Compose the two implications and coefficient normalization into the exact root equivalence.
    Output: The exact root, conditional only on the explicit construction package.
    - **M1200-S-DEFINITIONS** (definition): Fix the jump coefficient, interface defect, test-function class, domains, and binder order.
      Output: The exact objects used by both implications.
    - **M1200-S-BOUNDARIES** (normalization): Retain equal states, stationary interfaces, arbitrary real flux, and every smooth compactly supported spacetime test function.
      Output: No excluded degenerate case or strengthened regularity premise.
    - **M1200-N-UNFOLD** (reduction): Unfold vanishing defect to a scalar coefficient multiplied by every admissible trace integral.
      Output: The quantified product-zero formulation.
    - **M1200-B-FORWARD** (branch): From vanishing against all tests, derive that the jump coefficient is zero.
      Output: Zero interface coefficient.
      - **M1200-C-TEST** (construction): Construct one smooth compactly supported spacetime test function whose interface-trace integral is nonzero.
        Output: An admissible phi with nonzero integral along x = s*t, uniformly for s.
        - **M1200-L-TRACE** (core_lemma): Verify smoothness and compact support of the selected spacetime bump and identify its interface trace.
          Output: Admissibility plus the pointwise trace formula.
        - **M1200-L-INTEGRAL** (core_lemma): Prove the selected interface trace has a strictly positive, hence nonzero, Lebesgue integral.
          Output: A cancellable scalar test integral.
    - **M1200-B-REVERSE** (branch): From the jump equality, show every admissible interface defect is zero.
      Output: The reverse implication for arbitrary tests.
    - **M1200-L-ALGEBRA** (core_lemma): Transport between zero jump coefficient and the canonical Rankine-Hugoniot equality.
      Output: The exact sign and equality normalization.

## Node ledgers

### M1200-ROOT

The exact frozen scalar Rankine-Hugoniot equivalence.

Formal target: `Stage1Instances.THM_M_1200.RankineHugoniotTarget`

Output: The canonical target.

Semantic ledger:
1. Premises: all incoming proof_requires children.
2. Inference: checked child-to-parent composition required.
3. Output: The canonical target..
4. Outgoing use: the unique parent proof edge, or root publication.

### M1200-S-DEFINITIONS

Fix the jump coefficient, interface defect, test-function class, domains, and binder order.

Formal target: `Definitions in Statement.lean`

Output: The exact objects used by both implications.

Semantic ledger:
1. Premises: the exact frozen context and named inputs.
2. Inference: Fix the jump coefficient, interface defect, test-function class, domains, and binder order..
3. Output: The exact objects used by both implications..
4. Outgoing use: the declared parent proof edge, or non-proof overlay.

### M1200-S-BOUNDARIES

Retain equal states, stationary interfaces, arbitrary real flux, and every smooth compactly supported spacetime test function.

Formal target: `Canonical boundary package`

Output: No excluded degenerate case or strengthened regularity premise.

Semantic ledger:
1. Premises: the exact frozen context and named inputs.
2. Inference: Retain equal states, stationary interfaces, arbitrary real flux, and every smooth compactly supported spacetime test function..
3. Output: No excluded degenerate case or strengthened regularity premise..
4. Outgoing use: the declared parent proof edge, or non-proof overlay.

### M1200-S-FOUNDATION

Freeze the classical-analysis, integration, computation, and TCB policy.

Formal target: `Foundation and trust certificate`

Output: An accepted policy for every terminal body.

Semantic ledger:
1. Premises: the exact frozen context and named inputs.
2. Inference: Freeze the classical-analysis, integration, computation, and TCB policy..
3. Output: An accepted policy for every terminal body..
4. Outgoing use: the declared parent proof edge, or non-proof overlay.

### M1200-N-UNFOLD

Unfold vanishing defect to a scalar coefficient multiplied by every admissible trace integral.

Formal target: `InterfaceDefectVanishes f uL uR s`

Output: The quantified product-zero formulation.

Semantic ledger:
1. Premises: the exact frozen context and named inputs.
2. Inference: Unfold vanishing defect to a scalar coefficient multiplied by every admissible trace integral..
3. Output: The quantified product-zero formulation..
4. Outgoing use: the declared parent proof edge, or non-proof overlay.

### M1200-B-FORWARD

From vanishing against all tests, derive that the jump coefficient is zero.

Formal target: `InterfaceDefectVanishes f uL uR s -> jumpCoefficient f uL uR s = 0`

Output: Zero interface coefficient.

Semantic ledger:
1. Premises: all incoming proof_requires children.
2. Inference: checked child-to-parent composition required.
3. Output: Zero interface coefficient..
4. Outgoing use: the unique parent proof edge, or root publication.

### M1200-C-TEST

Construct one smooth compactly supported spacetime test function whose interface-trace integral is nonzero.

Formal target: `NonzeroTracePackage`

Output: An admissible phi with nonzero integral along x = s*t, uniformly for s.

Semantic ledger:
1. Premises: all incoming proof_requires children.
2. Inference: checked child-to-parent composition required.
3. Output: An admissible phi with nonzero integral along x = s*t, uniformly for s..
4. Outgoing use: the unique parent proof edge, or root publication.

### M1200-L-TRACE

Verify smoothness and compact support of the selected spacetime bump and identify its interface trace.

Formal target: `ContDiff Real top phi and HasCompactSupport phi`

Output: Admissibility plus the pointwise trace formula.

Semantic ledger:
1. Premises: the exact frozen context and named inputs.
2. Inference: Verify smoothness and compact support of the selected spacetime bump and identify its interface trace..
3. Output: Admissibility plus the pointwise trace formula..
4. Outgoing use: the declared parent proof edge, or non-proof overlay.

### M1200-L-INTEGRAL

Prove the selected interface trace has a strictly positive, hence nonzero, Lebesgue integral.

Formal target: `integral (fun t => phi (t, s*t)) != 0`

Output: A cancellable scalar test integral.

Semantic ledger:
1. Premises: the exact frozen context and named inputs.
2. Inference: Prove the selected interface trace has a strictly positive, hence nonzero, Lebesgue integral..
3. Output: A cancellable scalar test integral..
4. Outgoing use: the declared parent proof edge, or non-proof overlay.

### M1200-B-REVERSE

From the jump equality, show every admissible interface defect is zero.

Formal target: `s * (uR-uL) = f uR-f uL -> InterfaceDefectVanishes f uL uR s`

Output: The reverse implication for arbitrary tests.

Semantic ledger:
1. Premises: the exact frozen context and named inputs.
2. Inference: From the jump equality, show every admissible interface defect is zero..
3. Output: The reverse implication for arbitrary tests..
4. Outgoing use: the declared parent proof edge, or non-proof overlay.

### M1200-L-ALGEBRA

Transport between zero jump coefficient and the canonical Rankine-Hugoniot equality.

Formal target: `jumpCoefficient f uL uR s = 0 <-> s*(uR-uL)=f uR-f uL`

Output: The exact sign and equality normalization.

Semantic ledger:
1. Premises: the exact frozen context and named inputs.
2. Inference: Transport between zero jump coefficient and the canonical Rankine-Hugoniot equality..
3. Output: The exact sign and equality normalization..
4. Outgoing use: the declared parent proof edge, or non-proof overlay.

### M1200-T-ASSEMBLE

Compose the two implications and coefficient normalization into the exact root equivalence.

Formal target: `NonzeroTracePackage -> RankineHugoniotTarget`

Output: The exact root, conditional only on the explicit construction package.

Semantic ledger:
1. Premises: all incoming proof_requires children.
2. Inference: checked child-to-parent composition required.
3. Output: The exact root, conditional only on the explicit construction package..
4. Outgoing use: the unique parent proof edge, or root publication.

### M1200-X-SOURCE

Pinpoint primary sources for the weak-interface reduction, bump argument, and algebraic jump law.

Formal target: `Reviewed node-specific source crosswalk`

Output: Human-source evidence only.

Semantic ledger:
1. Premises: the exact frozen context and named inputs.
2. Inference: Pinpoint primary sources for the weak-interface reduction, bump argument, and algebraic jump law..
3. Output: Human-source evidence only..
4. Outgoing use: the declared parent proof edge, or non-proof overlay.

### M1200-X-PROVENANCE

Resolve terminal bodies, revisions, licenses, axioms, and transitive trust closure.

Formal target: `Transitive provenance record`

Output: No supporting import is mistaken for root closure.

Semantic ledger:
1. Premises: the exact frozen context and named inputs.
2. Inference: Resolve terminal bodies, revisions, licenses, axioms, and transitive trust closure..
3. Output: No supporting import is mistaken for root closure..
4. Outgoing use: the declared parent proof edge, or non-proof overlay.

## Closure boundary

The only kernel-backed registry node is the previously frozen definition surface. The critical open cut is `M1200-C-TEST`; its trace-admissibility and nonzero-integral children must be implemented before the forward branch can close. The checked conditional composition consumes this package explicitly and gives it no closure credit. Source review, provenance/trust closure, readable review, validation, release, and theorem completion remain open.
