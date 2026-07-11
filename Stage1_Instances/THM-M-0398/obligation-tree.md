# THM-M-0398 frozen obligation architecture

Item: `S56-M-0398-OBLIGATION_TREE`

The registry freezes 15 semantic obligations for the exact rational-set form
of the Thue-Siegel-Roth theorem. Eligibility was assigned before proof
execution. The checked interface in `ObligationTree.lean` shows only that a
uniform positive-constant Roth estimate specializes at `C = 1` to the exact
root; it does not supply that estimate.

## Typed route

```text
M0398-ROOT exact canonical proposition
`-- M0398-T checked C=1 specialization
    `-- M0398-L4 uniform positive-constant finiteness engine
        |-- M0398-N1 infinite set to growing-denominator sequence
        |-- M0398-C1 auxiliary polynomial construction
        |-- M0398-C2 Roth index and nonvanishing lemma
        |-- M0398-L1 analytic upper estimate
        |-- M0398-L2 arithmetic/product-formula lower estimate
        `-- M0398-L3 parameter separation and contradiction
```

`M0398-S` refines the statement into exact expansion `S1`, normalized positive
denominator boundary `S2`, and foundation/trust policy `S3`. `M0398-X1` is the
node-specific primary-source crosswalk, while `M0398-X2` is the future terminal
proof-body, axiom, TCB, and reproducibility audit. Those nodes use source,
documentation, trust, and workflow edges; neither can masquerade as a proof
premise.

## Node ledger

### m0398-root
Exact `Stage1Instances.THMM0398.ThueSiegelRoth`. `[H1, M3, R4]`; no inhabitant.

### m0398-s
Frozen statement and foundation interface. `[H1, M4, R4]`.

### m0398-s1
Checked definitional expansion `thueSiegelRoth_iff`. `[H1, M0-L, R4]`.

### m0398-s2
Checked normalized-denominator positivity via `denominator_pos`. `[H1, M0-L, R4]`.

### m0398-s3
Planned exact foundation, axiom, computation, and TCB policy certificate. `[H1, M4, R4]`.

### m0398-t
Checked conditional specialization from the constant-factor engine to the exact root. `[H1, M0-L, R4]`; it gives no proof credit for its open premise.

### m0398-n1
Extract a distinct growing-denominator sequence from an infinite exceptional set. `[H1, M4, R4]`.

### m0398-c1
Construct the multivariate integer auxiliary polynomial with degree, height, and index invariants. `[H1, M4, R4]`; split-required.

### m0398-c2
Supply the Roth index/nonvanishing lemma at separated approximation points. `[H1, M4, R4]`; split-required.

### m0398-l1
Derive the approximation-driven upper bound for the selected nonzero evaluation. `[H1, M4, R4]`.

### m0398-l2
Derive the denominator-clearing, conjugate, and product-formula lower bound. `[H1, M4, R4]`.

### m0398-l3
Optimize degrees and denominator separation to contradict the simultaneous bounds. `[H1, M4, R4]`.

### m0398-l4
Recompose the substantive packages into `FiniteExceptionalWithConstant`. `[H1, M4, R4]`; this is the minimal open root cut set.

### m0398-x1
Pinpoint Roth 1955 passages, conventions, assumptions, and errata for every node. `[H1, M4, R4]`; human-source boundary only.

### m0398-x2
Audit the eventual terminal body's provenance, dependency closure, axioms, TCB, and replay. `[H1, M4, R4]`; release overlay only.

## Freeze boundary

This architecture does not implement Roth's auxiliary-polynomial argument,
close the root, improve H/R debt, complete the audit, or complete the theorem.
Any split, merge, exclusion, or target correction requires an append-only
registry revision rather than silently changing this denominator.
