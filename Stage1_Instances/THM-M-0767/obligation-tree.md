# THM-M-0767 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 28 canonical obligations before proof admission. Twenty-five are
root-relevant machine, human-source, and readable obligations. `M0767-X-X3` through `M0767-X-X5`
are informational provenance/trust overlays and cannot contribute mathematical proof credit. The
canonical registry projection has SHA-256
`9bf54713d38d6a18baeea4e55c8d9ec54f2ac0f02b7024fabf2cda9bc69acd66`.
Eligibility was assigned from the exact statement and proof architecture, not from the already
observed availability of `Cardinal.cantor`. No obligation is closed by this freeze.

## Typed route

```text
M0767-ROOT  exact set-subtype cardinal target [open M3]
|-- M0767-S  statement, universe, boundaries, transports, foundation policy
|-- M0767-N  powerset-cardinal normalization
|-- M0767-C  singleton construction and injectivity
|-- M0767-B  no reverse injection branch
|-- M0767-L  diagonal engine
|-- M0767-X  imported bodies, provenance, axioms, and TCB boundary
`-- M0767-T  exact composition back to CanonicalTarget
    |-- M0767-T-T1  checked powerset normalization [open]
    `-- M0767-T-T2  Cardinal.cantor application through exact wrapper [open]
```

The 46 edges in `typed-graphs.json` keep seven graph roles separate. Proof/refinement reach every
required mathematical obligation from `M0767-ROOT` and are acyclic. Provenance, trust,
documentation, and workflow links therefore cannot masquerade as proof premises. The evidence
graph is deliberately empty because this phase creates architecture rather than proof receipts.

## Layer decisions

`M0767-S` records the subtype representation, universe equality, empty/finite boundaries, checked
alternate encodings, and the pending foundation-policy decision. `M0767-N` owns the directional
use of `Cardinal.mk_powerset`. The branch, construction, and core-lemma layers expand the actual
body of pinned `Cardinal.cantor`: singleton injectivity supplies the forward comparison, while
`Function.cantor_injective` and `Function.cantor_surjective` supply the diagonal contradiction to a
reverse embedding. There is no finite/infinite or local/global split; uniform polymorphism handles
all sets, and this applicability decision remains visible in the statement and boundary nodes.

All nonleaves have `step_budget: "split-required"`; every current leaf has a substantive ledger
and a budget below 100. A later proof phase must split any leaf if transitive source, trust, or
composition inspection reveals hidden work. Every parent still needs an exact checked composition
certificate that consumes all required children.

## Status boundary

The remaining immediate root cut is `M0767-T-T1` plus `M0767-T-T2`. A pinned checked wrapper exists,
but it receives no M0 credit here: proof-body admission, transitive declaration and axiom closure,
node-scoped evidence, parent composition, primary-source H0, readable R0, hermetic replay, and
independent acceptance remain downstream. The root stays `[H1, M3, R4]`; neither `AUDIT-Z` nor
`THEOREM-Z` is claimed.
