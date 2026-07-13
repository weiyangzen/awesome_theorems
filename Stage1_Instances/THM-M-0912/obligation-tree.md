# THM-M-0912 obligation tree

Item: `S56-M-0912-OBLIGATION_TREE`

The registry freezes 16 canonical obligations before any candidate is adopted as proof.  The
machine proof route has three explicit children: derive a positive row from the source domain,
obtain the pinned predecessor recurrence, and commute its summands into DLMF order.  Separate
source, provenance, trust, readability, and workflow nodes remain release-critical without being
counted as proof premises.

```text
M0912-ROOT
`-- M0912-T-ROOT-COMPOSE
    |-- M0912-N-POSITIVE-ROW
    |-- M0912-T-PREDECESSOR-COMPOSE
    |   |-- M0912-L-CHOOSE-SUCC-RIGHT
    |   `-- M0912-L-POSITIVE-COLUMN-REINDEX
    `-- M0912-N-SUMMAND-ORDER
```

## m0912-root

The exact frozen proposition quantifies natural row `m` and column `n`, assumes `n <= m` and
`1 <= n`, and concludes the predecessor recurrence in the DLMF summand order.  Its elaborated
expression is checked against the statement-phase expression rather than compared by name.

## m0912-s-interface

This node fixes the binder order, natural domain, two curried hypotheses, and exact conclusion.

## m0912-s-boundary

Positive diagonal indices, including `(1,1)`, are admitted.  Column zero and columns beyond the
row are excluded.  These are semantic domain choices, not proof conveniences.

## m0912-s-transports

The conjunction spelling, mathlib summand order, and restricted successor encoding have checked
bidirectional transports in `Statement.lean`.  The unrestricted all-natural successor theorem is
broader and is not substituted for the root.

## m0912-s-foundation

This node owns the final Lean kernel, natural recursion, axiom, computation, and TCB policy.
Transitive acceptance remains open.

## m0912-n-positive-row

The checked bridge derives `0 < m` by transitivity from `1 <= n` and `n <= m`.

## m0912-n-summand-order

The checked bridge uses natural addition commutativity to change mathlib's predecessor-first order
into the order printed by DLMF.

## m0912-l-choose-succ-right

This imported bridge is the positive-row recurrence used by the selected terminal theorem body.
It remains part of the pinned body architecture rather than a foundation primitive.

## m0912-l-positive-column-reindex

This node represents a positive column as a successor and cancels its subtract-one expression.
It records the other material step in `Nat.choose_eq_choose_pred_add`.

## m0912-t-predecessor-compose

The selected pinned terminal is `Nat.choose_eq_choose_pred_add`.  Its body consumes the two core
nodes above.  `predecessorRecurrence_of_chooseSuccRight_and_reindex` checks that abstract
child-to-parent composition while keeping both imported children explicit.  The anchor audit
classifies the terminal as an exact `M0-W` route candidate, but this phase does not install or
accept it.

## m0912-t-root-compose

`root_of_bridges_and_predecessorAnchor` consumes all three explicit child packages and yields the
architecture-local root.  A checker compares that root's explicit elaborated expression with
`PascalIdentityTarget` and its frozen SHA-256.

## m0912-x-source

The DLMF formula is a modern statement lead.  Historical attribution, a complete primary proof,
definitions, corrections, errata, node mapping, and independent `H0` review remain open.

## m0912-x-provenance

The selected body, supporting declarations, source file, immutable revision, source blobs, origin,
imports, aliases, and license require release-grade transitive closure.  Alternate recurrence names
share the same `Nat.choose` family and receive no duplicate semantic or proof-body credit.

## m0912-x-trust

This root-relevant release overlay owns declaration dependencies, axioms, compiled artifacts,
executable TCB, unsafe and oracle boundaries, supply-chain closure, and independent replay.

## m0912-x-readable

A complete reader-facing counting or recursive-definition proof with formal anchors and an
independent review remains open.  This architecture inventory is not `R0`.

## m0912-x-workflow

This root-relevant overlay binds dependency-ordered proof, validation, freshness, revocation,
independent verification, and release acceptance without becoming a mathematical proof premise.

## Status boundary

Proof, refinement, provenance, evidence, trust, documentation, and workflow remain separate typed
graphs.  No obligation has accepted closure.  The authoritative root stays `[H1, M3, R4]`, with
`audit_complete=false` and `theorem_complete=false`.  Proof adoption, `H0`, `R0`, transitive trust,
hermetic replay, independent verification, release, and master acceptance are downstream.
